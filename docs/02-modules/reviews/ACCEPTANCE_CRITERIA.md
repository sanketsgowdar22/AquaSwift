# Reviews Module — Acceptance Criteria

## AC-REV-001: Review Submitted for Completed Order

**User Story:** US-REV-001
**Given** an order in DELIVERED status,
**When** the customer POST /orders/{id}/reviews with rating 4 and comment,
**Then** the review is created and linked to the order.

---

## AC-REV-002: Cannot Review Non-Delivered Order

**User Story:** US-REV-001
**Given** an order not yet in DELIVERED status,
**When** the customer attempts to submit a review,
**Then** the system returns 400 with code `ORDER_NOT_DELIVERED`.

---

## AC-REV-003: Duplicate Review Rejected

**User Story:** US-REV-001
**Given** a customer has already reviewed an order,
**When** they attempt to submit another review for the same order,
**Then** the system returns 409 with code `REVIEW_ALREADY_EXISTS`.

---

## AC-REV-004: Rating Validated 1-5

**User Story:** US-REV-001
**Given** a review submission,
**When** the rating is outside 1-5,
**Then** the system returns 422 validation error.
