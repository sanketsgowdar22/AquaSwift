# Quality Module — Acceptance Criteria

## AC-QUAL-001: Customer Sees Only Approved Records

**User Story:** US-QUAL-001
**Given** quality records exist with status PENDING, APPROVED, and REJECTED,
**When** a customer GET /quality/records?source_id={id},
**Then** only APPROVED records are returned.

---

## AC-QUAL-002: Admin Creates Quality Record

**User Story:** US-QUAL-002
**Given** an authenticated admin with `quality:write`,
**When** they POST /admin/quality/records with test data and certificate,
**Then** the record is created with status PENDING and certificate stored in S3.

---

## AC-QUAL-003: Admin Approves Quality Record

**User Story:** US-QUAL-002
**Given** a quality record with status PENDING,
**When** the admin PATCHes it with `{ "status": "APPROVED" }`,
**Then** the status changes to APPROVED and an audit log is written.

---

## AC-QUAL-004: Admin Rejects Quality Record

**User Story:** US-QUAL-002
**Given** a quality record with status PENDING,
**When** the admin PATCHes it with `{ "status": "REJECTED", "notes": "TDS too high" }`,
**Then** the status changes to REJECTED with notes and an audit log is written.
