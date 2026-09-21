# Businesses Module — Acceptance Criteria

## AC-BIZ-001: Admin Creates Business

**User Story:** US-BIZ-001
**Given** a super admin, **When** they POST /admin/businesses with name and registration, **Then** the business is created and audit log written.

---

## AC-BIZ-002: Admin Adds User to Business

**User Story:** US-BIZ-002
**Given** a business exists, **When** admin POST /admin/businesses/{id}/users with user_id and role ADMIN, **Then** the user is linked as business admin.

---

## AC-BIZ-003: Admin Adds Business Site

**User Story:** US-BIZ-003
**Given** a business exists, **When** admin POST /admin/businesses/{id}/sites with address and name, **Then** the site is created with geocoded address.
