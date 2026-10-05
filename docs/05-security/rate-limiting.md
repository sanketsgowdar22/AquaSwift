# WoW — Rate Limiting Strategy

## 1. Purpose

Rate limiting protects the WoW platform against:

- **Brute-force attacks** on authentication endpoints (OTP, login)
- **Abuse** of public APIs (catalog browsing, price quotes)
- **Resource exhaustion** from excessive requests
- **Scraping** of catalog/pricing data
- **Denial of service** attacks
- **Cost amplification** (SMS/OTP abuse → MSG91 costs)

## 2. Threat Model

| Threat | Endpoint Category | Risk |
|--------|------------------|------|
| OTP brute-force | `/auth/otp/verify` | HIGH — 6-digit OTP is guessable in ~1M attempts |
| OTP cost abuse | `/auth/otp/request` | HIGH — Each OTP costs money (SMS) |
| Login brute-force | `/auth/login` | MEDIUM — Password-based, lockout after N attempts |
| API scraping | `/catalog/*` | LOW — Public data, but excessive use wastes resources |
| Order spam | `POST /orders` | MEDIUM — Could create fraudulent/duplicate orders |
| Payment abuse | `/payments/*` | HIGH — Financial impact |
| Admin enumeration | `/admin/*` | MEDIUM — Information disclosure |

## 3. Strategy

### Algorithm

**Sliding window counter** using Redis sorted sets.

- More accurate than fixed windows (no burst-at-boundary issue)
- Low Redis memory footprint
- O(1) check per request

### Storage

**Redis** (already in docker-compose as `wow-redis` on port 6379).

Use database index 3 to separate from cache (index 0), Celery broker (index 1), and Celery results (index 2).

### Library

**`slowapi`** — integrates with FastAPI/Starlette, uses the `limits` library under the hood, supports Redis storage.

```
pip install slowapi
```

### Fallback Behavior

If Redis is unavailable:
- **Development:** Log warning, allow all requests (do not block development)
- **Production:** Log critical alert, apply in-memory fallback with conservative limits

## 4. Rate Limits by Endpoint Category

### Authentication Endpoints

| Endpoint | Limit | Key | Rationale |
|----------|-------|-----|-----------|
| `POST /auth/otp/request` | 3/minute | IP + phone | SMS cost prevention |
| `POST /auth/otp/verify` | 5/minute | IP + phone | Brute-force prevention |
| `POST /auth/login` | 5/minute | IP | Password brute-force |
| `POST /auth/refresh` | 10/minute | IP | Token refresh abuse |
| `POST /auth/logout` | 10/minute | User ID | Low risk, sensible limit |

### Public APIs

| Endpoint | Limit | Key | Rationale |
|----------|-------|-----|-----------|
| `GET /catalog/*` | 30/minute | IP | Scraping prevention |
| `GET /quality/*` | 30/minute | IP | Scraping prevention |
| `GET /health` | 60/minute | IP | Monitoring tools may poll |

### Authenticated Customer APIs

| Endpoint | Limit | Key | Rationale |
|----------|-------|-----|-----------|
| `POST /orders/quote` | 10/minute | User ID | Quote abuse |
| `POST /orders` | 5/minute | User ID | Order spam |
| `POST /orders/{id}/cancel` | 5/minute | User ID | Cancel abuse |
| `GET /orders` | 20/minute | User ID | Listing |
| `POST /coupons/validate` | 10/minute | User ID | Coupon enumeration |
| `POST /addresses` | 10/minute | User ID | Address spam |
| `POST /orders/{id}/reviews` | 5/minute | User ID | Review spam |

### Authenticated Driver APIs

| Endpoint | Limit | Key | Rationale |
|----------|-------|-----|-----------|
| `POST /deliveries/*/respond` | 10/minute | User ID | Rapid accept/reject |
| `POST /deliveries/*/start` | 10/minute | User ID | Status update |
| `POST /deliveries/*/complete` | 5/minute | User ID | Completion abuse |
| `PATCH /drivers/me/status` | 10/minute | User ID | Toggle abuse |

### Admin APIs

| Endpoint | Limit | Key | Rationale |
|----------|-------|-----|-----------|
| `GET /admin/*` | 30/minute | User ID | Read operations |
| `POST /admin/*` | 15/minute | User ID | Write operations |
| `PATCH /admin/*` | 15/minute | User ID | Update operations |
| `DELETE /admin/*` | 10/minute | User ID | Destructive operations |

