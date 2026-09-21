# Refunds Module — Tasks

## T-RFD-001: Create Refund Model & Schemas

**User Story:** All refund stories
**Type:** Backend
**Description:** Create `refunds` model and Pydantic schemas.
**Files:** `backend/app/refunds/models.py`, `backend/app/refunds/schemas.py`
**Dependencies:** T-PAY-001
**Estimated Effort:** S

---

## T-RFD-002: Implement Auto-Refund on Cancellation

**User Story:** US-RFD-001
**Type:** Backend
**Description:** When order transitions to CANCELLED (and payment was SUCCESS), auto-create refund record, call PaymentGatewayAdapter.refund(), set status PROCESSING.
**Files:** `backend/app/refunds/service.py`
**Dependencies:** T-RFD-001, T-ORD-005, Razorpay adapter
**Estimated Effort:** M

---

## T-RFD-003: Implement Manual Refund

**User Story:** US-RFD-002
**Type:** Backend
**Description:** Admin POST /admin/refunds with payment_id, amount, reason (mandatory). Create refund, call gateway, audit log.
**Files:** `backend/app/refunds/service.py`
**Dependencies:** T-RFD-001
**Estimated Effort:** S

---

## T-RFD-004: Implement Refund Webhook Processing

**User Story:** US-RFD-003
**Type:** Backend
**Description:** Handle refund.processed and refund.failed webhook events. Update refund status, transition order to REFUNDED if applicable, notify customer.
**Files:** `backend/app/refunds/service.py`, `backend/app/payments/service.py`
**Dependencies:** T-PAY-004
**Estimated Effort:** M

---

## T-RFD-005: Create Refund API Routes & Tests

**User Story:** All refund stories
**Type:** Backend
**Description:** Admin: GET /admin/refunds, GET /admin/refunds/{id}, POST /admin/refunds. Tests for auto-refund, manual refund, webhook processing.
**Files:** `backend/app/refunds/router.py`, `backend/app/refunds/tests/`
**Dependencies:** T-RFD-002 through T-RFD-004
**Estimated Effort:** M
