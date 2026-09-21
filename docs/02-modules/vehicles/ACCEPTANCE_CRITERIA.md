# Vehicles Module — Acceptance Criteria

## AC-VEH-001: Admin Creates Vehicle

**User Story:** US-VEH-001
**Given** an authenticated admin with `vehicles:write`,
**When** they POST /admin/vehicles with registration_number, type, and capacity_litres,
**Then** the vehicle is created with status ACTIVE and audit log is written.

---

## AC-VEH-002: Duplicate Registration Rejected

**User Story:** US-VEH-001
**Given** a vehicle with registration "TS09AB1234" already exists,
**When** the admin creates another with the same number,
**Then** the system returns 409 with code `VEHICLE_ALREADY_EXISTS`.

---

## AC-VEH-003: Admin Assigns Driver to Vehicle

**User Story:** US-VEH-002
**Given** an ACTIVE vehicle and an available driver,
**When** the admin POST /admin/vehicles/{id}/assign-driver with driver_id,
**Then** the vehicle's current_driver_id is set and the driver's current_vehicle_id is updated.

---

## AC-VEH-004: Capacity Is Integer Litres

**User Story:** US-VEH-001
**Given** an admin creates a vehicle,
**When** capacity_litres is non-integer or negative,
**Then** the system returns 422 validation error.
