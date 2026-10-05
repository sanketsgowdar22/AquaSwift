"""AquaSwift — Orders Schemas"""
from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    variant_id: uuid.UUID
    quantity_litres: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    address_id: uuid.UUID
    items: list[OrderItemCreate] = Field(..., min_length=1)
    coupon_code: str | None = None
    idempotency_key: str | None = None
    notes: str | None = None


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    variant_id: uuid.UUID
    purpose_name: str
    quality_name: str
    delivery_method_name: str
    quantity_litres: int
    unit_price: Decimal
    water_total: Decimal
    delivery_charge: Decimal
    discount_total: Decimal
    tax_total: Decimal
    final_total: Decimal
    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: uuid.UUID
    order_number: str
    customer_id: uuid.UUID
    status: str
    order_type: str
    total_quantity_litres: int
    items: list[OrderItemResponse] = []
    notes: str | None
    created_at: datetime
    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    items: list[OrderResponse]
    total: int
    page: int
    page_size: int


class CancelOrderRequest(BaseModel):
    reason: str = Field(..., min_length=5)
