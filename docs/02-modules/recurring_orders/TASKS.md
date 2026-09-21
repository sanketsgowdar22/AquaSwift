# Recurring Orders Module — Tasks

## T-REC-001: Create Recurring Order Models

**User Story:** All recurring stories
**Type:** Backend
**Description:** Create `recurring_orders` and `recurring_order_instances` models.
**Files:** `backend/app/recurring_orders/models.py`
**Dependencies:** T-ORD-001, T-CAT-001, T-ADDR-001
**Estimated Effort:** S

---

## T-REC-002: Implement Recurring Order CRUD

**User Story:** US-REC-001, US-REC-003
**Type:** Backend
**Description:** Create, pause, resume, cancel recurring orders. Admin and customer endpoints.
**Files:** `backend/app/recurring_orders/service.py`, `backend/app/recurring_orders/router.py`
**Dependencies:** T-REC-001
**Estimated Effort:** M

---

## T-REC-003: Implement Instance Generation Celery Task

**User Story:** US-REC-002
**Type:** Backend
**Description:** Daily Celery beat task: scan ACTIVE recurring orders, generate order instances for upcoming dates, call order creation service for each.
**Files:** `backend/app/recurring_orders/tasks.py`
**Dependencies:** T-REC-001, T-ORD-003
**Estimated Effort:** L

---

## T-REC-004: Write Recurring Order Tests

**User Story:** All recurring stories
**Type:** Backend
**Description:** Test CRUD, pause/resume, instance generation, schedule handling.
**Files:** `backend/app/recurring_orders/tests/`
**Dependencies:** T-REC-003
**Estimated Effort:** M
