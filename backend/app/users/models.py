"""
AquaSwift — Users Models

UserRole join table, CustomerProfile, and DriverProfile per DATABASE_ARCHITECTURE.md §2.1.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserRole(Base):
    """Join table linking users to roles (many-to-many)."""

    __tablename__ = "user_roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role")

    __table_args__ = (
        # Unique constraint: a user can have each role at most once
        {"sqlite_autoincrement": True},
    )


class CustomerProfile(Base):
    """
    Customer profile linked 1:1 to a User.

    Auto-created on registration. Stores customer-specific data.
    """

    __tablename__ = "customer_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    customer_type = Column(String(20), nullable=False, default="INDIVIDUAL")  # INDIVIDUAL, BUSINESS
    business_id = Column(UUID(as_uuid=True), nullable=True)  # FK added when businesses module is built
    preferences = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User")


class DriverProfile(Base):
    """
    Driver profile linked 1:1 to a User.

    Created by admin when onboarding a driver.
    """

    __tablename__ = "driver_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    license_number = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="UNAVAILABLE", index=True)  # AVAILABLE, UNAVAILABLE, ON_DELIVERY
    current_vehicle_id = Column(UUID(as_uuid=True), nullable=True)  # FK added when vehicles module is built
    gps_lat = Column(Numeric(10, 7), nullable=True)
    gps_lng = Column(Numeric(10, 7), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User")
