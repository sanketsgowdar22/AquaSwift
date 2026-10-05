"""AquaSwift — Addresses Router"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.database import get_db
from app.core.security import get_current_user
from app.addresses import service
from app.addresses.schemas import AddressCreate, AddressResponse, AddressUpdate

router = APIRouter()


@router.get("/addresses", response_model=list[AddressResponse], tags=["Addresses"])
async def list_addresses(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await service.list_addresses(db, current_user.id)


@router.post("/addresses", response_model=AddressResponse, tags=["Addresses"])
async def create_address(data: AddressCreate, current_user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    return await service.create_address(db, current_user.id, data)


@router.patch("/addresses/{address_id}", response_model=AddressResponse, tags=["Addresses"])
async def update_address(address_id: uuid.UUID, data: AddressUpdate,
                         current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await service.update_address(db, current_user.id, address_id, data)


@router.delete("/addresses/{address_id}", tags=["Addresses"])
async def delete_address(address_id: uuid.UUID, current_user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    await service.delete_address(db, current_user.id, address_id)
    return {"message": "Address deleted."}
