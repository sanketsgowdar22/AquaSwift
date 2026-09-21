# Deliveries Module — Acceptance Criteria

## AC-DEL-001: Auto-Offer Sends Push to Driver

**User Story:** US-DEL-001
**Given** a delivery in PENDING_ASSIGNMENT and an available driver with sufficient vehicle capacity,
**When** auto-offer runs,
**Then** the delivery transitions to OFFERED, a delivery_assignment is created, and a push notification is sent to the driver.

---

## AC-DEL-002: Driver Accepts Offer

**User Story:** US-DEL-002
**Given** a delivery OFFERED to a driver,
**When** the driver POST /deliveries/{id}/respond with `{ "accept": true }`,
**Then** the delivery transitions to ASSIGNED, inventory is allocated, and the customer is notified.

---

## AC-DEL-003: Driver Rejects Offer

**User Story:** US-DEL-002
**Given** a delivery OFFERED to a driver,
**When** the driver POST /deliveries/{id}/respond with `{ "accept": false, "reason": "Too far" }`,
**Then** the delivery transitions to REASSIGNING, rejection is recorded, and the next driver is auto-offered.

---

## AC-DEL-004: Offer Timeout Triggers Re-Offer

**User Story:** US-DEL-002
**Given** a delivery OFFERED to a driver and the timeout has elapsed,
**When** the timeout Celery task fires,
**Then** the delivery transitions to REASSIGNING, timeout is recorded, and the next driver is offered.

---

## AC-DEL-005: Max Attempts Exhausted Alerts Ops

**User Story:** US-DEL-002
**Given** a delivery has been offered to the maximum number of drivers (all rejected/timed out),
**When** the last attempt fails,
**Then** the delivery returns to PENDING_ASSIGNMENT and an ops alert is generated.

---

## AC-DEL-006: Driver Starts Trip

**User Story:** US-DEL-003
**Given** a delivery in ASSIGNED status,
**When** the driver POST /deliveries/{id}/start,
**Then** the delivery transitions to STARTED, an event is logged, and the customer is notified "driver en route".

---

## AC-DEL-007: Driver Arrives

**User Story:** US-DEL-003
**Given** a delivery in STARTED status,
**When** the driver POST /deliveries/{id}/arrive,
**Then** the delivery transitions to ARRIVED, an event is logged, and the customer is notified "driver arrived".

---

## AC-DEL-008: Complete Delivery with OTP

**User Story:** US-DEL-004
**Given** a delivery in ARRIVED status,
**When** the driver POST /deliveries/{id}/complete with correct OTP and full quantity,
**Then** the delivery transitions to DELIVERED, a DELIVERED inventory txn is written, proof is stored, and the customer is notified.

---

## AC-DEL-009: OTP Mismatch Rejected

**User Story:** US-DEL-004
**Given** a delivery in ARRIVED status,
**When** the driver submits an incorrect OTP,
**Then** the system returns 400 with code `INVALID_OTP` and the delivery remains in ARRIVED.

---

## AC-DEL-010: Partial Delivery Creates Remainder

**User Story:** US-DEL-005
**Given** a delivery allocated 5,000L and driver delivers 3,000L,
**When** the driver completes with quantity 3,000L,
**Then** the original delivery transitions to PARTIALLY_DELIVERED with 3,000L, a new delivery for 2,000L is created in PENDING_ASSIGNMENT, and inventory txns are written correctly.

---

## AC-DEL-011: Failed Delivery Releases Inventory

**User Story:** US-DEL-006
**Given** a delivery in STARTED status and the driver reports a vehicle breakdown,
**When** the delivery transitions to FAILED,
**Then** allocated inventory is released, a replacement delivery is created, ops is alerted, and the customer is notified.

---

## AC-DEL-012: Admin Manual Assignment

**User Story:** US-DEL-008
**Given** a delivery in PENDING_ASSIGNMENT and an admin with `deliveries:assign`,
**When** the admin POST /admin/deliveries/{id}/assign with driver_id,
**Then** the delivery transitions to ASSIGNED (skipping OFFERED), the driver is notified, and assignment is recorded.

---

## AC-DEL-013: Admin Reassignment

**User Story:** US-DEL-008
**Given** a delivery in ASSIGNED status,
**When** the admin POST /admin/deliveries/{id}/reassign with a new driver_id,
**Then** the previous assignment is cancelled, a new assignment is created, and both drivers are notified.

---

## AC-DEL-014: Delivery Events Logged

**User Story:** US-DEL-009
**Given** any delivery status change,
**When** the transition completes,
**Then** a delivery_event row is written with event_type, actor_id, metadata, and timestamp.

---

## AC-DEL-015: Parent Order Updates on Delivery Completion

**User Story:** US-DEL-003
**Given** an order with 2 deliveries,
**When** the first delivery completes,
**Then** the parent order transitions to PARTIALLY_DELIVERED; when the second completes, the order transitions to DELIVERED.

---

## AC-DEL-016: Delivery Proof Photo Stored

**User Story:** US-DEL-004
**Given** a driver submits a proof photo during completion,
**When** the delivery completes,
**Then** the photo is uploaded to S3 and the URL is stored in delivery.proof_photo_url.
