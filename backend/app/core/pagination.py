"""
AquaSwift — Pagination Utilities

Supports both cursor-based (for infinite scroll) and offset-based
(for admin tables) pagination.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel

from app.core.config import settings

T = TypeVar("T")


# ---- Offset Pagination ----


class OffsetPaginationParams:
    """FastAPI dependency for offset-based pagination."""

    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number (1-indexed)"),
        page_size: int = Query(
            default=settings.DEFAULT_PAGE_SIZE,
            ge=1,
            le=settings.MAX_PAGE_SIZE,
            description="Items per page",
        ),
    ):
        self.page = page
        self.page_size = page_size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Standardized paginated response envelope."""

    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse[T]":
        total_pages = max(1, (total + page_size - 1) // page_size)
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )


# ---- Cursor Pagination ----


class CursorPaginationParams:
    """FastAPI dependency for cursor-based pagination (infinite scroll)."""

    def __init__(
        self,
        cursor: str | None = Query(None, description="Cursor for next page"),
        limit: int = Query(
            default=settings.DEFAULT_PAGE_SIZE,
            ge=1,
            le=settings.MAX_PAGE_SIZE,
            description="Items per page",
        ),
    ):
        self.cursor = cursor
        self.limit = limit


class CursorPaginatedResponse(BaseModel, Generic[T]):
    """Standardized cursor-paginated response envelope."""

    items: list[T]
    next_cursor: str | None
    has_more: bool

    @classmethod
    def create(
        cls,
        items: list[T],
        next_cursor: str | None,
        has_more: bool,
    ) -> "CursorPaginatedResponse[T]":
        return cls(items=items, next_cursor=next_cursor, has_more=has_more)
