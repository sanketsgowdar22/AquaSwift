# Refunds Module — User Stories

## US-RFD-001: Auto-Refund on Cancellation

**As a** system,
**I want to** automatically initiate a refund when a paid order is cancelled,
**So that** customers receive their money back without manual intervention.

**SRS Requirements:** RFD-001, RFD-002
**Priority:** MUST
**Phase:** V1

---

## US-RFD-002: Admin Manual Refund

**As an** admin (P4/P5),
**I want to** manually initiate a refund with a mandatory reason,
**So that** I can handle edge cases and customer complaints.

**SRS Requirements:** RFD-003, RFD-004
**Priority:** MUST
**Phase:** V1

---

## US-RFD-003: Refund Status Tracking

**As a** system,
**I want** refund status to be updated via gateway webhook (refund.processed/refund.failed),
**So that** the customer and admin can track refund progress.

**SRS Requirements:** RFD-005, RFD-006
**Priority:** MUST
**Phase:** V1
