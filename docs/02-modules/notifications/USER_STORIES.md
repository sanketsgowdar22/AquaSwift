# Notifications Module — User Stories

## US-NTF-001: Event-Driven Notification Dispatch

**As a** system,
**I want** lifecycle events (order confirmed, driver en route, delivery complete) to trigger notifications automatically,
**So that** users are informed at each stage without manual intervention.

**SRS Requirements:** NTF-001, NTF-002, NTF-003
**Priority:** MUST
**Phase:** V1

---

## US-NTF-002: Multi-Channel Delivery

**As a** system,
**I want** notifications to be sent via the appropriate channel (Push, SMS, Email) based on event type,
**So that** critical events reach users via the best available channel.

**SRS Requirements:** NTF-004, NTF-005
**Priority:** MUST
**Phase:** V1

---

## US-NTF-003: Notification Resilience

**As a** system,
**I want** notification delivery failures to not block business operations, with fallback and retry,
**So that** a push notification failure does not prevent order completion.

**SRS Requirements:** NTF-006
**Priority:** MUST
**Phase:** V1

---

## US-NTF-004: Device Token Registration

**As a** customer or driver,
**I want to** register my device for push notifications,
**So that** I receive real-time updates on my phone.

**SRS Requirements:** NTF-007
**Priority:** MUST
**Phase:** V1

---

## US-NTF-005: Customer Views Notifications

**As a** customer (P1),
**I want to** view my notification history in the app,
**So that** I can see past alerts and updates.

**SRS Requirements:** NTF-008
**Priority:** SHOULD
**Phase:** V1

---

## US-NTF-006: DLT-Compliant SMS Templates

**As a** system,
**I want** all SMS notifications to use DLT-registered templates,
**So that** messages are delivered without carrier blocking.

**SRS Requirements:** NTF-009
**Priority:** MUST
**Phase:** V1
