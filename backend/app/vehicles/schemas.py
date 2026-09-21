"""AquaSwift — Vehicles Schemas"""
from __future__ import annotations
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class VehicleResponse(BaseModel):
    id: uuid.UUID
    registration_number: str
    type: str
    capacity_litres: int
    status: str
    current_driver_id: uuid.UUID | None
    created_at: datetime
    model_config = {"from_attributes": True}


class VehicleCreate(BaseModel):
    registration_number: str = Field(..., max_length=20)
    type: str = Field(..., max_length=50)
    capacity_litres: int = Field(..., gt=0)


class VehicleUpdate(BaseModel):
    type: str | None = None
    capacity_litres: int | None = Field(None, gt=0)
    status: str | None = Field(None, pattern="^(ACTIVE|INACTIVE|MAINTENANCE)$")


class AssignDriverRequest(BaseModel):
    driver_profile_id: uuid.UUID
