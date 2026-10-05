"""AquaSwift — Coupons Service"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit import audit_log
from app.core.exceptions import NotFoundError, ValidationError
from app.coupons.models import Coupon
from app.coupons.schemas import CouponCreate, CouponUpdate, ValidateCouponResponse


async def validate_coupon(db: AsyncSession, code: str, order_amount: Decimal) -> ValidateCouponResponse:
    result = await db.execute(select(Coupon).where(Coupon.code == code.upper()))
    coupon = result.scalar_one_or_none()
    if not coupon or not coupon.is_active:
        return ValidateCouponResponse(valid=False, message="Invalid or inactive coupon code.")
    now = datetime.now(timezone.utc)
    if now < coupon.valid_from or now > coupon.valid_to:
        return ValidateCouponResponse(valid=False, message="Coupon has expired or is not yet valid.")
    if coupon.total_usage_limit and coupon.current_usage_count >= coupon.total_usage_limit:
        return ValidateCouponResponse(valid=False, message="Coupon usage limit reached.")
    if coupon.min_order_amount and order_amount < coupon.min_order_amount:
        return ValidateCouponResponse(valid=False, message=f"Minimum order amount is ₹{coupon.min_order_amount}.")
    discount = _calculate_discount(coupon, order_amount)
    return ValidateCouponResponse(valid=True, coupon_id=coupon.id, discount_type=coupon.discount_type,
                                   discount_amount=discount, message="Coupon is valid.")


def _calculate_discount(coupon: Coupon, order_amount: Decimal) -> Decimal:
    if coupon.discount_type == "FIXED_AMOUNT":
        return min(coupon.discount_value, order_amount)
    elif coupon.discount_type == "PERCENTAGE":
        discount = order_amount * coupon.discount_value / 100
        if coupon.max_discount_amount:
            discount = min(discount, coupon.max_discount_amount)
        return round(discount, 2)
    return Decimal("0")


async def use_coupon(db: AsyncSession, coupon_id: uuid.UUID) -> None:
    coupon = await db.get(Coupon, coupon_id)
    if coupon:
        coupon.current_usage_count += 1
        await db.flush()


async def list_coupons(db: AsyncSession) -> list[Coupon]:
    result = await db.execute(select(Coupon).order_by(Coupon.created_at.desc()))
    return list(result.scalars().all())


async def create_coupon(db: AsyncSession, data: CouponCreate, actor_id: uuid.UUID) -> Coupon:
    coupon = Coupon(**data.model_dump())
    coupon.code = coupon.code.upper()
    db.add(coupon)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="CREATE", entity_type="coupon", entity_id=coupon.id)
    return coupon


async def update_coupon(db: AsyncSession, coupon_id: uuid.UUID, data: CouponUpdate, actor_id: uuid.UUID) -> Coupon:
    coupon = await db.get(Coupon, coupon_id)
    if not coupon:
        raise NotFoundError("Coupon", coupon_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(coupon, field, value)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="UPDATE", entity_type="coupon", entity_id=coupon_id)
    return coupon
