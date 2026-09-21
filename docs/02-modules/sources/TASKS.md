# Sources Module — Tasks

## T-SRC-001: Create Water Source Model

**User Story:** US-SRC-001, US-SRC-002
**Type:** Backend
**Description:** Create `water_sources` model with name, type, gps coordinates, capacity_litres (BIGINT), status.
**Files:** `backend/app/inventory/models.py` (or `backend/app/sources/models.py`)
**Dependencies:** None
**Estimated Effort:** S

---

## T-SRC-002: Create Source Schemas & Service

**User Story:** US-SRC-001
**Type:** Backend
**Description:** Create Pydantic schemas and CRUD service for sources. Include inventory balance in detail view.
**Files:** `backend/app/sources/schemas.py`, `backend/app/sources/service.py`
**Dependencies:** T-SRC-001
**Estimated Effort:** S

---

## T-SRC-003: Create Source API Routes

**User Story:** US-SRC-001, US-SRC-002
**Type:** Backend
**Description:** Admin routes: GET /admin/sources, GET /admin/sources/{id}, POST /admin/sources, PATCH /admin/sources/{id}.
**Files:** `backend/app/sources/router.py`
**Dependencies:** T-SRC-002
**Estimated Effort:** S

---

## T-SRC-004: Write Source Tests

**User Story:** All source stories
**Type:** Backend
**Description:** Test CRUD, status validation, capacity constraints, audit logging.
**Files:** `backend/app/sources/tests/`
**Dependencies:** T-SRC-003
**Estimated Effort:** S
