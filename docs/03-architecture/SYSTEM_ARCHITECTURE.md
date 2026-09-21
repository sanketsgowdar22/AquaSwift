# AquaSwift — System Architecture

**Version:** 1.0
**Status:** Draft
**Last Updated:** 2026-09-03

---

## 1. Architecture Overview

AquaSwift is a **modular monolith** (DEC-ARCH-001) — a single deployable backend serving three client applications through a unified REST API.

```
┌─────────────────┐  ┌──────────────────┐  ┌───────────────────┐
│  Customer App   │  │   Driver App     │  │  Admin Dashboard  │
│  (Flutter)      │  │   (Flutter)      │  │  (Next.js + TS)   │
│  Android + iOS  │  │   Android + iOS  │  │  Web              │
└────────┬────────┘  └────────┬─────────┘  └─────────┬─────────┘
         │                    │                       │
         └────────────────────┼───────────────────────┘
                              │ HTTPS / REST
                              ▼
                   ┌──────────────────────┐
                   │   API Gateway /      │
                   │   Load Balancer      │
                   └──────────┬───────────┘
                              │
                   ┌──────────▼───────────┐
                   │   FastAPI Backend    │
                   │   (Modular Monolith) │
                   │                      │
                   │  ┌─────────────────┐ │
                   │  │ Auth │ RBAC     │ │
                   │  │ Users│ Catalog  │ │
                   │  │ Inventory│Pricing│ │
                   │  │ Orders│Deliveries│ │
                   │  │ Payments│ ...    │ │
                   │  └─────────────────┘ │
                   └───┬──────┬───────┬───┘
                       │      │       │
              ┌────────▼┐ ┌───▼────┐ ┌▼────────────┐
              │PostgreSQL│ │ Redis  │ │Celery Workers│
              │  (RDS)   │ │(Cache/ │ │  + Beat      │
              │          │ │ Broker)│ │              │
              └──────────┘ └────────┘ └──────────────┘
                                            │
                              ┌─────────────┼──────────────┐
                              ▼             ▼              ▼
                        ┌──────────┐ ┌──────────┐ ┌────────────┐
                        │ Razorpay │ │  MSG91   │ │   FCM      │
                        │(Payments)│ │(SMS/OTP) │ │  (Push)    │
                        └──────────┘ └──────────┘ └────────────┘
```

---

## 2. Technology Stack

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| **Customer App** | Flutter + Dart | Latest stable | Cross-platform (Android + iOS) from single codebase |
| **Driver App** | Flutter + Dart | Latest stable | Shared codebase patterns with customer app |
| **Admin Dashboard** | Next.js + TypeScript + Tailwind CSS | Latest stable | React ecosystem, SSR, TypeScript for type safety |
| **Backend** | Python + FastAPI | 3.11+ / 0.100+ | Async-capable, auto OpenAPI docs, Pydantic validation |
| **ORM** | SQLAlchemy + Alembic | 2.0+ | Explicit transactions, migration management |
| **Database** | PostgreSQL | 15+ | JSONB, strong transactions, robust indexing |
| **Cache / Broker** | Redis | 7+ | Catalog caching, Celery message broker |
| **Background Jobs** | Celery + Celery Beat | 5+ | Reservation expiry, report aggregation, notifications |
| **Object Storage** | AWS S3 | — | Delivery proof photos, quality certificates |
| **Maps** | Google Maps Platform | — | Geocoding, distance calculation |
| **Payments** | Razorpay | — | India-focused, gateway-hosted checkout |
| **SMS/OTP** | MSG91 | — | India DLT-compliant, dedicated OTP APIs |
| **Push** | Firebase Cloud Messaging (FCM) | — | Android + iOS push notifications |
| **Email** | SendGrid / AWS SES | — | Transactional email |
| **Containers** | Docker + docker-compose | — | Local development environment |
| **Cloud** | AWS (ECS/Fargate, RDS, ElastiCache, S3) | — | Production infrastructure |
| **CI/CD** | GitHub Actions | — | Lint, test, build, deploy |
| **Monitoring** | CloudWatch + Sentry | — | Metrics, alerting, error tracking |

See DEC-ARCH-002 for stack rationale.

---

## 3. Repository Structure

