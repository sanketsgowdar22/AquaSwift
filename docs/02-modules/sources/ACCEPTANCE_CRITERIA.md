# Sources Module — Acceptance Criteria

## AC-SRC-001: Admin Creates Water Source

**User Story:** US-SRC-001
**Given** an authenticated admin with `sources:write`,
**When** they POST /admin/sources with name, type, capacity, and GPS coordinates,
**Then** the source is created with status ACTIVE and an audit log is written.

---

## AC-SRC-002: Admin Views Source with Balance

**User Story:** US-SRC-002
**Given** a source exists with inventory transactions,
**When** the admin GET /admin/sources/{id},
**Then** the response includes source details and current inventory balance (available, reserved, allocated).

---

## AC-SRC-003: Admin Deactivates Source

**User Story:** US-SRC-001
**Given** a source with no reserved/allocated inventory,
**When** the admin PATCHes with `{ "status": "INACTIVE" }`,
**Then** the source is deactivated and cannot receive new inventory.

---

## AC-SRC-004: Cannot Deactivate Source with Active Reservations

**User Story:** US-SRC-002
**Given** a source has reserved or allocated inventory,
**When** the admin attempts to deactivate it,
**Then** the system returns 400 with code `SOURCE_HAS_ACTIVE_INVENTORY`.
