# Recurring Orders Module — Acceptance Criteria

## AC-REC-001: Recurring Order Created

**User Story:** US-REC-001
**Given** a customer with a valid variant, address, and quantity, **When** they create a recurring order with frequency WEEKLY and schedule_days [1,4], **Then** the recurring order is created with status ACTIVE and next_instance_date computed.

---

## AC-REC-002: Instance Generated on Schedule

**User Story:** US-REC-002
**Given** an ACTIVE recurring order with next_instance_date = today, **When** the daily Celery task runs, **Then** a recurring_order_instance is created and linked to a new order, and next_instance_date is updated.

---

## AC-REC-003: Paused Order Skips Generation

**User Story:** US-REC-003
**Given** a PAUSED recurring order, **When** the daily Celery task runs, **Then** no instance is generated for this recurring order.

---

## AC-REC-004: Customer Cancels Recurring Order

**User Story:** US-REC-003
**Given** an ACTIVE recurring order, **When** the customer cancels it, **Then** status → CANCELLED and no future instances are generated.