```
aquaswift/
├── backend/
│   ├── app/
│   │   ├── auth/              # Authentication & Identity
│   │   │   ├── models.py
│   │   │   ├── schemas.py     # Pydantic request/response
│   │   │   ├── service.py     # Business logic
│   │   │   ├── router.py      # FastAPI endpoints
│   │   │   └── tests/
│   │   ├── rbac/              # RBAC & Permissions
│   │   ├── users/             # User & Customer Management
│   │   ├── customers/         # Customer profiles
│   │   ├── businesses/        # B2B businesses
│   │   ├── sites/             # Business sites
│   │   ├── addresses/         # Address management
│   │   ├── catalog/           # Water purposes, quality, methods, variants
│   │   ├── quality/           # Water quality records
│   │   ├── inventory/         # Sources, ledger, balances
│   │   ├── pricing/           # Pricing rules, PricingService
│   │   ├── coupons/           # Coupon management
│   │   ├── orders/            # Order system + state machine
│   │   ├── deliveries/        # Delivery system + dispatch
│   │   ├── drivers/           # Driver management
│   │   ├── vehicles/          # Vehicle / Fleet
│   │   ├── payments/          # Payment processing
│   │   ├── refunds/           # Refund processing
│   │   ├── notifications/     # Channel-agnostic notification service
│   │   ├── reviews/           # Reviews / Ratings
│   │   ├── admin/             # Admin operations, dashboard
│   │   ├── reports/           # Reporting / aggregation
│   │   ├── analytics/         # Analytics (Phase 2)
│   │   ├── bulk_orders/       # Bulk order workflow
│   │   ├── recurring_orders/  # Recurring order workflow
│   │   ├── invoices/          # Invoicing (Phase 2)
│   │   ├── routes/            # Route optimization (stub)
│   │   ├── audit/             # Audit logging
│   │   ├── core/              # Cross-cutting concerns
│   │   │   ├── config.py      # Typed settings (Pydantic BaseSettings)
│   │   │   ├── database.py    # SQLAlchemy engine, session factory
│   │   │   ├── security.py    # JWT creation/verification, password hashing
│   │   │   ├── dependencies.py # require_permission(), get_current_user()
│   │   │   ├── exceptions.py  # Structured error classes
│   │   │   ├── middleware.py   # CORS, rate limiting, request logging
│   │   │   ├── pagination.py  # Cursor/offset pagination utilities
│   │   │   ├── cache.py       # Redis cache utilities
│   │   │   └── audit.py       # Audit logger utility
│   │   └── main.py            # FastAPI app factory, router registration
│   ├── alembic/               # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── tests/                 # Integration / E2E tests
│   ├── scripts/               # Seed data, utilities
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── customer_app/              # Flutter customer app
│   ├── lib/
│   │   ├── features/          # Feature-first organization
│   │   ├── core/              # Shared services, models, config
│   │   └── main.dart
│   └── pubspec.yaml
├── driver_app/                # Flutter driver app
│   ├── lib/
│   │   ├── features/
│   │   ├── core/
│   │   └── main.dart
│   └── pubspec.yaml
├── admin_web/                 # Next.js admin dashboard
│   ├── src/
│   │   ├── app/               # App router pages
│   │   ├── components/        # Shared UI components
│   │   ├── lib/               # API client, utilities
│   │   └── types/             # TypeScript type definitions
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml         # Local dev: Postgres, Redis, backend, admin
├── .github/
│   └── workflows/
│       ├── backend.yml        # Backend CI (lint, test, build)
│       ├── admin.yml          # Admin dashboard CI
│       └── mobile.yml         # Flutter CI
├── docs/                      # All documentation (Phase 0 output)
└── .env.example               # Root environment template
```

### Module Internal Structure

Every backend module follows this consistent pattern:

```
backend/app/<module>/
├── __init__.py
├── models.py       # SQLAlchemy models (tables)
├── schemas.py      # Pydantic request/response schemas
├── service.py      # Business logic (all domain logic lives here)
├── router.py       # FastAPI route definitions (thin — delegates to service)
├── dependencies.py # Module-specific FastAPI dependencies (optional)
├── constants.py    # Module constants, enums (optional)
├── exceptions.py   # Module-specific exception classes (optional)
└── tests/
    ├── test_service.py  # Unit tests for business logic
    ├── test_router.py   # Integration tests for endpoints
    └── conftest.py      # Test fixtures
```

**Key rule**: Business logic lives in `service.py`, never inline in routers. Routers are thin wrappers that parse requests, call services, and format responses.

