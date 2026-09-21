# Businesses Module — Tasks

## T-BIZ-001: Create Business Models

**User Story:** All business stories
**Type:** Backend
**Description:** Create `businesses`, `business_users`, `business_sites` models.
**Files:** `backend/app/businesses/models.py`
**Dependencies:** T-AUTH-001, T-ADDR-001
**Estimated Effort:** S

---

## T-BIZ-002: Implement Business Admin CRUD

**User Story:** US-BIZ-001
**Type:** Backend
**Description:** Admin CRUD for businesses, business users, and business sites. Audit logging.
**Files:** `backend/app/businesses/service.py`, `backend/app/businesses/router.py`
**Dependencies:** T-BIZ-001
**Estimated Effort:** M

---

## T-BIZ-003: Write Business Tests

**User Story:** All business stories
**Type:** Backend
**Description:** Test CRUD, user assignment, site management.
**Files:** `backend/app/businesses/tests/`
**Dependencies:** T-BIZ-002
**Estimated Effort:** S
