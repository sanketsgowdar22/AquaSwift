"""AquaSwift — Inventory Service. SELECT ... FOR UPDATE on balances for concurrency safety."""
from __future__ import annotations
import uuid
import structlog
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit import audit_log
from app.core.exceptions import InsufficientInventoryError, NotFoundError, ValidationError
from app.inventory.models import InventoryBalance, InventoryTransaction

logger = structlog.get_logger()


async def _get_or_create_balance(db: AsyncSession, source_id: uuid.UUID, lock: bool = False) -> InventoryBalance:
    query = select(InventoryBalance).where(InventoryBalance.source_id == source_id)
    if lock:
        query = query.with_for_update()
    result = await db.execute(query)
    balance = result.scalar_one_or_none()
    if not balance:
        balance = InventoryBalance(source_id=source_id, available_litres=0, reserved_litres=0, allocated_litres=0)
        db.add(balance)
        await db.flush()
    return balance


async def receive(db: AsyncSession, source_id: uuid.UUID, quantity_litres: int, actor_id: uuid.UUID, notes: str | None = None) -> InventoryBalance:
    """Receive water into a source — increases available balance."""
    balance = await _get_or_create_balance(db, source_id, lock=True)
    txn = InventoryTransaction(
        source_id=source_id, type="RECEIVED", quantity_litres=quantity_litres,
        reference_type="manual", notes=notes, created_by=actor_id,
    )
    db.add(txn)
    balance.available_litres += quantity_litres
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="INVENTORY_RECEIVE", entity_type="inventory",
                    entity_id=source_id, after_state={"quantity": quantity_litres})
    logger.info("inventory_received", source_id=str(source_id), quantity=quantity_litres)
    return balance


async def reserve(db: AsyncSession, source_id: uuid.UUID, quantity_litres: int, actor_id: uuid.UUID,
                  reference_type: str = "order", reference_id: uuid.UUID | None = None) -> InventoryBalance:
    """Reserve inventory for an order. Uses SELECT ... FOR UPDATE for concurrency safety."""
    balance = await _get_or_create_balance(db, source_id, lock=True)
    if balance.available_litres < quantity_litres:
        raise InsufficientInventoryError(requested=quantity_litres, available=balance.available_litres, source_id=str(source_id))
    txn = InventoryTransaction(
        source_id=source_id, type="RESERVED", quantity_litres=-quantity_litres,
        reference_type=reference_type, reference_id=reference_id, created_by=actor_id,
    )
    db.add(txn)
    balance.available_litres -= quantity_litres
    balance.reserved_litres += quantity_litres
    await db.flush()
    logger.info("inventory_reserved", source_id=str(source_id), quantity=quantity_litres)
    return balance


async def release(db: AsyncSession, source_id: uuid.UUID, quantity_litres: int, actor_id: uuid.UUID,
                  reference_type: str = "order", reference_id: uuid.UUID | None = None) -> InventoryBalance:
    """Release reserved inventory back to available (e.g., order cancelled)."""
    balance = await _get_or_create_balance(db, source_id, lock=True)
    txn = InventoryTransaction(
        source_id=source_id, type="RELEASED", quantity_litres=quantity_litres,
        reference_type=reference_type, reference_id=reference_id, created_by=actor_id,
    )
    db.add(txn)
    balance.reserved_litres = max(0, balance.reserved_litres - quantity_litres)
    balance.available_litres += quantity_litres
    await db.flush()
    logger.info("inventory_released", source_id=str(source_id), quantity=quantity_litres)
    return balance


async def allocate(db: AsyncSession, source_id: uuid.UUID, quantity_litres: int, actor_id: uuid.UUID,
                   reference_type: str = "delivery", reference_id: uuid.UUID | None = None) -> InventoryBalance:
    """Move from reserved to allocated (delivery dispatched)."""
    balance = await _get_or_create_balance(db, source_id, lock=True)
    txn = InventoryTransaction(
        source_id=source_id, type="ALLOCATED", quantity_litres=-quantity_litres,
        reference_type=reference_type, reference_id=reference_id, created_by=actor_id,
    )
    db.add(txn)
    balance.reserved_litres = max(0, balance.reserved_litres - quantity_litres)
    balance.allocated_litres += quantity_litres
    await db.flush()
    return balance


async def deliver(db: AsyncSession, source_id: uuid.UUID, quantity_litres: int, actor_id: uuid.UUID,
                  reference_type: str = "delivery", reference_id: uuid.UUID | None = None) -> InventoryBalance:
    """Mark allocated inventory as delivered."""
    balance = await _get_or_create_balance(db, source_id, lock=True)
    txn = InventoryTransaction(
        source_id=source_id, type="DELIVERED", quantity_litres=-quantity_litres,
        reference_type=reference_type, reference_id=reference_id, created_by=actor_id,
    )
    db.add(txn)
    balance.allocated_litres = max(0, balance.allocated_litres - quantity_litres)
    await db.flush()
    return balance


async def adjust(db: AsyncSession, source_id: uuid.UUID, quantity_litres: int, reason: str, actor_id: uuid.UUID) -> InventoryBalance:
    """Admin adjustment with mandatory reason."""
    balance = await _get_or_create_balance(db, source_id, lock=True)
    txn = InventoryTransaction(
        source_id=source_id, type="ADJUSTED", quantity_litres=quantity_litres,
        reference_type="adjustment", notes=reason, created_by=actor_id,
    )
    db.add(txn)
    balance.available_litres += quantity_litres
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="INVENTORY_ADJUST", entity_type="inventory",
                    entity_id=source_id, after_state={"quantity": quantity_litres, "reason": reason})
    logger.info("inventory_adjusted", source_id=str(source_id), quantity=quantity_litres, reason=reason)
    return balance


async def get_balances(db: AsyncSession) -> list[dict]:
    """Get all inventory balances with source names."""
    from app.sources.models import WaterSource
    result = await db.execute(
        select(InventoryBalance, WaterSource.name)
        .outerjoin(WaterSource, WaterSource.id == InventoryBalance.source_id)
        .order_by(WaterSource.name)
    )
    balances = []
    for bal, name in result.all():
        balances.append({
            "source_id": bal.source_id, "source_name": name,
            "available_litres": bal.available_litres, "reserved_litres": bal.reserved_litres,
            "allocated_litres": bal.allocated_litres,
            "total_litres": bal.available_litres + bal.reserved_litres + bal.allocated_litres,
        })
    return balances


async def get_ledger(db: AsyncSession, source_id: uuid.UUID | None = None, limit: int = 50) -> list[InventoryTransaction]:
    query = select(InventoryTransaction).order_by(InventoryTransaction.created_at.desc()).limit(limit)
    if source_id:
        query = query.where(InventoryTransaction.source_id == source_id)
    result = await db.execute(query)
    return list(result.scalars().all())
