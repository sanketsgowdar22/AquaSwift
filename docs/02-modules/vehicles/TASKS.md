# Vehicles Module — Tasks

## T-VEH-001: Create Vehicle Model

**User Story:** US-VEH-001
**Type:** Backend
**Description:** Create `vehicles` model with registration_number, type, capacity_litres (BIGINT), status, current_driver_id FK.
**Files:** `backend/app/vehicles/models.py`
**Dependencies:** T-USR-001
**Estimated Effort:** S

---

## T-VEH-002: Create Vehicle Schemas & CRUD Service

**User Story:** US-VEH-001, US-VEH-002
**Type:** Backend
**Description:** Create schemas and admin CRUD service. Include driver assignment/reassignment. Audit log on all writes.
**Files:** `backend/app/vehicles/schemas.py`, `backend/app/vehicles/service.py`
**Dependencies:** T-VEH-001
**Estimated Effort:** S

---

## T-VEH-003: Create Vehicle API Routes

**User Story:** All vehicle stories
**Type:** Backend
**Description:** Admin: GET/POST/PATCH /admin/vehicles, POST /admin/vehicles/{id}/assign-driver.
**Files:** `backend/app/vehicles/router.py`
**Dependencies:** T-VEH-002
**Estimated Effort:** S

---

## T-VEH-004: Write Vehicle Tests

**User Story:** All vehicle stories
**Type:** Backend
**Description:** Test CRUD, driver assignment, capacity validation, status management.
**Files:** `backend/app/vehicles/tests/`
**Dependencies:** T-VEH-003
**Estimated Effort:** S
