"""AquaSwift — Reviews Models"""
from __future__ import annotations
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False, index=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    driver_id = Column(UUID(as_uuid=True), ForeignKey("driver_profiles.id"), nullable=True, index=True)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (UniqueConstraint("order_id", "customer_id", name="uq_review_order_customer"),)
