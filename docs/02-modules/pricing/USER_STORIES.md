# Pricing Module — User Stories

## US-PRC-001: Server-Side Price Quoting

**As a** customer (P1),
**I want to** receive an accurate price quote before placing my order,
**So that** I know exactly what I'll pay before committing.

**SRS Requirements:** PRC-001, PRC-004
**Priority:** MUST
**Phase:** V1

---

## US-PRC-002: Pricing Rule Versioning

**As a** system,
**I want** every pricing rule to be versioned and the version ID stored in the commercial snapshot,
**So that** we can trace which pricing rule produced any historical order's price.

**SRS Requirements:** PRC-002
**Priority:** MUST
**Phase:** V1

---

## US-PRC-003: Tiered Pricing Support

**As a** super admin (P5),
**I want to** configure tiered pricing (price per litre decreases at higher volumes),
**So that** bulk customers get volume discounts.

**SRS Requirements:** PRC-003
**Priority:** MUST
**Phase:** V1

---

## US-PRC-004: Stale Cart Re-Quote

**As a** system,
**I want** the final price at order creation to be compared with the quoted price and the customer re-confirmed if prices differ,
**So that** customers are never silently overcharged.

**SRS Requirements:** PRC-004
**Priority:** MUST
**Phase:** V1

---

## US-PRC-005: Admin Manages Pricing Rules

**As a** super admin (P5),
**I want to** create, update, and deactivate pricing rules with date-based activation,
**So that** prices can be scheduled and adjusted without code deployments.

**SRS Requirements:** PRC-005, PRC-006, PRC-007
**Priority:** MUST
**Phase:** V1

---

## US-PRC-006: Delivery Pricing

**As a** system,
**I want** delivery charges to be computed based on the delivery method and distance,
**So that** delivery costs are fair and transparent.

**SRS Requirements:** PRC-008, PRC-009
**Priority:** MUST
**Phase:** V1

---

## US-PRC-007: Business/Bulk Pricing

**As a** system,
**I want** pricing rules to optionally target customer_type (INDIVIDUAL/BUSINESS),
**So that** B2B customers can receive negotiated rates.

**SRS Requirements:** PRC-010, PRC-011
**Priority:** MUST
**Phase:** V1 (schema) / Phase 2 (UI)
