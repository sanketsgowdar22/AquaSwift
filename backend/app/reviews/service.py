"""AquaSwift — Reviews Service"""
from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError, ValidationError
from app.orders.models import Order
from app.reviews.models import Review


async def create_review(db: AsyncSession, order_id: uuid.UUID, customer_id: uuid.UUID,
                        rating: int, comment: str | None = None) -> Review:
    order = await db.get(Order, order_id)
    if not order:
        raise NotFoundError("Order", order_id)
    if order.status != "DELIVERED":
        raise ValidationError(code="ORDER_NOT_DELIVERED", message="Can only review delivered orders.")
    if order.customer_id != customer_id:
        raise ValidationError(code="NOT_YOUR_ORDER", message="You can only review your own orders.")

    # Check for duplicate
    result = await db.execute(select(Review).where(Review.order_id == order_id, Review.customer_id == customer_id))
    if result.scalar_one_or_none():
        raise ValidationError(code="ALREADY_REVIEWED", message="You have already reviewed this order.")

    if not 1 <= rating <= 5:
        raise ValidationError(code="INVALID_RATING", message="Rating must be between 1 and 5.")

    review = Review(order_id=order_id, customer_id=customer_id, rating=rating, comment=comment)
    db.add(review)
    await db.flush()
    return review


async def list_driver_reviews(db: AsyncSession, driver_id: uuid.UUID) -> list[Review]:
    result = await db.execute(select(Review).where(Review.driver_id == driver_id).order_by(Review.created_at.desc()))
    return list(result.scalars().all())
