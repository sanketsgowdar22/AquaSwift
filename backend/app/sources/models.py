"""AquaSwift — Sources Models"""
from __future__ import annotations
import uuid
from sqlalchemy import BigInteger, Column, DateTime, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class WaterSource(Base):
    __tablename__ = "water_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # Borewell, Municipal, Treatment Plant
    gps_lat = Column(Numeric(10, 7), nullable=True)
    gps_lng = Column(Numeric(10, 7), nullable=True)
    capacity_litres = Column(BigInteger, nullable=False)
    status = Column(String(20), nullable=False, default="ACTIVE")  # ACTIVE, INACTIVE, MAINTENANCE
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
