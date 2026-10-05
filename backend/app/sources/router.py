"""AquaSwift — Sources Router"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.sources import service
from app.sources.schemas import SourceCreate, SourceResponse, SourceUpdate

router = APIRouter()


@router.get("/admin/sources", response_model=list[SourceResponse], tags=["Admin - Sources"])
async def list_sources(_=Depends(require_permission("sources:read")), db: AsyncSession = Depends(get_db)):
    return await service.list_sources(db)


@router.post("/admin/sources", response_model=SourceResponse, tags=["Admin - Sources"])
async def create_source(data: SourceCreate, user: User = Depends(require_permission("sources:write")),
                        db: AsyncSession = Depends(get_db)):
    return await service.create_source(db, data, user.id)


@router.patch("/admin/sources/{source_id}", response_model=SourceResponse, tags=["Admin - Sources"])
async def update_source(source_id: uuid.UUID, data: SourceUpdate,
                        user: User = Depends(require_permission("sources:write")),
                        db: AsyncSession = Depends(get_db)):
    return await service.update_source(db, source_id, data, user.id)