---

## 4. Module Dependency Graph

Modules are organized in dependency layers. A module may only depend on modules in the same or lower layers. No circular dependencies.

```
Layer 0 (Foundation):
  core → (no module dependencies — config, db, security, exceptions)

Layer 1 (Identity):
  auth → core
  rbac → core, auth
  users → core, auth, rbac

Layer 2 (Data Configuration):
  addresses → core, auth, rbac
  catalog → core, auth, rbac, audit
  quality → core, auth, rbac, catalog, audit
  sources → core, auth, rbac, audit

Layer 3 (Business Logic):
  inventory → core, auth, rbac, sources, audit
  pricing → core, auth, rbac, catalog, audit
  coupons → core, auth, rbac, audit

Layer 4 (Commerce):
  orders → core, auth, rbac, users, addresses, catalog, inventory, pricing, coupons, audit
  payments → core, auth, rbac, orders, audit
  refunds → core, auth, rbac, payments, orders, audit

Layer 5 (Fulfilment):
  deliveries → core, auth, rbac, orders, inventory, drivers, vehicles, audit
  drivers → core, auth, rbac, users, vehicles
  vehicles → core, auth, rbac, audit

Layer 6 (Communication):
  notifications → core, auth, users (all lifecycle modules emit events)
  reviews → core, auth, rbac, orders, deliveries

Layer 7 (Operations):
  admin → core, auth, rbac (orchestrates across all modules)
  reports → core, auth, rbac, orders, deliveries, inventory, users
  audit → core (standalone — called by all modules)

Layer 8 (B2B / Future):
  businesses → core, auth, rbac, users, addresses
  bulk_orders → core, auth, rbac, businesses, orders, pricing
  recurring_orders → core, auth, rbac, orders, pricing
  invoices → core, auth, rbac, businesses, orders, payments
  routes → core, deliveries, drivers, addresses
  analytics → core, auth, rbac, orders, deliveries, inventory
```

```mermaid
graph TD
    CORE[core] --> AUTH[auth]
    CORE --> RBAC[rbac]
    AUTH --> RBAC
    RBAC --> USR[users]
    RBAC --> ADDR[addresses]
    RBAC --> CAT[catalog]
    RBAC --> QUAL[quality]
    RBAC --> SRC[sources]
    SRC --> INV[inventory]
    CAT --> PRC[pricing]
    RBAC --> CPN[coupons]
    INV --> ORD[orders]
    PRC --> ORD
    CPN --> ORD
    ORD --> PAY[payments]
    PAY --> RFD[refunds]
    ORD --> DEL[deliveries]
    INV --> DEL
    RBAC --> DRV[drivers]
    RBAC --> VEH[vehicles]
    DRV --> DEL
    VEH --> DEL
    ORD --> REV[reviews]
    DEL --> REV
    USR --> NTF[notifications]
    ORD --> RPT[reports]
    DEL --> RPT
    INV --> RPT
    RBAC --> ADM[admin]
    CORE --> AUD[audit]
    USR --> BIZ[businesses]
    BIZ --> BULK[bulk_orders]
    ORD --> REC[recurring_orders]
    BIZ --> INVC[invoices]
    DEL --> RTE[routes]
    ORD --> ANL[analytics]
```

---

## 5. Cross-Cutting Concerns

### 5.1 Authentication & Authorization

All protected endpoints use a two-layer security model:

1. **Authentication**: `get_current_user()` FastAPI dependency extracts and validates the JWT from the `Authorization: Bearer <token>` header. Returns the authenticated user or raises 401.

2. **Authorization**: `require_permission("resource:action")` FastAPI dependency checks whether the authenticated user's role grants the required permission. Returns 403 if insufficient.

```python
# Example endpoint with auth + RBAC
@router.post("/admin/water-purposes")
async def create_purpose(
    data: PurposeCreate,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permission("catalog:write")),
    db: AsyncSession = Depends(get_db),
):
    return await catalog_service.create_purpose(db, data, current_user)
```

### 5.2 Error Handling

All errors use a standardized error envelope. Clients branch on `code`, never on `message`:

```json
{
  "code": "INVENTORY_INSUFFICIENT",
  "message": "Requested quantity exceeds available inventory at all sources.",
  "details": {
    "requested_litres": 5000,
    "max_available_litres": 3200,
    "source_id": "uuid..."
  }
}
```

