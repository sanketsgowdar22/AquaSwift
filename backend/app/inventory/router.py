"""AquaSwift — Inventory Router"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.inventory import service
from app.inventory.schemas import AdjustRequest, BalanceResponse, ReceiveRequest, TransactionResponse

router = APIRouter()


@router.get("/admin/inventory/balances", response_model=list[BalanceResponse], tags=["Admin - Inventory"])
async def get_balances(_=Depends(require_permission("inventory:read")), db: AsyncSession = Depends(get_db)):
    return await service.get_balances(db)


@router.get("/admin/inventory/ledger", response_model=list[TransactionResponse], tags=["Admin - Inventory"])
async def get_ledger(source_id: uuid.UUID | None = None, limit: int = Query(50, ge=1, le=200),
                     _=Depends(require_permission("inventory:read")), db: AsyncSession = Depends(get_db)):
    return await service.get_ledger(db, source_id=source_id, limit=limit)


@router.post("/admin/inventory/receive", response_model=BalanceResponse, tags=["Admin - Inventory"])
async def receive_inventory(data: ReceiveRequest, user: User = Depends(require_permission("inventory:write")),
                            db: AsyncSession = Depends(get_db)):
    bal = await service.receive(db, data.source_id, data.quantity_litres, user.id, data.notes)
    return BalanceResponse(source_id=bal.source_id, available_litres=bal.available_litres,
                           reserved_litres=bal.reserved_litres, allocated_litres=bal.allocated_litres,
                           total_litres=bal.available_litres + bal.reserved_litres + bal.allocated_litres)


@router.post("/admin/inventory/adjust", response_model=BalanceResponse, tags=["Admin - Inventory"])
async def adjust_inventory(data: AdjustRequest, user: User = Depends(require_permission("inventory:adjust")),
                           db: AsyncSession = Depends(get_db)):
    bal = await service.adjust(db, data.source_id, data.quantity_litres, data.reason, user.id)
    return BalanceResponse(source_id=bal.source_id, available_litres=bal.available_litres,
                           reserved_litres=bal.reserved_litres, allocated_litres=bal.allocated_litres,
                           total_litres=bal.available_litres + bal.reserved_litres + bal.allocated_litres)
