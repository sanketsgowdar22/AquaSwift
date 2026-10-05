# Payments Module — Acceptance Criteria

## AC-PAY-001: Payment Intent Created with Order

**User Story:** US-PAY-001
**Given** a customer places an order,
**When** the order is created,
**Then** a payment record is created with INITIATED status and Razorpay gateway_order_id is returned.

---

## AC-PAY-002: Webhook Confirms Payment

**User Story:** US-PAY-002
**Given** a valid payment.captured webhook from Razorpay,
**When** POST /payments/webhook processes it,
**Then** payment status → SUCCESS, order transitions PENDING_PAYMENT → CONFIRMED, raw payload stored.

---

## AC-PAY-003: Invalid Webhook Signature Rejected

**User Story:** US-PAY-002
**Given** a webhook request with an invalid HMAC signature,
**When** POST /payments/webhook processes it,
**Then** the system returns 400, logs a security alert, and does not update any records.

---

## AC-PAY-004: Duplicate Webhook Idempotent

**User Story:** US-PAY-002
**Given** a webhook event_id has already been processed,
**When** Razorpay retries the same event,
**Then** the system returns 200 without re-processing.

---

## AC-PAY-005: No Card Data Touches Server

**User Story:** US-PAY-001
**Given** the payment flow uses Razorpay's gateway-hosted checkout,
**When** the customer enters card details,
**Then** card data is handled entirely by Razorpay and never reaches the AquaSwift server.

---

## AC-PAY-006: Payment Retry Creates New Intent

**User Story:** US-PAY-003
**Given** a payment with FAILED status,
**When** the customer POST /payments/{id}/retry,
**Then** a new Razorpay order is created and the customer can re-attempt payment.

---

## AC-PAY-007: Admin Views Payment with Transactions

**User Story:** US-PAY-005
**Given** a payment with multiple gateway events,
**When** the admin GET /admin/payments/{id},
**Then** the response includes payment details and all payment_transactions with raw payloads.

---

## AC-PAY-008: Gateway Payload Stored as JSONB

**User Story:** US-PAY-004
**Given** any gateway webhook event,
**When** the webhook is processed,
**Then** the complete raw JSON payload is stored in payment_transactions.raw_payload.