Standard error codes per module are defined in each module's `exceptions.py`. HTTP status codes:
- `400` — Validation error, business rule violation
- `401` — Missing or invalid authentication
- `403` — Insufficient permissions
- `404` — Resource not found
- `409` — Conflict (idempotency key, state machine violation)
- `422` — Request schema validation failure
- `429` — Rate limit exceeded
- `500` — Unexpected server error

### 5.3 Database Transactions

Every mutating endpoint is wrapped in an explicit database transaction:

```python
async with db.begin():
    order = await order_service.create_order(db, data, user)
    await inventory_service.reserve(db, order)
    payment = await payment_service.create_intent(db, order)
    # If any step raises, the entire transaction rolls back
```

The `get_db()` dependency provides a session-per-request with automatic rollback on exception.

### 5.4 Caching Strategy

| Data | Cache Type | TTL | Invalidation |
|------|-----------|-----|--------------|
| Catalog (purposes, qualities, methods, variants) | Redis | ≤ 60s | On any catalog write |
| Pricing rules (active) | Redis | ≤ 60s | On pricing rule write |
| Inventory balances | Not cached | — | Derived from ledger on each request |
| User sessions / JWT | Not cached | — | JWT is self-contained; verify signature |
| Report aggregations | Redis/DB | Job-based | Rebuilt on scheduled Celery jobs |

### 5.5 Background Job Architecture

```
┌─────────────────────────────────────────────┐
│              Celery Workers                  │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │ reservation_expiry_task (Beat: 1min)  │   │
│  │ - Find PENDING_PAYMENT orders past    │   │
│  │   timeout → release inventory → FAIL  │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │ send_notification_task (on-demand)    │   │
│  │ - Send push/SMS/email via adapters    │   │
│  │ - Retry with fallback on failure      │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │ report_aggregation_task (Beat: daily) │   │
│  │ - Aggregate sales, delivery, customer │   │
│  │   metrics into report tables          │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │ reconciliation_task (Beat: hourly)    │   │
│  │ - Verify inventory conservation law   │   │
│  │ - Alert on discrepancy               │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │ recurring_order_task (Beat: daily)    │   │ (Phase 2)
│  │ - Generate order instances for        │   │
│  │   upcoming scheduled dates            │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### 5.6 Structured Logging

All log entries include:
- `timestamp` (UTC ISO 8601)
- `level` (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `module` (originating module name)
- `request_id` (correlation ID for request tracing)
- `user_id` (authenticated user, if any)
- `action` (what happened)
- `details` (structured context — JSON)

Format: JSON lines for machine parsing by CloudWatch/log aggregation.

---

## 6. Deployment Architecture

### 6.1 Local Development

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: aquaswift
      POSTGRES_USER: aquaswift
      POSTGRES_PASSWORD: dev_password
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports: ["8000:8000"]
    depends_on: [postgres, redis]
    environment:
      - DATABASE_URL=postgresql+asyncpg://aquaswift:dev_password@postgres/aquaswift
      - REDIS_URL=redis://redis:6379/0
    volumes: ["./backend:/app"]

  celery_worker:
    build: ./backend
    command: celery -A app.core.celery_app worker --loglevel=info
    depends_on: [postgres, redis]

  celery_beat:
    build: ./backend
    command: celery -A app.core.celery_app beat --loglevel=info
    depends_on: [postgres, redis]

  admin_web:
    build: ./admin_web
    command: npm run dev
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 6.2 Production (AWS)

```
┌─────────────────────────────────────────────────────────────┐
│                         AWS VPC                              │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 Public Subnet                        │    │
│  │  ┌──────────────────┐  ┌───────────────────────┐   │    │
│  │  │ ALB (Load         │  │ CloudFront (CDN)      │   │    │
│  │  │ Balancer)          │  │ - Admin static assets │   │    │
│  │  │ - SSL termination  │  │ - Customer app assets │   │    │
│  │  └────────┬───────────┘  └───────────────────────┘   │    │
│  └───────────┼──────────────────────────────────────────┘    │
│              │                                               │
│  ┌───────────▼──────────────────────────────────────────┐    │
│  │                 Private Subnet                        │    │
│  │                                                       │    │
│  │  ┌──────────────────────────────────────────────┐    │    │
│  │  │ ECS/Fargate Cluster                          │    │    │
│  │  │                                              │    │    │
│  │  │  ┌─────────────┐  ┌─────────────────────┐   │    │    │
│  │  │  │ Backend     │  │ Celery Workers (2+)  │   │    │    │
│  │  │  │ Service     │  │                      │   │    │    │
│  │  │  │ (2+ tasks)  │  │ Celery Beat (1 task) │   │    │    │
│  │  │  └─────────────┘  └─────────────────────┘   │    │    │
│  │  │                                              │    │    │
│  │  │  ┌─────────────────────────────────────┐     │    │    │
│  │  │  │ Admin Dashboard (Next.js)           │     │    │    │
│  │  │  └─────────────────────────────────────┘     │    │    │
│  │  └──────────────────────────────────────────────┘    │    │
│  │                                                       │    │
│  │  ┌──────────────┐  ┌────────────────┐                │    │
│  │  │ RDS Postgres  │  │ ElastiCache    │                │    │
│  │  │ (Primary +    │  │ Redis          │                │    │
│  │  │  Read Replica)│  │                │                │    │
│  │  └──────────────┘  └────────────────┘                │    │
│  │                                                       │    │
│  │  ┌──────────────┐                                    │    │
│  │  │ S3 Bucket    │                                    │    │
│  │  │ (Photos,     │                                    │    │
│  │  │  Certs)      │                                    │    │
│  │  └──────────────┘                                    │    │
│  └───────────────────────────────────────────────────────┘    │
│                                                              │
│  Monitoring: CloudWatch + Sentry                             │
│  Secrets: AWS Secrets Manager / Parameter Store              │
└──────────────────────────────────────────────────────────────┘
```

### 6.3 CI/CD Pipeline

```
GitHub PR → GitHub Actions
  ├── Backend:
  │   ├── Lint (ruff, black --check)
  │   ├── Type check (mypy)
  │   ├── Unit tests (pytest)
  │   ├── Integration tests (pytest + test DB)
  │   └── Build Docker image
  ├── Admin Web:
  │   ├── Lint (ESLint)
  │   ├── Type check (tsc --noEmit)
  │   ├── Unit tests (Jest/Vitest)
  │   └── Build
  └── Mobile:
      ├── Lint (dart analyze)
      ├── Unit tests (flutter test)
      └── Build (Android APK, iOS)

