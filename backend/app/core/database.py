"""
AquaSwift — Database Configuration

Async SQLAlchemy engine + session factory. Provides the `get_db()` FastAPI
dependency for session-per-request with automatic rollback on exception.
"""

from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# ---- Engine ----

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)

# ---- Session Factory ----

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ---- Declarative Base ----


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


# ---- FastAPI Dependency ----


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session per request.

    - Commits on success
    - Rolls back on exception
    - Always closes the session
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
