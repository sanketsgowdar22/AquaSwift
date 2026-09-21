# Payments Module — Tasks

## T-PAY-001: Create Payment Models

**User Story:** US-PAY-001, US-PAY-004
**Type:** Backend
**Description:** Create `payments` and `payment_transactions` models per DATABASE_ARCHITECTURE.md.
**Files:** `backend/app/payments/models.py`
**Dependencies:** T-ORD-001
**Estimated Effort:** S

---

## T-PAY-002: Create Payment Schemas

**User Story:** All payment stories
**Type:** Backend
**Description:** Create schemas: PaymentResponse, PaymentDetailResponse, WebhookPayload, PaymentRetryResponse.
**Files:** `backend/app/payments/schemas.py`
**Dependencies:** T-PAY-001
**Estimated Effort:** S

---

## T-PAY-003: Implement Payment Intent Service

**User Story:** US-PAY-001
**Type:** Backend
**Description:** Implement `create_payment_intent(order)` — call PaymentGatewayAdapter.create_order() with amount in paise, store payment record with INITIATED status, return gateway order details for client.
**Files:** `backend/app/payments/service.py`
**Dependencies:** T-PAY-001, Razorpay adapter
**Estimated Effort:** M

---

## T-PAY-004: Implement Webhook Handler

**User Story:** US-PAY-002
**Type:** Backend
**Description:** Implement POST /payments/webhook: (1) verify HMAC signature, (2) check idempotency (event_id processed?), (3) parse event type, (4) on payment.captured: update payment status → SUCCESS, transition order PENDING_PAYMENT → CONFIRMED, (5) store raw payload, (6) return 200.
**Files:** `backend/app/payments/service.py`, `backend/app/payments/router.py`
**Dependencies:** T-PAY-003, T-ORD-004 (order state machine), Razorpay adapter
**Estimated Effort:** L

---

## T-PAY-005: Implement Payment Retry

**User Story:** US-PAY-003
**Type:** Backend
**Description:** Implement POST /payments/{id}/retry — create a new Razorpay order for the same amount, return new payment details to client. Original payment marked as FAILED.
**Files:** `backend/app/payments/service.py`
**Dependencies:** T-PAY-003
**Estimated Effort:** S

---

## T-PAY-006: Create Payment API Routes

**User Story:** All payment stories
**Type:** Backend
**Description:** Public: POST /payments/webhook. Customer: POST /payments/{id}/retry. Admin: GET /admin/payments, GET /admin/payments/{id}.
**Files:** `backend/app/payments/router.py`
**Dependencies:** T-PAY-003 through T-PAY-005
**Estimated Effort:** S

---

## T-PAY-007: Write Payment Tests

**User Story:** All payment stories
**Type:** Backend
**Description:** Test: intent creation, webhook verification (valid/invalid signature), idempotent webhook, payment.captured triggers order confirmation, payment.failed handling, retry flow, admin view.
**Files:** `backend/app/payments/tests/`
**Dependencies:** T-PAY-006
**Estimated Effort:** L
