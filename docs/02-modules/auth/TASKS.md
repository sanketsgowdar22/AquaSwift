# Auth Module — Tasks

## T-AUTH-001: Create Auth SQLAlchemy Models

**User Story:** US-AUTH-001, US-AUTH-002
**Type:** Backend
**Description:** Create `users` model with phone, email, password_hash, full_name, is_active fields. Include OTP tracking fields (or separate OTP table) for code, expiry, attempt count.
**Files:** `backend/app/auth/models.py`
**Dependencies:** None (foundation module)
**Estimated Effort:** S

---

## T-AUTH-002: Create Auth Pydantic Schemas

**User Story:** US-AUTH-001, US-AUTH-002, US-AUTH-003
**Type:** Backend
**Description:** Create request/response schemas: OTPRequestSchema, OTPVerifySchema, LoginSchema, TokenResponseSchema, RefreshTokenSchema.
**Files:** `backend/app/auth/schemas.py`
**Dependencies:** T-AUTH-001
**Estimated Effort:** S

---

## T-AUTH-003: Implement OTP Request Service

**User Story:** US-AUTH-001
**Type:** Backend
**Description:** Implement `request_otp(phone)` in auth service — validate phone format, generate 6-digit OTP, store with configurable expiry, call SMSProvider.send_otp(). Enforce rate limit before generating.
**Files:** `backend/app/auth/service.py`
**Dependencies:** T-AUTH-001, T-AUTH-002, MSG91 adapter (T-INT-SMS-001)
**Estimated Effort:** M

---

## T-AUTH-004: Implement OTP Verification Service

**User Story:** US-AUTH-001
**Type:** Backend
**Description:** Implement `verify_otp(phone, otp)` — validate OTP against stored value, check expiry, create user if new (AUTH-008), issue JWT + refresh token. On failure, increment attempt counter.
**Files:** `backend/app/auth/service.py`
**Dependencies:** T-AUTH-003, T-AUTH-006
**Estimated Effort:** M

---

## T-AUTH-005: Implement Admin Login Service

**User Story:** US-AUTH-002
**Type:** Backend
**Description:** Implement `login(email, password)` — verify email exists, verify bcrypt hash, issue JWT + refresh token. Return 401 on invalid credentials.
**Files:** `backend/app/auth/service.py`
**Dependencies:** T-AUTH-001, T-AUTH-006
**Estimated Effort:** S

---

## T-AUTH-006: Implement JWT & Refresh Token Utilities

**User Story:** US-AUTH-003
**Type:** Backend
**Description:** Implement JWT creation (short-lived, e.g. 1 hour), refresh token generation (long-lived, e.g. 30 days), token refresh endpoint, and token invalidation on logout/security events. Store refresh tokens in DB with expiry.
**Files:** `backend/app/core/security.py`, `backend/app/auth/service.py`
**Dependencies:** T-AUTH-001
**Estimated Effort:** M

---

## T-AUTH-007: Create Auth API Routes

**User Story:** US-AUTH-001, US-AUTH-002, US-AUTH-003
**Type:** Backend
**Description:** Create FastAPI router with endpoints: POST /auth/otp/request, POST /auth/otp/verify, POST /auth/login, POST /auth/refresh, POST /auth/logout.
**Files:** `backend/app/auth/router.py`
**Dependencies:** T-AUTH-003, T-AUTH-004, T-AUTH-005, T-AUTH-006
**Estimated Effort:** S

---

## T-AUTH-008: Implement Rate Limiting Middleware

**User Story:** US-AUTH-004
**Type:** Backend
**Description:** Implement Redis-backed rate limiter for auth endpoints — max 5 OTP requests/min per phone, max 10 OTP verifications/min per phone. Return 429 with Retry-After header.
**Files:** `backend/app/core/middleware.py`, `backend/app/auth/router.py`
**Dependencies:** T-AUTH-007, Redis setup
**Estimated Effort:** M

---

## T-AUTH-009: Implement OTP Fallback Channel

**User Story:** US-AUTH-005
**Type:** Backend
**Description:** Add fallback logic to OTP request — if SMS delivery fails (MSG91 returns error), attempt email OTP delivery if user has email on file. Log fallback events.
**Files:** `backend/app/auth/service.py`
**Dependencies:** T-AUTH-003, Email adapter
**Estimated Effort:** S

---

## T-AUTH-010: Write Auth Unit & Integration Tests

**User Story:** All auth stories
**Type:** Backend
**Description:** Write tests: OTP request/verify happy path, expiry rejection, rate limiting, admin login, token refresh, token invalidation, fallback channel.
**Files:** `backend/app/auth/tests/test_service.py`, `backend/app/auth/tests/test_router.py`
**Dependencies:** T-AUTH-007
**Estimated Effort:** M
