"""
AquaSwift — Auth Service

Core authentication logic: OTP flow, email+password login, JWT issuance,
refresh token rotation, logout.
"""

from __future__ import annotations

import random
import string
import uuid
from datetime import datetime, timedelta, timezone

import structlog
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.adapters.sms import sms_adapter
from app.auth.models import RefreshToken, User
from app.core.cache import cache_delete, cache_get, cache_set
from app.core.config import settings
from app.core.exceptions import (
    ConflictError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_token,
)

logger = structlog.get_logger()


# ---- OTP Management ----


def _generate_otp() -> str:
    """Generate a random numeric OTP."""
    return "".join(random.choices(string.digits, k=settings.OTP_LENGTH))


async def request_otp(phone: str) -> dict:
    """
    Request an OTP for phone-based authentication.

    Rate-limited per phone number. OTP stored in Redis with TTL.
    """
    # Rate limiting check
    rate_key = f"otp_rate:{phone}"
    rate_count = await cache_get(rate_key)
    if rate_count and int(rate_count) >= settings.OTP_RATE_LIMIT_PER_MINUTE:
        raise RateLimitError(retry_after=60)

    # Generate and store OTP
    otp = _generate_otp()
    otp_key = f"otp:{phone}"

    await cache_set(otp_key, {"otp": otp, "attempts": 0}, ttl_seconds=settings.OTP_EXPIRY_SECONDS)

    # Update rate counter
    current_rate = int(rate_count) if rate_count else 0
    await cache_set(rate_key, current_rate + 1, ttl_seconds=60)

    # Send OTP via adapter
    sent = await sms_adapter.send_otp(phone, otp)

    logger.info("otp_requested", phone=phone, sent=sent)

    return {
        "message": "OTP sent successfully.",
        "detail": {
            "phone": phone,
            "expires_in": settings.OTP_EXPIRY_SECONDS,
            # Include OTP in dev mode for testing
            **({"otp": otp} if settings.is_development else {}),
        },
    }


async def verify_otp_and_login(
    db: AsyncSession, phone: str, otp: str, full_name: str | None = None
) -> dict:
    """
    Verify OTP and either register or login the user.

    If the phone number is new, creates a user (full_name required).
    If existing, logs in the user.
    Returns JWT access + refresh tokens.
    """
    # Fetch stored OTP from Redis
    otp_key = f"otp:{phone}"
    otp_data = await cache_get(otp_key)

    if not otp_data:
        raise ValidationError(code="OTP_EXPIRED", message="OTP has expired or was not requested.")

    attempts = otp_data.get("attempts", 0)
    if attempts >= settings.OTP_MAX_ATTEMPTS:
        await cache_delete(otp_key)
        raise ValidationError(code="OTP_MAX_ATTEMPTS", message="Maximum OTP verification attempts exceeded.")

    if otp_data["otp"] != otp:
        # Increment attempts
        otp_data["attempts"] = attempts + 1
        await cache_set(otp_key, otp_data, ttl_seconds=settings.OTP_EXPIRY_SECONDS)
        raise ValidationError(code="OTP_INVALID", message="Invalid OTP.")

    # OTP valid — clear it
    await cache_delete(otp_key)

    # Find or create user
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()

    is_new_user = False
    if user is None:
        # New user — registration
        if not full_name:
            raise ValidationError(
                code="NAME_REQUIRED",
                message="Full name is required for new users.",
            )
        user = User(phone=phone, full_name=full_name)
        db.add(user)
        await db.flush()
        is_new_user = True

        # Assign CUSTOMER role by default
        from app.rbac.models import Role
        from app.users.models import UserRole

        result = await db.execute(select(Role).where(Role.name == "CUSTOMER"))
        customer_role = result.scalar_one_or_none()
        if customer_role:
            db.add(UserRole(user_id=user.id, role_id=customer_role.id))
            await db.flush()

        logger.info("user_registered", user_id=str(user.id), phone=phone)

    if not user.is_active:
        raise ValidationError(code="USER_DEACTIVATED", message="Your account has been deactivated.")

    # Issue tokens
    tokens = await _issue_tokens(db, user)

    logger.info("user_logged_in", user_id=str(user.id), phone=phone, is_new=is_new_user)

    return tokens


