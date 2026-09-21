# Coupons Module — Acceptance Criteria

## AC-CPN-001: Valid Coupon Returns Discount

**User Story:** US-CPN-001
**Given** an active coupon "FIRST50" (50% off, max ₹500),
**When** the customer validates it with an order amount of ₹2,000,
**Then** the system returns discount_amount = 500.00 (50% of 2000 capped at 500).

---

## AC-CPN-002: Expired Coupon Rejected

**User Story:** US-CPN-001
**Given** a coupon with valid_to in the past,
**When** the customer validates it,
**Then** the system returns 400 with code `COUPON_EXPIRED`.

---

## AC-CPN-003: Total Usage Limit Enforced

**User Story:** US-CPN-003
**Given** a coupon with total_usage_limit=100 and current_usage_count=100,
**When** a customer validates it,
**Then** the system returns 400 with code `COUPON_USAGE_EXHAUSTED`.

---

## AC-CPN-004: Per-Customer Limit Enforced

**User Story:** US-CPN-003
**Given** a coupon with per_customer_limit=1 and the customer has already used it,
**When** the customer validates it again,
**Then** the system returns 400 with code `COUPON_ALREADY_USED`.

---

## AC-CPN-005: Minimum Order Amount Enforced

**User Story:** US-CPN-001
**Given** a coupon with min_order_amount=₹1,000,
**When** the customer's order total is ₹800,
**Then** the system returns 400 with code `MIN_ORDER_NOT_MET`.

---

## AC-CPN-006: Fixed Discount Applied

**User Story:** US-CPN-002
**Given** a FIXED_AMOUNT coupon with discount_value=200,
**When** applied to an order of ₹1,500,
**Then** the discount is ₹200 and final_total reflects the reduction.

---

## AC-CPN-007: Usage Count Incremented on Order

**User Story:** US-CPN-003
**Given** a coupon with current_usage_count=5,
**When** an order is created using the coupon,
**Then** current_usage_count becomes 6.

---

## AC-CPN-008: Usage Count Decremented on Cancellation

**User Story:** US-CPN-003
**Given** an order was created with a coupon,
**When** the order is cancelled,
**Then** current_usage_count is decremented by 1.
