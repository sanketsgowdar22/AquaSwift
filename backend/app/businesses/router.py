"""AquaSwift — B2B Admin Router (stub CRUD)"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.businesses.models import Business
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.core.exceptions import NotFoundError

router = APIRouter()


class BusinessCreate(BaseModel):
    name: str = Field(..., min_length=1)
    registration_number: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None


class BusinessResponse(BaseModel):
    id: uuid.UUID
    name: str
    registration_number: str | None
    contact_email: str | None
    contact_phone: str | None
    is_active: bool
    model_config = {"from_attributes": True}


@router.get("/admin/businesses", response_model=list[BusinessResponse], tags=["Admin - B2B"])
async def list_businesses(_=Depends(require_permission("businesses:read")), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Business).order_by(Business.name))
    return list(result.scalars().all())


@router.post("/admin/businesses", response_model=BusinessResponse, tags=["Admin - B2B"])
async def create_business(data: BusinessCreate, user: User = Depends(require_permission("businesses:write")),
                           db: AsyncSession = Depends(get_db)):
    biz = Business(**data.model_dump())
    db.add(biz)
    await db.flush()
    return biz


@router.patch("/admin/businesses/{biz_id}", response_model=BusinessResponse, tags=["Admin - B2B"])
async def update_business(biz_id: uuid.UUID, data: BusinessCreate,
                           user: User = Depends(require_permission("businesses:write")),
                           db: AsyncSession = Depends(get_db)):
    biz = await db.get(Business, biz_id)
    if not biz:
        raise NotFoundError("Business", biz_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(biz, field, value)
    await db.flush()
    return biz
