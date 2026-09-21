# Audit Module — User Stories

## US-AUD-001: Automatic Audit Logging

**As a** system, **I want** every admin write operation to automatically log to the append-only audit_logs table, **So that** all changes are traceable.
**SRS Requirements:** AUD-001, AUD-002, AUD-003 **Priority:** MUST **Phase:** V1

---

## US-AUD-002: Entity History Reconstruction

**As an** admin (P4/P5), **I want to** view the complete change history of any entity, **So that** I can investigate issues and verify compliance.
**SRS Requirements:** AUD-004, AUD-005 **Priority:** MUST **Phase:** V1

---

## US-AUD-003: Audit Log Immutability

**As a** system, **I want** audit logs to be append-only (no update/delete), **So that** the audit trail is tamper-proof.
**SRS Requirements:** AUD-006 **Priority:** MUST **Phase:** V1

---

## US-AUD-004: Admin Audit Log Querying

**As an** admin (P4/P5), **I want to** search audit logs by entity, actor, action, and date range, **So that** I can find specific changes quickly.
**SRS Requirements:** AUD-007 **Priority:** MUST **Phase:** V1
