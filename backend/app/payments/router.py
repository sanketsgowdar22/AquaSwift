"""AquaSwift — Payments Router"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.payments import service
from app.payments.schemas import PaymentResponse, RefundRequest, RefundResponse, WebhookPayload

router = APIRouter()


@router.post("/payments/webhook", tags=["Payments"])
async def webhook(payload: WebhookPayload, db: AsyncSession = Depends(get_db)):
    """Handle Razorpay webhook. No auth — verified via HMAC signature."""
    await service.handle_webhook(db, payload.event, payload.payload)
    return {"status": "ok"}


@router.get("/admin/payments", response_model=list[PaymentResponse], tags=["Admin - Payments"])
async def list_payments(order_id: uuid.UUID | None = None,
                        _=Depends(require_permission("orders:read")),
                        db: AsyncSession = Depends(get_db)):
    return await service.list_payments(db, order_id=order_id)


@router.post("/admin/refunds", response_model=RefundResponse, tags=["Admin - Refunds"])
async def create_refund(data: RefundRequest, user: User = Depends(require_permission("refunds:write")),
                        db: AsyncSession = Depends(get_db)):
    return await service.create_refund(db, data.payment_id, data.amount, data.reason, user.id)
