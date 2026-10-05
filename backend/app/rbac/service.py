"""
AquaSwift — RBAC Service

Core authorization logic: check_user_permission() is called by the
require_permission() dependency for every protected endpoint.
"""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.rbac.models import Role


async def get_all_roles(db: AsyncSession) -> list[Role]:
    """Get all platform roles."""
    result = await db.execute(select(Role).order_by(Role.name))
    return list(result.scalars().all())


async def get_role_by_name(db: AsyncSession, name: str) -> Role | None:
    """Get a role by name."""
    result = await db.execute(select(Role).where(Role.name == name))
    return result.scalar_one_or_none()


async def get_role_by_id(db: AsyncSession, role_id: uuid.UUID) -> Role | None:
    """Get a role by ID."""
    result = await db.execute(select(Role).where(Role.id == role_id))
    return result.scalar_one_or_none()


async def check_user_permission(user, permission: str) -> bool:
    """
    Check if a user has a specific permission.

    Called by the require_permission() dependency. The user object is
    expected to have user_roles eagerly loaded or accessible.

    Permission format: "resource:action" (e.g., "catalog:write", "orders:create")
    """
    # Lazy import to avoid circular deps
    from sqlalchemy import select as sa_select

    from app.core.database import async_session_factory

    async with async_session_factory() as db:
        # Get user's roles via user_roles join table
        from app.users.models import UserRole

        result = await db.execute(
            sa_select(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user.id)
        )
        roles = result.scalars().all()

        # Check if any of the user's roles contain the required permission
        for role in roles:
            if permission in (role.permissions or []):
                return True

    return False


async def get_user_permissions(user_id: uuid.UUID, db: AsyncSession) -> list[str]:
    """Get all permissions for a user across all their roles."""
    from app.users.models import UserRole

    result = await db.execute(
        select(Role)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id)
    )
    roles = result.scalars().all()

    permissions = set()
    for role in roles:
        permissions.update(role.permissions or [])

    return sorted(permissions)
