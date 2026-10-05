"""
AquaSwift — Seed Data Script

Seeds initial data required for the application to function:
- Platform roles and permissions
- Default admin user (development only)

Usage:
    docker-compose exec backend python -m scripts.seed_data
"""

from __future__ import annotations

import asyncio
import uuid

import structlog

from app.core.config import settings
from app.core.database import async_session_factory
from app.core.security import hash_password

logger = structlog.get_logger()

# ---- Role & Permission Definitions ----

PLATFORM_ROLES = {
    "CUSTOMER": {
        "description": "Individual or business customer",
        "permissions": [
            "catalog:read",
            "addresses:read",
            "addresses:write",
            "orders:create",
            "orders:read",
            "payments:read",
            "notifications:read",
            "reviews:write",
        ],
    },
    "DRIVER": {
        "description": "Delivery driver",
        "permissions": [
            "deliveries:read",
            "deliveries:respond",
            "deliveries:execute",
            "drivers:read",
            "drivers:write",
        ],
    },
    "OPS_MANAGER": {
        "description": "Operations manager",
        "permissions": [
            "catalog:read",
            "orders:read",
            "orders:cancel",
            "deliveries:read",
            "deliveries:assign",
            "inventory:read",
            "inventory:write",
            "drivers:read",
            "vehicles:read",
            "customers:read",
            "reports:read",
            "quality:read",
            "quality:write",
            "sources:read",
            "sources:write",
        ],
    },
    "SUPER_ADMIN": {
        "description": "Full platform access",
        "permissions": [
            "catalog:read",
            "catalog:write",
            "orders:read",
            "orders:cancel",
            "deliveries:read",
            "deliveries:assign",
            "inventory:read",
            "inventory:write",
            "inventory:adjust",
            "pricing:read",
            "pricing:write",
            "coupons:read",
            "coupons:write",
            "drivers:read",
            "drivers:write",
            "vehicles:read",
            "vehicles:write",
            "customers:read",
            "customers:write",
            "businesses:read",
            "businesses:write",
            "reports:read",
            "analytics:read",
            "quality:read",
            "quality:write",
            "sources:read",
            "sources:write",
            "roles:read",
            "roles:write",
            "audit:read",
            "refunds:read",
            "refunds:write",
            "invoices:read",
            "invoices:write",
            "notifications:admin",
            "addresses:read",
        ],
    },
}


async def seed_roles() -> None:
    """Seed platform roles and permissions into the database."""
    from sqlalchemy import select

    from app.rbac.models import Role

    async with async_session_factory() as db:
        for role_name, role_data in PLATFORM_ROLES.items():
            result = await db.execute(select(Role).where(Role.name == role_name))
            existing = result.scalar_one_or_none()

            if existing:
                # Update permissions
                existing.permissions = role_data["permissions"]
                existing.description = role_data["description"]
                logger.info("role_updated", role=role_name)
            else:
                role = Role(
                    name=role_name,
                    description=role_data["description"],
                    permissions=role_data["permissions"],
                )
                db.add(role)
                logger.info("role_created", role=role_name, permissions=len(role_data["permissions"]))

        await db.commit()

    logger.info("seed_roles_complete", roles=list(PLATFORM_ROLES.keys()))


async def seed_admin_user() -> None:
    """Seed a default admin user for development."""
    if settings.is_production:
        logger.warning("skipping_admin_seed", reason="production environment")
        return

    from sqlalchemy import select

    from app.auth.models import User
    from app.rbac.models import Role
    from app.users.models import UserRole

    async with async_session_factory() as db:
        # Check if admin already exists
        result = await db.execute(select(User).where(User.email == "admin@aquaswift.in"))
        existing = result.scalar_one_or_none()

        if existing:
            logger.info("admin_user_exists", email="admin@aquaswift.in")
            return

        # Create admin user
        admin = User(
            email="admin@aquaswift.in",
            password_hash=hash_password("admin123"),
            full_name="AquaSwift Admin",
        )
        db.add(admin)
        await db.flush()

        # Assign SUPER_ADMIN role
        result = await db.execute(select(Role).where(Role.name == "SUPER_ADMIN"))
        admin_role = result.scalar_one_or_none()
        if admin_role:
            db.add(UserRole(user_id=admin.id, role_id=admin_role.id))

        await db.commit()
        logger.info("admin_user_created", email="admin@aquaswift.in", password="admin123")


async def main() -> None:
    """Run all seed operations."""
    logger.info("seed_start")
    await seed_roles()
    await seed_admin_user()
    logger.info("seed_complete")


if __name__ == "__main__":
    asyncio.run(main())
