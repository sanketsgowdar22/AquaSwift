# Payments Module — User Stories

## US-PAY-001: Payment Intent Creation

**As a** system,
**I want to** create a Razorpay payment order when a customer order is created,
**So that** the customer can complete payment via the gateway-hosted checkout.

**SRS Requirements:** PAY-001, PAY-002
**Priority:** MUST
**Phase:** V1

---

## US-PAY-002: Webhook Payment Verification

**As a** system,
**I want to** receive and verify Razorpay webhook events as the sole payment confirmation path,
**So that** payment status is updated securely and cannot be spoofed.

**SRS Requirements:** PAY-003, PAY-004, PAY-005
**Priority:** MUST
**Phase:** V1

---

## US-PAY-003: Payment Retry

**As a** customer (P1),
**I want to** retry a failed payment for my order,
**So that** I don't have to place a new order if my first payment attempt fails.

**SRS Requirements:** PAY-006
**Priority:** MUST
**Phase:** V1

---

## US-PAY-004: Gateway Payload Storage

**As a** system,
**I want** every gateway event to be stored as raw JSONB in payment_transactions,
**So that** we have a complete financial audit trail.

**SRS Requirements:** PAY-007, PAY-008
**Priority:** MUST
**Phase:** V1

---

## US-PAY-005: Admin Views Payment Records

**As an** admin (P4/P5),
**I want to** view payment records with full gateway transaction history,
**So that** I can investigate payment issues and reconcile.

**SRS Requirements:** PAY-009, PAY-010
**Priority:** MUST
**Phase:** V1
