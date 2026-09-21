# RBAC Module — Tasks

## T-RBAC-001: Create Roles & UserRoles Models

**User Story:** US-RBAC-002
**Type:** Backend
**Description:** Create `roles` model (name, permissions JSONB) and `user_roles` join model. Seed initial roles with permission sets via seed script.
**Files:** `backend/app/rbac/models.py`, `backend/scripts/seed_data.py`
**Dependencies:** T-AUTH-001 (users model)
**Estimated Effort:** S

---

## T-RBAC-002: Define Permission Constants

**User Story:** US-RBAC-001
**Type:** Backend
**Description:** Define all granular permissions as constants (e.g., `catalog:read`, `catalog:write`, `orders:create`, `inventory:adjust`). Map each role to its permission set.
**Files:** `backend/app/rbac/constants.py`
**Dependencies:** None
**Estimated Effort:** S

---

## T-RBAC-003: Implement require_permission() Dependency

**User Story:** US-RBAC-001
**Type:** Backend
**Description:** Create FastAPI dependency `require_permission(permission: str)` that loads the user's role(s), checks if any role grants the required permission, and raises 403 if not. Works with `get_current_user()` from auth.
**Files:** `backend/app/core/dependencies.py`
**Dependencies:** T-AUTH-006 (JWT), T-RBAC-001
**Estimated Effort:** M

---

## T-RBAC-004: Implement Role Assignment Endpoints

**User Story:** US-RBAC-003
**Type:** Backend
**Description:** Create admin endpoints: POST /admin/users/{id}/roles (assign role), DELETE /admin/users/{id}/roles/{role_id} (revoke role). Both require `roles:write` permission. Log to audit.
**Files:** `backend/app/rbac/router.py`, `backend/app/rbac/service.py`
**Dependencies:** T-RBAC-003
**Estimated Effort:** S

---

## T-RBAC-005: Design Business Permission Schema (Phase 2)

**User Story:** US-RBAC-004
**Type:** Backend
**Description:** Design and implement `business_users.role` (ADMIN/EMPLOYEE) with business-scoped permission checking. Employees can only order for assigned sites and view own orders.
**Files:** `backend/app/rbac/service.py`, `backend/app/businesses/models.py`
**Dependencies:** T-RBAC-003, businesses module
**Estimated Effort:** L

---

## T-RBAC-006: Write RBAC Tests

**User Story:** All RBAC stories
**Type:** Backend
**Description:** Test: permission check passes for valid role, 403 for invalid role, customer cannot access admin endpoints, driver cannot access customer endpoints, role assignment/revocation.
**Files:** `backend/app/rbac/tests/test_service.py`, `backend/app/rbac/tests/test_dependencies.py`
**Dependencies:** T-RBAC-004
**Estimated Effort:** M
