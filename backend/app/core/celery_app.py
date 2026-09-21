"""
AquaSwift — Celery Application

Central Celery app for background tasks and periodic jobs.
"""

from __future__ import annotations

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "aquaswift",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule={
        # Reservation expiry — every 60 seconds
        # "reservation-expiry": {
        #     "task": "app.inventory.tasks.expire_reservations",
        #     "schedule": 60.0,
        # },
        # Reconciliation — every hour
        # "inventory-reconciliation": {
        #     "task": "app.inventory.tasks.reconcile_inventory",
        #     "schedule": 3600.0,
        # },
        # Report aggregation — daily at 2 AM
        # "report-aggregation": {
        #     "task": "app.reports.tasks.aggregate_reports",
        #     "schedule": crontab(hour=2, minute=0),
        # },
    },
)

# Auto-discover tasks from all installed modules
celery_app.autodiscover_tasks(
    [
        "app.inventory",
        "app.notifications",
        "app.reports",
        "app.recurring_orders",
    ]
)
