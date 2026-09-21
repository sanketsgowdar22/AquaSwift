"""
AquaSwift — Structured Error Classes

All application errors subclass `AppError` and produce a standardized JSON
error envelope. Clients branch on `code`, never on `message`.

Envelope format:
    {
        "code": "INVENTORY_INSUFFICIENT",
        "message": "Human-readable description.",
        "details": { ... }
    }
"""

from __future__ import annotations

from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.responses import ORJSONResponse


# ---- Base Error ----


class AppError(Exception):
    """Base application error. All domain errors should subclass this."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: dict[str, Any] | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
        }
        if self.details:
            result["details"] = self.details
        return result


# ---- Specific Errors ----


class NotFoundError(AppError):
    """Resource not found."""

    def __init__(self, resource: str, identifier: Any = None):
        details = {"resource": resource}
        if identifier is not None:
            details["identifier"] = str(identifier)
        super().__init__(
            code="NOT_FOUND",
            message=f"{resource} not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class ConflictError(AppError):
    """Resource conflict (duplicate, state violation)."""

    def __init__(self, code: str = "CONFLICT", message: str = "Resource conflict."):
        super().__init__(code=code, message=message, status_code=status.HTTP_409_CONFLICT)


class PermissionDeniedError(AppError):
    """Insufficient permissions."""

    def __init__(self, message: str = "You do not have permission for this action."):
        super().__init__(
            code="INSUFFICIENT_PERMISSIONS",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class ValidationError(AppError):
    """Business rule validation failure."""

    def __init__(self, code: str = "VALIDATION_ERROR", message: str = "Validation failed.", details: dict | None = None):
        super().__init__(code=code, message=message, status_code=status.HTTP_400_BAD_REQUEST, details=details)


class InsufficientInventoryError(AppError):
    """Not enough inventory available."""

    def __init__(self, requested: int, available: int, source_id: str | None = None):
        details: dict[str, Any] = {
            "requested_litres": requested,
            "max_available_litres": available,
        }
        if source_id:
            details["source_id"] = source_id
        super().__init__(
            code="INVENTORY_INSUFFICIENT",
            message="Requested quantity exceeds available inventory.",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details,
        )


class IllegalTransitionError(AppError):
    """Invalid state machine transition."""

    def __init__(self, entity: str, from_status: str, to_status: str):
        super().__init__(
            code="ILLEGAL_TRANSITION",
            message=f"Cannot transition {entity} from '{from_status}' to '{to_status}'.",
            status_code=status.HTTP_409_CONFLICT,
            details={"from_status": from_status, "to_status": to_status},
        )


class RateLimitError(AppError):
    """Rate limit exceeded."""

    def __init__(self, retry_after: int = 60):
        super().__init__(
            code="RATE_LIMIT_EXCEEDED",
            message="Too many requests. Please try again later.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details={"retry_after_seconds": retry_after},
        )


class PriceChangedError(AppError):
    """Price changed between quote and order creation."""

    def __init__(self, old_total: str, new_total: str):
        super().__init__(
            code="PRICE_CHANGED",
            message="The price has changed since your last quote. Please review the new price.",
            status_code=status.HTTP_409_CONFLICT,
            details={"old_total": old_total, "new_total": new_total},
        )


# ---- Exception Handlers ----


async def app_error_handler(request: Request, exc: AppError) -> ORJSONResponse:
    """Convert AppError to standardized JSON response."""
    return ORJSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> ORJSONResponse:
    """Convert FastAPI HTTPException to standardized JSON response."""
    detail = exc.detail
    if isinstance(detail, dict):
        content = detail
    else:
        content = {"code": "HTTP_ERROR", "message": str(detail)}
    return ORJSONResponse(status_code=exc.status_code, content=content)


async def unhandled_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    """Catch-all for unhandled exceptions — never leak stack traces."""
    import structlog

    logger = structlog.get_logger()
    logger.error("unhandled_exception", exc_type=type(exc).__name__, exc_msg=str(exc), path=request.url.path)

    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred.",
        },
    )
