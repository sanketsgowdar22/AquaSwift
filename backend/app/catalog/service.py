"""AquaSwift — Catalog Service with Redis caching"""

from __future__ import annotations

import uuid

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.catalog.models import DeliveryMethod, WaterPurpose, WaterPurposeQuality, WaterQualityType, WaterVariant
from app.catalog.schemas import (DeliveryMethodCreate, DeliveryMethodUpdate, PurposeCreate, PurposeUpdate,
                                  QualityTypeCreate, QualityTypeUpdate, VariantCreate, VariantUpdate)
from app.core.audit import audit_log
from app.core.cache import cache_delete_pattern, cache_get, cache_set
from app.core.exceptions import ConflictError, NotFoundError

logger = structlog.get_logger()
CACHE_TTL = 60  # seconds


# ---- Water Purposes ----

async def list_purposes(db: AsyncSession, include_inactive: bool = False) -> list[WaterPurpose]:
    cached = await cache_get("catalog:purposes")
    if cached and not include_inactive:
        return cached
    query = select(WaterPurpose).order_by(WaterPurpose.display_order)
    if not include_inactive:
        query = query.where(WaterPurpose.is_active == True)
    result = await db.execute(query)
    purposes = result.scalars().all()
    if not include_inactive:
        data = [{"id": str(p.id), "name": p.name, "description": p.description,
                 "icon_url": p.icon_url, "display_order": p.display_order, "is_active": p.is_active} for p in purposes]
        await cache_set("catalog:purposes", data, ttl_seconds=CACHE_TTL)
    return purposes


async def create_purpose(db: AsyncSession, data: PurposeCreate, actor_id: uuid.UUID) -> WaterPurpose:
    purpose = WaterPurpose(**data.model_dump())
    db.add(purpose)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="CREATE", entity_type="water_purpose", entity_id=purpose.id,
                    after_state=data.model_dump())
    await cache_delete_pattern("catalog:*")
    return purpose


async def update_purpose(db: AsyncSession, purpose_id: uuid.UUID, data: PurposeUpdate, actor_id: uuid.UUID) -> WaterPurpose:
    result = await db.execute(select(WaterPurpose).where(WaterPurpose.id == purpose_id))
    purpose = result.scalar_one_or_none()
    if not purpose:
        raise NotFoundError("WaterPurpose", purpose_id)
    before = {"name": purpose.name, "description": purpose.description, "is_active": purpose.is_active}
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(purpose, field, value)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="UPDATE", entity_type="water_purpose", entity_id=purpose_id,
                    before_state=before, after_state=data.model_dump(exclude_unset=True))
    await cache_delete_pattern("catalog:*")
    return purpose


# ---- Water Quality Types ----

async def list_quality_types(db: AsyncSession, include_inactive: bool = False) -> list[WaterQualityType]:
    cached = await cache_get("catalog:qualities")
    if cached and not include_inactive:
        return cached
    query = select(WaterQualityType).order_by(WaterQualityType.name)
    if not include_inactive:
        query = query.where(WaterQualityType.is_active == True)
    result = await db.execute(query)
    qualities = result.scalars().all()
    if not include_inactive:
        data = [{"id": str(q.id), "name": q.name, "description": q.description, "is_active": q.is_active} for q in qualities]
        await cache_set("catalog:qualities", data, ttl_seconds=CACHE_TTL)
    return qualities


async def create_quality_type(db: AsyncSession, data: QualityTypeCreate, actor_id: uuid.UUID) -> WaterQualityType:
    qt = WaterQualityType(**data.model_dump())
    db.add(qt)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="CREATE", entity_type="water_quality_type", entity_id=qt.id,
                    after_state=data.model_dump())
    await cache_delete_pattern("catalog:*")
    return qt


async def update_quality_type(db: AsyncSession, qt_id: uuid.UUID, data: QualityTypeUpdate, actor_id: uuid.UUID) -> WaterQualityType:
    result = await db.execute(select(WaterQualityType).where(WaterQualityType.id == qt_id))
    qt = result.scalar_one_or_none()
    if not qt:
        raise NotFoundError("WaterQualityType", qt_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(qt, field, value)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="UPDATE", entity_type="water_quality_type", entity_id=qt_id)
    await cache_delete_pattern("catalog:*")
    return qt


# ---- Delivery Methods ----

async def list_delivery_methods(db: AsyncSession, include_inactive: bool = False) -> list[DeliveryMethod]:
    query = select(DeliveryMethod).order_by(DeliveryMethod.name)
    if not include_inactive:
        query = query.where(DeliveryMethod.is_active == True)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_delivery_method(db: AsyncSession, data: DeliveryMethodCreate, actor_id: uuid.UUID) -> DeliveryMethod:
    dm = DeliveryMethod(**data.model_dump())
    db.add(dm)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="CREATE", entity_type="delivery_method", entity_id=dm.id)
    await cache_delete_pattern("catalog:*")
    return dm


async def update_delivery_method(db: AsyncSession, dm_id: uuid.UUID, data: DeliveryMethodUpdate, actor_id: uuid.UUID) -> DeliveryMethod:
    result = await db.execute(select(DeliveryMethod).where(DeliveryMethod.id == dm_id))
    dm = result.scalar_one_or_none()
    if not dm:
        raise NotFoundError("DeliveryMethod", dm_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(dm, field, value)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="UPDATE", entity_type="delivery_method", entity_id=dm_id)
    await cache_delete_pattern("catalog:*")
    return dm


# ---- Water Variants ----

async def list_variants(db: AsyncSession, purpose_id: uuid.UUID | None = None, include_inactive: bool = False) -> list[dict]:
    query = select(WaterVariant)
    if purpose_id:
        query = query.where(WaterVariant.purpose_id == purpose_id)
    if not include_inactive:
        query = query.where(WaterVariant.is_active == True)
    result = await db.execute(query)
    variants = result.scalars().all()

    enriched = []
    for v in variants:
        p = await db.get(WaterPurpose, v.purpose_id)
        q = await db.get(WaterQualityType, v.quality_id)
        dm = await db.get(DeliveryMethod, v.delivery_method_id)
        enriched.append({
            "id": v.id, "purpose_id": v.purpose_id, "quality_id": v.quality_id,
            "delivery_method_id": v.delivery_method_id, "min_quantity_litres": v.min_quantity_litres,
            "max_quantity_litres": v.max_quantity_litres, "is_active": v.is_active,
            "purpose_name": p.name if p else None, "quality_name": q.name if q else None,
            "delivery_method_name": dm.name if dm else None,
        })
    return enriched


async def create_variant(db: AsyncSession, data: VariantCreate, actor_id: uuid.UUID) -> WaterVariant:
    if data.max_quantity_litres < data.min_quantity_litres:
        raise ConflictError(code="INVALID_QUANTITY_RANGE", message="max_quantity_litres must be >= min_quantity_litres")
    variant = WaterVariant(**data.model_dump())
    db.add(variant)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="CREATE", entity_type="water_variant", entity_id=variant.id)
    await cache_delete_pattern("catalog:*")
    return variant


async def update_variant(db: AsyncSession, variant_id: uuid.UUID, data: VariantUpdate, actor_id: uuid.UUID) -> WaterVariant:
    result = await db.execute(select(WaterVariant).where(WaterVariant.id == variant_id))
    variant = result.scalar_one_or_none()
    if not variant:
        raise NotFoundError("WaterVariant", variant_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(variant, field, value)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="UPDATE", entity_type="water_variant", entity_id=variant_id)
    await cache_delete_pattern("catalog:*")
    return variant
