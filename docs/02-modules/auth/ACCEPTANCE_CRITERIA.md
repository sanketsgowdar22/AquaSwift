# Auth Module — Acceptance Criteria

## AC-AUTH-001: OTP Request Success

**User Story:** US-AUTH-001
**Given** a valid Indian mobile number (+91XXXXXXXXXX),
**When** the customer sends POST /auth/otp/request with the phone number,
**Then** the system returns 200 with `expires_in_seconds`, sends a 6-digit OTP via SMS, and stores the OTP with a configurable expiry.

---

## AC-AUTH-002: OTP Verification and Token Issuance

**User Story:** US-AUTH-001
**Given** a valid OTP has been sent and is not expired,
**When** the user sends POST /auth/otp/verify with correct phone and OTP,
**Then** the system returns 200 with access_token (JWT), refresh_token, token_type, expires_in, and user object.

---

## AC-AUTH-003: OTP Expiry Rejection

**User Story:** US-AUTH-001
**Given** an OTP was sent more than the configured expiry time ago,
**When** the user attempts to verify with that OTP,
**Then** the system returns 400 with code `OTP_EXPIRED`.

---

## AC-AUTH-004: Invalid OTP Rejection

**User Story:** US-AUTH-001
**Given** an OTP is active,
**When** the user sends an incorrect OTP code,
**Then** the system returns 400 with code `OTP_INVALID` and increments the attempt counter.

---

## AC-AUTH-005: New User Auto-Creation

**User Story:** US-AUTH-001
**Given** no user account exists for the provided phone number,
**When** OTP verification succeeds,
**Then** a new user record and customer_profile are created, and tokens are issued for the new user.

---

## AC-AUTH-006: Existing User Login

**User Story:** US-AUTH-001
**Given** a user account exists for the provided phone number,
**When** OTP verification succeeds,
**Then** tokens are issued for the existing user without creating a duplicate.

---

## AC-AUTH-007: Admin Login Success

**User Story:** US-AUTH-002
**Given** a valid admin email and correct password,
**When** the admin sends POST /auth/login,
**Then** the system returns 200 with access_token, refresh_token, and user object with admin role.

---

## AC-AUTH-008: Admin Login Invalid Credentials

**User Story:** US-AUTH-002
**Given** an invalid email or incorrect password,
**When** the admin sends POST /auth/login,
**Then** the system returns 401 with code `INVALID_CREDENTIALS`.

---

## AC-AUTH-009: Token Refresh

**User Story:** US-AUTH-003
**Given** a valid, non-expired refresh token,
**When** the user sends POST /auth/refresh,
**Then** the system returns a new access_token and refresh_token, and invalidates the old refresh token.

---

## AC-AUTH-010: Token Refresh with Expired Token

**User Story:** US-AUTH-003
**Given** an expired or invalidated refresh token,
**When** the user sends POST /auth/refresh,
**Then** the system returns 401 with code `TOKEN_EXPIRED`.

---

## AC-AUTH-011: Logout Invalidation

**User Story:** US-AUTH-003
**Given** an authenticated user,
**When** the user sends POST /auth/logout,
**Then** all refresh tokens for that user are invalidated, and subsequent refresh attempts fail.

---

## AC-AUTH-012: OTP Rate Limiting

**User Story:** US-AUTH-004
**Given** a phone number that has already requested 5 OTPs within the last minute,
**When** another OTP request is made for that phone number,
**Then** the system returns 429 with a Retry-After header.

---

## AC-AUTH-013: OTP Verify Rate Limiting

**User Story:** US-AUTH-004
**Given** a phone number with 10 OTP verification attempts within the last minute,
**When** another verification attempt is made,
**Then** the system returns 429.

---

## AC-AUTH-014: SMS Failure Fallback

**User Story:** US-AUTH-005
**Given** SMS OTP delivery fails (MSG91 returns error) and the user has an email address on file,
**When** the OTP request is processed,
**Then** the system retries via email OTP and returns success with a note about the fallback channel.
