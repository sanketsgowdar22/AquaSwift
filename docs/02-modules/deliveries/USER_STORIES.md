# Deliveries Module — User Stories

## US-DEL-001: Auto-Offer Delivery to Drivers

**As a** system,
**I want to** automatically offer new deliveries to eligible available drivers,
**So that** deliveries are dispatched quickly without manual admin intervention.

**SRS Requirements:** DEL-001, DEL-002, DEL-003
**Priority:** MUST
**Phase:** V1

---

## US-DEL-002: Driver Responds to Delivery Offer

**As a** driver (P3),
**I want to** accept or reject delivery offers with an accept/reject/timeout flow,
**So that** I control which deliveries I take.

**SRS Requirements:** DEL-004, DEL-005, DEL-006
**Priority:** MUST
**Phase:** V1

---

## US-DEL-003: Driver Executes Delivery

**As a** driver (P3),
**I want to** start trip, mark arrived, and complete delivery with OTP verification,
**So that** I can track my delivery progress and prove completion.

**SRS Requirements:** DEL-007, DEL-008, DEL-009, DEL-010
**Priority:** MUST
**Phase:** V1

---

## US-DEL-004: Proof of Delivery

**As a** system,
**I want** delivery completion to require OTP verification from the customer and optional GPS/photo proof,
**So that** deliveries are verifiably completed.

**SRS Requirements:** DEL-011, DEL-012, DEL-013
**Priority:** MUST
**Phase:** V1

---

## US-DEL-005: Partial Delivery Handling

**As a** driver (P3),
**I want to** report a partial delivery (less than allocated quantity),
**So that** the remainder is tracked and a follow-up delivery is created.

**SRS Requirements:** DEL-014, DEL-015
**Priority:** MUST
**Phase:** V1

---

## US-DEL-006: Failed Delivery Handling

**As a** system,
**I want** failed deliveries (customer unavailable, vehicle issue) to release inventory and alert ops,
**So that** inventory is not lost and the issue is resolved.

**SRS Requirements:** DEL-016, DEL-017
**Priority:** MUST
**Phase:** V1

---

## US-DEL-007: Customer Tracks Delivery

**As a** customer (P1),
**I want to** see the real-time status of my delivery (assigned, en route, arrived),
**So that** I know when to expect my water.

**SRS Requirements:** DEL-018
**Priority:** MUST
**Phase:** V1

---

## US-DEL-008: Admin Manages Deliveries

**As an** admin (P4/P5),
**I want to** view all deliveries, manually assign/reassign drivers, and handle escalations,
**So that** I can manage the dispatch pipeline and resolve issues.

**SRS Requirements:** DEL-019, DEL-020, DEL-021
**Priority:** MUST
**Phase:** V1

---

## US-DEL-009: Delivery Event Logging

**As a** system,
**I want** every delivery lifecycle event to be logged with timestamp, actor, and metadata,
**So that** we have a complete audit trail for each delivery.

**SRS Requirements:** DEL-022
**Priority:** MUST
**Phase:** V1
