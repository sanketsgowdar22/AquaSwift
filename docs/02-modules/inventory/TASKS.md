# Inventory Module — Tasks

## T-INV-001: Create Inventory Models

**User Story:** US-INV-001 through US-INV-011
**Type:** Backend
**Description:** Create `inventory_transactions` (append-only ledger) and `inventory_balances` (reconciled cache) models. Enforce BIGINT for all quantities.
**Files:** `backend/app/inventory/models.py`
**Dependencies:** T-SRC-001
**Estimated Effort:** M

---

## T-INV-002: Create Inventory Schemas

**User Story:** All inventory stories
**Type:** Backend
**Description:** Create schemas: ReceiveRequest, AdjustRequest (mandatory reason), LossRequest (mandatory reason), TransactionResponse, BalanceResponse, LedgerListResponse.
**Files:** `backend/app/inventory/schemas.py`
**Dependencies:** T-INV-001
**Estimated Effort:** S

---

## T-INV-003: Implement Receive Inventory Service

**User Story:** US-INV-001
**Type:** Backend
**Description:** Implement `receive_inventory(source_id, quantity_litres, actor)` — validate source is ACTIVE, create RECEIVED transaction, update balance cache, audit log.
**Files:** `backend/app/inventory/service.py`
**Dependencies:** T-INV-001
**Estimated Effort:** S

---

## T-INV-004: Implement Reserve Inventory Service

**User Story:** US-INV-002, US-INV-011
**Type:** Backend
**Description:** Implement `reserve_inventory(source_id, quantity_litres, order_id, actor)` — SELECT ... FOR UPDATE on balance row, check available >= requested, create RESERVED transaction, update balance cache. Raise InventoryInsufficientError if unavailable.
**Files:** `backend/app/inventory/service.py`
**Dependencies:** T-INV-001
**Estimated Effort:** M

---

## T-INV-005: Implement Allocate Inventory Service

**User Story:** US-INV-003
**Type:** Backend
**Description:** Implement `allocate_inventory(source_id, quantity_litres, delivery_id, actor)` — validate quantity <= reserved for this order, create ALLOCATED transaction, update balance.
**Files:** `backend/app/inventory/service.py`
**Dependencies:** T-INV-004
**Estimated Effort:** S

---

## T-INV-006: Implement Release Inventory Service

**User Story:** US-INV-004
**Type:** Backend
**Description:** Implement `release_inventory(source_id, quantity_litres, reference_id, actor, was_allocated)` — create RELEASED transaction, update balance. Used by order cancellation, delivery failure, and reservation expiry.
**Files:** `backend/app/inventory/service.py`
**Dependencies:** T-INV-004
**Estimated Effort:** S

---

## T-INV-007: Implement Deliver Inventory Service

**User Story:** US-INV-005
**Type:** Backend
**Description:** Implement `deliver_inventory(source_id, quantity_litres, delivery_id, actor)` — validate quantity <= allocated for this delivery, create DELIVERED transaction, update balance.
**Files:** `backend/app/inventory/service.py`
**Dependencies:** T-INV-005
**Estimated Effort:** S

---

## T-INV-008: Implement Manual Adjustment Service

**User Story:** US-INV-006, US-INV-007
**Type:** Backend
**Description:** Implement `adjust_inventory(source_id, quantity_litres, reason, actor)` and `record_loss(source_id, quantity_litres, reason, actor)`. Both require mandatory reason; both write audit log.
**Files:** `backend/app/inventory/service.py`
**Dependencies:** T-INV-001
**Estimated Effort:** S

---

## T-INV-009: Implement Reservation Expiry Celery Task

**User Story:** US-INV-009
**Type:** Backend
**Description:** Create Celery beat task that runs every 60 seconds. Finds orders in PENDING_PAYMENT past configurable timeout (default 15 min), releases inventory, transitions order to FAILED, notifies customer.
**Files:** `backend/app/inventory/tasks.py`
**Dependencies:** T-INV-006, T-ORD state machine
**Estimated Effort:** M

---

## T-INV-010: Implement Reconciliation Task

**User Story:** US-INV-010
**Type:** Backend
**Description:** Create Celery task that runs hourly. For each source, sum ledger by type, compute expected balance, compare to cached balance. If discrepancy found, log alert and send ops notification.
**Files:** `backend/app/inventory/tasks.py`
**Dependencies:** T-INV-001
**Estimated Effort:** M

---

## T-INV-011: Create Inventory API Routes

**User Story:** US-INV-008
**Type:** Backend
**Description:** Admin routes: GET /admin/inventory/balances, GET /admin/inventory/balances/{source_id}, GET /admin/inventory/transactions, POST receive/adjust/loss/reconcile.
**Files:** `backend/app/inventory/router.py`
**Dependencies:** T-INV-003 through T-INV-008
**Estimated Effort:** M

---

## T-INV-012: Write Inventory Tests

**User Story:** All inventory stories
**Type:** Backend
**Description:** Test: receive, reserve (happy + oversell), allocate, release, deliver, adjustment (with/without reason), loss recording, conservation law, concurrent reservation (race condition test), reservation expiry, reconciliation discrepancy detection.
**Files:** `backend/app/inventory/tests/`
**Dependencies:** T-INV-011
**Estimated Effort:** XL
