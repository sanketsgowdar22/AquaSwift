# Drivers Module — Acceptance Criteria

## AC-DRV-001: Driver Toggles to Available

**User Story:** US-DRV-001
**Given** a driver with status UNAVAILABLE and no active delivery,
**When** they PATCH /drivers/me/status with `{ "status": "AVAILABLE" }`,
**Then** status changes to AVAILABLE and the driver becomes eligible for delivery offers.

---

## AC-DRV-002: Cannot Toggle While On Delivery

**User Story:** US-DRV-001
**Given** a driver with status ON_DELIVERY,
**When** they attempt to toggle status,
**Then** the system returns 400 with code `DRIVER_ON_DELIVERY`.

---

## AC-DRV-003: Driver Views Delivery History

**User Story:** US-DRV-002
**Given** a driver with past deliveries,
**When** they GET /drivers/me/deliveries?page=1,
**Then** paginated delivery records are returned with status, quantity, and timestamps.

---

## AC-DRV-004: Driver Views Earnings

**User Story:** US-DRV-003
**Given** a driver with completed deliveries,
**When** they GET /drivers/me/earnings?period=weekly,
**Then** the system returns total deliveries, total litres, and estimated earnings for the current week.

---

## AC-DRV-005: Admin Creates Driver Profile

**User Story:** US-DRV-004
**Given** an authenticated admin with `drivers:write`,
**When** they POST /admin/drivers with user_id and license_number,
**Then** a driver_profile is created with status UNAVAILABLE.

---

## AC-DRV-006: Admin Deactivates Driver

**User Story:** US-DRV-004
**Given** a driver with no active deliveries,
**When** the admin deactivates the driver profile,
**Then** the driver cannot receive offers and their status shows UNAVAILABLE.
