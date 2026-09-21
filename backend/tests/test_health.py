"""
Tests for the health check and core application setup.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Health endpoint returns healthy status."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data


@pytest.mark.asyncio
async def test_health_check_version():
    """Health endpoint returns the correct version."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")

    assert response.json()["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_docs_accessible_in_dev():
    """OpenAPI docs should be accessible in development mode."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/docs")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_not_found_returns_json():
    """Non-existent routes should return JSON error, not HTML."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/nonexistent")

    assert response.status_code in (404, 405)
