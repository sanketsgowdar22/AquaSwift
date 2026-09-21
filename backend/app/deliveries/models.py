"""AquaSwift — Deliveries Models per DATABASE_ARCHITECTURE.md §2.7"""
from __future__ import annotations
import uuid
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from app.core.database import Base

DELIVERY_TRANSITIONS = {
    "PENDING_ASSIGNMENT": ["OFFERED", "ASSIGNED"],
    "OFFERED": ["ASSIGNED", "PENDING_ASSIGNMENT"],  # accept or reject
    "ASSIGNED": ["STARTED"],
    "STARTED": ["ARRIVED"],
    "ARRIVED": ["DELIVERED", "PARTIALLY_DELIVERED"],
    "PARTIALLY_DELIVERED": ["DELIVERED"],
    "DELIVERED": [],
    "CANCELLED": [],
}


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False, index=True)
    source_id = Column(UUID(as_uuid=True), ForeignKey("water_sources.id"), nullable=True)
    driver_id = Column(UUID(as_uuid=True), ForeignKey("driver_profiles.id"), nullable=True, index=True)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=True)
    status = Column(String(25), nullable=False, default="PENDING_ASSIGNMENT", index=True)
    quantity_litres = Column(BigInteger, nullable=False)
    delivered_quantity_litres = Column(BigInteger, nullable=True)
    otp_code = Column(String(6), nullable=True)
    proof_photo_url = Column(String(500), nullable=True)
    gps_lat = Column(Numeric(10, 7), nullable=True)
    gps_lng = Column(Numeric(10, 7), nullable=True)
    parent_delivery_id = Column(UUID(as_uuid=True), ForeignKey("deliveries.id"), nullable=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=True, index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class DeliveryAssignment(Base):
    __tablename__ = "delivery_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    delivery_id = Column(UUID(as_uuid=True), ForeignKey("deliveries.id"), nullable=False, index=True)
    driver_id = Column(UUID(as_uuid=True), ForeignKey("driver_profiles.id"), nullable=False, index=True)
    status = Column(String(20), nullable=False)  # OFFERED, ACCEPTED, REJECTED, TIMED_OUT
    offered_at = Column(DateTime(timezone=True), nullable=False)
    responded_at = Column(DateTime(timezone=True), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    attempt_number = Column(Integer, nullable=False)


class DeliveryEvent(Base):
    __tablename__ = "delivery_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    delivery_id = Column(UUID(as_uuid=True), ForeignKey("deliveries.id"), nullable=False, index=True)
    event_type = Column(String(30), nullable=False)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    metadata_ = Column("metadata", JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
