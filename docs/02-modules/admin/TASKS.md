# Admin Module — Tasks

## T-ADM-001: Implement Dashboard Summary Endpoint

**User Story:** US-ADM-001
**Type:** Backend
**Description:** Implement GET /admin/dashboard returning: active orders count, pending deliveries, low-inventory alerts, today's revenue, driver availability, and recent alerts.
**Files:** `backend/app/admin/service.py`, `backend/app/admin/router.py`
**Dependencies:** T-ORD-001, T-DEL-001, T-INV-001
**Estimated Effort:** M

---

## T-ADM-002: Implement Role Management Endpoints

**User Story:** US-ADM-002
**Type:** Backend
**Description:** GET /admin/roles (list), POST/DELETE /admin/users/{id}/roles. Delegate to RBAC module.
**Files:** `backend/app/admin/router.py`
**Dependencies:** T-RBAC-004
**Estimated Effort:** S

---

## T-ADM-003: Write Admin Tests

**User Story:** All admin stories
**Type:** Backend
**Description:** Test dashboard metrics, role management, permission enforcement.
**Files:** `backend/app/admin/tests/`
**Dependencies:** T-ADM-001, T-ADM-002
**Estimated Effort:** M
