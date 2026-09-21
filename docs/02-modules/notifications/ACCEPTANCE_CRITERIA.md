# Notifications Module — Acceptance Criteria

## AC-NTF-001: Order Confirmed Triggers Push + SMS

**User Story:** US-NTF-001
**Given** an order transitions to CONFIRMED,
**When** the notification service is invoked,
**Then** a push notification and SMS are sent to the customer, and notification records are created.

---

## AC-NTF-002: Push Failure Falls Back to SMS

**User Story:** US-NTF-003
**Given** a push notification fails (invalid token),
**When** the retry/fallback logic runs,
**Then** the notification is delivered via SMS instead, and the failed token is removed.

---

## AC-NTF-003: Notification Failure Doesn't Block Business Logic

**User Story:** US-NTF-003
**Given** the notification service raises an exception,
**When** a state transition triggers it,
**Then** the business operation (order confirmation, delivery completion) completes successfully regardless.

---

## AC-NTF-004: Device Token Registered

**User Story:** US-NTF-004
**Given** a customer opens the app,
**When** they POST /notifications/register-device with FCM token,
**Then** the token is stored and future push notifications are sent to this device.

---

## AC-NTF-005: Customer Views Notification History

**User Story:** US-NTF-005
**Given** a customer has received notifications,
**When** they GET /notifications,
**Then** a paginated list of notifications is returned sorted by created_at DESC.

---

## AC-NTF-006: SMS Uses DLT Template

**User Story:** US-NTF-006
**Given** an SMS notification is being sent,
**When** the MSG91 adapter is called,
**Then** the request includes the DLT-registered template_id.
