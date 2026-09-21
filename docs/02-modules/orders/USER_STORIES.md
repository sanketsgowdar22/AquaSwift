# Orders Module — User Stories

## US-ORD-001: Customer Places Order

**As a** customer (P1),
**I want to** place a water order by selecting a variant, quantity, address, and optional timeslot,
**So that** water is delivered to my location.

**SRS Requirements:** ORD-001, ORD-002, ORD-003, ORD-004, ORD-005
**Priority:** MUST
**Phase:** V1

---

## US-ORD-002: Order Idempotency

**As a** system,
**I want** order creation to support an Idempotency-Key header,
**So that** network retries do not create duplicate orders.

**SRS Requirements:** ORD-006
**Priority:** MUST
**Phase:** V1

---

## US-ORD-003: Customer Views Orders

**As a** customer (P1),
**I want to** view my order history with status, details, and tracking,
**So that** I can monitor my past and active orders.

**SRS Requirements:** ORD-007, ORD-009
**Priority:** MUST
**Phase:** V1

---

## US-ORD-004: Customer Cancels Order

**As a** customer (P1),
**I want to** cancel my order before it is out for delivery,
**So that** I can change my mind without penalty in the early stages.

**SRS Requirements:** ORD-010, ORD-011
**Priority:** MUST
**Phase:** V1

---

## US-ORD-005: Order State Machine

**As a** system,
**I want** all order status transitions to go through the state machine with validation,
**So that** illegal transitions are prevented and side effects always fire.

**SRS Requirements:** ORD-008, ORD-012, ORD-013, ORD-014
**Priority:** MUST
**Phase:** V1

---

## US-ORD-006: Order Generates Deliveries

**As a** system,
**I want** confirmed orders to automatically generate delivery records,
**So that** the fulfilment pipeline is triggered without manual intervention.

**SRS Requirements:** ORD-015
**Priority:** MUST
**Phase:** V1

---

## US-ORD-007: Commercial Snapshot Immutability

**As a** system,
**I want** order_items to contain frozen commercial snapshots (purpose, quality, prices) at creation time,
**So that** historical orders are self-contained and unaffected by catalog/pricing changes.

**SRS Requirements:** ORD-016, ORD-017
**Priority:** MUST
**Phase:** V1

---

## US-ORD-008: Admin Order Management

**As an** admin (P4/P5),
**I want to** view all orders, filter by status/date/customer, and cancel orders with a mandatory reason,
**So that** I can manage operations and handle exceptions.

**SRS Requirements:** ORD-018, ORD-019, ORD-020
**Priority:** MUST
**Phase:** V1

---

## US-ORD-009: Customer Reorders

**As a** customer (P1),
**I want to** re-order from a previous order (pre-filled variant, quantity, address),
**So that** I can quickly place repeat orders.

**SRS Requirements:** ORD-021
**Priority:** SHOULD
**Phase:** V1

---

## US-ORD-010: Scheduled Orders

**As a** customer (P1),
**I want to** place an order with a preferred delivery time window,
**So that** I receive water at a convenient time.

**SRS Requirements:** ORD-022
**Priority:** SHOULD
**Phase:** V1
