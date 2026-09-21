# Users Module — Acceptance Criteria

## AC-USR-001: Customer Views Own Profile

**User Story:** US-USR-001
**Given** an authenticated customer,
**When** they GET /users/me,
**Then** the system returns their profile with name, phone, email, and customer_type.

---

## AC-USR-002: Customer Updates Profile

**User Story:** US-USR-001
**Given** an authenticated customer,
**When** they PATCH /users/me with updated name and email,
**Then** the profile is updated and the response reflects the new values.

---

## AC-USR-003: Auto-Created Profile on Registration

**User Story:** US-USR-001
**Given** a new user who just verified OTP for the first time,
**When** the user account is created,
**Then** a customer_profile record is also created with customer_type = INDIVIDUAL.

---

## AC-USR-004: Admin Lists Customers with Filtering

**User Story:** US-USR-003
**Given** an authenticated admin with `customers:read` permission,
**When** they GET /admin/customers?search=Ravi&page=1&page_size=20,
**Then** the system returns a paginated list of matching customers.

---

## AC-USR-005: Admin Views Customer Detail

**User Story:** US-USR-003
**Given** an authenticated admin,
**When** they GET /admin/customers/{id},
**Then** the system returns the customer's profile, order history, and addresses.

---

## AC-USR-006: Admin Deactivates Customer

**User Story:** US-USR-003
**Given** an authenticated super admin,
**When** they PATCH /admin/customers/{id} with `{ "is_active": false }`,
**Then** the customer account is deactivated, login is prevented, and an audit log is written.
