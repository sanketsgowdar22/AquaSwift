# Notifications Module — Tasks

## T-NTF-001: Create Notification Model & Schemas

**User Story:** US-NTF-005
**Type:** Backend
**Description:** Create `notifications` model (user_id, channel, event_type, template, payload, status, sent_at, failure_reason). Create Pydantic schemas.
**Files:** `backend/app/notifications/models.py`, `backend/app/notifications/schemas.py`
**Dependencies:** T-AUTH-001
**Estimated Effort:** S

---

## T-NTF-002: Implement NotificationService

**User Story:** US-NTF-001, US-NTF-002
**Type:** Backend
**Description:** Implement channel-agnostic `NotificationService.send(user, event_type, context)`. Determines channel(s) based on event type, renders template, dispatches to adapter, records in DB.
**Files:** `backend/app/notifications/service.py`
**Dependencies:** T-NTF-001, Push/SMS/Email adapters
**Estimated Effort:** L

---

## T-NTF-003: Implement Async Notification Task

**User Story:** US-NTF-003
**Type:** Backend
**Description:** Celery task for notification sending — call site emits event, Celery task handles delivery. Retry with fallback on failure (push fails → try SMS).
**Files:** `backend/app/notifications/tasks.py`
**Dependencies:** T-NTF-002
**Estimated Effort:** M

---

## T-NTF-004: Implement Device Registration

**User Story:** US-NTF-004
**Type:** Backend
**Description:** Implement POST /notifications/register-device — store FCM token with user_id, platform, last_seen. Handle token rotation and cleanup.
**Files:** `backend/app/notifications/service.py`, `backend/app/notifications/router.py`
**Dependencies:** T-NTF-001
**Estimated Effort:** S

---

## T-NTF-005: Implement Notification Listing

**User Story:** US-NTF-005
**Type:** Backend
**Description:** Implement GET /notifications — list user's notifications with pagination.
**Files:** `backend/app/notifications/router.py`
**Dependencies:** T-NTF-001
**Estimated Effort:** S

---

## T-NTF-006: Define Event-Channel Mapping & Templates

**User Story:** US-NTF-006
**Type:** Backend
**Description:** Define mapping of event types to channels and DLT template IDs. E.g., order_confirmed → [Push, SMS], delivery_arrived → [Push, SMS].
**Files:** `backend/app/notifications/constants.py`
**Dependencies:** None
**Estimated Effort:** S

---

## T-NTF-007: Write Notification Tests

**User Story:** All notification stories
**Type:** Backend
**Description:** Test: event dispatch, channel selection, template rendering, async task, retry/fallback, device registration, notification listing.
**Files:** `backend/app/notifications/tests/`
**Dependencies:** T-NTF-005
**Estimated Effort:** M
