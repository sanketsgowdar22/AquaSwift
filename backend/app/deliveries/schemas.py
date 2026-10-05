"""AquaSwift — Deliveries Schemas"""
from __future__ import annotations
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class DeliveryResponse(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    source_id: uuid.UUID | None
    driver_id: uuid.UUID | None
    vehicle_id: uuid.UUID | None
    status: str
    quantity_litres: int
    delivered_quantity_litres: int | None
    otp_code: str | None
    scheduled_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    model_config = {"from_attributes": True}


class AssignDeliveryRequest(BaseModel):
    driver_id: uuid.UUID
    vehicle_id: uuid.UUID | None = None
    source_id: uuid.UUID | None = None


class RespondRequest(BaseModel):
    accept: bool
    rejection_reason: str | None = None


class CompleteDeliveryRequest(BaseModel):
    otp: str = Field(..., min_length=6, max_length=6)
    delivered_quantity_litres: int = Field(..., gt=0)
    gps_lat: float | None = None
    gps_lng: float | None = None
