"""AquaSwift — Quality Schemas"""
from __future__ import annotations
import uuid
from datetime import date, datetime
from pydantic import BaseModel, Field


class QualityRecordResponse(BaseModel):
    id: uuid.UUID
    source_id: uuid.UUID
    ph_level: float | None
    tds: int | None
    turbidity: float | None
    treatment_type: str | None
    tested_by: str | None
    test_date: date
    certificate_url: str | None
    status: str
    notes: str | None
    created_at: datetime
    model_config = {"from_attributes": True}


class QualityRecordCreate(BaseModel):
    source_id: uuid.UUID
    ph_level: float | None = None
    tds: int | None = None
    turbidity: float | None = None
    treatment_type: str | None = None
    tested_by: str | None = None
    test_date: date
    certificate_url: str | None = None
    notes: str | None = None


class QualityRecordUpdate(BaseModel):
    status: str | None = Field(None, pattern="^(PENDING|APPROVED|REJECTED)$")
    notes: str | None = None
