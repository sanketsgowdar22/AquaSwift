# Phase 1 — Core Platform & Security

## 1. Phase Identity

- **Phase:** P1
- **Name:** Core Platform & Security
- **Status:** NOT STARTED
- **Depends On:** P0 (Audit & Foundation) approved

## 2. Objective

Establish the technical foundation required by all applications: harden authentication, implement rate limiting, set up database migrations, create test infrastructure, and remove the demo auth bypass.

## 3. Scope

### P1.1 — Authentication Hardening
- Revert demo authentication bypass in `frontend/lib/auth.tsx`
- Verify OTP request/verify flow
- Verify admin email/password login
- Verify JWT creation/refresh/invalidation
- Verify token expiry behavior

### P1.2 — Rate Limiting (New Feature)
- Implement Redis-backed rate limiting middleware
- Configure limits per endpoint category
- Return HTTP 429 with Retry-After headers
- See `docs/05-security/rate-limiting.md`

### P1.3 — RBAC Verification
- Verify role model (CUSTOMER, DRIVER, ADMIN, SUPER_ADMIN)
- Verify permission checks on protected endpoints
- Verify admin-only endpoint protection

### P1.4 — Database Migrations
- Verify Alembic configuration
- Create initial migration from current models
- Test migration up/down
- Document migration workflow

### P1.5 — Test Infrastructure
- Set up pytest fixtures (async DB session, test client, auth helpers)
- Write core module unit tests
- Write auth endpoint tests
- Write rate limiting tests

### P1.6 — Security Headers & CORS
- Review CORS configuration
- Add security headers where applicable
- Verify error response standardization

## 4. Out of Scope

- Customer app feature implementation (Phase 2)
- Driver app feature implementation (Phase 3)
- Admin dashboard feature implementation (Phase 5)
- Frontend ↔ Backend integration (Phases 2-5)

## 5. Existing Implementation

| Component | Status |
|-----------|--------|
| Auth models (users, OTP) | ✅ Implemented |
| Auth service (OTP, login, JWT) | ✅ Implemented |
| Auth router (5 endpoints) | ✅ Implemented |
| RBAC models (roles, permissions) | ✅ Implemented |
| RBAC router | ✅ Implemented |
| JWT utilities (core/security.py) | ✅ Implemented |
| Middleware (CORS, RequestID, Logging) | ✅ Implemented |
| Error handling (core/exceptions.py) | ✅ Implemented |
| Redis client (core/cache.py) | ✅ Implemented |
| Rate limiting | ❌ Not implemented |
| Test infrastructure | ❌ Only health check test |
| Demo auth bypass | ⚠️ Active in frontend/lib/auth.tsx |

## 6. Existing Modules

| Module | Existing Tasks |
|--------|---------------|
| auth | T-AUTH-001 through T-AUTH-010 |
| rbac | T-RBAC-001 through T-RBAC-006 |
| users | T-USR-001 through T-USR-006 |
| core | (infrastructure — no dedicated task IDs) |

## 7. Existing Tasks (Preserved)

These existing tasks belong to Phase 1:

| Task | Description | Current Status |
|------|------------|---------------|
| T-AUTH-001 | Create Auth SQLAlchemy Models | IMPLEMENTED |
| T-AUTH-002 | Create Auth Pydantic Schemas | IMPLEMENTED |
| T-AUTH-003 | Implement OTP Request Service | IMPLEMENTED |
| T-AUTH-004 | Implement OTP Verification Service | IMPLEMENTED |
| T-AUTH-005 | Implement Admin Login Service | IMPLEMENTED |
| T-AUTH-006 | Implement JWT & Refresh Token Utilities | IMPLEMENTED |
| T-AUTH-007 | Create Auth API Routes | IMPLEMENTED |
| T-AUTH-008 | Implement Rate Limiting Middleware | NOT_STARTED |
| T-AUTH-009 | Implement OTP Fallback Channel | NOT_STARTED |
| T-AUTH-010 | Write Auth Unit & Integration Tests | NOT_STARTED |
| T-RBAC-001 | Create Role & Permission Models | IMPLEMENTED |
| T-RBAC-002 | Create RBAC Schemas | IMPLEMENTED |
| T-RBAC-003 | Implement RBAC Service | IMPLEMENTED |
| T-RBAC-004 | Create RBAC Router | IMPLEMENTED |
| T-RBAC-005 | Implement Permission Decorators | IMPLEMENTED |
| T-RBAC-006 | Write RBAC Tests | NOT_STARTED |
| T-USR-001 | Create User Models | IMPLEMENTED |
| T-USR-002 | Create User Schemas | IMPLEMENTED |
| T-USR-003 | Implement User Service | IMPLEMENTED |
| T-USR-004 | Create User Router | IMPLEMENTED |
| T-USR-005 | Implement Admin User Management | IMPLEMENTED |
| T-USR-006 | Write User Tests | NOT_STARTED |

