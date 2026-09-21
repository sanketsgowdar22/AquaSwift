# Drivers Module — Tasks

## T-DRV-001: Create Driver Model (extends driver_profiles)

**User Story:** US-DRV-004
**Type:** Backend
**Description:** Leverage driver_profiles model (T-USR-001). Add driver-specific service functions for status management and vehicle assignment.
**Files:** `backend/app/drivers/service.py`
**Dependencies:** T-USR-001
**Estimated Effort:** S

---

## T-DRV-002: Implement Availability Toggle

**User Story:** US-DRV-001
**Type:** Backend
**Description:** Implement PATCH /drivers/me/status — toggle between AVAILABLE and UNAVAILABLE. Cannot toggle while ON_DELIVERY.
**Files:** `backend/app/drivers/service.py`
**Dependencies:** T-DRV-001
**Estimated Effort:** S

---

## T-DRV-003: Implement Driver Delivery History

**User Story:** US-DRV-002
**Type:** Backend
**Description:** Implement GET /drivers/me/deliveries with pagination, date filtering. Return delivery summary with status, quantity, completion time.
**Files:** `backend/app/drivers/service.py`
**Dependencies:** T-DEL-001
**Estimated Effort:** S

---

## T-DRV-004: Implement Earnings Service

**User Story:** US-DRV-003
**Type:** Backend
**Description:** Implement GET /drivers/me/earnings — aggregate delivery completion data by day/week/month. Return total deliveries, total litres, estimated earnings.
**Files:** `backend/app/drivers/service.py`
**Dependencies:** T-DEL-001
**Estimated Effort:** M

---

## T-DRV-005: Create Driver API Routes & Admin CRUD

**User Story:** All driver stories
**Type:** Backend
**Description:** Driver: GET /drivers/me, PATCH /drivers/me/status, GET /drivers/me/deliveries, GET /drivers/me/earnings. Admin: GET/POST/PATCH /admin/drivers.
**Files:** `backend/app/drivers/router.py`
**Dependencies:** T-DRV-002 through T-DRV-004
**Estimated Effort:** S

---

## T-DRV-006: Write Driver Tests

**User Story:** All driver stories
**Type:** Backend
**Description:** Test availability toggle, cannot toggle during delivery, delivery history, earnings aggregation, admin CRUD.
**Files:** `backend/app/drivers/tests/`
**Dependencies:** T-DRV-005
**Estimated Effort:** M
