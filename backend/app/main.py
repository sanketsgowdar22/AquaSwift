"""
AquaSwift — FastAPI Application Factory

Creates and configures the FastAPI application with middleware, exception
handlers, and router registration.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse

from app.core.cache import close_redis
from app.core.config import settings
from app.core.exceptions import (
    AppError,
    app_error_handler,
    http_exception_handler,
    unhandled_exception_handler,
)
from app.core.middleware import RequestIDMiddleware, RequestLoggingMiddleware, setup_cors

logger = structlog.get_logger()


# ---- Lifespan ----


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("starting_up", app=settings.APP_NAME, version=settings.APP_VERSION, env=settings.APP_ENV)
    yield
    # Shutdown
    await close_redis()
    logger.info("shutting_down")


# ---- App Factory ----


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Water tanker delivery platform API",
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    # ---- Middleware (order matters — outermost first) ----
    application.add_middleware(RequestLoggingMiddleware)
    application.add_middleware(RequestIDMiddleware)
    setup_cors(application)

    # ---- Exception Handlers ----
    application.add_exception_handler(AppError, app_error_handler)
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(Exception, unhandled_exception_handler)

    # ---- Register Routers ----
    _register_routers(application)

    return application


def _register_routers(application: FastAPI) -> None:
    """Register all module routers."""

    # Health check (always available, no auth)
    @application.get("/health", tags=["System"])
    async def health_check():
        return {
            "status": "healthy",
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
        }

    # ---- Layer 1: Identity ----
    from app.auth.router import router as auth_router
    application.include_router(auth_router)

    from app.rbac.router import router as rbac_router
    application.include_router(rbac_router)

    from app.users.router import router as users_router
    application.include_router(users_router)

    # ---- Layer 2: Data Configuration ----
    from app.catalog.router import router as catalog_router
    application.include_router(catalog_router)

    from app.quality.router import router as quality_router
    application.include_router(quality_router)

    from app.sources.router import router as sources_router
    application.include_router(sources_router)

    from app.addresses.router import router as addresses_router
    application.include_router(addresses_router)

    # ---- Layer 3: Business Logic ----
    from app.inventory.router import router as inventory_router
    application.include_router(inventory_router)

    from app.pricing.router import router as pricing_router
    application.include_router(pricing_router)

    from app.coupons.router import router as coupons_router
    application.include_router(coupons_router)

    # ---- Layer 4: Commerce ----
    from app.orders.router import router as orders_router
    application.include_router(orders_router)

    from app.payments.router import router as payments_router
    application.include_router(payments_router)

    # ---- Layer 5: Fulfilment ----
    from app.vehicles.router import router as vehicles_router
    application.include_router(vehicles_router)

    from app.deliveries.router import router as deliveries_router
    application.include_router(deliveries_router)

    from app.drivers.router import router as drivers_router
    application.include_router(drivers_router)

    # ---- Layer 6: Communication ----
    from app.notifications.router import router as notifications_router
    application.include_router(notifications_router)

    from app.reviews.router import router as reviews_router
    application.include_router(reviews_router)

    # ---- Layer 7: Operations ----
    from app.admin.router import router as admin_router
    application.include_router(admin_router)

    from app.businesses.router import router as businesses_router
    application.include_router(businesses_router)


# ---- Create the app instance ----

app = create_app()
