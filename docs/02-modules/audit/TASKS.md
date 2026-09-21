# Audit Module — Tasks

## T-AUD-001: Create Audit Log Model

**User Story:** US-AUD-001, US-AUD-003
**Type:** Backend
**Description:** Create `audit_logs` model (append-only). Enforce no UPDATE/DELETE via application-level check or DB trigger.
**Files:** `backend/app/audit/models.py`
**Dependencies:** T-AUTH-001
**Estimated Effort:** S

---

## T-AUD-002: Implement Audit Logger Utility

**User Story:** US-AUD-001
**Type:** Backend
**Description:** Implement `audit_log(db, actor, action, entity_type, entity_id, before_state, after_state)` utility function. Called from all admin write services.
**Files:** `backend/app/core/audit.py`
**Dependencies:** T-AUD-001
**Estimated Effort:** S

---

## T-AUD-003: Implement Entity History Endpoint

**User Story:** US-AUD-002
**Type:** Backend
**Description:** Implement GET /admin/audit-logs/{entity_type}/{entity_id} — return complete ordered history of changes for a specific entity.
**Files:** `backend/app/audit/service.py`, `backend/app/audit/router.py`
**Dependencies:** T-AUD-001
**Estimated Effort:** S

---

## T-AUD-004: Implement Audit Log Search Endpoint

**User Story:** US-AUD-004
**Type:** Backend
**Description:** Implement GET /admin/audit-logs with filters: entity_type, actor_id, action, date_from, date_to. Paginated, run on read replica.
**Files:** `backend/app/audit/router.py`
**Dependencies:** T-AUD-001
**Estimated Effort:** S

---

## T-AUD-005: Write Audit Tests

**User Story:** All audit stories
**Type:** Backend
**Description:** Test: audit log creation on admin write, entity history reconstruction, immutability enforcement, search filtering.
**Files:** `backend/app/audit/tests/`
**Dependencies:** T-AUD-004
**Estimated Effort:** M
