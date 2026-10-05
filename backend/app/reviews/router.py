"""AquaSwift — Reviews Router"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.core.security import get_current_user
from app.reviews import service

router = APIRouter()


class CreateReviewRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None


class ReviewResponse(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    customer_id: uuid.UUID
    rating: int
    comment: str | None
    model_config = {"from_attributes": True}


@router.post("/orders/{order_id}/reviews", response_model=ReviewResponse, tags=["Reviews"])
async def create_review(order_id: uuid.UUID, data: CreateReviewRequest,
                        user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await service.create_review(db, order_id, user.id, data.rating, data.comment)


@router.get("/drivers/me/reviews", tags=["Reviews"])
async def driver_reviews(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.users.models import DriverProfile
    from sqlalchemy import select
    result = await db.execute(select(DriverProfile).where(DriverProfile.user_id == user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        return {"items": []}
    reviews = await service.list_driver_reviews(db, profile.id)
    return {"items": reviews}
