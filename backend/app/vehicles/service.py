"""AquaSwift — Vehicles Service"""
from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit import audit_log
from app.core.exceptions import NotFoundError
from app.vehicles.models import Vehicle
from app.vehicles.schemas import VehicleCreate, VehicleUpdate


async def list_vehicles(db: AsyncSession) -> list[Vehicle]:
    result = await db.execute(select(Vehicle).order_by(Vehicle.registration_number))
    return list(result.scalars().all())


async def create_vehicle(db: AsyncSession, data: VehicleCreate, actor_id: uuid.UUID) -> Vehicle:
    v = Vehicle(**data.model_dump())
    db.add(v)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="CREATE", entity_type="vehicle", entity_id=v.id)
    return v


async def update_vehicle(db: AsyncSession, vid: uuid.UUID, data: VehicleUpdate, actor_id: uuid.UUID) -> Vehicle:
    v = await db.get(Vehicle, vid)
    if not v:
        raise NotFoundError("Vehicle", vid)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(v, field, value)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="UPDATE", entity_type="vehicle", entity_id=vid)
    return v


async def assign_driver(db: AsyncSession, vid: uuid.UUID, driver_profile_id: uuid.UUID, actor_id: uuid.UUID) -> Vehicle:
    v = await db.get(Vehicle, vid)
    if not v:
        raise NotFoundError("Vehicle", vid)
    v.current_driver_id = driver_profile_id
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="ASSIGN_DRIVER", entity_type="vehicle", entity_id=vid)
    return v