On merge to main:
  ├── Build & push Docker images to ECR
  ├── Run database migrations (Alembic)
  └── Deploy to staging → manual promotion to production
```

---

## 7. Security Architecture

### 7.1 Authentication Flow

```
Customer/Driver (OTP):
  Client → POST /auth/otp/request {phone} → Server → MSG91 → SMS → User
  Client → POST /auth/otp/verify {phone, otp} → Server verifies → JWT + Refresh Token

Admin (Email/Password):
  Client → POST /auth/login {email, password} → Server verifies bcrypt hash → JWT + Refresh Token

Token Refresh:
  Client → POST /auth/refresh {refresh_token} → Server validates → New JWT + New Refresh Token
```

### 7.2 RBAC Permission Model

```
Role: CUSTOMER
  Permissions: orders:create, orders:read:own, addresses:crud:own,
               reviews:create, catalog:read, profile:crud:own

Role: DRIVER
  Permissions: deliveries:read:assigned, deliveries:respond,
               deliveries:update:assigned, drivers:read:own,
               drivers:update:own, earnings:read:own

Role: OPS_MANAGER
  Permissions: orders:read, orders:cancel, deliveries:read,
               deliveries:assign, deliveries:reassign, inventory:read,
               inventory:adjust, drivers:read, vehicles:read,
               customers:read, reports:read, audit:read

Role: SUPER_ADMIN
  Permissions: * (all permissions)
```

### 7.3 API Security

| Control | Implementation |
|---------|---------------|
| Authentication | JWT verification on every protected endpoint |
| Authorization | `require_permission()` RBAC check |
| Rate Limiting | Redis-backed token bucket on /auth/* endpoints |
| Input Validation | Pydantic schema validation on all requests |
| SQL Injection | SQLAlchemy parameterized queries (never raw SQL) |
| CORS | Explicit allow-list of origins (no wildcards in production) |
| TLS | All traffic encrypted via ALB SSL termination |
| Secrets | Environment variables via AWS Secrets Manager |
| Payment Data | Gateway-hosted fields only — zero PCI scope |
| Idempotency | `Idempotency-Key` header on POST /orders, POST /payments/verify |
