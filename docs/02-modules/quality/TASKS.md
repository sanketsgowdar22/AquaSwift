# Quality Module — Tasks

## T-QUAL-001: Create Quality Record Model

**User Story:** US-QUAL-002
**Type:** Backend
**Description:** Create `water_quality_records` model with source_id FK, ph_level, tds, turbidity, treatment_type, tested_by, test_date, certificate_url, status (PENDING/APPROVED/REJECTED), notes.
**Files:** `backend/app/quality/models.py`
**Dependencies:** T-SRC-001 (water_sources model)
**Estimated Effort:** S

---

## T-QUAL-002: Create Quality Schemas

**User Story:** US-QUAL-001, US-QUAL-002
**Type:** Backend
**Description:** Create Pydantic schemas for quality records: Create, Update, Response, List.
**Files:** `backend/app/quality/schemas.py`
**Dependencies:** T-QUAL-001
**Estimated Effort:** S

---

## T-QUAL-003: Implement Quality Service

**User Story:** US-QUAL-001, US-QUAL-002
**Type:** Backend
**Description:** Implement: list_approved_records(source_id), create_record(data), update_record(id, data), approve/reject_record(id). Certificate upload via StorageProvider. Audit logging on all writes.
**Files:** `backend/app/quality/service.py`
**Dependencies:** T-QUAL-001, S3 adapter
**Estimated Effort:** M

---

## T-QUAL-004: Create Quality API Routes

**User Story:** US-QUAL-001, US-QUAL-002
**Type:** Backend
**Description:** Public: GET /quality/records, GET /quality/records/{id}. Admin: POST /admin/quality/records, PATCH /admin/quality/records/{id}.
**Files:** `backend/app/quality/router.py`
**Dependencies:** T-QUAL-003
**Estimated Effort:** S

---

## T-QUAL-005: Write Quality Tests

**User Story:** All quality stories
**Type:** Backend
**Description:** Test: public sees only APPROVED records, admin CRUD, status transitions, certificate URL storage.
**Files:** `backend/app/quality/tests/`
**Dependencies:** T-QUAL-004
**Estimated Effort:** S
