# WoW — Security Documentation

This directory contains security documentation for the WoW platform.

## Documents

| Document | Description |
|----------|------------|
| [rate-limiting.md](rate-limiting.md) | Rate limiting strategy, endpoint limits, and implementation plan |
| [authentication.md](authentication.md) | Authentication architecture, OTP flow, JWT management |
| [rbac.md](rbac.md) | Role-based access control model and permission enforcement |

## Security Status

| Control | Status | Phase |
|---------|--------|-------|
| JWT Authentication | ✅ Implemented | P1 |
| OTP-based Customer Login | ✅ Implemented | P1 |
| Email/Password Admin Login | ✅ Implemented | P1 |
| RBAC (Role-Based Access) | ✅ Implemented | P1 |
| CORS Configuration | ✅ Implemented | P1 |
| Request ID Tracking | ✅ Implemented | P1 |
| Rate Limiting | ❌ Not Implemented | P1 |
| Security Headers | ❌ Not Implemented | P1 |
| Demo Auth Bypass | ⚠️ Active (must remove in P1) | P1 |
| Input Validation (Pydantic) | ✅ Implemented | P1 |
| SQL Injection Prevention (SQLAlchemy ORM) | ✅ Implemented | P1 |
| Production Secret Rotation | ❌ Planned | P7 |

## Known Vulnerabilities

1. **Demo Authentication Bypass** — `frontend/lib/auth.tsx` lines 35-47 auto-authenticate without backend. Must be reverted in Phase 1.
2. **No Rate Limiting** — All endpoints are unprotected against abuse. Must be implemented in Phase 1.
3. **Default JWT Secret** — `JWT_SECRET_KEY=change-me-to-a-secure-random-string-in-production` in `.env`. Must be rotated for production.
