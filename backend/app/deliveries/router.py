"""AquaSwift — Deliveries Router"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.core.security import get_current_user
from app.deliveries import service
from app.deliveries.schemas import AssignDeliveryRequest, CompleteDeliveryRequest, DeliveryResponse, RespondRequest

router = APIRouter()


@router.post("/deliveries/{did}/respond", response_model=DeliveryResponse, tags=["Deliveries - Driver"])
async def respond(did: uuid.UUID, data: RespondRequest, user: User = Depends(get_current_user),
                  db: AsyncSession = Depends(get_db)):
    return await service.respond_to_delivery(db, did, user.id, data.accept, data.rejection_reason)


@router.post("/deliveries/{did}/start", response_model=DeliveryResponse, tags=["Deliveries - Driver"])
async def start(did: uuid.UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await service.start_delivery(db, did, user.id)


@router.post("/deliveries/{did}/arrive", response_model=DeliveryResponse, tags=["Deliveries - Driver"])
async def arrive(did: uuid.UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await service.arrive_delivery(db, did, user.id)


@router.post("/deliveries/{did}/complete", response_model=DeliveryResponse, tags=["Deliveries - Driver"])
async def complete(did: uuid.UUID, data: CompleteDeliveryRequest, user: User = Depends(get_current_user),
                   db: AsyncSession = Depends(get_db)):
    return await service.complete_delivery(db, did, user.id, data.otp, data.delivered_quantity_litres,
                                            data.gps_lat, data.gps_lng)


# Admin
@router.get("/admin/deliveries", tags=["Admin - Deliveries"])
async def admin_list(status: str | None = None, page: int = Query(1, ge=1),
                     _=Depends(require_permission("deliveries:read")), db: AsyncSession = Depends(get_db)):
    deliveries, total = await service.list_deliveries(db, status=status, page=page)
    return {"items": deliveries, "total": total}


@router.post("/admin/deliveries/{did}/assign", response_model=DeliveryResponse, tags=["Admin - Deliveries"])
async def admin_assign(did: uuid.UUID, data: AssignDeliveryRequest,
                       user: User = Depends(require_permission("deliveries:assign")),
                       db: AsyncSession = Depends(get_db)):
    return await service.assign_delivery(db, did, data.driver_id, data.vehicle_id, data.source_id, user.id)