async def email_login(db: AsyncSession, email: str, password: str) -> dict:
    """
    Authenticate admin users via email + password.
    """
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None or not user.password_hash:
        raise ValidationError(code="INVALID_CREDENTIALS", message="Invalid email or password.")

    if not verify_password(password, user.password_hash):
        raise ValidationError(code="INVALID_CREDENTIALS", message="Invalid email or password.")

    if not user.is_active:
        raise ValidationError(code="USER_DEACTIVATED", message="Your account has been deactivated.")

    tokens = await _issue_tokens(db, user)
    logger.info("admin_logged_in", user_id=str(user.id), email=email)
    return tokens


async def refresh_access_token(db: AsyncSession, refresh_token_str: str) -> dict:
    """
    Rotate a refresh token: verify the old one, revoke it, issue new pair.
    """
    payload = verify_token(refresh_token_str, expected_type="refresh")
    jti = payload.get("jti")
    user_id = payload.get("sub")

    if not jti or not user_id:
        raise ValidationError(code="INVALID_TOKEN", message="Invalid refresh token.")

    # Find the refresh token record
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token_jti == jti)
    )
    token_record = result.scalar_one_or_none()

    if token_record is None or token_record.is_revoked:
        # Potential token reuse attack — revoke all user tokens
        await _revoke_all_user_tokens(db, uuid.UUID(user_id))
        raise ValidationError(code="TOKEN_REVOKED", message="Refresh token has been revoked.")

    # Revoke the old token
    token_record.is_revoked = True

    # Get the user
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise ValidationError(code="USER_NOT_FOUND", message="User not found or deactivated.")

    # Issue new tokens
    tokens = await _issue_tokens(db, user)
    logger.info("token_refreshed", user_id=user_id)
    return tokens


async def logout(db: AsyncSession, refresh_token_str: str) -> None:
    """Revoke the refresh token on logout."""
    try:
        payload = verify_token(refresh_token_str, expected_type="refresh")
        jti = payload.get("jti")
        if jti:
            result = await db.execute(
                select(RefreshToken).where(RefreshToken.token_jti == jti)
            )
            token_record = result.scalar_one_or_none()
            if token_record:
                token_record.is_revoked = True
                logger.info("user_logged_out", user_id=payload.get("sub"))
    except Exception:
        pass  # Ignore invalid tokens on logout


# ---- Internal Helpers ----


async def _issue_tokens(db: AsyncSession, user: User) -> dict:
    """Issue access + refresh token pair and store refresh token record."""
    # Get user roles for the access token
    role_names = []
    if user.user_roles:
        for ur in user.user_roles:
            from app.rbac.models import Role
            result = await db.execute(select(Role).where(Role.id == ur.role_id))
            role = result.scalar_one_or_none()
            if role:
                role_names.append(role.name)

    primary_role = role_names[0] if role_names else "CUSTOMER"

    access_token = create_access_token(
        user_id=str(user.id),
        role=primary_role,
        extra_claims={"roles": role_names},
    )

    refresh_token_str = create_refresh_token(user_id=str(user.id))

    # Decode the refresh token to get the JTI
    refresh_payload = verify_token(refresh_token_str, expected_type="refresh")

    # Store refresh token record
    token_record = RefreshToken(
        user_id=user.id,
        token_jti=refresh_payload["jti"],
        expires_at=datetime.fromtimestamp(refresh_payload["exp"], tz=timezone.utc),
    )
    db.add(token_record)

    from app.auth.schemas import UserBriefResponse

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": UserBriefResponse(
            id=user.id,
            phone=user.phone,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            roles=role_names,
            created_at=user.created_at,
        ).model_dump(),
    }


async def _revoke_all_user_tokens(db: AsyncSession, user_id: uuid.UUID) -> None:
    """Revoke all refresh tokens for a user (security measure)."""
    from sqlalchemy import update

    await db.execute(
        update(RefreshToken)
        .where(RefreshToken.user_id == user_id, RefreshToken.is_revoked == False)
        .values(is_revoked=True)
    )
    logger.warning("all_tokens_revoked", user_id=str(user_id), reason="potential_reuse_attack")
