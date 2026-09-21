"""AquaSwift — Payments Schemas"""
from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class PaymentResponse(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    amount: Decimal
    currency: str
    status: str
    gateway: str
    gateway_order_id: str | None
    gateway_payment_id: str | None
    created_at: datetime
    model_config = {"from_attributes": True}


class WebhookPayload(BaseModel):
    """Razorpay webhook payload (simplified)."""
    event: str  # payment.captured, payment.failed, refund.processed
    payload: dict


class RefundRequest(BaseModel):
    payment_id: uuid.UUID
    amount: Decimal = Field(..., gt=0)
    reason: str = Field(..., min_length=5)


class RefundResponse(BaseModel):
    id: uuid.UUID
    payment_id: uuid.UUID
    amount: Decimal
    reason: str
    status: str
    created_at: datetime
    model_config = {"from_attributes": True}
