"""
AquaSwift — Redis Cache Utilities

Provides a Redis connection factory and helper functions for caching with
TTL support and write-through invalidation.
"""

from __future__ import annotations

import json
from typing import Any

import redis.asyncio as aioredis

from app.core.config import settings

# ---- Connection Pool ----

_redis_pool: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    """Get or create the Redis connection pool."""
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=20,
        )
    return _redis_pool


async def close_redis() -> None:
    """Close the Redis connection pool on shutdown."""
    global _redis_pool
    if _redis_pool is not None:
        await _redis_pool.close()
        _redis_pool = None


# ---- Cache Helpers ----


async def cache_get(key: str) -> Any | None:
    """
    Get a value from cache.

    Returns the deserialized value, or None if not found.
    """
    r = await get_redis()
    value = await r.get(key)
    if value is not None:
        return json.loads(value)
    return None


async def cache_set(key: str, value: Any, ttl_seconds: int = 60) -> None:
    """
    Set a value in cache with a TTL.

    Args:
        key: Cache key
        value: Any JSON-serializable value
        ttl_seconds: Time-to-live in seconds (default 60)
    """
    r = await get_redis()
    await r.set(key, json.dumps(value, default=str), ex=ttl_seconds)


async def cache_delete(key: str) -> None:
    """Delete a specific cache key."""
    r = await get_redis()
    await r.delete(key)


async def cache_delete_pattern(pattern: str) -> None:
    """
    Delete all keys matching a glob pattern.

    Example: cache_delete_pattern("catalog:*") invalidates all catalog cache.
    """
    r = await get_redis()
    cursor = 0
    while True:
        cursor, keys = await r.scan(cursor=cursor, match=pattern, count=100)
        if keys:
            await r.delete(*keys)
        if cursor == 0:
            break
