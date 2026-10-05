"""AquaSwift — Drivers Router"""
from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.database import get_db
from app.core.security import get_current_user
from app.drivers import service
from pydantic import BaseModel

router = APIRouter()


class StatusUpdate(BaseModel):
    status: str


@router.patch("/drivers/me/status", tags=["Drivers"])
async def update_status(data: StatusUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    profile = await service.toggle_status(db, user.id, data.status)
    return {"status": profile.status}


@router.get("/drivers/me/deliveries", tags=["Drivers"])
async def my_deliveries(page: int = Query(1, ge=1), user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    deliveries, total = await service.get_my_deliveries(db, user.id, page=page)
    return {"items": deliveries, "total": total}
