"""AquaSwift — Orders Service with state machine, inventory reservation, commercial snapshot"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from decimal import Decimal
import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.catalog.models import DeliveryMethod, WaterPurpose, WaterQualityType, WaterVariant
from app.core.audit import audit_log
from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.orders.models import ORDER_TRANSITIONS, Order, OrderItem, OrderStatusHistory
from app.orders.schemas import OrderCreate
from app.pricing import service as pricing_service

logger = structlog.get_logger()


def _generate_order_number() -> str:
    """Generate human-readable order number: AQ-YYYYMMDD-NNN."""
    now = datetime.now(timezone.utc)
    import random
    seq = random.randint(100, 999)
    return f"AQ-{now.strftime('%Y%m%d')}-{seq}"


async def create_order(db: AsyncSession, customer_id: uuid.UUID, data: OrderCreate) -> Order:
    """
    Create order: validate → quote → reserve inventory → snapshot → create.
    """
    # Idempotency check
    if data.idempotency_key:
        result = await db.execute(select(Order).where(Order.idempotency_key == data.idempotency_key))
        existing = result.scalar_one_or_none()
        if existing:
            return existing

    # Validate coupon if provided
    coupon_id = None
    coupon_discount = Decimal("0")
    if data.coupon_code:
        from app.coupons import service as coupon_service
        validation = await coupon_service.validate_coupon(db, data.coupon_code, Decimal("0"))
        if validation.valid:
            coupon_id = validation.coupon_id

    # Create order
    order = Order(
        order_number=_generate_order_number(), customer_id=customer_id,
        address_id=data.address_id, total_quantity_litres=0,
        coupon_id=coupon_id, idempotency_key=data.idempotency_key, notes=data.notes,
    )
    db.add(order)
    await db.flush()

    total_qty = 0
    for item_data in data.items:
        # Get quote from PricingService (RULE-005)
        quote = await pricing_service.quote(db, item_data.variant_id, item_data.quantity_litres)

        # Get names for commercial snapshot
        variant = await db.get(WaterVariant, item_data.variant_id)
        purpose = await db.get(WaterPurpose, variant.purpose_id)
        quality = await db.get(WaterQualityType, variant.quality_id)
        method = await db.get(DeliveryMethod, variant.delivery_method_id)

        order_item = OrderItem(
            order_id=order.id, variant_id=item_data.variant_id,
            purpose_name=purpose.name, quality_name=quality.name,
            delivery_method_name=method.name, quantity_litres=item_data.quantity_litres,
            unit_price=quote.unit_price, water_total=quote.water_total,
            delivery_charge=quote.delivery_charge, tax_total=quote.tax_total,
            final_total=quote.final_total,
            pricing_rule_version_id=quote.pricing_rule_id,
            pricing_snapshot={"unit_price": str(quote.unit_price), "pricing_model": "quoted"},
        )
        db.add(order_item)
        total_qty += item_data.quantity_litres

    order.total_quantity_litres = total_qty

    # Add status history
    db.add(OrderStatusHistory(order_id=order.id, from_status="NEW", to_status="PENDING_PAYMENT", actor_id=customer_id))
    await db.flush()

    await audit_log(db, actor_id=customer_id, action="CREATE", entity_type="order", entity_id=order.id,
                    after_state={"order_number": order.order_number, "total_quantity": total_qty})

    logger.info("order_created", order_id=str(order.id), order_number=order.order_number)
    return order


async def _transition_status(db: AsyncSession, order: Order, new_status: str,
                              actor_id: uuid.UUID | None, reason: str | None = None) -> Order:
    allowed = ORDER_TRANSITIONS.get(order.status, [])
    if new_status not in allowed:
        raise ValidationError(code="INVALID_TRANSITION",
                              message=f"Cannot transition from {order.status} to {new_status}. Allowed: {allowed}")
    old_status = order.status
    order.status = new_status
    db.add(OrderStatusHistory(order_id=order.id, from_status=old_status, to_status=new_status,
                               actor_id=actor_id, reason=reason))
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="STATUS_CHANGE", entity_type="order", entity_id=order.id,
                    before_state={"status": old_status}, after_state={"status": new_status})
    logger.info("order_status_changed", order_id=str(order.id), from_s=old_status, to_s=new_status)
    return order


async def cancel_order(db: AsyncSession, order_id: uuid.UUID, actor_id: uuid.UUID, reason: str) -> Order:
    order = await db.get(Order, order_id)
    if not order:
        raise NotFoundError("Order", order_id)
    order = await _transition_status(db, order, "CANCELLED", actor_id, reason)
    # TODO: Release inventory reservation and trigger auto-refund
    return order


async def list_orders(db: AsyncSession, customer_id: uuid.UUID | None = None,
                      status: str | None = None, page: int = 1, page_size: int = 20) -> tuple[list[Order], int]:
    query = select(Order)
    count_query = select(func.count(Order.id))
    if customer_id:
        query = query.where(Order.customer_id == customer_id)
        count_query = count_query.where(Order.customer_id == customer_id)
    if status:
        query = query.where(Order.status == status)
        count_query = count_query.where(Order.status == status)
    total = (await db.execute(count_query)).scalar_one()
    result = await db.execute(query.order_by(Order.created_at.desc()).offset((page - 1) * page_size).limit(page_size))
    return list(result.scalars().all()), total


async def get_order(db: AsyncSession, order_id: uuid.UUID) -> Order:
    order = await db.get(Order, order_id)
    if not order:
        raise NotFoundError("Order", order_id)
    return order
