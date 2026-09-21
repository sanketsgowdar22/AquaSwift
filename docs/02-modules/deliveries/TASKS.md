# Deliveries Module — Tasks

## T-DEL-001: Create Delivery Models

**User Story:** All delivery stories
**Type:** Backend
**Description:** Create `deliveries`, `delivery_assignments`, and `delivery_events` models per DATABASE_ARCHITECTURE.md.
**Files:** `backend/app/deliveries/models.py`
**Dependencies:** T-ORD-001, T-SRC-001, T-DRV-001, T-VEH-001
**Estimated Effort:** M

---

## T-DEL-002: Create Delivery Schemas

**User Story:** All delivery stories
**Type:** Backend
**Description:** Create schemas: DeliveryResponse, DeliveryDetailResponse, RespondRequest (accept/reject), StartRequest, ArriveRequest, CompleteRequest (OTP, quantity, photo), AssignRequest.
**Files:** `backend/app/deliveries/schemas.py`
**Dependencies:** T-DEL-001
**Estimated Effort:** M

---

## T-DEL-003: Implement Delivery State Machine

**User Story:** US-DEL-001 through US-DEL-006
**Type:** Backend
**Description:** Implement `transition_delivery(db, delivery, new_status, actor, ...)` with ALLOWED_TRANSITIONS map, validation, event writing, and side-effect dispatch. Include OTP validation for DELIVERED, quantity validation for PARTIALLY_DELIVERED.
**Files:** `backend/app/deliveries/state_machine.py`
**Dependencies:** T-DEL-001
**Estimated Effort:** L

---

## T-DEL-004: Implement Auto-Offer Service

**User Story:** US-DEL-001
**Type:** Backend
**Description:** Implement `auto_offer_delivery(delivery)` — find eligible driver (AVAILABLE status, vehicle capacity >= delivery quantity, optional proximity), create delivery_assignment in OFFERED status, send push notification, start offer timeout timer (configurable, e.g., 120s via Celery countdown).
**Files:** `backend/app/deliveries/service.py`
**Dependencies:** T-DEL-003, T-DRV-001, FCM adapter
**Estimated Effort:** L

---

## T-DEL-005: Implement Offer Timeout Handler

**User Story:** US-DEL-002
**Type:** Backend
**Description:** Celery task triggered after offer timeout: check if delivery still in OFFERED status, transition to REASSIGNING, record timeout in delivery_assignments, call auto_offer with next driver. After max attempts, transition to PENDING_ASSIGNMENT and alert ops.
**Files:** `backend/app/deliveries/tasks.py`
**Dependencies:** T-DEL-004
**Estimated Effort:** M

---

## T-DEL-006: Implement Driver Response Handler

**User Story:** US-DEL-002
**Type:** Backend
**Description:** Implement `respond_to_offer(delivery_id, driver_id, accept, rejection_reason?)`. If accept: transition OFFERED → ASSIGNED, allocate inventory, notify customer. If reject: transition OFFERED → REASSIGNING, record reason, re-offer.
**Files:** `backend/app/deliveries/service.py`
**Dependencies:** T-DEL-003, T-INV-005
**Estimated Effort:** M

---

## T-DEL-007: Implement Delivery Execution Endpoints

**User Story:** US-DEL-003
**Type:** Backend
**Description:** Implement driver actions: start(delivery_id) → STARTED + event + customer notification, arrive(delivery_id) → ARRIVED + event + customer notification. Update parent order status if applicable.
**Files:** `backend/app/deliveries/service.py`
**Dependencies:** T-DEL-003
**Estimated Effort:** M

---

## T-DEL-008: Implement Delivery Completion

**User Story:** US-DEL-004
**Type:** Backend
**Description:** Implement `complete_delivery(delivery_id, otp, quantity, gps, photo?)`. Validate OTP, compare quantity vs allocated. If full quantity → DELIVERED + DELIVERED inventory txn. Upload proof photo to S3. Check if all deliveries done → transition parent order.
**Files:** `backend/app/deliveries/service.py`
**Dependencies:** T-DEL-003, T-INV-007, S3 adapter
**Estimated Effort:** L

---

## T-DEL-009: Implement Partial Delivery

**User Story:** US-DEL-005
**Type:** Backend
**Description:** If delivered_quantity < allocated_quantity: transition to PARTIALLY_DELIVERED, create DELIVERED inventory txn for actual quantity, create new delivery for remainder quantity in PENDING_ASSIGNMENT, notify customer.
**Files:** `backend/app/deliveries/service.py`
**Dependencies:** T-DEL-008
**Estimated Effort:** M

---

## T-DEL-010: Implement Failed Delivery

**User Story:** US-DEL-006
**Type:** Backend
**Description:** Transition to FAILED, release allocated inventory, write event with failure reason, create replacement delivery (PENDING_ASSIGNMENT), alert ops team.
**Files:** `backend/app/deliveries/service.py`
**Dependencies:** T-DEL-003, T-INV-006
**Estimated Effort:** M

---

## T-DEL-011: Implement Admin Assign/Reassign

**User Story:** US-DEL-008
**Type:** Backend
**Description:** Admin manual assignment: POST /admin/deliveries/{id}/assign, POST /admin/deliveries/{id}/reassign. Create assignment record, transition delivery, notify driver.
**Files:** `backend/app/deliveries/service.py`
**Dependencies:** T-DEL-003
**Estimated Effort:** S

---

## T-DEL-012: Create Delivery API Routes

**User Story:** All delivery stories
**Type:** Backend
**Description:** Driver: GET /deliveries/active, POST respond/start/arrive/complete. Admin: GET list/detail, POST assign/reassign.
**Files:** `backend/app/deliveries/router.py`
**Dependencies:** T-DEL-004 through T-DEL-011
**Estimated Effort:** M

---

## T-DEL-013: Write Delivery Tests

**User Story:** All delivery stories
**Type:** Backend
**Description:** Test: auto-offer, accept/reject/timeout loop, max attempts fallback, start/arrive/complete flow, OTP verification, partial delivery remainder creation, failed delivery inventory release, admin assign/reassign, parent order status updates.
**Files:** `backend/app/deliveries/tests/`
**Dependencies:** T-DEL-012
**Estimated Effort:** XL
