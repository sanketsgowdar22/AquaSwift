"""
AquaSwift — Users Schemas
"""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class UserProfileResponse(BaseModel):
    id: uuid.UUID
    phone: str | None
    email: str | None
    full_name: str
    is_active: bool
    roles: list[str] = []
    customer_profile: CustomerProfileResponse | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class CustomerProfileResponse(BaseModel):
    id: uuid.UUID
    customer_type: str
    preferences: dict | None = None

    model_config = {"from_attributes": True}


class UpdateProfileRequest(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=255)


class AdminUserListResponse(BaseModel):
    items: list[UserProfileResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AdminUpdateUserRequest(BaseModel):
    full_name: str | None = None
    is_active: bool | None = None


class DriverProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    license_number: str | None
    status: str
    gps_lat: float | None
    gps_lng: float | None
    created_at: datetime

    model_config = {"from_attributes": True}


# Fix forward references
UserProfileResponse.model_rebuild()
