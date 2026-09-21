# Inventory Module — Acceptance Criteria

## AC-INV-001: Receive Increases Available Balance

**User Story:** US-INV-001
**Given** a source has 10,000L available,
**When** admin records receipt of 5,000L,
**Then** available balance becomes 15,000L, a RECEIVED transaction is written, and audit log is created.

---

## AC-INV-002: Reserve Decreases Available, Increases Reserved

**User Story:** US-INV-002
**Given** a source has 10,000L available,
**When** an order reserves 3,000L,
**Then** available becomes 7,000L, reserved becomes 3,000L, and a RESERVED transaction is written.

---

## AC-INV-003: Reservation Rejected on Insufficient Inventory

**User Story:** US-INV-002
**Given** a source has 2,000L available,
**When** an order attempts to reserve 5,000L,
**Then** the system returns error code `INVENTORY_INSUFFICIENT` and no transaction is written.

---

## AC-INV-004: Concurrent Reservations Cannot Oversell

**User Story:** US-INV-011
**Given** a source has 5,000L available,
**When** two concurrent orders each try to reserve 3,000L simultaneously,
**Then** exactly one succeeds (3,000L reserved) and the other fails with `INVENTORY_INSUFFICIENT`.

---

## AC-INV-005: Allocate Moves Reserved to Allocated

**User Story:** US-INV-003
**Given** 3,000L is reserved for an order,
**When** a delivery is assigned,
**Then** reserved decreases by 3,000L, allocated increases by 3,000L, and an ALLOCATED transaction is written.

---

## AC-INV-006: Release Returns to Available

**User Story:** US-INV-004
**Given** 3,000L is reserved for a cancelled order,
**When** the cancellation releases inventory,
**Then** reserved decreases by 3,000L, available increases by 3,000L, and a RELEASED transaction is written.

---

## AC-INV-007: Deliver Deducts Allocated

**User Story:** US-INV-005
**Given** 3,000L is allocated to a delivery,
**When** the delivery is completed,
**Then** allocated decreases by 3,000L and a DELIVERED transaction is written.

---

## AC-INV-008: Manual Adjustment Requires Reason

**User Story:** US-INV-006
**Given** an admin with `inventory:adjust` permission,
**When** they POST /admin/inventory/adjust without a reason,
**Then** the system returns 400 with code `MISSING_ADJUSTMENT_REASON`.

---

## AC-INV-009: Manual Adjustment with Reason Succeeds

**User Story:** US-INV-006
**Given** an admin provides a quantity and mandatory reason,
**When** they POST /admin/inventory/adjust,
**Then** the adjustment is recorded, balance is updated, and audit log includes the reason.

---

## AC-INV-010: Loss Recording Reduces Available

**User Story:** US-INV-007
**Given** a source has 10,000L available,
**When** the admin records 500L loss with reason "Pipe leak — Section B",
**Then** available becomes 9,500L and a LOST_WASTAGE transaction is written.

---

## AC-INV-011: Ledger Is Append-Only

**User Story:** US-INV-001
**Given** inventory transactions exist in the ledger,
**When** any attempt is made to UPDATE or DELETE a transaction,
**Then** the operation is rejected (database constraint or application-level enforcement).

---

## AC-INV-012: Reservation Expiry Releases Inventory

**User Story:** US-INV-009
**Given** an order in PENDING_PAYMENT status is older than the configured timeout,
**When** the reservation expiry Celery task runs,
**Then** the reserved inventory is released, the order transitions to FAILED, and the customer is notified.

---

## AC-INV-013: Conservation Law Holds

**User Story:** US-INV-010
**Given** multiple transactions of various types exist for a source,
**When** the reconciliation task runs,
**Then** available + reserved + allocated + delivered + lost_wastage = total_received, and no alert is generated.

---

## AC-INV-014: Reconciliation Detects Discrepancy

**User Story:** US-INV-010
**Given** the cached balance disagrees with the ledger sum,
**When** the reconciliation task runs,
**Then** an alert is generated, the ops team is notified, and the discrepancy details are logged.

---

## AC-INV-015: Admin Views Ledger with Filters

**User Story:** US-INV-008
**Given** an admin with `inventory:read` permission,
**When** they GET /admin/inventory/transactions?source_id=X&type=RESERVED&created_after=2026-09-01,
**Then** the system returns matching ledger entries sorted by created_at DESC.

---

## AC-INV-016: All Quantities Are Integer Litres

**User Story:** All inventory stories
**Given** any inventory operation,
**When** a non-integer quantity is submitted,
**Then** the system returns 422 validation error (BIGINT integer litres only).
