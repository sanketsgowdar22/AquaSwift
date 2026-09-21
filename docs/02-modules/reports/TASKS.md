# Reports Module — Tasks

## T-RPT-001: Implement Sales Report

**User Story:** US-RPT-001
**Type:** Backend
**Description:** Implement GET /admin/reports/sales with filters: date_from, date_to, purpose_id, quality_id. Aggregate order_items to produce revenue, volume, order count by period.
**Files:** `backend/app/reports/service.py`, `backend/app/reports/router.py`
**Dependencies:** T-ORD-001
**Estimated Effort:** M

---

## T-RPT-002: Implement Inventory & Delivery Reports

**User Story:** US-RPT-002, US-RPT-003
**Type:** Backend
**Description:** Inventory: aggregate transactions by source/type/period. Delivery: aggregate by driver, avg completion time, success/failure rate.
**Files:** `backend/app/reports/service.py`
**Dependencies:** T-INV-001, T-DEL-001
**Estimated Effort:** M

---

## T-RPT-003: Implement Report Aggregation Celery Task

**User Story:** US-RPT-005
**Type:** Backend
**Description:** Daily Celery beat task that pre-aggregates key metrics into report tables or materialized views.
**Files:** `backend/app/reports/tasks.py`
**Dependencies:** T-RPT-001, T-RPT-002
**Estimated Effort:** M

---

## T-RPT-004: Write Report Tests

**User Story:** All report stories
**Type:** Backend
**Description:** Test: sales aggregation, inventory summary, delivery metrics, date filtering, read-replica routing.
**Files:** `backend/app/reports/tests/`
**Dependencies:** T-RPT-001, T-RPT-002
**Estimated Effort:** M
