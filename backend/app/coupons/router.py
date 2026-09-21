"""AquaSwift — Coupons Router"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.coupons import service
from app.coupons.schemas import CouponCreate, CouponResponse, CouponUpdate, ValidateCouponRequest, ValidateCouponResponse

router = APIRouter()


@router.post("/coupons/validate", response_model=ValidateCouponResponse, tags=["Coupons"])
async def validate_coupon(data: ValidateCouponRequest, db: AsyncSession = Depends(get_db)):
    return await service.validate_coupon(db, data.code, data.order_amount)


@router.get("/admin/coupons", response_model=list[CouponResponse], tags=["Admin - Coupons"])
async def list_coupons(_=Depends(require_permission("coupons:read")), db: AsyncSession = Depends(get_db)):
    return await service.list_coupons(db)


@router.post("/admin/coupons", response_model=CouponResponse, tags=["Admin - Coupons"])
async def create_coupon(data: CouponCreate, user: User = Depends(require_permission("coupons:write")),
                        db: AsyncSession = Depends(get_db)):
    return await service.create_coupon(db, data, user.id)


@router.patch("/admin/coupons/{coupon_id}", response_model=CouponResponse, tags=["Admin - Coupons"])
async def update_coupon(coupon_id: uuid.UUID, data: CouponUpdate,
                        user: User = Depends(require_permission("coupons:write")),
                        db: AsyncSession = Depends(get_db)):
    return await service.update_coupon(db, coupon_id, data, user.id)
