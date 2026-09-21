# Pricing Module — Acceptance Criteria

## AC-PRC-001: Quote Returns Full Breakdown

**User Story:** US-PRC-001
**Given** a valid variant, quantity, and address,
**When** the customer POST /orders/quote,
**Then** the response includes water_total, delivery_charge, discount, tax, and final_total.

---

## AC-PRC-002: PER_LITRE Pricing Computes Correctly

**User Story:** US-PRC-001
**Given** a pricing rule with pricing_model=PER_LITRE and base_price=0.50,
**When** the customer quotes 5,000 litres,
**Then** water_total = 2,500.00.

---

## AC-PRC-003: TIERED Pricing Applies Correct Tiers

**User Story:** US-PRC-003
**Given** a tiered pricing rule: [{0-1000: ₹0.60}, {1001-5000: ₹0.50}, {5001+: ₹0.40}],
**When** the customer quotes 3,000 litres,
**Then** water_total = (1000 × 0.60) + (2000 × 0.50) = 600 + 1000 = 1,600.00.

---

## AC-PRC-004: Most Specific Rule Matches

**User Story:** US-PRC-005
**Given** a global rule (purpose=null, quality=null) and a specific rule (purpose=Drinking, quality=RO+UV),
**When** pricing for Drinking RO+UV water,
**Then** the specific rule is used, not the global fallback.

---

## AC-PRC-005: Stale Price Triggers Re-Confirmation

**User Story:** US-PRC-004
**Given** the customer received a quote of ₹2,500 but the pricing rule changed since,
**When** the customer submits the order,
**Then** the system returns 409 with code `PRICE_CHANGED` and the new quote.

---

## AC-PRC-006: Delivery Charge Based on Distance

**User Story:** US-PRC-006
**Given** a distance-band delivery pricing rule: [{0-5km: ₹100}, {5-15km: ₹200}, {15+: ₹350}],
**When** the delivery distance is 12km,
**Then** delivery_charge = 200.00.

---

## AC-PRC-007: Pricing Rule Version Increments on Update

**User Story:** US-PRC-002
**Given** a pricing rule at version 3,
**When** the admin updates the base_price,
**Then** the version becomes 4, the old rule is preserved for audit, and cache is invalidated.

---

## AC-PRC-008: Commercial Snapshot Stores Rule Version

**User Story:** US-PRC-002
**Given** a pricing rule at version 4,
**When** an order is created,
**Then** the order_item's pricing_rule_version_id references version 4 and pricing_snapshot contains the full computation.

---

## AC-PRC-009: Customer-Type Pricing Differentiation

**User Story:** US-PRC-007
**Given** separate pricing rules for INDIVIDUAL (₹0.60/L) and BUSINESS (₹0.45/L),
**When** a business customer quotes the same product,
**Then** the BUSINESS rate is applied.

---

## AC-PRC-010: No Matching Rule Returns Error

**User Story:** US-PRC-001
**Given** no active pricing rule matches the requested variant,
**When** a quote is requested,
**Then** the system returns 400 with code `NO_PRICING_RULE`.
