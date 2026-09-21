# Addresses Module — Acceptance Criteria

## AC-ADDR-001: Add Address with Geocoding

**User Story:** US-ADDR-001
**Given** an authenticated customer provides a valid address,
**When** they POST /addresses,
**Then** the system geocodes the address via Google Maps, stores lat/lng, and returns the address with coordinates.

---

## AC-ADDR-002: Add Address with Delivery Notes

**User Story:** US-ADDR-001
**Given** an authenticated customer,
**When** they POST /addresses with notes "Terrace tank, back gate access",
**Then** the notes are stored and returned in the address response.

---

## AC-ADDR-003: Update Address Re-Geocodes

**User Story:** US-ADDR-001
**Given** an existing address,
**When** the customer PATCHes the address_line_1 or pincode,
**Then** the system re-geocodes and updates lat/lng.

---

## AC-ADDR-004: Delete Address

**User Story:** US-ADDR-001
**Given** an existing address not referenced by an active order,
**When** the customer DELETEs the address,
**Then** the address is removed and no longer appears in the list.

---

## AC-ADDR-005: Select Address During Order

**User Story:** US-ADDR-002
**Given** a customer has saved addresses,
**When** they place an order with an existing address_id,
**Then** the order is linked to that address without re-geocoding.

---

## AC-ADDR-006: Geocoding Failure Graceful Degradation

**User Story:** US-ADDR-001
**Given** the Google Maps API is temporarily unavailable,
**When** a customer adds an address,
**Then** the address is saved with null lat/lng, and geocoding is queued for retry.

---

## AC-ADDR-007: Admin Views Customer Addresses

**User Story:** US-ADDR-003
**Given** an authenticated admin with `addresses:read` permission,
**When** they GET /admin/addresses?user_id={uuid},
**Then** the system returns all addresses for that customer.
