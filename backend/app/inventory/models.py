"""AquaSwift — Inventory Models. Append-only ledger + balance cache per DATABASE_ARCHITECTURE.md §2.5"""
from __future__ import annotations
import uuid
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class InventoryTransaction(Base):
    """APPEND-ONLY — no UPDATE or DELETE permitted (RULE-004)."""
    __tablename__ = "inventory_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("water_sources.id"), nullable=False, index=True)
    type = Column(String(20), nullable=False, index=True)  # RECEIVED, RESERVED, RELEASED, ALLOCATED, DELIVERED, ADJUSTED, LOST_WASTAGE
    quantity_litres = Column(BigInteger, nullable=False)  # Signed: positive=increase, negative=decrease
    reference_type = Column(String(30), nullable=True)  # order, delivery, adjustment
    reference_id = Column(UUID(as_uuid=True), nullable=True)
    notes = Column(Text, nullable=True)  # Mandatory for ADJUSTED and LOST_WASTAGE
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)


class InventoryBalance(Base):
    """Reconciled cache — not the source of truth. One row per source."""
    __tablename__ = "inventory_balances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("water_sources.id"), unique=True, nullable=False)
    available_litres = Column(BigInteger, nullable=False, default=0)
    reserved_litres = Column(BigInteger, nullable=False, default=0)
    allocated_litres = Column(BigInteger, nullable=False, default=0)
    last_reconciled_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
