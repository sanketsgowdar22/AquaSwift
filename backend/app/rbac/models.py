"""
AquaSwift — RBAC Models

Roles table storing platform roles with their permission sets.
Permissions are stored as a JSONB array of strings (e.g., ["catalog:read", "orders:create"]).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.database import Base


class Role(Base):
    """
    Platform role definition.

    Each role has a unique name and a JSONB array of permission strings.
    Roles: CUSTOMER, DRIVER, OPS_MANAGER, SUPER_ADMIN.
    """

    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    permissions = Column(JSONB, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
