"""
AquaSwift — Application Configuration

Typed settings via Pydantic BaseSettings. All configuration is loaded from
environment variables (or .env file). Every setting has a sensible default
for local development.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration — single source of truth for all settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---- Application ----
    APP_NAME: str = "AquaSwift"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # ---- Database ----
    DATABASE_URL: str = "postgresql+asyncpg://aquaswift:aquaswift_dev@db:5432/aquaswift"
    DATABASE_ECHO: bool = False

    # ---- Redis ----
    REDIS_URL: str = "redis://redis:6379/0"

    # ---- Security / JWT ----
    JWT_SECRET_KEY: str = "change-me-to-a-secure-random-string-in-production"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    JWT_ALGORITHM: str = "HS256"

    # ---- CORS ----
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
    ]

    # ---- OTP ----
    OTP_EXPIRY_SECONDS: int = 300
    OTP_LENGTH: int = 6
    OTP_MAX_ATTEMPTS: int = 5
    OTP_RATE_LIMIT_PER_MINUTE: int = 5

    # ---- Pagination ----
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # ---- Razorpay ----
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    RAZORPAY_WEBHOOK_SECRET: str = ""

    # ---- MSG91 (SMS/OTP) ----
    MSG91_AUTH_KEY: str = ""
    MSG91_SENDER_ID: str = "AQUASW"
    MSG91_OTP_TEMPLATE_ID: str = ""

    # ---- Firebase (Push) ----
    GOOGLE_APPLICATION_CREDENTIALS: str = ""
    FCM_PROJECT_ID: str = ""

    # ---- Google Maps ----
    GOOGLE_MAPS_API_KEY: str = ""

    # ---- Email (SendGrid) ----
    SENDGRID_API_KEY: str = ""
    EMAIL_FROM: str = "noreply@aquaswift.in"
    EMAIL_FROM_NAME: str = "AquaSwift"

    # ---- AWS S3 ----
    AWS_S3_BUCKET: str = "aquaswift-media-dev"
    AWS_S3_REGION: str = "ap-south-1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    # ---- Celery ----
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"


# Singleton — import this everywhere
settings = Settings()
