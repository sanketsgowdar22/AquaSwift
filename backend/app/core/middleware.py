"""
AquaSwift — Middleware

CORS configuration, request ID injection, and structured request logging.
"""

from __future__ import annotations

import time
import uuid

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings

logger = structlog.get_logger()


# ---- CORS Setup ----


def setup_cors(app) -> None:
    """Add CORS middleware with configured origins."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# ---- Request ID Middleware ----


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Inject a unique request ID into every request/response.

    The ID is available as `request.state.request_id` and returned in the
    `X-Request-ID` response header for client-side correlation.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


# ---- Request Logging Middleware ----


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Log every request with method, path, status, and duration.

    Uses structlog for structured JSON logging in production.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.perf_counter()

        response = await call_next(request)

        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        request_id = getattr(request.state, "request_id", "unknown")

        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            request_id=request_id,
        )

        return response
