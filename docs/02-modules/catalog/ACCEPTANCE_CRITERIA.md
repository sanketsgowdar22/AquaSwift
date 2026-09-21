# Catalog Module — Acceptance Criteria

## AC-CAT-001: Customer Browses Active Purposes

**User Story:** US-CAT-001
**Given** the catalog contains both active and deactivated purposes,
**When** a customer GET /catalog/purposes,
**Then** only active purposes are returned, sorted by display_order.

---

## AC-CAT-002: Qualities Filtered by Purpose

**User Story:** US-CAT-001
**Given** a purpose "Drinking" is linked to "RO+UV" and "Mineral",
**When** a customer GET /catalog/purposes/{drinking_id}/qualities,
**Then** only "RO+UV" and "Mineral" are returned.

---

## AC-CAT-003: Variants Filtered by Parameters

**User Story:** US-CAT-001
**Given** variants exist for different purpose-quality-method combinations,
**When** a customer GET /catalog/variants?purpose_id=X&quality_id=Y,
**Then** only matching active variants with their min/max quantity are returned.

---

## AC-CAT-004: Admin Creates Purpose

**User Story:** US-CAT-002
**Given** an authenticated admin with `catalog:write`,
**When** they POST /admin/catalog/purposes with `{ "name": "Washing", "description": "..." }`,
**Then** the purpose is created, an audit log is written, and the catalog cache is invalidated.

---

## AC-CAT-005: Admin Deactivates Purpose (Soft-Delete)

**User Story:** US-CAT-007
**Given** a purpose is referenced by existing order_items,
**When** the admin PATCHes it with `{ "is_active": false }`,
**Then** it is deactivated (not deleted), hidden from customer reads, but order history remains intact.

---

## AC-CAT-006: Admin Creates Variant with Validation

**User Story:** US-CAT-006
**Given** a valid purpose-quality link exists,
**When** the admin creates a variant with valid min/max quantities,
**Then** the variant is created successfully.

---

## AC-CAT-007: Variant Creation Fails Without Purpose-Quality Link

**User Story:** US-CAT-006
**Given** no purpose-quality link exists for the specified combination,
**When** the admin attempts to create a variant,
**Then** the system returns 400 with code `INVALID_PURPOSE_QUALITY_COMBINATION`.

---

## AC-CAT-008: Variant Quantity Validation

**User Story:** US-CAT-006
**Given** an admin attempts to create a variant,
**When** min_quantity_litres > max_quantity_litres or quantities are negative,
**Then** the system returns 422 with validation error.

---

## AC-CAT-009: Duplicate Variant Rejected

**User Story:** US-CAT-006
**Given** a variant already exists for the same purpose+quality+method combination,
**When** the admin creates another variant with the same combination,
**Then** the system returns 409 with code `VARIANT_ALREADY_EXISTS`.

---

## AC-CAT-010: Cache Serves Catalog Reads

**User Story:** US-CAT-008
**Given** catalog data is cached in Redis,
**When** a customer requests GET /catalog/purposes,
**Then** the response is served from cache (no DB query) until TTL expires.

---

## AC-CAT-011: Cache Invalidated on Write

**User Story:** US-CAT-008
**Given** a cached catalog response exists,
**When** an admin creates/updates/deactivates a catalog entity,
**Then** the relevant cache keys are invalidated and the next read fetches from DB.

---

## AC-CAT-012: Admin Manages Purpose-Quality Links

**User Story:** US-CAT-005
**Given** a purpose and quality type both exist,
**When** the admin POSTs /admin/catalog/purpose-qualities with both IDs,
**Then** the link is created and the quality appears in the purpose's quality list.
