"""AquaSwift — Catalog Schemas"""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class PurposeResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    icon_url: str | None
    display_order: int
    is_active: bool
    model_config = {"from_attributes": True}


class PurposeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    icon_url: str | None = None
    display_order: int = 0


class PurposeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    icon_url: str | None = None
    display_order: int | None = None
    is_active: bool | None = None


class QualityTypeResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    is_active: bool
    model_config = {"from_attributes": True}


class QualityTypeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class QualityTypeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class DeliveryMethodResponse(BaseModel):
    id: uuid.UUID
    name: str
    is_active: bool
    model_config = {"from_attributes": True}


class DeliveryMethodCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class DeliveryMethodUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None


class VariantResponse(BaseModel):
    id: uuid.UUID
    purpose_id: uuid.UUID
    quality_id: uuid.UUID
    delivery_method_id: uuid.UUID
    min_quantity_litres: int
    max_quantity_litres: int
    is_active: bool
    purpose_name: str | None = None
    quality_name: str | None = None
    delivery_method_name: str | None = None
    model_config = {"from_attributes": True}


class VariantCreate(BaseModel):
    purpose_id: uuid.UUID
    quality_id: uuid.UUID
    delivery_method_id: uuid.UUID
    min_quantity_litres: int = Field(..., gt=0)
    max_quantity_litres: int = Field(..., gt=0)


class VariantUpdate(BaseModel):
    min_quantity_litres: int | None = Field(None, gt=0)
    max_quantity_litres: int | None = Field(None, gt=0)
    is_active: bool | None = None
