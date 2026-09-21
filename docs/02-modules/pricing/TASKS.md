# Pricing Module — Tasks

## T-PRC-001: Create Pricing Models

**User Story:** US-PRC-005, US-PRC-006
**Type:** Backend
**Description:** Create `pricing_rules` model (version, purpose_id, quality_id, customer_type, pricing_model, base_price, tiers JSONB, active_from/to, is_active) and `delivery_pricing_rules` model (delivery_method_id, pricing_model, base_price, bands JSONB).
**Files:** `backend/app/pricing/models.py`
**Dependencies:** T-CAT-001
**Estimated Effort:** M

---

## T-PRC-002: Create Pricing Schemas

**User Story:** All pricing stories
**Type:** Backend
**Description:** Create schemas: PricingRuleCreate, PricingRuleUpdate, PricingRuleResponse, DeliveryPricingRuleCreate, QuoteRequest, QuoteResponse.
**Files:** `backend/app/pricing/schemas.py`
**Dependencies:** T-PRC-001
**Estimated Effort:** S

---

## T-PRC-003: Implement PricingService.quote()

**User Story:** US-PRC-001, US-PRC-003, US-PRC-004
**Type:** Backend
**Description:** Implement the single `PricingService.quote(variant_id, quantity_litres, customer_type, address, coupon_code?)` function. Steps: (1) find best-match active pricing rule, (2) compute water_total based on pricing_model (FIXED/PER_LITRE/TIERED), (3) compute delivery_charge from delivery pricing rules + distance, (4) apply coupon discount if valid, (5) compute tax, (6) return full price breakdown. This function is the SOLE pricing authority (RULE-005).
**Files:** `backend/app/pricing/service.py`
**Dependencies:** T-PRC-001, T-CAT-001, T-CPN (coupon validation)
**Estimated Effort:** XL

---

## T-PRC-004: Implement Pricing Rule Matching Logic

**User Story:** US-PRC-005, US-PRC-007
**Type:** Backend
**Description:** Implement rule matching: find the most specific active rule for the given purpose+quality+customer_type+date. Specificity order: exact match > wildcard customer_type > wildcard quality > global fallback.
**Files:** `backend/app/pricing/service.py`
**Dependencies:** T-PRC-001
**Estimated Effort:** M

---

## T-PRC-005: Implement Stale Price Detection

**User Story:** US-PRC-004
**Type:** Backend
**Description:** During order creation, re-run quote() and compare with the client-provided quoted price. If prices differ beyond a tolerance (e.g., ₹1), return 409 with code `PRICE_CHANGED` and the new quote for re-confirmation.
**Files:** `backend/app/pricing/service.py`, `backend/app/orders/service.py`
**Dependencies:** T-PRC-003
**Estimated Effort:** S

---

## T-PRC-006: Implement Pricing Rule Admin CRUD

**User Story:** US-PRC-005
**Type:** Backend
**Description:** Admin CRUD for pricing rules and delivery pricing rules. On update, increment version number. Audit log on all writes. Cache invalidation on write.
**Files:** `backend/app/pricing/service.py`
**Dependencies:** T-PRC-001
**Estimated Effort:** M

---

## T-PRC-007: Create Pricing API Routes

**User Story:** All pricing stories
**Type:** Backend
**Description:** Admin routes: GET/POST/PATCH pricing rules and delivery pricing rules. Quote endpoint: POST /orders/quote (customer-facing, calls PricingService.quote()).
**Files:** `backend/app/pricing/router.py`
**Dependencies:** T-PRC-003, T-PRC-006
**Estimated Effort:** S

---

## T-PRC-008: Write Pricing Tests

**User Story:** All pricing stories
**Type:** Backend
**Description:** Test: FIXED/PER_LITRE/TIERED computation, rule matching specificity, stale price detection, coupon integration, delivery charge computation, version incrementing, edge cases (zero quantity, max quantity).
**Files:** `backend/app/pricing/tests/`
**Dependencies:** T-PRC-007
**Estimated Effort:** L
