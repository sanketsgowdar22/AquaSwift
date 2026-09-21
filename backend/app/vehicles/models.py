"""AquaSwift — Vehicles Models"""
from __future__ import annotations
import uuid
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registration_number = Column(String(20), unique=True, nullable=False)
    type = Column(String(50), nullable=False)
    capacity_litres = Column(BigInteger, nullable=False)
    status = Column(String(20), nullable=False, default="ACTIVE")  # ACTIVE, INACTIVE, MAINTENANCE
    current_driver_id = Column(UUID(as_uuid=True), ForeignKey("driver_profiles.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
