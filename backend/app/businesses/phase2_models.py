"""AquaSwift — Phase 2/3 Stub Models (recurring_orders, invoices)"""
from __future__ import annotations
import uuid
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Time, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from app.core.database import Base


class RecurringOrder(Base):
    __tablename__ = "recurring_orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    variant_id = Column(UUID(as_uuid=True), ForeignKey("water_variants.id"), nullable=False)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False)
    quantity_litres = Column(BigInteger, nullable=False)
    frequency = Column(String(20), nullable=False)  # DAILY, WEEKLY, BIWEEKLY, MONTHLY
    schedule_days = Column(JSONB, nullable=True)
    preferred_window_start = Column(Time, nullable=True)
    preferred_window_end = Column(Time, nullable=True)
    status = Column(String(20), nullable=False, default="ACTIVE")
    next_instance_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class RecurringOrderInstance(Base):
    __tablename__ = "recurring_order_instances"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recurring_order_id = Column(UUID(as_uuid=True), ForeignKey("recurring_orders.id"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True)
    scheduled_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")
    failure_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_number = Column(String(30), unique=True, nullable=False)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    billing_period_start = Column(Date, nullable=False)
    billing_period_end = Column(Date, nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)
    tax_total = Column(Numeric(12, 2), nullable=False, default=0)
    total = Column(Numeric(12, 2), nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")
    due_date = Column(Date, nullable=False)
    payment_terms_days = Column(Integer, nullable=False, default=30)
    pdf_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
