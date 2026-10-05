"""
AquaSwift — Users Service
"""

from __future__ import annotations

import uuid

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.core.exceptions import NotFoundError, ValidationError
from app.rbac.models import Role
from app.users.models import CustomerProfile, DriverProfile, UserRole

logger = structlog.get_logger()


async def get_user_profile(db: AsyncSession, user: User) -> dict:
    """Get the full user profile with roles and customer/driver profile."""
    # Get roles
    result = await db.execute(
        select(Role).join(UserRole).where(UserRole.user_id == user.id)
    )
    roles = [r.name for r in result.scalars().all()]

    # Get customer profile if exists
    result = await db.execute(
        select(CustomerProfile).where(CustomerProfile.user_id == user.id)
    )
    customer_profile = result.scalar_one_or_none()

    return {
        "id": user.id,
        "phone": user.phone,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "roles": roles,
        "customer_profile": customer_profile,
        "created_at": user.created_at,
    }


async def update_profile(db: AsyncSession, user: User, full_name: str | None = None) -> User:
    """Update the current user's profile."""
    if full_name:
        user.full_name = full_name
    await db.flush()
    return user


async def list_users(
    db: AsyncSession, page: int = 1, page_size: int = 20
) -> tuple[list[dict], int]:
    """List all users with pagination (admin)."""
    offset = (page - 1) * page_size

    # Count
    count_result = await db.execute(select(func.count(User.id)))
    total = count_result.scalar_one()

    # Fetch
    result = await db.execute(
        select(User).order_by(User.created_at.desc()).offset(offset).limit(page_size)
    )
    users = result.scalars().all()

    user_dicts = []
    for u in users:
        role_result = await db.execute(
            select(Role).join(UserRole).where(UserRole.user_id == u.id)
        )
        roles = [r.name for r in role_result.scalars().all()]
        user_dicts.append({
            "id": u.id,
            "phone": u.phone,
            "email": u.email,
            "full_name": u.full_name,
            "is_active": u.is_active,
            "roles": roles,
            "created_at": u.created_at,
        })

    return user_dicts, total


async def admin_update_user(
    db: AsyncSession, user_id: uuid.UUID, full_name: str | None = None, is_active: bool | None = None
) -> User:
    """Admin: update a user's profile."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise NotFoundError("User", user_id)
    if full_name is not None:
        user.full_name = full_name
    if is_active is not None:
        user.is_active = is_active
    await db.flush()
    return user


async def assign_role(db: AsyncSession, user_id: uuid.UUID, role_name: str) -> None:
    """Admin: assign a role to a user."""
    # Verify user exists
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise NotFoundError("User", user_id)

    # Find role
    result = await db.execute(select(Role).where(Role.name == role_name))
    role = result.scalar_one_or_none()
    if not role:
        raise NotFoundError("Role", role_name)

    # Check if already assigned
    result = await db.execute(
        select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role.id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise ValidationError(code="ROLE_ALREADY_ASSIGNED", message=f"User already has the {role_name} role.")

    db.add(UserRole(user_id=user_id, role_id=role.id))
    await db.flush()

    # Create customer or driver profile if needed
    if role_name == "CUSTOMER":
        existing_profile = await db.execute(
            select(CustomerProfile).where(CustomerProfile.user_id == user_id)
        )
        if not existing_profile.scalar_one_or_none():
            db.add(CustomerProfile(user_id=user_id))

    elif role_name == "DRIVER":
        existing_profile = await db.execute(
            select(DriverProfile).where(DriverProfile.user_id == user_id)
        )
        if not existing_profile.scalar_one_or_none():
            db.add(DriverProfile(user_id=user_id))

    await db.flush()
    logger.info("role_assigned", user_id=str(user_id), role=role_name)
