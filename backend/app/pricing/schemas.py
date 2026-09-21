"""AquaSwift — Pricing Schemas"""
from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class PricingRuleResponse(BaseModel):
    id: uuid.UUID
    version: int
    purpose_id: uuid.UUID | None
    quality_id: uuid.UUID | None
    customer_type: str | None
    pricing_model: str
    base_price: Decimal
    tiers: list | None
    active_from: datetime
    active_to: datetime | None
    is_active: bool
    model_config = {"from_attributes": True}


class PricingRuleCreate(BaseModel):
    purpose_id: uuid.UUID | None = None
    quality_id: uuid.UUID | None = None
    customer_type: str | None = None
    pricing_model: str = Field(..., pattern="^(FIXED|PER_LITRE|TIERED)$")
    base_price: Decimal = Field(..., ge=0)
    tiers: list | None = None
    active_from: datetime
    active_to: datetime | None = None


class PricingRuleUpdate(BaseModel):
    base_price: Decimal | None = Field(None, ge=0)
    tiers: list | None = None
    active_to: datetime | None = None
    is_active: bool | None = None


class QuoteRequest(BaseModel):
    variant_id: uuid.UUID
    quantity_litres: int = Field(..., gt=0)
    customer_type: str = "INDIVIDUAL"


class QuoteResponse(BaseModel):
    variant_id: uuid.UUID
    quantity_litres: int
    unit_price: Decimal
    water_total: Decimal
    delivery_charge: Decimal
    tax_total: Decimal
    final_total: Decimal
    pricing_rule_id: uuid.UUID | None
    pricing_rule_version: int | None
