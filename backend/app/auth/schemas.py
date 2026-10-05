"""
AquaSwift — Auth Schemas
"""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class OTPRequestSchema(BaseModel):
    phone: str = Field(..., pattern=r"^\+91\d{10}$", description="Indian phone number with +91 prefix")


class OTPVerifySchema(BaseModel):
    phone: str = Field(..., pattern=r"^\+91\d{10}$")
    otp: str = Field(..., min_length=6, max_length=6)
    full_name: str | None = Field(None, min_length=1, max_length=255, description="Required for new users")


class EmailLoginSchema(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=6)


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserBriefResponse


class UserBriefResponse(BaseModel):
    id: uuid.UUID
    phone: str | None
    email: str | None
    full_name: str
    is_active: bool
    roles: list[str] = []
    created_at: datetime

    model_config = {"from_attributes": True}


# Fix forward reference
TokenResponse.model_rebuild()


class MessageResponse(BaseModel):
    message: str
    detail: dict | None = None
