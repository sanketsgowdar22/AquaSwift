# Reviews Module — Tasks

## T-REV-001: Create Review Model & Schemas

**User Story:** All review stories
**Type:** Backend
**Description:** Create `reviews` model and Pydantic schemas. Enforce UNIQUE(order_id, customer_id), rating CHECK(1-5).
**Files:** `backend/app/reviews/models.py`, `backend/app/reviews/schemas.py`
**Dependencies:** T-ORD-001, T-DEL-001
**Estimated Effort:** S

---

## T-REV-002: Implement Review Submission Service

**User Story:** US-REV-001
**Type:** Backend
**Description:** Implement POST /orders/{id}/reviews — validate order is DELIVERED and belongs to customer, enforce one review per order. Store rating + comment.
**Files:** `backend/app/reviews/service.py`
**Dependencies:** T-REV-001
**Estimated Effort:** S

---

## T-REV-003: Create Review API Routes & Tests

**User Story:** All review stories
**Type:** Backend
**Description:** Customer: POST /orders/{id}/reviews. Driver: GET /drivers/me/reviews. Admin: GET /admin/reviews. Tests for submission, duplicate rejection, driver view, admin filtering.
**Files:** `backend/app/reviews/router.py`, `backend/app/reviews/tests/`
**Dependencies:** T-REV-002
**Estimated Effort:** M
