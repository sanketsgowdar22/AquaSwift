# RBAC Module — User Stories

## US-RBAC-001: Endpoint Permission Enforcement

**As a** system operator,
**I want** every protected API endpoint to enforce role-based permissions server-side,
**So that** users can only access functionality appropriate to their role.

**SRS Requirements:** RBAC-001, RBAC-003, RBAC-004, RBAC-005, RBAC-006
**Priority:** MUST
**Phase:** V1

---

## US-RBAC-002: Platform Role Definitions

**As a** super admin (P5),
**I want** predefined platform roles (CUSTOMER, DRIVER, OPS_MANAGER, SUPER_ADMIN) with specific permissions,
**So that** each user type has appropriate access levels.

**SRS Requirements:** RBAC-002, RBAC-003
**Priority:** MUST
**Phase:** V1

---

## US-RBAC-003: Role Assignment Management

**As a** super admin (P5),
**I want to** assign and revoke roles for users,
**So that** I can manage access control as the team changes.

**SRS Requirements:** RBAC-008
**Priority:** MUST
**Phase:** V1

---

## US-RBAC-004: Business Permission Scoping

**As a** business admin (P2),
**I want** my employees to have limited permissions within my business (order for assigned sites only),
**So that** I maintain control over business operations while delegating ordering.

**SRS Requirements:** RBAC-007
**Priority:** MUST
**Phase:** Phase 2
