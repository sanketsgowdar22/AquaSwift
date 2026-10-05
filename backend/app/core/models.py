"""
AquaSwift — Base Model Mixins

Reusable mixins that provide common columns across all domain models.
Every table uses UUID primary keys, TIMESTAMPTZ timestamps, and optional
soft-delete support.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

# ---- UUID Primary Key Mixin ----


class UUIDMixin:
    """Provides a UUID primary key column."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )


# ---- Timestamp Mixin ----


class TimestampMixin:
    """Provides created_at and updated_at columns with auto-set."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# ---- Soft-Delete Mixin ----


class SoftDeleteMixin:
    """Provides soft-delete capability (is_active flag + deleted_at timestamp)."""

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
