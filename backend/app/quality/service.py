"""AquaSwift — Quality Service"""
from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit import audit_log
from app.core.exceptions import NotFoundError
from app.quality.models import WaterQualityRecord
from app.quality.schemas import QualityRecordCreate, QualityRecordUpdate


async def list_records(db: AsyncSession, source_id: uuid.UUID | None = None) -> list[WaterQualityRecord]:
    query = select(WaterQualityRecord).order_by(WaterQualityRecord.created_at.desc())
    if source_id:
        query = query.where(WaterQualityRecord.source_id == source_id)
    return list((await db.execute(query)).scalars().all())


async def create_record(db: AsyncSession, data: QualityRecordCreate, actor_id: uuid.UUID) -> WaterQualityRecord:
    record = WaterQualityRecord(**data.model_dump())
    db.add(record)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="CREATE", entity_type="water_quality_record", entity_id=record.id)
    return record


async def update_record(db: AsyncSession, record_id: uuid.UUID, data: QualityRecordUpdate, actor_id: uuid.UUID) -> WaterQualityRecord:
    result = await db.execute(select(WaterQualityRecord).where(WaterQualityRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundError("WaterQualityRecord", record_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(record, field, value)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="UPDATE", entity_type="water_quality_record", entity_id=record_id)
    return record
