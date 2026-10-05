"""AquaSwift — Drivers Service"""
from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError, ValidationError
from app.users.models import DriverProfile


async def toggle_status(db: AsyncSession, user_id: uuid.UUID, status: str) -> DriverProfile:
    result = await db.execute(select(DriverProfile).where(DriverProfile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise NotFoundError("DriverProfile", user_id)
    if profile.status == "ON_DELIVERY" and status != "ON_DELIVERY":
        raise ValidationError(code="CANNOT_TOGGLE", message="Cannot change status while on delivery.")
    if status not in ("AVAILABLE", "UNAVAILABLE"):
        raise ValidationError(code="INVALID_STATUS", message="Status must be AVAILABLE or UNAVAILABLE.")
    profile.status = status
    await db.flush()
    return profile


async def get_my_deliveries(db: AsyncSession, user_id: uuid.UUID, page: int = 1, page_size: int = 20):
    from app.deliveries.models import Delivery
    result = await db.execute(select(DriverProfile).where(DriverProfile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise NotFoundError("DriverProfile", user_id)
    from app.deliveries import service as del_svc
    return await del_svc.list_deliveries(db, driver_id=profile.id, page=page, page_size=page_size)
