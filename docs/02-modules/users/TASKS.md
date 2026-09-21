# Users Module — Tasks

## T-USR-001: Create Customer/Driver Profile Models

**User Story:** US-USR-001, US-USR-002
**Type:** Backend
**Description:** Create `customer_profiles` and `driver_profiles` SQLAlchemy models with FK to users.
**Files:** `backend/app/users/models.py`
**Dependencies:** T-AUTH-001
**Estimated Effort:** S

---

## T-USR-002: Create User/Profile Schemas

**User Story:** US-USR-001, US-USR-002, US-USR-003
**Type:** Backend
**Description:** Create Pydantic schemas for profile read/update, customer list, customer detail (with orders/addresses).
**Files:** `backend/app/users/schemas.py`
**Dependencies:** T-USR-001
**Estimated Effort:** S

---

## T-USR-003: Implement Profile CRUD Service

**User Story:** US-USR-001, US-USR-002
**Type:** Backend
**Description:** Implement get_profile(), update_profile() for both customer and driver profiles.
**Files:** `backend/app/users/service.py`
**Dependencies:** T-USR-001, T-USR-002
**Estimated Effort:** S

---

## T-USR-004: Implement Admin Customer Service

**User Story:** US-USR-003
**Type:** Backend
**Description:** Implement list_customers(filters, pagination), get_customer_detail(id), deactivate_customer(id). Include order history and addresses in detail view.
**Files:** `backend/app/users/service.py`
**Dependencies:** T-USR-001
**Estimated Effort:** M

---

## T-USR-005: Create User API Routes

**User Story:** All user stories
**Type:** Backend
**Description:** Create routes: GET/PATCH /users/me, GET /admin/customers, GET /admin/customers/{id}, PATCH /admin/customers/{id}.
**Files:** `backend/app/users/router.py`
**Dependencies:** T-USR-003, T-USR-004
**Estimated Effort:** S

---

## T-USR-006: Write User Tests

**User Story:** All user stories
**Type:** Backend
**Description:** Test profile CRUD, admin customer list/detail, customer deactivation, pagination/filtering.
**Files:** `backend/app/users/tests/`
**Dependencies:** T-USR-005
**Estimated Effort:** M
