# Coupons Module — Tasks

## T-CPN-001: Create Coupon Model

**User Story:** US-CPN-004
**Type:** Backend
**Description:** Create `coupons` model with code, discount_type, discount_value, min_order_amount, max_discount_amount, valid_from/to, total_usage_limit, per_customer_limit, current_usage_count, is_active.
**Files:** `backend/app/coupons/models.py`
**Dependencies:** None
**Estimated Effort:** S

---

## T-CPN-002: Create Coupon Schemas

**User Story:** All coupon stories
**Type:** Backend
**Description:** Create schemas: CouponValidateRequest/Response, CouponCreate, CouponUpdate, CouponResponse.
**Files:** `backend/app/coupons/schemas.py`
**Dependencies:** T-CPN-001
**Estimated Effort:** S

---

## T-CPN-003: Implement Coupon Validation Service

**User Story:** US-CPN-001, US-CPN-003
**Type:** Backend
**Description:** Implement `validate_coupon(code, user_id, order_amount)` — check: (1) code exists and is_active, (2) current date within valid_from/to, (3) total usage < limit, (4) user's usage < per_customer_limit, (5) order_amount >= min_order_amount. Return discount amount.
**Files:** `backend/app/coupons/service.py`
**Dependencies:** T-CPN-001
**Estimated Effort:** M

---

## T-CPN-004: Integrate Coupon with PricingService

**User Story:** US-CPN-002
**Type:** Backend
**Description:** Integrate coupon validation into PricingService.quote(). If coupon_code provided, validate and apply discount. For PERCENTAGE: apply to water_total, cap at max_discount_amount. For FIXED_AMOUNT: subtract from total. Discount cannot make total negative.
**Files:** `backend/app/pricing/service.py`
**Dependencies:** T-CPN-003, T-PRC-003
**Estimated Effort:** S

---

## T-CPN-005: Implement Coupon Usage Tracking

**User Story:** US-CPN-003
**Type:** Backend
**Description:** On order creation, increment current_usage_count. Track per-customer usage via order's coupon_id FK. On order cancellation, decrement usage count.
**Files:** `backend/app/coupons/service.py`
**Dependencies:** T-CPN-003
**Estimated Effort:** S

---

## T-CPN-006: Create Coupon API Routes

**User Story:** All coupon stories
**Type:** Backend
**Description:** Customer: POST /coupons/validate. Admin: GET/POST/PATCH /admin/coupons.
**Files:** `backend/app/coupons/router.py`
**Dependencies:** T-CPN-003
**Estimated Effort:** S

---

## T-CPN-007: Write Coupon Tests

**User Story:** All coupon stories
**Type:** Backend
**Description:** Test: validation (valid, expired, usage exceeded, min order not met), percentage/fixed discount, max_discount_amount cap, usage tracking on order create/cancel.
**Files:** `backend/app/coupons/tests/`
**Dependencies:** T-CPN-006
**Estimated Effort:** M
