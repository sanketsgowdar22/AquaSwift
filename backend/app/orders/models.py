"""AquaSwift — Orders Models per DATABASE_ARCHITECTURE.md §2.6"""
from __future__ import annotations
import uuid
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


# ---- Order State Machine ----
ORDER_TRANSITIONS = {
    "PENDING_PAYMENT": ["CONFIRMED", "CANCELLED"],
    "CONFIRMED": ["PROCESSING", "CANCELLED"],
    "PROCESSING": ["DISPATCHED", "CANCELLED"],
    "DISPATCHED": ["IN_TRANSIT"],
    "IN_TRANSIT": ["DELIVERED", "PARTIALLY_DELIVERED"],
    "PARTIALLY_DELIVERED": ["DELIVERED", "IN_TRANSIT"],
    "DELIVERED": [],
    "CANCELLED": [],
}


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String(20), unique=True, nullable=False, index=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False)
    order_type = Column(String(20), nullable=False, default="STANDARD")  # STANDARD, SCHEDULED, RECURRING, BULK
    status = Column(String(30), nullable=False, default="PENDING_PAYMENT", index=True)
    total_quantity_litres = Column(BigInteger, nullable=False)
    scheduled_window_start = Column(DateTime(timezone=True), nullable=True)
    scheduled_window_end = Column(DateTime(timezone=True), nullable=True)
    coupon_id = Column(UUID(as_uuid=True), ForeignKey("coupons.id"), nullable=True)
    idempotency_key = Column(String(64), unique=True, nullable=True, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    items = relationship("OrderItem", back_populates="order", lazy="selectin")


class OrderItem(Base):
    """Commercial snapshot — immutable after creation (RULE-006)."""
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False, index=True)
    variant_id = Column(UUID(as_uuid=True), ForeignKey("water_variants.id"), nullable=False)
    purpose_name = Column(String(100), nullable=False)  # Frozen snapshot
    quality_name = Column(String(100), nullable=False)
    delivery_method_name = Column(String(100), nullable=False)
    quantity_litres = Column(BigInteger, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    water_total = Column(Numeric(12, 2), nullable=False)
    delivery_charge = Column(Numeric(12, 2), nullable=False, default=0)
    discount_total = Column(Numeric(12, 2), nullable=False, default=0)
    tax_total = Column(Numeric(12, 2), nullable=False, default=0)
    final_total = Column(Numeric(12, 2), nullable=False)
    pricing_rule_version_id = Column(UUID(as_uuid=True), nullable=True)
    pricing_snapshot = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    order = relationship("Order", back_populates="items")


class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False, index=True)
    from_status = Column(String(30), nullable=False)
    to_status = Column(String(30), nullable=False)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
