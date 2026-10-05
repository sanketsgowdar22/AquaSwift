"""
AquaSwift — Auth Router
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import service
from app.auth.schemas import (
    EmailLoginSchema,
    MessageResponse,
    OTPRequestSchema,
    OTPVerifySchema,
    RefreshTokenSchema,
)
from app.core.database import get_db

router = APIRouter()


@router.post("/auth/otp/request", response_model=MessageResponse, tags=["Authentication"])
async def request_otp(data: OTPRequestSchema):
    """
    Request an OTP for phone-based registration/login.

    Public endpoint — no authentication required.
    In development mode, the OTP is returned in the response for testing.
    """
    result = await service.request_otp(data.phone)
    return result


@router.post("/auth/otp/verify", tags=["Authentication"])
async def verify_otp(
    data: OTPVerifySchema,
    db: AsyncSession = Depends(get_db),
):
    """
    Verify OTP and authenticate.

    If the phone number is new, registers the user (full_name required).
    Returns JWT access + refresh tokens.
    """
    return await service.verify_otp_and_login(db, data.phone, data.otp, data.full_name)


@router.post("/auth/login", tags=["Authentication"])
async def email_login(
    data: EmailLoginSchema,
    db: AsyncSession = Depends(get_db),
):
    """
    Login with email + password (admin users).

    Returns JWT access + refresh tokens.
    """
    return await service.email_login(db, data.email, data.password)


@router.post("/auth/refresh", tags=["Authentication"])
async def refresh_token(
    data: RefreshTokenSchema,
    db: AsyncSession = Depends(get_db),
):
    """
    Refresh the access token using a refresh token.

    Implements token rotation: the old refresh token is revoked and
    a new pair is issued.
    """
    return await service.refresh_access_token(db, data.refresh_token)


@router.post("/auth/logout", response_model=MessageResponse, tags=["Authentication"])
async def logout(
    data: RefreshTokenSchema,
    db: AsyncSession = Depends(get_db),
):
    """
    Logout by revoking the refresh token.
    """
    await service.logout(db, data.refresh_token)
    return MessageResponse(message="Logged out successfully.")
