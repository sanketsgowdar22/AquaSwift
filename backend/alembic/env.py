"""
Alembic Environment Configuration

Uses async SQLAlchemy engine from the app's database module.
Imports all models so Alembic's autogenerate can detect schema changes.
"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.core.database import Base

# Import all models here so Alembic sees them for autogenerate.
# As modules are added, import their models below:
from app.core.audit import AuditLog  # noqa: F401

# Layer 1: Identity
from app.auth.models import User, RefreshToken  # noqa: F401
from app.rbac.models import Role  # noqa: F401
from app.users.models import UserRole, CustomerProfile, DriverProfile  # noqa: F401

# Layer 2-7: All remaining modules
from app.catalog.models import WaterPurpose, WaterQualityType, DeliveryMethod, WaterPurposeQuality, WaterVariant  # noqa: F401
from app.sources.models import WaterSource  # noqa: F401
from app.quality.models import WaterQualityRecord  # noqa: F401
from app.addresses.models import Address  # noqa: F401
from app.inventory.models import InventoryTransaction, InventoryBalance  # noqa: F401
from app.pricing.models import PricingRule, DeliveryPricingRule  # noqa: F401
from app.coupons.models import Coupon  # noqa: F401
from app.orders.models import Order, OrderItem, OrderStatusHistory  # noqa: F401
from app.vehicles.models import Vehicle  # noqa: F401
from app.deliveries.models import Delivery, DeliveryAssignment, DeliveryEvent  # noqa: F401
from app.payments.models import Payment, PaymentTransaction, Refund  # noqa: F401
from app.notifications.models import Notification, DeviceToken  # noqa: F401
from app.reviews.models import Review  # noqa: F401
from app.businesses.models import Business, BusinessUser, BusinessSite, BulkRequest, BulkQuote  # noqa: F401
from app.businesses.phase2_models import RecurringOrder, RecurringOrderInstance, Invoice  # noqa: F401

# Alembic Config object
config = context.config

# Setup Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (generates SQL without connecting)."""
    url = settings.DATABASE_URL.replace("+asyncpg", "+psycopg2")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Execute migrations against a connection."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
