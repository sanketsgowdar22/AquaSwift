# Catalog Module — User Stories

## US-CAT-001: Browse Water Catalog

**As a** customer (P1),
**I want to** browse available water purposes, quality types, delivery methods, and variants,
**So that** I can find and select the right water product for my needs.

**SRS Requirements:** CAT-009
**Priority:** MUST
**Phase:** V1

---

## US-CAT-002: Admin Manages Water Purposes

**As a** super admin (P5),
**I want to** create, update, and deactivate water purposes via admin endpoints,
**So that** the catalog can expand without code changes.

**SRS Requirements:** CAT-001, CAT-010
**Priority:** MUST
**Phase:** V1

---

## US-CAT-003: Admin Manages Quality Types

**As a** super admin (P5),
**I want to** create, update, and deactivate water quality types,
**So that** new quality classifications can be added dynamically.

**SRS Requirements:** CAT-002, CAT-010
**Priority:** MUST
**Phase:** V1

---

## US-CAT-004: Admin Manages Delivery Methods

**As a** super admin (P5),
**I want to** create, update, and deactivate delivery methods,
**So that** new delivery options (e.g., new tanker types) can be added dynamically.

**SRS Requirements:** CAT-003, CAT-010
**Priority:** MUST
**Phase:** V1

---

## US-CAT-005: Admin Manages Purpose-Quality Links

**As a** super admin (P5),
**I want to** link and unlink quality types to/from purposes,
**So that** I control which quality options appear for each water purpose.

**SRS Requirements:** CAT-004, CAT-012
**Priority:** MUST
**Phase:** V1

---

## US-CAT-006: Admin Manages Water Variants

**As a** super admin (P5),
**I want to** create and manage water variants (purpose × quality × delivery method with quantity ranges),
**So that** customers can order specific water product configurations.

**SRS Requirements:** CAT-005, CAT-006, CAT-010, CAT-012
**Priority:** MUST
**Phase:** V1

---

## US-CAT-007: Catalog Soft-Delete Protection

**As a** system,
**I want** catalog records referenced by historical orders to be soft-deleted only (deactivation),
**So that** order history and commercial snapshots remain intact.

**SRS Requirements:** CAT-007, CAT-008
**Priority:** MUST
**Phase:** V1

---

## US-CAT-008: Catalog Caching

**As a** system operator,
**I want** catalog data to be cached in Redis with short TTL and write-through invalidation,
**So that** catalog browsing is fast while changes are visible within 60 seconds.

**SRS Requirements:** CAT-011
**Priority:** MUST
**Phase:** V1