### Payment APIs

| Endpoint | Limit | Key | Rationale |
|----------|-------|-----|-----------|
| `POST /payments/webhook` | 100/minute | IP | Gateway callbacks (high volume) |
| `POST /payments/*/retry` | 3/minute | User ID | Retry abuse |

## 5. Configuration

All limits are configurable via environment variables:

```env
# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_STORAGE_URL=redis://redis:6379/3

# Per-category defaults (format: "count/period")
RATE_LIMIT_AUTH_OTP_REQUEST=3/minute
RATE_LIMIT_AUTH_OTP_VERIFY=5/minute
RATE_LIMIT_AUTH_LOGIN=5/minute
RATE_LIMIT_PUBLIC_DEFAULT=30/minute
RATE_LIMIT_USER_DEFAULT=60/minute
RATE_LIMIT_ORDER_CREATE=5/minute
RATE_LIMIT_ADMIN_DEFAULT=30/minute
RATE_LIMIT_PAYMENT_WEBHOOK=100/minute
```

### Development Override

```env
# In development, set higher limits or disable entirely
RATE_LIMIT_ENABLED=false
```

## 6. HTTP Response Behavior

When a limit is exceeded:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 42
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1696118400

{
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests. Please try again later.",
  "details": {
    "retry_after_seconds": 42
  }
}
```

### Response Headers

| Header | Description |
|--------|------------|
| `Retry-After` | Seconds until the client can retry |
| `X-RateLimit-Limit` | Maximum requests allowed in window |
| `X-RateLimit-Remaining` | Requests remaining in current window |
| `X-RateLimit-Reset` | Unix timestamp when window resets |

## 7. Implementation Plan

### Files to Create/Modify

| File | Action |
|------|--------|
| `backend/app/core/rate_limit.py` | **Create** — Rate limiter setup, key functions, storage config |
| `backend/app/core/config.py` | **Update** — Add rate limit settings |
| `backend/app/core/middleware.py` | **Update** — Register rate limit middleware |
| `backend/app/auth/router.py` | **Update** — Apply endpoint-specific limits |
| `backend/requirements.txt` | **Update** — Add `slowapi` |
| `backend/.env` | **Update** — Add rate limit config |
| `backend/tests/test_rate_limit.py` | **Create** — Rate limit tests |

### Task Reference

- **T-AUTH-008:** Implement Rate Limiting Middleware
- **T-CORE-003:** Implement rate limiting middleware (slowapi + Redis)

## 8. Testing Strategy

### Test Cases

| Test | Expected Behavior |
|------|-------------------|
| Request within limit | 200 OK + rate limit headers |
| Request at limit boundary | 200 OK + `X-RateLimit-Remaining: 0` |
| Request exceeding limit | 429 + `Retry-After` header |
| Wait for window reset + retry | 200 OK |
| Authenticated request with user key | Per-user limit applied |
| Unauthenticated request with IP key | Per-IP limit applied |
| Redis unavailable (dev) | 200 OK + warning log |
| Redis unavailable (prod) | In-memory fallback |
| Rate limit disabled via config | All requests pass |

### Development/Test Environment

In test environments, rate limiting should be:
- Disabled by default (`RATE_LIMIT_ENABLED=false`)
- Enabled explicitly for rate limit tests
- Never block the test suite unexpectedly

## 9. Monitoring & Alerting

### Metrics to Track

- Rate limit hits per endpoint per minute
- 429 responses per minute
- Top rate-limited IPs
- Top rate-limited users
- Redis rate limit key count

### Alerts

- **High 429 rate** (>10% of requests) → Potential DDoS or misconfigured client
- **Redis rate limit storage unavailable** → Fallback active, investigate
- **Single IP generating >50% of rate limited requests** → Potential attack

## 10. Bypass Policy

| Scenario | Policy |
|----------|--------|
| Internal health checks | Exempt `/health` from strict limits |
| Razorpay webhooks | Higher limit (100/min), IP whitelist in production |
| Load testing | Disable via `RATE_LIMIT_ENABLED=false` |
| Development | Disable by default |
| CI/CD test runs | Disable by default |
