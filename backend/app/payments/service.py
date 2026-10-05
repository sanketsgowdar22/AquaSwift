"""AquaSwift — Payments Service"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from decimal import Decimal
import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit import audit_log
from app.core.exceptions import NotFoundError, ValidationError
from app.payments.adapters.razorpay import razorpay_adapter
from app.payments.models import Payment, PaymentTransaction, Refund

logger = structlog.get_logger()


async def create_payment_intent(db: AsyncSession, order_id: uuid.UUID, amount: Decimal,
                                 idempotency_key: str | None = None) -> Payment:
    """Create a payment intent and corresponding gateway order."""
    if idempotency_key:
        result = await db.execute(select(Payment).where(Payment.idempotency_key == idempotency_key))
        existing = result.scalar_one_or_none()
        if existing:
            return existing

    amount_paise = int(amount * 100)
    gateway_response = await razorpay_adapter.create_order(amount_paise)

    payment = Payment(
        order_id=order_id, amount=amount, gateway_order_id=gateway_response["id"],
        idempotency_key=idempotency_key,
    )
    db.add(payment)
    await db.flush()
    logger.info("payment_created", payment_id=str(payment.id), order_id=str(order_id))
    return payment


async def handle_webhook(db: AsyncSession, event: str, payload: dict) -> None:
    """Handle incoming Razorpay webhook events. Idempotent processing."""
    gateway_payment_id = payload.get("payment", {}).get("entity", {}).get("id")
    gateway_order_id = payload.get("payment", {}).get("entity", {}).get("order_id")

    if not gateway_order_id:
        logger.warning("webhook_no_order_id", event=event)
        return

    result = await db.execute(select(Payment).where(Payment.gateway_order_id == gateway_order_id))
    payment = result.scalar_one_or_none()
    if not payment:
        logger.warning("webhook_payment_not_found", gateway_order_id=gateway_order_id)
        return

    # Idempotent: check if already processed
    if payment.status == "SUCCESS" and event == "payment.captured":
        return

    # Record the transaction
    txn = PaymentTransaction(
        payment_id=payment.id, gateway_reference_id=gateway_payment_id,
        event_type=event, raw_payload=payload, verified_at=datetime.now(timezone.utc),
    )
    db.add(txn)

    if event == "payment.captured":
        payment.status = "SUCCESS"
        payment.gateway_payment_id = gateway_payment_id
        # Transition order to CONFIRMED
        from app.orders.models import Order
        order = await db.get(Order, payment.order_id)
        if order and order.status == "PENDING_PAYMENT":
            from app.orders import service as order_service
            await order_service._transition_status(db, order, "CONFIRMED", None)
        logger.info("payment_captured", payment_id=str(payment.id))

    elif event == "payment.failed":
        payment.status = "FAILED"
        logger.info("payment_failed", payment_id=str(payment.id))

    await db.flush()
    await audit_log(db, actor_id=None, action="WEBHOOK", entity_type="payment", entity_id=payment.id,
                    after_state={"event": event, "status": payment.status})


async def create_refund(db: AsyncSession, payment_id: uuid.UUID, amount: Decimal,
                        reason: str, actor_id: uuid.UUID | None = None) -> Refund:
    payment = await db.get(Payment, payment_id)
    if not payment:
        raise NotFoundError("Payment", payment_id)
    if payment.status != "SUCCESS":
        raise ValidationError(code="PAYMENT_NOT_SUCCESS", message="Can only refund successful payments.")

    amount_paise = int(amount * 100)
    gateway_resp = await razorpay_adapter.initiate_refund(
        payment.gateway_payment_id or "", amount_paise, reason
    )

    refund = Refund(
        payment_id=payment_id, amount=amount, reason=reason,
        status="PROCESSING", gateway_refund_id=gateway_resp.get("id"),
        initiated_by=actor_id,
    )
    db.add(refund)
    payment.status = "REFUNDED"
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="REFUND", entity_type="payment", entity_id=payment_id)
    logger.info("refund_created", refund_id=str(refund.id), payment_id=str(payment_id))
    return refund


async def list_payments(db: AsyncSession, order_id: uuid.UUID | None = None) -> list[Payment]:
    query = select(Payment).order_by(Payment.created_at.desc())
    if order_id:
        query = query.where(Payment.order_id == order_id)
    return list((await db.execute(query)).scalars().all())
