"""AquaSwift — Quality Models per DATABASE_ARCHITECTURE.md §2.5"""

from __future__ import annotations

import uuid

from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class WaterQualityRecord(Base):
    __tablename__ = "water_quality_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("water_sources.id"), nullable=False, index=True)
    ph_level = Column(Numeric(4, 2), nullable=True)
    tds = Column(Integer, nullable=True)
    turbidity = Column(Numeric(6, 2), nullable=True)
    treatment_type = Column(String(100), nullable=True)
    tested_by = Column(String(255), nullable=True)
    test_date = Column(Date, nullable=False)
    certificate_url = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="PENDING")  # PENDING, APPROVED, REJECTED
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    source = relationship("WaterSource")
