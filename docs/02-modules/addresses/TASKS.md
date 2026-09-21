# Addresses Module — Tasks

## T-ADDR-001: Create Address & Business Site Models

**User Story:** US-ADDR-001, US-ADDR-004
**Type:** Backend
**Description:** Create `addresses` model (user_id, label, address lines, city, state, pincode, lat, lng, formatted_address, notes, is_default) and `business_sites` model (business_id, address_id, name, contact).
**Files:** `backend/app/addresses/models.py`
**Dependencies:** T-AUTH-001, T-BIZ-001 (business model)
**Estimated Effort:** S

---

## T-ADDR-002: Create Address Schemas

**User Story:** US-ADDR-001, US-ADDR-002
**Type:** Backend
**Description:** Create Pydantic schemas: AddressCreate, AddressUpdate, AddressResponse, AddressList.
**Files:** `backend/app/addresses/schemas.py`
**Dependencies:** T-ADDR-001
**Estimated Effort:** S

---

## T-ADDR-003: Implement Address CRUD Service with Geocoding

**User Story:** US-ADDR-001
**Type:** Backend
**Description:** Implement create, update, delete, list addresses. On create/update, call MapsProvider.geocode() to populate lat/lng. Handle geocoding failure gracefully.
**Files:** `backend/app/addresses/service.py`
**Dependencies:** T-ADDR-001, Google Maps adapter
**Estimated Effort:** M

---

## T-ADDR-004: Create Address API Routes

**User Story:** US-ADDR-001, US-ADDR-002, US-ADDR-003
**Type:** Backend
**Description:** Create routes: GET/POST/PATCH/DELETE /addresses, GET /admin/addresses.
**Files:** `backend/app/addresses/router.py`
**Dependencies:** T-ADDR-003
**Estimated Effort:** S

---

## T-ADDR-005: Write Address Tests

**User Story:** All address stories
**Type:** Backend
**Description:** Test CRUD operations, geocoding integration, admin address view, business site schema.
**Files:** `backend/app/addresses/tests/`
**Dependencies:** T-ADDR-004
**Estimated Effort:** S
