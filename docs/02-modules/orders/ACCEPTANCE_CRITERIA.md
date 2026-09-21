# Orders Module — Acceptance Criteria

## AC-ORD-001: Order Creation with Payment Intent

**User Story:** US-ORD-001
**Given** a customer with a valid address and available inventory,
**When** they POST /orders with variant_id, quantity, address_id,
**Then** the system creates an order in PENDING_PAYMENT, reserves inventory, creates a Razorpay payment intent, and returns order + payment details.

---

## AC-ORD-002: Order Item Contains Frozen Snapshot

**User Story:** US-ORD-007
**Given** an order is created,
**When** the order_items are inspected,
**Then** each item contains purpose_name, quality_name, delivery_method_name, unit_price, water_total, delivery_charge, discount_total, tax_total, final_total, and pricing_rule_version_id.

---

## AC-ORD-003: Snapshot Unchanged After Catalog Update

**User Story:** US-ORD-007
**Given** an order was created with purpose_name "Drinking" at ₹0.50/L,
**When** the admin changes the purpose name or price,
**Then** the existing order_items still show "Drinking" at ₹0.50/L.

---

## AC-ORD-004: Idempotent Order Creation

**User Story:** US-ORD-002
**Given** an order was already created with Idempotency-Key "abc-123",
**When** the same request with the same key is sent again,
**Then** the system returns the original order with HTTP 200 (not a duplicate 201).

---

## AC-ORD-005: Customer Cancel Before OUT_FOR_DELIVERY

**User Story:** US-ORD-004
**Given** an order in CONFIRMED status,
**When** the customer POST /orders/{id}/cancel,
**Then** the order transitions to CANCELLED, inventory is released, and refund is initiated.

---

## AC-ORD-006: Customer Cannot Cancel After OUT_FOR_DELIVERY

**User Story:** US-ORD-004
**Given** an order in OUT_FOR_DELIVERY status,
**When** the customer attempts to cancel,
**Then** the system returns 400 with code `CANCELLATION_NOT_ALLOWED`.

---

## AC-ORD-007: Admin Cancel Requires Reason

**User Story:** US-ORD-008
**Given** an admin cancels an order,
**When** no reason is provided,
**Then** the system returns 400 with code `REASON_REQUIRED`.

---

## AC-ORD-008: Invalid State Transition Rejected

**User Story:** US-ORD-005
**Given** an order in DELIVERED status,
**When** a transition to CONFIRMED is attempted,
**Then** the system raises IllegalTransitionError and the order status is unchanged.

---

## AC-ORD-009: Status History Written on Transition

**User Story:** US-ORD-005
**Given** an order transitions from CONFIRMED to PROCESSING,
**When** the transition completes,
**Then** an order_status_history row is written with from_status, to_status, actor_id, and timestamp.

---

## AC-ORD-010: Order Generates Delivery Records

**User Story:** US-ORD-006
**Given** an order transitions to PROCESSING,
**When** the delivery generation runs,
**Then** one or more delivery records are created in PENDING_ASSIGNMENT status with the correct quantity split.

---

## AC-ORD-011: Multi-Delivery Split for Large Orders

**User Story:** US-ORD-006
**Given** an order for 20,000L but max vehicle capacity is 12,000L,
**When** deliveries are generated,
**Then** two deliveries are created: 12,000L and 8,000L.

---

## AC-ORD-012: Reorder Pre-Fills Correctly

**User Story:** US-ORD-009
**Given** a completed order for 5,000L Drinking RO+UV to address A,
**When** the customer POST /orders/{id}/reorder,
**Then** a new quote is returned with the same variant, quantity, and address but current pricing.

---

## AC-ORD-013: Scheduled Order Stores Window

**User Story:** US-ORD-010
**Given** a customer places an order with scheduled_window_start and scheduled_window_end,
**When** the order is created,
**Then** the windows are stored and the delivery is scheduled for that window.

---

## AC-ORD-014: Order Transitions to DELIVERED When All Deliveries Complete

**User Story:** US-ORD-005
**Given** an order with 2 deliveries,
**When** both deliveries reach DELIVERED status,
**Then** the order automatically transitions to DELIVERED.

---

## AC-ORD-015: Customer Only Sees Own Orders

**User Story:** US-ORD-003
**Given** two customers with separate orders,
**When** customer A GET /orders,
**Then** only customer A's orders are returned.
