# WoW — Authentication Architecture

## 1. Overview

WoW uses two authentication methods:

| User Type | Method | Flow |
|-----------|--------|------|
| Customer | OTP (phone-based) | Phone → SMS OTP → Verify → JWT |
| Admin / Driver | Email + Password | Email + Password → JWT |

Both methods result in a JWT access token + refresh token pair.

## 2. Customer OTP Flow

```
1. Customer enters phone number
2. POST /auth/otp/request { phone: "+919876543210" }
3. Server generates 6-digit OTP, stores with 5-min expiry
4. SMS sent via MSG91 provider
5. Customer enters OTP
6. POST /auth/otp/verify { phone: "+919876543210", otp: "123456" }
7. Server validates OTP, creates user if new, issues tokens
8. Response: { access_token, refresh_token, user }
```

### Implementation Files

- `backend/app/auth/service.py` — `request_otp()`, `verify_otp()`
- `backend/app/auth/router.py` — `POST /auth/otp/request`, `POST /auth/otp/verify`
- `backend/app/auth/adapters/` — MSG91 SMS adapter

### Security Controls

- OTP expiry: 300 seconds (configurable via `OTP_EXPIRY_SECONDS`)
- OTP length: 6 digits (configurable via `OTP_LENGTH`)
- Max verification attempts: 5 (configurable via `OTP_MAX_ATTEMPTS`)
- Rate limit: 3 requests/minute/phone (via `OTP_RATE_LIMIT_PER_MINUTE`)
- Rate limit on verification: 5 attempts/minute/phone

## 3. Admin/Driver Login Flow

```
1. Admin/Driver enters email + password
2. POST /auth/login { email, password }
3. Server verifies email exists, bcrypt hash matches
4. Issues JWT access token + refresh token
5. Response: { access_token, refresh_token, user }
```

### Implementation Files

- `backend/app/auth/service.py` — `login()`
- `backend/app/auth/router.py` — `POST /auth/login`
- `backend/app/core/security.py` — `verify_password()`, `hash_password()`

### Security Controls

- Password hashing: bcrypt
- Rate limit: 5 attempts/minute/IP
- Failed login: returns 401 (no information leakage about email existence)

## 4. Token Management

### Access Token

- Algorithm: HS256 (configurable via `JWT_ALGORITHM`)
- Expiry: 60 minutes (configurable via `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`)
- Payload: `{ sub: user_id, roles: [...], exp, iat }`
- Signed with `JWT_SECRET_KEY`

### Refresh Token

- Expiry: 30 days (configurable via `JWT_REFRESH_TOKEN_EXPIRE_DAYS`)
- Stored in database (allows server-side revocation)
- One-time use: consumed on refresh, new pair issued

### Token Refresh

```
POST /auth/refresh { refresh_token: "..." }
→ Validates refresh token exists + not expired + not revoked
→ Issues new access + refresh token pair
→ Revokes old refresh token
```

### Logout

```
POST /auth/logout
Authorization: Bearer <access_token>
→ Revokes all refresh tokens for the user
```

### Implementation Files

- `backend/app/core/security.py` — `create_access_token()`, `decode_token()`
- `backend/app/auth/service.py` — `refresh_token()`, `logout()`
- `backend/app/auth/models.py` — RefreshToken model

## 5. Frontend Authentication

### Current Implementation

File: `frontend/lib/auth.tsx`

- Stores access token in cookies (`access_token`, 1 day)
- Stores refresh token in cookies (`refresh_token`, 30 days)
- Stores user data in cookies (`user_data`)
- Hydrates on mount from cookies
- AuthProvider context wraps all pages

### ⚠️ Demo Mode (MUST BE REMOVED — Phase 1)

Lines 35-47 of `auth.tsx` contain a demo bypass that auto-authenticates without backend. This was added for preview/screenshot purposes and **MUST be reverted** in Phase 1.

## 6. Authorization Headers

All protected API requests include:

```
Authorization: Bearer <jwt_access_token>
```

Backend middleware (`core/dependencies.py`) extracts and validates the token, injects the user into request state.