## 8. New Tasks (Phase 1 Only)

| Task | Description | Dependencies |
|------|------------|-------------|
| T-CORE-001 | Set up pytest async fixtures + test client | None |
| T-CORE-002 | Create Alembic initial migration | T-AUTH-001 |
| T-CORE-003 | Implement rate limiting middleware (slowapi + Redis) | T-AUTH-008 |
| T-CORE-004 | Revert demo authentication bypass | T-AUTH-007 |
| T-CORE-005 | Add security headers middleware | None |
| T-CORE-006 | Verify CORS configuration | None |

## 9. User Stories

Existing auth/rbac user stories apply:
- US-AUTH-001 through US-AUTH-005
- US-RBAC-001 through US-RBAC-004
- US-USR-001 through US-USR-003

## 10. Functional Requirements

- OTP-based customer login must work end-to-end
- Admin email/password login must work end-to-end
- JWT access + refresh tokens must be issued correctly
- Rate limiting must block excessive requests with HTTP 429
- RBAC must prevent unauthorized access to admin endpoints
- Demo auth bypass must be removed

## 11. Non-Functional Requirements

- Rate limiting storage must use Redis (already in docker-compose)
- Rate limits must be configurable via environment variables
- Tests must run without external dependencies (mocked Redis/DB)
- Alembic migrations must be reversible

## 12. Dependencies

- Redis service (docker-compose — already configured)
- PostgreSQL service (docker-compose — already configured)

## 13. API Requirements

All auth endpoints must be functional and tested:
- `POST /auth/otp/request`
- `POST /auth/otp/verify`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`

## 14. Database Requirements

- Alembic initial migration must create all tables
- Migration must be reversible (upgrade + downgrade)

## 15. Frontend/UI Requirements

- Remove demo auth bypass from `frontend/lib/auth.tsx`
- Login page must use real API endpoints when backend is available
- Graceful error handling when backend is unavailable

## 16. Security Requirements

- All auth endpoints rate-limited
- OTP endpoints: 3-5 requests/minute/IP
- Login endpoints: 5-10 requests/minute/IP
- Rate limit responses include Retry-After header
- No demo/bypass authentication in any non-development context
- JWT tokens signed with configurable secret

## 17. Testing Requirements

- Auth service unit tests (OTP, login, token refresh)
- Auth router API tests
- Rate limiting tests (within limit, at limit, exceeded, recovery)
- RBAC permission tests
- Minimum test coverage for Phase 1 modules: 70%

## 18. Acceptance Criteria

- [ ] Demo auth bypass removed
- [ ] OTP login flow works (request → verify → token)
- [ ] Admin login flow works (email/password → token)
- [ ] Token refresh works
- [ ] Rate limiting blocks excess requests with 429
- [ ] Rate limits configurable via .env
- [ ] RBAC prevents unauthorized admin access
- [ ] Alembic migration creates all tables
- [ ] Auth tests pass
- [ ] Rate limiting tests pass
- [ ] RBAC tests pass

## 19. Risks

| Risk | Mitigation |
|------|-----------|
| Rate limiting library incompatible with latest FastAPI | Test with slowapi first; fallback to custom middleware |
| Redis unavailable in dev | Graceful degradation (log warning, skip limits) |
| Demo auth removal breaks frontend preview | Frontend shows login page; dev credentials documented |

## 20. Deliverables

- Rate limiting middleware (`backend/app/core/rate_limit.py`)
- Test fixtures (`backend/tests/conftest.py` — enhanced)
- Auth tests (`backend/tests/test_auth.py`)
- Rate limiting tests (`backend/tests/test_rate_limit.py`)
- Initial Alembic migration
- Updated `frontend/lib/auth.tsx` (demo bypass removed)

## 21. Definition of Done

All acceptance criteria pass. All tests pass. Demo bypass removed. Rate limiting active.

## 22. Exit Criteria

- Authentication works end-to-end (OTP + admin login)
- Rate limiting prevents abuse on all auth endpoints
- RBAC prevents unauthorized access
- Database migrations work (up + down)
- Test suite passes with >70% coverage on Phase 1 modules
- No demo authentication bypass exists
- Security documentation reflects actual implementation

**Phase 1 must be complete before Phase 2 (Customer App) begins.**
