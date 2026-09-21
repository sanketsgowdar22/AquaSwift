# RBAC Module — Acceptance Criteria

## AC-RBAC-001: Permission Check Passes for Valid Role

**User Story:** US-RBAC-001
**Given** an authenticated user with the SUPER_ADMIN role,
**When** they access any admin endpoint requiring `catalog:write` permission,
**Then** the request proceeds successfully (200/201).

---

## AC-RBAC-002: Permission Check Fails for Invalid Role

**User Story:** US-RBAC-001
**Given** an authenticated user with the CUSTOMER role,
**When** they access an admin endpoint requiring `catalog:write` permission,
**Then** the system returns 403 Forbidden with code `INSUFFICIENT_PERMISSIONS`.

---

## AC-RBAC-003: Customer Cannot Access Admin Endpoints

**User Story:** US-RBAC-001
**Given** an authenticated customer,
**When** they attempt to access any /admin/* endpoint,
**Then** the system returns 403 for every such endpoint.

---

## AC-RBAC-004: Driver Cannot Access Customer Endpoints

**User Story:** US-RBAC-001
**Given** an authenticated driver,
**When** they attempt to POST /orders (place an order),
**Then** the system returns 403.

---

## AC-RBAC-005: Role Assignment by Super Admin

**User Story:** US-RBAC-003
**Given** a super admin is authenticated,
**When** they POST /admin/users/{id}/roles with a valid role_id,
**Then** the role is assigned to the user, an audit log is written, and 201 is returned.

---

## AC-RBAC-006: Role Revocation by Super Admin

**User Story:** US-RBAC-003
**Given** a super admin is authenticated and a user has an assigned role,
**When** they DELETE /admin/users/{id}/roles/{role_id},
**Then** the role is revoked, an audit log is written, and 200 is returned.

---

## AC-RBAC-007: Non-Admin Cannot Manage Roles

**User Story:** US-RBAC-003
**Given** an authenticated OPS_MANAGER,
**When** they attempt to assign or revoke roles,
**Then** the system returns 403 (only SUPER_ADMIN can manage roles).

---

## AC-RBAC-008: Unauthenticated Request Rejected

**User Story:** US-RBAC-001
**Given** a request with no Authorization header or an invalid JWT,
**When** it hits any protected endpoint,
**Then** the system returns 401 Unauthorized.
