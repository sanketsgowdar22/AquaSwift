"""AquaSwift — Notifications Router"""
from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from app.auth.models import User
from app.core.database import get_db
from app.core.security import get_current_user
from app.notifications import service

router = APIRouter()


class RegisterDeviceRequest(BaseModel):
    token: str = Field(..., min_length=1)
    platform: str = Field(..., pattern="^(android|ios|web)$")


class NotificationResponse(BaseModel):
    id: str
    title: str
    body: str
    channel: str
    event_type: str | None
    is_read: bool
    created_at: str
    model_config = {"from_attributes": True}


@router.post("/notifications/register-device", tags=["Notifications"])
async def register_device(data: RegisterDeviceRequest, user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    dt = await service.register_device(db, user.id, data.token, data.platform)
    return {"message": "Device registered.", "device_id": str(dt.id)}


@router.get("/notifications", tags=["Notifications"])
async def list_notifications(limit: int = Query(50, ge=1, le=200),
                              user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    notifs = await service.list_notifications(db, user.id, limit=limit)
    return {"items": notifs}
