"""AquaSwift — Sources Schemas"""
from __future__ import annotations
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class SourceResponse(BaseModel):
    id: uuid.UUID
    name: str
    type: str
    gps_lat: float | None
    gps_lng: float | None
    capacity_litres: int
    status: str
    created_at: datetime
    model_config = {"from_attributes": True}


class SourceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., min_length=1, max_length=50)
    gps_lat: float | None = None
    gps_lng: float | None = None
    capacity_litres: int = Field(..., gt=0)


class SourceUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    gps_lat: float | None = None
    gps_lng: float | None = None
    capacity_litres: int | None = Field(None, gt=0)
    status: str | None = Field(None, pattern="^(ACTIVE|INACTIVE|MAINTENANCE)$")
