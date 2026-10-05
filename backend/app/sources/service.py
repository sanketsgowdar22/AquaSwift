"""AquaSwift — Sources Service"""
from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit import audit_log
from app.core.exceptions import NotFoundError
from app.sources.models import WaterSource
from app.sources.schemas import SourceCreate, SourceUpdate


async def list_sources(db: AsyncSession) -> list[WaterSource]:
    result = await db.execute(select(WaterSource).order_by(WaterSource.name))
    return list(result.scalars().all())


async def get_source(db: AsyncSession, source_id: uuid.UUID) -> WaterSource:
    result = await db.execute(select(WaterSource).where(WaterSource.id == source_id))
    source = result.scalar_one_or_none()
    if not source:
        raise NotFoundError("WaterSource", source_id)
    return source


async def create_source(db: AsyncSession, data: SourceCreate, actor_id: uuid.UUID) -> WaterSource:
    source = WaterSource(**data.model_dump())
    db.add(source)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="CREATE", entity_type="water_source", entity_id=source.id)
    return source


async def update_source(db: AsyncSession, source_id: uuid.UUID, data: SourceUpdate, actor_id: uuid.UUID) -> WaterSource:
    source = await get_source(db, source_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(source, field, value)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="UPDATE", entity_type="water_source", entity_id=source_id)
    return source
