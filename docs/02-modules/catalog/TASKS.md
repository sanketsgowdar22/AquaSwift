# Catalog Module — Tasks

## T-CAT-001: Create Catalog SQLAlchemy Models

**User Story:** US-CAT-002, US-CAT-003, US-CAT-004, US-CAT-005, US-CAT-006
**Type:** Backend
**Description:** Create models: `water_purposes`, `water_quality_types`, `delivery_methods`, `water_purpose_qualities` (join), `water_variants`. All with is_active, quantity fields as BIGINT.
**Files:** `backend/app/catalog/models.py`
**Dependencies:** None
**Estimated Effort:** M

---

## T-CAT-002: Create Catalog Pydantic Schemas

**User Story:** All catalog stories
**Type:** Backend
**Description:** Create request/response schemas for all catalog entities: Create, Update, Response, List for purposes, qualities, methods, variants.
**Files:** `backend/app/catalog/schemas.py`
**Dependencies:** T-CAT-001
**Estimated Effort:** M

---

## T-CAT-003: Implement Catalog Read Service

**User Story:** US-CAT-001
**Type:** Backend
**Description:** Implement public read services: list_purposes(), get_qualities_for_purpose(), list_delivery_methods(), list_variants(filters). Filter out is_active=false for customer endpoints.
**Files:** `backend/app/catalog/service.py`
**Dependencies:** T-CAT-001
**Estimated Effort:** M

---

## T-CAT-004: Implement Catalog Admin CRUD Service

**User Story:** US-CAT-002, US-CAT-003, US-CAT-004, US-CAT-005, US-CAT-006
**Type:** Backend
**Description:** Implement admin CRUD for all catalog entities. Validate purpose-quality link before variant creation. Call audit logger on all writes. Invalidate Redis cache on writes.
**Files:** `backend/app/catalog/service.py`
**Dependencies:** T-CAT-001, T-CAT-007 (cache), audit module
**Estimated Effort:** L

---

## T-CAT-005: Implement Soft-Delete Logic

**User Story:** US-CAT-007
**Type:** Backend
**Description:** Implement deactivation (is_active=false) instead of hard-delete. Check if record is referenced by order_items before allowing deletion; if referenced, only deactivate. Deactivated records excluded from customer reads but retained for order history.
**Files:** `backend/app/catalog/service.py`
**Dependencies:** T-CAT-004
**Estimated Effort:** S

---

## T-CAT-006: Implement Variant Validation

**User Story:** US-CAT-006
**Type:** Backend
**Description:** Before creating a variant, validate: (1) purpose-quality link exists in water_purpose_qualities, (2) combination is unique, (3) min_quantity < max_quantity, (4) quantities are positive integers.
**Files:** `backend/app/catalog/service.py`
**Dependencies:** T-CAT-004
**Estimated Effort:** S

---

## T-CAT-007: Implement Redis Catalog Cache

**User Story:** US-CAT-008
**Type:** Backend
**Description:** Implement Redis caching for catalog read endpoints with ≤60s TTL. Cache key structure: `catalog:{entity}:{filters_hash}`. Implement cache invalidation function called on every catalog write.
**Files:** `backend/app/catalog/cache.py`, `backend/app/core/cache.py`
**Dependencies:** T-CAT-003, Redis setup
**Estimated Effort:** M

---

## T-CAT-008: Create Catalog API Routes

**User Story:** All catalog stories
**Type:** Backend
**Description:** Create public routes: GET /catalog/purposes, GET /catalog/purposes/{id}/qualities, GET /catalog/delivery-methods, GET /catalog/variants. Create admin routes: POST/PATCH for all entities.
**Files:** `backend/app/catalog/router.py`
**Dependencies:** T-CAT-003, T-CAT-004
**Estimated Effort:** M

---

## T-CAT-009: Write Catalog Tests

**User Story:** All catalog stories
**Type:** Backend
**Description:** Test: public read endpoints, admin CRUD, soft-delete protection, variant validation, cache hit/miss/invalidation, deactivated records hidden from customers.
**Files:** `backend/app/catalog/tests/`
**Dependencies:** T-CAT-008
**Estimated Effort:** L
