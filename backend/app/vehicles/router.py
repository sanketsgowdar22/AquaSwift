"""AquaSwift — Vehicles Router"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.vehicles import service
from app.vehicles.schemas import AssignDriverRequest, VehicleCreate, VehicleResponse, VehicleUpdate

router = APIRouter()


@router.get("/admin/vehicles", response_model=list[VehicleResponse], tags=["Admin - Vehicles"])
async def list_vehicles(_=Depends(require_permission("vehicles:read")), db: AsyncSession = Depends(get_db)):
    return await service.list_vehicles(db)


@router.post("/admin/vehicles", response_model=VehicleResponse, tags=["Admin - Vehicles"])
async def create_vehicle(data: VehicleCreate, user: User = Depends(require_permission("vehicles:write")),
                         db: AsyncSession = Depends(get_db)):
    return await service.create_vehicle(db, data, user.id)


@router.patch("/admin/vehicles/{vid}", response_model=VehicleResponse, tags=["Admin - Vehicles"])
async def update_vehicle(vid: uuid.UUID, data: VehicleUpdate,
                         user: User = Depends(require_permission("vehicles:write")),
                         db: AsyncSession = Depends(get_db)):
    return await service.update_vehicle(db, vid, data, user.id)


@router.post("/admin/vehicles/{vid}/assign-driver", response_model=VehicleResponse, tags=["Admin - Vehicles"])
async def assign_driver(vid: uuid.UUID, data: AssignDriverRequest,
                        user: User = Depends(require_permission("vehicles:write")),
                        db: AsyncSession = Depends(get_db)):
    return await service.assign_driver(db, vid, data.driver_profile_id, user.id)
