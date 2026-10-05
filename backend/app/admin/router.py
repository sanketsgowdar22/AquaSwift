"""AquaSwift — Admin Dashboard + Reports + Audit Log Router"""
from __future__ import annotations
import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.audit import AuditLog
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.deliveries.models import Delivery
from app.inventory.models import InventoryBalance
from app.orders.models import Order
from app.users.models import DriverProfile

router = APIRouter()


# ---- Dashboard ----

@router.get("/admin/dashboard", tags=["Admin - Dashboard"])
async def dashboard(_=Depends(require_permission("orders:read")), db: AsyncSession = Depends(get_db)):
    """Admin dashboard: aggregated metrics."""
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Active orders
    active_orders = (await db.execute(
        select(func.count(Order.id)).where(Order.status.in_(["CONFIRMED", "PROCESSING", "DISPATCHED", "IN_TRANSIT"]))
    )).scalar_one()

    # Today's orders
    today_orders = (await db.execute(
        select(func.count(Order.id)).where(Order.created_at >= today_start)
    )).scalar_one()

    # Pending deliveries
    pending_deliveries = (await db.execute(
        select(func.count(Delivery.id)).where(Delivery.status.in_(["PENDING_ASSIGNMENT", "OFFERED", "ASSIGNED"]))
    )).scalar_one()

    # Available drivers
    available_drivers = (await db.execute(
        select(func.count(DriverProfile.id)).where(DriverProfile.status == "AVAILABLE")
    )).scalar_one()

    # Low inventory alerts (sources with < 5000L available)
    low_inventory = (await db.execute(
        select(func.count(InventoryBalance.id)).where(InventoryBalance.available_litres < 5000)
    )).scalar_one()

    # Total users
    total_users = (await db.execute(select(func.count(User.id)))).scalar_one()

    return {
        "active_orders": active_orders,
        "today_orders": today_orders,
        "pending_deliveries": pending_deliveries,
        "available_drivers": available_drivers,
        "low_inventory_alerts": low_inventory,
        "total_users": total_users,
    }


# ---- Reports ----

@router.get("/admin/reports/sales", tags=["Admin - Reports"])
async def sales_report(days: int = Query(30, ge=1, le=365),
                       _=Depends(require_permission("reports:read")), db: AsyncSession = Depends(get_db)):
    """Sales summary for the last N days."""
    since = datetime.now(timezone.utc) - timedelta(days=days)
    result = await db.execute(
        select(func.count(Order.id), func.sum(Order.total_quantity_litres))
        .where(Order.created_at >= since, Order.status != "CANCELLED")
    )
    row = result.one()
    return {"period_days": days, "total_orders": row[0] or 0, "total_litres": row[1] or 0}


@router.get("/admin/reports/deliveries", tags=["Admin - Reports"])
async def delivery_report(days: int = Query(30, ge=1, le=365),
                          _=Depends(require_permission("reports:read")), db: AsyncSession = Depends(get_db)):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    completed = (await db.execute(
        select(func.count(Delivery.id)).where(Delivery.status == "DELIVERED", Delivery.completed_at >= since)
    )).scalar_one()
    return {"period_days": days, "completed_deliveries": completed}


# ---- Audit Logs ----

@router.get("/admin/audit-logs", tags=["Admin - Audit"])
async def list_audit_logs(entity_type: str | None = None, entity_id: uuid.UUID | None = None,
                          action: str | None = None, limit: int = Query(50, ge=1, le=200),
                          _=Depends(require_permission("audit:read")), db: AsyncSession = Depends(get_db)):
    query = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    if entity_type:
        query = query.where(AuditLog.entity_type == entity_type)
    if entity_id:
        query = query.where(AuditLog.entity_id == entity_id)
    if action:
        query = query.where(AuditLog.action == action)
    result = await db.execute(query)
    return {"items": list(result.scalars().all())}
