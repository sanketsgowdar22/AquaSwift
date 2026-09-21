# Inventory Module — User Stories

## US-INV-001: Admin Records Water Receipt

**As an** admin (P4/P5),
**I want to** record incoming water at a source,
**So that** the available inventory balance increases and the ledger tracks the receipt.

**SRS Requirements:** INV-001, INV-003
**Priority:** MUST
**Phase:** V1

---

## US-INV-002: Inventory Reservation on Order

**As a** system,
**I want to** automatically reserve inventory from a source when an order is created,
**So that** the ordered quantity is held and cannot be oversold.

**SRS Requirements:** INV-004, INV-005, INV-006, INV-018
**Priority:** MUST
**Phase:** V1

---

## US-INV-003: Inventory Allocation for Delivery

**As a** system,
**I want to** allocate reserved inventory to a specific delivery and vehicle,
**So that** the driver knows the exact quantity and source for pickup.

**SRS Requirements:** INV-007
**Priority:** MUST
**Phase:** V1

---

## US-INV-004: Inventory Release on Cancellation

**As a** system,
**I want to** release reserved/allocated inventory when an order is cancelled or a delivery fails,
**So that** the inventory returns to the available pool.

**SRS Requirements:** INV-008
**Priority:** MUST
**Phase:** V1

---

## US-INV-005: Inventory Delivered Deduction

**As a** system,
**I want to** deduct allocated inventory when a delivery is completed,
**So that** the ledger accurately reflects water that has left the source.

**SRS Requirements:** INV-009
**Priority:** MUST
**Phase:** V1

---

## US-INV-006: Admin Manual Adjustment

**As an** admin (P4/P5),
**I want to** make manual inventory adjustments with a mandatory reason,
**So that** I can correct discrepancies while maintaining an audit trail.

**SRS Requirements:** INV-010, INV-011
**Priority:** MUST
**Phase:** V1

---

## US-INV-007: Admin Loss/Wastage Recording

**As an** admin (P4/P5),
**I want to** record inventory loss or wastage with a mandatory reason,
**So that** the conservation law accounts for all water.

**SRS Requirements:** INV-012
**Priority:** MUST
**Phase:** V1

---

## US-INV-008: Admin Views Inventory Dashboard

**As an** admin (P4/P5),
**I want to** view inventory balances for all sources and the transaction ledger,
**So that** I have real-time visibility into water supply and movements.

**SRS Requirements:** INV-002, INV-013, INV-014
**Priority:** MUST
**Phase:** V1

---

## US-INV-009: Reservation Expiry

**As a** system,
**I want** expired reservations (orders not paid within timeout) to be automatically released,
**So that** inventory doesn't stay locked indefinitely for abandoned orders.

**SRS Requirements:** INV-015, INV-016
**Priority:** MUST
**Phase:** V1

---

## US-INV-010: Conservation Law Verification

**As a** system,
**I want to** periodically verify that the conservation law holds (available + reserved + allocated + delivered + lost = received),
**So that** any ledger discrepancy is detected and alerted.

**SRS Requirements:** INV-017
**Priority:** MUST
**Phase:** V1

---

## US-INV-011: Concurrency-Safe Reservation

**As a** system,
**I want** inventory reservation to use row-level locking (SELECT ... FOR UPDATE) on balance rows,
**So that** concurrent orders cannot oversell available inventory.

**SRS Requirements:** INV-018
**Priority:** MUST
**Phase:** V1
