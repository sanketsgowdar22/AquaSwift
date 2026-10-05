"""AquaSwift — Orders Router"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.core.security import get_current_user
from app.orders import service
from app.orders.schemas import CancelOrderRequest, OrderCreate, OrderListResponse, OrderResponse

router = APIRouter()


@router.post("/orders", response_model=OrderResponse, tags=["Orders"])
async def create_order(data: OrderCreate, current_user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    return await service.create_order(db, current_user.id, data)


@router.get("/orders", response_model=OrderListResponse, tags=["Orders"])
async def list_my_orders(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
                         current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    orders, total = await service.list_orders(db, customer_id=current_user.id, page=page, page_size=page_size)
    return OrderListResponse(items=orders, total=total, page=page, page_size=page_size)


@router.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
async def get_order(order_id: uuid.UUID, current_user: User = Depends(get_current_user),
                    db: AsyncSession = Depends(get_db)):
    return await service.get_order(db, order_id)


@router.post("/orders/{order_id}/cancel", response_model=OrderResponse, tags=["Orders"])
async def cancel_order(order_id: uuid.UUID, data: CancelOrderRequest,
                       current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await service.cancel_order(db, order_id, current_user.id, data.reason)


# ---- Admin ----
@router.get("/admin/orders", response_model=OrderListResponse, tags=["Admin - Orders"])
async def admin_list_orders(status: str | None = None, page: int = Query(1, ge=1),
                            page_size: int = Query(20, ge=1, le=100),
                            _=Depends(require_permission("orders:read")), db: AsyncSession = Depends(get_db)):
    orders, total = await service.list_orders(db, status=status, page=page, page_size=page_size)
    return OrderListResponse(items=orders, total=total, page=page, page_size=page_size)
