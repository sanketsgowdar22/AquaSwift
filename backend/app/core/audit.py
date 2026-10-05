"""
AquaSwift — Audit Logger

Append-only audit logging utility. Every admin write operation calls this
to create a tamper-proof trail of changes.

The audit_logs table is append-only — no UPDATE or DELETE allowed.
"""

from __future__ import annotations

import uuid
from typing import Any

import structlog
from sqlalchemy import Column, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.core.models import TimestampMixin

logger = structlog.get_logger()


# ---- Audit Log Model ----


class AuditLog(Base):
    """
    Append-only audit log table.

    Records all admin write operations with before/after state snapshots.
    """

    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    action = Column(String(50), nullable=False, index=True)  # CREATE, UPDATE, DELETE, etc.
    entity_type = Column(String(100), nullable=False, index=True)
    entity_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    before_state = Column(JSONB, nullable=True)
    after_state = Column(JSONB, nullable=True)
    metadata_ = Column("metadata", JSONB, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )


# ---- Audit Logger Function ----


async def audit_log(
    db: AsyncSession,
    *,
    actor_id: uuid.UUID | None,
    action: str,
    entity_type: str,
    entity_id: uuid.UUID | None = None,
    before_state: dict[str, Any] | None = None,
    after_state: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> AuditLog:
    """
    Write an audit log entry.

    This function should be called from every service that performs admin
    write operations. The entry is written within the caller's transaction,
    so it commits or rolls back together with the business operation.

    Args:
        db: Database session (from the caller's transaction)
        actor_id: UUID of the user performing the action
        action: Action type (CREATE, UPDATE, DELETE, DEACTIVATE, etc.)
        entity_type: Entity being modified (e.g., "water_purpose", "pricing_rule")
        entity_id: UUID of the specific entity
        before_state: JSON snapshot of the entity before the change
        after_state: JSON snapshot of the entity after the change
        metadata: Additional context (e.g., reason for change)

    Returns:
        The created AuditLog entry
    """
    entry = AuditLog(
        actor_id=actor_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        before_state=before_state,
        after_state=after_state,
        metadata_=metadata,
    )
    db.add(entry)

    logger.info(
        "audit_log",
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id) if entity_id else None,
        actor_id=str(actor_id) if actor_id else None,
    )

    return entry
