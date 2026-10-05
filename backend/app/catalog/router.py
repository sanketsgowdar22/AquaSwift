"""AquaSwift — Catalog Router"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.catalog import service
from app.catalog.schemas import (DeliveryMethodCreate, DeliveryMethodResponse, DeliveryMethodUpdate,
                                  PurposeCreate, PurposeResponse, PurposeUpdate,
                                  QualityTypeCreate, QualityTypeResponse, QualityTypeUpdate,
                                  VariantCreate, VariantResponse, VariantUpdate)
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.core.security import get_current_user

router = APIRouter()


# ---- Public (no auth) ----

@router.get("/catalog/purposes", response_model=list[PurposeResponse], tags=["Catalog"])
async def list_purposes(db: AsyncSession = Depends(get_db)):
    return await service.list_purposes(db)


@router.get("/catalog/qualities", response_model=list[QualityTypeResponse], tags=["Catalog"])
async def list_qualities(db: AsyncSession = Depends(get_db)):
    return await service.list_quality_types(db)


@router.get("/catalog/methods", response_model=list[DeliveryMethodResponse], tags=["Catalog"])
async def list_methods(db: AsyncSession = Depends(get_db)):
    return await service.list_delivery_methods(db)


@router.get("/catalog/variants", response_model=list[VariantResponse], tags=["Catalog"])
async def list_variants(purpose_id: uuid.UUID | None = None, db: AsyncSession = Depends(get_db)):
    return await service.list_variants(db, purpose_id=purpose_id)


# ---- Admin ----

@router.post("/admin/catalog/purposes", response_model=PurposeResponse, tags=["Admin - Catalog"])
async def create_purpose(data: PurposeCreate, user: User = Depends(require_permission("catalog:write")),
                         db: AsyncSession = Depends(get_db)):
    return await service.create_purpose(db, data, user.id)


@router.patch("/admin/catalog/purposes/{purpose_id}", response_model=PurposeResponse, tags=["Admin - Catalog"])
async def update_purpose(purpose_id: uuid.UUID, data: PurposeUpdate,
                         user: User = Depends(require_permission("catalog:write")),
                         db: AsyncSession = Depends(get_db)):
    return await service.update_purpose(db, purpose_id, data, user.id)


@router.post("/admin/catalog/qualities", response_model=QualityTypeResponse, tags=["Admin - Catalog"])
async def create_quality(data: QualityTypeCreate, user: User = Depends(require_permission("catalog:write")),
                         db: AsyncSession = Depends(get_db)):
    return await service.create_quality_type(db, data, user.id)


@router.patch("/admin/catalog/qualities/{qt_id}", response_model=QualityTypeResponse, tags=["Admin - Catalog"])
async def update_quality(qt_id: uuid.UUID, data: QualityTypeUpdate,
                         user: User = Depends(require_permission("catalog:write")),
                         db: AsyncSession = Depends(get_db)):
    return await service.update_quality_type(db, qt_id, data, user.id)


@router.post("/admin/catalog/methods", response_model=DeliveryMethodResponse, tags=["Admin - Catalog"])
async def create_method(data: DeliveryMethodCreate, user: User = Depends(require_permission("catalog:write")),
                        db: AsyncSession = Depends(get_db)):
    return await service.create_delivery_method(db, data, user.id)


@router.patch("/admin/catalog/methods/{dm_id}", response_model=DeliveryMethodResponse, tags=["Admin - Catalog"])
async def update_method(dm_id: uuid.UUID, data: DeliveryMethodUpdate,
                        user: User = Depends(require_permission("catalog:write")),
                        db: AsyncSession = Depends(get_db)):
    return await service.update_delivery_method(db, dm_id, data, user.id)


@router.post("/admin/catalog/variants", response_model=VariantResponse, tags=["Admin - Catalog"])
async def create_variant(data: VariantCreate, user: User = Depends(require_permission("catalog:write")),
                         db: AsyncSession = Depends(get_db)):
    v = await service.create_variant(db, data, user.id)
    variants = await service.list_variants(db, include_inactive=True)
    return next((x for x in variants if x["id"] == v.id), v)


@router.patch("/admin/catalog/variants/{variant_id}", response_model=VariantResponse, tags=["Admin - Catalog"])
async def update_variant(variant_id: uuid.UUID, data: VariantUpdate,
                         user: User = Depends(require_permission("catalog:write")),
                         db: AsyncSession = Depends(get_db)):
    v = await service.update_variant(db, variant_id, data, user.id)
    variants = await service.list_variants(db, include_inactive=True)
    return next((x for x in variants if x["id"] == v.id), v)
