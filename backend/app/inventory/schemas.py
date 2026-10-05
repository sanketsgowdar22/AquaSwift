"""AquaSwift — Inventory Schemas"""
from __future__ import annotations
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class BalanceResponse(BaseModel):
    source_id: uuid.UUID
    source_name: str | None = None
    available_litres: int
    reserved_litres: int
    allocated_litres: int
    total_litres: int = 0
    model_config = {"from_attributes": True}


class TransactionResponse(BaseModel):
    id: uuid.UUID
    source_id: uuid.UUID
    type: str
    quantity_litres: int
    reference_type: str | None
    reference_id: uuid.UUID | None
    notes: str | None
    created_by: uuid.UUID
    created_at: datetime
    model_config = {"from_attributes": True}


class ReceiveRequest(BaseModel):
    source_id: uuid.UUID
    quantity_litres: int = Field(..., gt=0)
    notes: str | None = None


class AdjustRequest(BaseModel):
    source_id: uuid.UUID
    quantity_litres: int  # Can be negative
    reason: str = Field(..., min_length=5, description="Mandatory reason for adjustment")
