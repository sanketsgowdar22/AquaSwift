"""AquaSwift — B2B Models per DATABASE_ARCHITECTURE.md §2.2 + §2.9"""
from __future__ import annotations
import uuid
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from app.core.database import Base


class Business(Base):
    __tablename__ = "businesses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    registration_number = Column(String(100), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(15), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class BusinessUser(Base):
    __tablename__ = "business_users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role = Column(String(20), nullable=False)  # ADMIN, EMPLOYEE
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    __table_args__ = (UniqueConstraint("business_id", "user_id", name="uq_business_user"),)


class BusinessSite(Base):
    __tablename__ = "business_sites"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False, index=True)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False)
    name = Column(String(255), nullable=False)
    contact_person = Column(String(255), nullable=True)
    contact_phone = Column(String(15), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class BulkRequest(Base):
    __tablename__ = "bulk_requests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    site_id = Column(UUID(as_uuid=True), ForeignKey("business_sites.id"), nullable=True)
    purpose_id = Column(UUID(as_uuid=True), ForeignKey("water_purposes.id"), nullable=False)
    quality_id = Column(UUID(as_uuid=True), ForeignKey("water_quality_types.id"), nullable=False)
    total_quantity_litres = Column(BigInteger, nullable=False)
    frequency = Column(String(20), nullable=True)
    schedule_start = Column(Date, nullable=False)
    schedule_end = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="PENDING")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class BulkQuote(Base):
    __tablename__ = "bulk_quotes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bulk_request_id = Column(UUID(as_uuid=True), ForeignKey("bulk_requests.id"), nullable=False)
    price_per_litre = Column(Numeric(12, 4), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    delivery_charge = Column(Numeric(12, 2), nullable=False, default=0)
    valid_until = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
