"""AquaSwift — Notifications Service"""
from __future__ import annotations
import uuid
import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.notifications.models import DeviceToken, Notification

logger = structlog.get_logger()


async def send_notification(db: AsyncSession, user_id: uuid.UUID, title: str, body: str,
                             channel: str = "push", event_type: str | None = None,
                             reference_type: str | None = None, reference_id: uuid.UUID | None = None) -> Notification:
    """Create and dispatch a notification. Channel adapters are stubs."""
    notif = Notification(
        user_id=user_id, title=title, body=body, channel=channel,
        event_type=event_type, reference_type=reference_type, reference_id=reference_id,
    )
    db.add(notif)
    await db.flush()

    # Dispatch via channel adapter (stub)
    if channel == "push":
        await _send_push_stub(user_id, title, body)
    elif channel == "sms":
        logger.info("notification_sms_stub", user_id=str(user_id), title=title)
    elif channel == "email":
        logger.info("notification_email_stub", user_id=str(user_id), title=title)

    return notif


async def _send_push_stub(user_id: uuid.UUID, title: str, body: str):
    logger.info("notification_push_stub", user_id=str(user_id), title=title, body=body)


async def list_notifications(db: AsyncSession, user_id: uuid.UUID, limit: int = 50) -> list[Notification]:
    result = await db.execute(
        select(Notification).where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc()).limit(limit)
    )
    return list(result.scalars().all())


async def register_device(db: AsyncSession, user_id: uuid.UUID, token: str, platform: str) -> DeviceToken:
    # Deactivate existing tokens for same device
    await db.execute(
        update(DeviceToken).where(DeviceToken.user_id == user_id, DeviceToken.token == token).values(is_active=True)
    )
    # Check if exists
    result = await db.execute(select(DeviceToken).where(DeviceToken.user_id == user_id, DeviceToken.token == token))
    existing = result.scalar_one_or_none()
    if existing:
        return existing

    dt = DeviceToken(user_id=user_id, token=token, platform=platform)
    db.add(dt)
    await db.flush()
    return dt
