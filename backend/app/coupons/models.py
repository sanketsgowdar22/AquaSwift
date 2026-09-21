"""AquaSwift — Coupons Models"""
from __future__ import annotations
import uuid
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    discount_type = Column(String(20), nullable=False)  # PERCENTAGE, FIXED_AMOUNT
    discount_value = Column(Numeric(12, 2), nullable=False)
    min_order_amount = Column(Numeric(12, 2), nullable=True)
    max_discount_amount = Column(Numeric(12, 2), nullable=True)
    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_to = Column(DateTime(timezone=True), nullable=False)
    total_usage_limit = Column(Integer, nullable=True)
    per_customer_limit = Column(Integer, nullable=False, default=1)
    current_usage_count = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
