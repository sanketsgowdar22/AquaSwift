"""AquaSwift — Deliveries Service with state machine and OTP verification"""
from __future__ import annotations
import random
import string
import uuid
from datetime import datetime, timezone
import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit import audit_log
from app.core.exceptions import NotFoundError, ValidationError
from app.deliveries.models import DELIVERY_TRANSITIONS, Delivery, DeliveryAssignment, DeliveryEvent

logger = structlog.get_logger()


async def create_delivery(db: AsyncSession, order_id: uuid.UUID, quantity_litres: int,
                          source_id: uuid.UUID | None = None) -> Delivery:
    otp = "".join(random.choices(string.digits, k=6))
    d = Delivery(order_id=order_id, quantity_litres=quantity_litres, source_id=source_id, otp_code=otp)
    db.add(d)
    await db.flush()
    db.add(DeliveryEvent(delivery_id=d.id, event_type="CREATED"))
    await db.flush()
    return d


async def assign_delivery(db: AsyncSession, delivery_id: uuid.UUID, driver_id: uuid.UUID,
                          vehicle_id: uuid.UUID | None, source_id: uuid.UUID | None, actor_id: uuid.UUID) -> Delivery:
    d = await db.get(Delivery, delivery_id)
    if not d:
        raise NotFoundError("Delivery", delivery_id)
    d.driver_id = driver_id
    if vehicle_id:
        d.vehicle_id = vehicle_id
    if source_id:
        d.source_id = source_id
    d.status = "ASSIGNED"
    db.add(DeliveryEvent(delivery_id=d.id, event_type="ASSIGNED", actor_id=actor_id))
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="ASSIGN", entity_type="delivery", entity_id=delivery_id)
    return d


async def respond_to_delivery(db: AsyncSession, delivery_id: uuid.UUID, driver_id: uuid.UUID,
                               accept: bool, rejection_reason: str | None = None) -> Delivery:
    d = await db.get(Delivery, delivery_id)
    if not d:
        raise NotFoundError("Delivery", delivery_id)
    if accept:
        d.status = "ASSIGNED"
        d.driver_id = driver_id
        db.add(DeliveryEvent(delivery_id=d.id, event_type="ACCEPTED", actor_id=None))
    else:
        db.add(DeliveryEvent(delivery_id=d.id, event_type="REJECTED", actor_id=None,
                              metadata_={"reason": rejection_reason}))
    await db.flush()
    return d


async def start_delivery(db: AsyncSession, delivery_id: uuid.UUID, actor_id: uuid.UUID) -> Delivery:
    d = await db.get(Delivery, delivery_id)
    if not d:
        raise NotFoundError("Delivery", delivery_id)
    if d.status != "ASSIGNED":
        raise ValidationError(code="INVALID_STATE", message="Delivery must be ASSIGNED to start.")
    d.status = "STARTED"
    db.add(DeliveryEvent(delivery_id=d.id, event_type="STARTED", actor_id=actor_id))
    await db.flush()
    return d


async def arrive_delivery(db: AsyncSession, delivery_id: uuid.UUID, actor_id: uuid.UUID) -> Delivery:
    d = await db.get(Delivery, delivery_id)
    if not d:
        raise NotFoundError("Delivery", delivery_id)
    if d.status != "STARTED":
        raise ValidationError(code="INVALID_STATE", message="Delivery must be STARTED to arrive.")
    d.status = "ARRIVED"
    db.add(DeliveryEvent(delivery_id=d.id, event_type="ARRIVED", actor_id=actor_id))
    await db.flush()
    return d


async def complete_delivery(db: AsyncSession, delivery_id: uuid.UUID, actor_id: uuid.UUID,
                             otp: str, delivered_qty: int, gps_lat: float | None = None,
                             gps_lng: float | None = None) -> Delivery:
    d = await db.get(Delivery, delivery_id)
    if not d:
        raise NotFoundError("Delivery", delivery_id)
    if d.status != "ARRIVED":
        raise ValidationError(code="INVALID_STATE", message="Delivery must be ARRIVED to complete.")
    if d.otp_code != otp:
        raise ValidationError(code="OTP_MISMATCH", message="Invalid delivery OTP.")

    d.delivered_quantity_litres = delivered_qty
    d.gps_lat = gps_lat
    d.gps_lng = gps_lng
    d.completed_at = datetime.now(timezone.utc)

    if delivered_qty < d.quantity_litres:
        d.status = "PARTIALLY_DELIVERED"
        # Create remainder delivery
        remainder = d.quantity_litres - delivered_qty
        remainder_otp = "".join(random.choices(string.digits, k=6))
        rem_del = Delivery(order_id=d.order_id, quantity_litres=remainder, source_id=d.source_id,
                           otp_code=remainder_otp, parent_delivery_id=d.id)
        db.add(rem_del)
    else:
        d.status = "DELIVERED"

    db.add(DeliveryEvent(delivery_id=d.id, event_type="DELIVERED", actor_id=actor_id,
                          metadata_={"delivered_qty": delivered_qty}))
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="COMPLETE", entity_type="delivery", entity_id=delivery_id)
    return d


async def list_deliveries(db: AsyncSession, status: str | None = None, driver_id: uuid.UUID | None = None,
                           page: int = 1, page_size: int = 20) -> tuple[list[Delivery], int]:
    query = select(Delivery)
    count_q = select(func.count(Delivery.id))
    if status:
        query = query.where(Delivery.status == status)
        count_q = count_q.where(Delivery.status == status)
    if driver_id:
        query = query.where(Delivery.driver_id == driver_id)
        count_q = count_q.where(Delivery.driver_id == driver_id)
    total = (await db.execute(count_q)).scalar_one()
    result = await db.execute(query.order_by(Delivery.created_at.desc()).offset((page - 1) * page_size).limit(page_size))
    return list(result.scalars().all()), total
