"""AquaSwift — Addresses Service"""
from __future__ import annotations
import uuid
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.addresses.models import Address
from app.addresses.schemas import AddressCreate, AddressUpdate
from app.core.exceptions import NotFoundError


async def list_addresses(db: AsyncSession, user_id: uuid.UUID) -> list[Address]:
    result = await db.execute(select(Address).where(Address.user_id == user_id).order_by(Address.is_default.desc(), Address.created_at.desc()))
    return list(result.scalars().all())


async def create_address(db: AsyncSession, user_id: uuid.UUID, data: AddressCreate) -> Address:
    if data.is_default:
        await db.execute(update(Address).where(Address.user_id == user_id).values(is_default=False))
    addr = Address(user_id=user_id, **data.model_dump())
    db.add(addr)
    await db.flush()
    return addr


async def update_address(db: AsyncSession, user_id: uuid.UUID, address_id: uuid.UUID, data: AddressUpdate) -> Address:
    result = await db.execute(select(Address).where(Address.id == address_id, Address.user_id == user_id))
    addr = result.scalar_one_or_none()
    if not addr:
        raise NotFoundError("Address", address_id)
    if data.is_default:
        await db.execute(update(Address).where(Address.user_id == user_id).values(is_default=False))
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(addr, field, value)
    await db.flush()
    return addr


async def delete_address(db: AsyncSession, user_id: uuid.UUID, address_id: uuid.UUID) -> None:
    result = await db.execute(select(Address).where(Address.id == address_id, Address.user_id == user_id))
    addr = result.scalar_one_or_none()
    if not addr:
        raise NotFoundError("Address", address_id)
    await db.delete(addr)
