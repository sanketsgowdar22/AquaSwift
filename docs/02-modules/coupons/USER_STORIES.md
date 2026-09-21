# Coupons Module — User Stories

## US-CPN-001: Customer Validates Coupon

**As a** customer (P1),
**I want to** validate a coupon code before placing my order,
**So that** I can see the discount before committing.

**SRS Requirements:** CPN-001, CPN-002
**Priority:** MUST
**Phase:** V1

---

## US-CPN-002: Coupon Applied During Order

**As a** customer (P1),
**I want** my coupon discount to be applied to the order total by PricingService.quote(),
**So that** the final price reflects the discount.

**SRS Requirements:** CPN-003
**Priority:** MUST
**Phase:** V1

---

## US-CPN-003: Coupon Usage Limits

**As a** system,
**I want** coupon usage to be tracked and enforced (total limit and per-customer limit),
**So that** coupons cannot be overused.

**SRS Requirements:** CPN-004
**Priority:** MUST
**Phase:** V1

---

## US-CPN-004: Admin Manages Coupons

**As a** super admin (P5),
**I want to** create, update, and deactivate coupons with configurable rules,
**So that** I can run promotions and control discounting.

**SRS Requirements:** CPN-005, CPN-006
**Priority:** MUST
**Phase:** V1
