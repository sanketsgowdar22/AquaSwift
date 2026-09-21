"""AquaSwift — Pricing Models per DATABASE_ARCHITECTURE.md §2.6"""
from __future__ import annotations
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from app.core.database import Base


class PricingRule(Base):
    __tablename__ = "pricing_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version = Column(Integer, nullable=False, default=1)
    purpose_id = Column(UUID(as_uuid=True), ForeignKey("water_purposes.id"), nullable=True)
    quality_id = Column(UUID(as_uuid=True), ForeignKey("water_quality_types.id"), nullable=True)
    customer_type = Column(String(20), nullable=True)  # INDIVIDUAL, BUSINESS
    area_id = Column(UUID(as_uuid=True), nullable=True)  # Phase 2
    pricing_model = Column(String(20), nullable=False)  # FIXED, PER_LITRE, TIERED
    base_price = Column(Numeric(12, 2), nullable=False)
    tiers = Column(JSONB, nullable=True)  # For TIERED: [{min_litres, max_litres, price_per_litre}]
    active_from = Column(DateTime(timezone=True), nullable=False)
    active_to = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class DeliveryPricingRule(Base):
    __tablename__ = "delivery_pricing_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    delivery_method_id = Column(UUID(as_uuid=True), ForeignKey("delivery_methods.id"), nullable=True)
    pricing_model = Column(String(20), nullable=False)  # FLAT, PER_KM, DISTANCE_BAND
    base_price = Column(Numeric(12, 2), nullable=False)
    bands = Column(JSONB, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
