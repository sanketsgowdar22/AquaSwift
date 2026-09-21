"""AquaSwift — Quality Router"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.quality import service
from app.quality.schemas import QualityRecordCreate, QualityRecordResponse, QualityRecordUpdate

router = APIRouter()


@router.get("/admin/quality/records", response_model=list[QualityRecordResponse], tags=["Admin - Quality"])
async def list_records(source_id: uuid.UUID | None = None, _=Depends(require_permission("quality:read")),
                       db: AsyncSession = Depends(get_db)):
    return await service.list_records(db, source_id=source_id)


@router.post("/admin/quality/records", response_model=QualityRecordResponse, tags=["Admin - Quality"])
async def create_record(data: QualityRecordCreate, user: User = Depends(require_permission("quality:write")),
                        db: AsyncSession = Depends(get_db)):
    return await service.create_record(db, data, user.id)


@router.patch("/admin/quality/records/{record_id}", response_model=QualityRecordResponse, tags=["Admin - Quality"])
async def update_record(record_id: uuid.UUID, data: QualityRecordUpdate,
                        user: User = Depends(require_permission("quality:write")),
                        db: AsyncSession = Depends(get_db)):
    return await service.update_record(db, record_id, data, user.id)
