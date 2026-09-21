# Refunds Module — Acceptance Criteria

## AC-RFD-001: Auto-Refund on Paid Order Cancellation

**User Story:** US-RFD-001
**Given** an order with a SUCCESS payment is cancelled,
**When** the cancellation completes,
**Then** a refund is auto-created, the gateway refund is initiated, and the customer is notified.

---

## AC-RFD-002: No Refund on Unpaid Cancellation

**User Story:** US-RFD-001
**Given** an order cancelled before payment (PENDING_PAYMENT),
**When** the cancellation completes,
**Then** no refund record is created (nothing to refund).

---

## AC-RFD-003: Admin Manual Refund Requires Reason

**User Story:** US-RFD-002
**Given** an admin initiates a refund,
**When** no reason is provided,
**Then** the system returns 400 with code `REASON_REQUIRED`.

---

## AC-RFD-004: Refund Webhook Updates Status

**User Story:** US-RFD-003
**Given** a refund is PROCESSING,
**When** refund.processed webhook arrives,
**Then** refund status → COMPLETED, order → REFUNDED, customer notified.

---

## AC-RFD-005: Failed Refund Alerts Ops

**User Story:** US-RFD-003
**Given** a refund is PROCESSING,
**When** refund.failed webhook arrives,
**Then** refund status → FAILED, ops team is alerted, and manual retry is available.
