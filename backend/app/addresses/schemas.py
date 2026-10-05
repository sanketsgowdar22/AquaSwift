"""AquaSwift — Addresses Schemas"""
from __future__ import annotations
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class AddressResponse(BaseModel):
    id: uuid.UUID
    label: str | None
    address_line_1: str
    address_line_2: str | None
    city: str
    state: str
    pincode: str
    lat: float | None
    lng: float | None
    formatted_address: str | None
    notes: str | None
    is_default: bool
    created_at: datetime
    model_config = {"from_attributes": True}


class AddressCreate(BaseModel):
    label: str | None = Field(None, max_length=50)
    address_line_1: str = Field(..., min_length=1, max_length=255)
    address_line_2: str | None = None
    city: str = Field(default="Hyderabad", max_length=100)
    state: str = Field(default="Telangana", max_length=100)
    pincode: str = Field(..., pattern=r"^\d{6}$")
    lat: float | None = None
    lng: float | None = None
    notes: str | None = None
    is_default: bool = False


class AddressUpdate(BaseModel):
    label: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    state: str | None = None
    pincode: str | None = Field(None, pattern=r"^\d{6}$")
    lat: float | None = None
    lng: float | None = None
    notes: str | None = None
    is_default: bool | None = None
