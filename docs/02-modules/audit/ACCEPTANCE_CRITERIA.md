# Audit Module — Acceptance Criteria

## AC-AUD-001: Admin Write Creates Audit Log

**User Story:** US-AUD-001
**Given** an admin creates/updates a pricing rule,
**When** the operation completes,
**Then** an audit_log row is written with actor_id, action, entity_type, entity_id, before_state, and after_state.

---

## AC-AUD-002: Audit Log Is Append-Only

**User Story:** US-AUD-003
**Given** audit log rows exist,
**When** any attempt is made to UPDATE or DELETE a row,
**Then** the operation is rejected.

---

## AC-AUD-003: Entity History Shows Complete Timeline

**User Story:** US-AUD-002
**Given** a pricing rule has been created, updated twice, and deactivated,
**When** admin GET /admin/audit-logs/pricing_rule/{id},
**Then** 4 audit entries are returned in chronological order with before/after snapshots.

---

## AC-AUD-004: Audit Search by Filters

**User Story:** US-AUD-004
**Given** audit logs from multiple actors and entity types,
**When** admin GET /admin/audit-logs?entity_type=water_purpose&action=UPDATE&date_from=2026-09-01,
**Then** only matching audit entries are returned.

---

## AC-AUD-005: Before/After State Captures Full Entity

**User Story:** US-AUD-001
**Given** an admin updates a catalog entity's name,
**When** the audit log is written,
**Then** before_state contains the full entity JSON before the change and after_state contains the full entity JSON after.
