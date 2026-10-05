"""
AquaSwift — Catalog Models

Water purposes, quality types, delivery methods, purpose-quality mappings,
and water variants per DATABASE_ARCHITECTURE.md §2.4.
"""

from __future__ import annotations

import uuid

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class WaterPurpose(Base):
    __tablename__ = "water_purposes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon_url = Column(String(500), nullable=True)
    display_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class WaterQualityType(Base):
    __tablename__ = "water_quality_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class DeliveryMethod(Base):
    __tablename__ = "delivery_methods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class WaterPurposeQuality(Base):
    __tablename__ = "water_purpose_qualities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    purpose_id = Column(UUID(as_uuid=True), ForeignKey("water_purposes.id"), nullable=False)
    quality_id = Column(UUID(as_uuid=True), ForeignKey("water_quality_types.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    purpose = relationship("WaterPurpose")
    quality = relationship("WaterQualityType")

    __table_args__ = (UniqueConstraint("purpose_id", "quality_id", name="uq_purpose_quality"),)


class WaterVariant(Base):
    __tablename__ = "water_variants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    purpose_id = Column(UUID(as_uuid=True), ForeignKey("water_purposes.id"), nullable=False)
    quality_id = Column(UUID(as_uuid=True), ForeignKey("water_quality_types.id"), nullable=False)
    delivery_method_id = Column(UUID(as_uuid=True), ForeignKey("delivery_methods.id"), nullable=False)
    min_quantity_litres = Column(BigInteger, nullable=False)
    max_quantity_litres = Column(BigInteger, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    purpose = relationship("WaterPurpose")
    quality = relationship("WaterQualityType")
    delivery_method = relationship("DeliveryMethod")

    __table_args__ = (
        UniqueConstraint("purpose_id", "quality_id", "delivery_method_id", name="uq_variant_combo"),
    )
