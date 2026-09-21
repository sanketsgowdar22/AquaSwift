"""AquaSwift — Coupons Schemas"""
from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class CouponResponse(BaseModel):
    id: uuid.UUID
    code: str
    discount_type: str
    discount_value: Decimal
    min_order_amount: Decimal | None
    max_discount_amount: Decimal | None
    valid_from: datetime
    valid_to: datetime
    total_usage_limit: int | None
    per_customer_limit: int
    current_usage_count: int
    is_active: bool
    model_config = {"from_attributes": True}


class CouponCreate(BaseModel):
    code: str = Field(..., min_length=3, max_length=50)
    discount_type: str = Field(..., pattern="^(PERCENTAGE|FIXED_AMOUNT)$")
    discount_value: Decimal = Field(..., gt=0)
    min_order_amount: Decimal | None = None
    max_discount_amount: Decimal | None = None
    valid_from: datetime
    valid_to: datetime
    total_usage_limit: int | None = None
    per_customer_limit: int = 1


class CouponUpdate(BaseModel):
    is_active: bool | None = None
    valid_to: datetime | None = None
    total_usage_limit: int | None = None


class ValidateCouponRequest(BaseModel):
    code: str
    order_amount: Decimal = Field(..., ge=0)


class ValidateCouponResponse(BaseModel):
    valid: bool
    coupon_id: uuid.UUID | None = None
    discount_type: str | None = None
    discount_amount: Decimal = Decimal("0")
    message: str
