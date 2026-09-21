# Admin Module — Acceptance Criteria

## AC-ADM-001: Dashboard Returns Metrics

**User Story:** US-ADM-001
**Given** orders, deliveries, and inventory data exist,
**When** an admin GET /admin/dashboard,
**Then** the response includes active orders count, pending deliveries, today's revenue, driver status summary, and low-inventory alerts.

---

## AC-ADM-002: Dashboard Accessible to Admin Only

**User Story:** US-ADM-001
**Given** a customer user,
**When** they attempt GET /admin/dashboard,
**Then** the system returns 403.

---

## AC-ADM-003: Role List Shows All Roles

**User Story:** US-ADM-002
**Given** a super admin,
**When** they GET /admin/roles,
**Then** all 4 roles (CUSTOMER, DRIVER, OPS_MANAGER, SUPER_ADMIN) with their permissions are returned.
