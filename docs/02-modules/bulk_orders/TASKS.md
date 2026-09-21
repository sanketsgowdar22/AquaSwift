# Bulk Orders Module — Tasks

## T-BULK-001: Create Bulk Request/Quote Models

**User Story:** US-BULK-001, US-BULK-002
**Type:** Backend
**Description:** Create `bulk_requests` and `bulk_quotes` models.
**Files:** `backend/app/bulk_orders/models.py`
**Dependencies:** T-BIZ-001, T-CAT-001
**Estimated Effort:** S

---

## T-BULK-002: Implement Bulk Admin Endpoints

**User Story:** US-BULK-001, US-BULK-002
**Type:** Backend
**Description:** Admin: GET /admin/bulk-requests, POST /{id}/quote, PATCH /{id}. Schemas, service, router.
**Files:** `backend/app/bulk_orders/service.py`, `backend/app/bulk_orders/router.py`
**Dependencies:** T-BULK-001
**Estimated Effort:** M

---

## T-BULK-003: Write Bulk Order Tests

**User Story:** All bulk stories
**Type:** Backend
**Description:** Test request creation, quote creation, status transitions.
**Files:** `backend/app/bulk_orders/tests/`
**Dependencies:** T-BULK-002
**Estimated Effort:** S
