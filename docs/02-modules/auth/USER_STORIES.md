# Auth Module — User Stories

## US-AUTH-001: OTP-Based Customer Registration/Login

**As a** customer (P1),
**I want to** register and login using my mobile number and OTP,
**So that** I can access the platform without remembering a password.

**SRS Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-008
**Priority:** MUST
**Phase:** V1

---

## US-AUTH-002: Admin Email/Password Login

**As an** operations manager (P4) or super admin (P5),
**I want to** login using my email and password,
**So that** I can access the admin dashboard securely.

**SRS Requirements:** AUTH-005
**Priority:** MUST
**Phase:** V1

---

## US-AUTH-003: Token Management

**As an** authenticated user,
**I want to** have my session managed via short-lived access tokens with automatic refresh,
**So that** I stay logged in without re-authenticating frequently while maintaining security.

**SRS Requirements:** AUTH-006, AUTH-007
**Priority:** MUST
**Phase:** V1

---

## US-AUTH-004: OTP Rate Limiting

**As a** system operator,
**I want** OTP request and verification endpoints to be rate-limited,
**So that** brute-force attacks are prevented.

**SRS Requirements:** AUTH-009
**Priority:** MUST
**Phase:** V1

---

## US-AUTH-005: OTP Delivery Fallback

**As a** customer (P1),
**I want** the system to retry OTP delivery via a fallback channel if SMS fails,
**So that** I can still log in even when SMS delivery is unreliable.

**SRS Requirements:** AUTH-010
**Priority:** MUST
**Phase:** V1
