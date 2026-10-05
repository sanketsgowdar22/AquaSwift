# WoW — Agent Governance

This file defines the rules, conventions, and development workflow for all AI coding agents working on the WoW (Water on Way) platform.

---

## 1. Project Identity

- **Name:** WoW — Water on Way
- **Domain:** Water tanker delivery platform for Hyderabad
- **Legacy Name:** AquaSwift (fully renamed — do not reintroduce)
- **Architecture:** Modular monolith (FastAPI backend) + Next.js frontend (3 apps in one repo)

---

## 2. Repository Structure

```
WoW/
├── backend/              FastAPI backend (Python 3.12)
│   ├── app/              20 domain modules + core
│   │   ├── core/         Config, DB, Auth, Middleware, Errors, Pagination
│   │   ├── auth/         OTP + JWT authentication
│   │   ├── rbac/         Role-based access control
│   │   ├── users/        User management
│   │   ├── addresses/    Customer addresses
│   │   ├── catalog/      Water purposes, quality, variants
│   │   ├── quality/      Water quality records
│   │   ├── sources/      Water sources
│   │   ├── inventory/    Append-only ledger
│   │   ├── pricing/      Rules engine
│   │   ├── coupons/      Coupon management
│   │   ├── orders/       Order state machine
│   │   ├── payments/     Razorpay integration
│   │   ├── deliveries/   Delivery tracking + driver assignment
│   │   ├── drivers/      Driver profiles
│   │   ├── vehicles/     Vehicle management
│   │   ├── notifications/ Push + SMS notifications
│   │   ├── reviews/      Order reviews
│   │   ├── businesses/   B2B entities
│   │   └── admin/        Admin aggregation endpoints
│   ├── alembic/          Database migrations
│   ├── scripts/          Seed data, utilities
│   ├── tests/            Test suite
│   └── Dockerfile        Multi-stage (dev + prod)
├── frontend/             Next.js 16 monorepo
│   ├── app/
│   │   ├── (customer)/app/  Customer PWA (mobile-first)
│   │   ├── driver/          Driver portal (mobile-first)
│   │   ├── admin/           Admin dashboard (17 pages)
│   │   └── login/           Auth page
│   ├── components/       Shared components (WowLogo, MapView)
│   └── lib/              Auth context, API client, utils
├── docs/
│   ├── 00-product/       PRD, Vision, Personas, Journeys, Scope, Glossary
│   ├── 01-requirements/  SRS, FR, NFR, Business Rules, Traceability
│   ├── 02-modules/       27 modules × (Tasks, User Stories, Acceptance Criteria)
│   ├── 03-architecture/  System, API, DB, ERD, State Machines, Integrations
│   ├── 04-phases/        Phase roadmap (P0–P7) + Traceability Matrix
│   ├── 05-security/      Rate limiting, auth security, RBAC
│   └── 06-migrations/    AquaSwift → WoW migration
├── docker-compose.yml    Postgres + Redis + Backend + Celery
├── AGENTS.md             This file
└── README.md
```

---

## 3. Development Phase Order

Development follows a strict phase order. Do not skip phases.

```
P0  Audit & Foundation        (Documentation, governance, planning)
P1  Core Platform & Security  (Auth hardening, rate limiting, test infra, migrations)
P2  Customer App              (Connect UI to real APIs, order lifecycle)
P3  Driver App                (Connect UI to real APIs, delivery lifecycle)
P4  Customer + Driver Integration (End-to-end order→delivery lifecycle)
P5  Admin Dashboard           (Connect admin UI to real APIs)
P6  E2E Validation            (Cross-app testing)
P7  Production Readiness      (CI/CD, monitoring, deployment)
```

### Phase Gates

An agent MUST NOT move to the next phase unless the current phase's exit criteria are met.

Before starting work, identify which phase the work belongs to.

If the work belongs to a phase that has not been reached, document it as a future task rather than implementing it.

---

## 4. Documentation Hierarchy

Every implementation must be traceable:

```
PRD → SRS → Phase → Module → User Story → Task → Implementation → Test → Acceptance
```

### Rules

- Do not create tasks without a module
- Do not create modules without a phase
- Do not implement features without tasks
- Do not claim completion without acceptance criteria passing
- Do not mark a phase complete without exit criteria passing

### Documentation Locations

| What | Where |
|------|-------|
| Product requirements | `docs/00-product/` |
| Technical requirements | `docs/01-requirements/` |
| Module docs (tasks, stories, AC) | `docs/02-modules/{module}/` |
| Architecture | `docs/03-architecture/` |
| Phase roadmaps | `docs/04-phases/` |
| Security docs | `docs/05-security/` |
| Migration tracking | `docs/06-migrations/` |

---

## 5. Task Governance

### Existing Tasks

The project has **157 existing tasks** across 27 modules. These are project planning assets.

**Rules:**
- Do NOT delete existing tasks
- Do NOT recreate tasks that already exist
- DO update task status when implementation changes
- DO add phase tags when organizing
- DO split tasks only when genuinely necessary
- DO verify implementation before marking complete

### Task ID Convention

Tasks follow the pattern: `T-{MODULE}-{NNN}`

Examples: `T-AUTH-001`, `T-ORD-003`, `T-DEL-007`

### Task Status Values

```
NOT_STARTED      — No implementation exists
IN_PROGRESS      — Partially implemented
BLOCKED          — Waiting on dependency
IMPLEMENTED      — Code exists, not tested
TESTED           — Tests pass
ACCEPTED         — Acceptance criteria verified
DEFERRED         — Intentionally postponed
DEPRECATED       — No longer required
```

Do not change status without inspecting implementation.

---

## 6. Preservation Rules

### MANDATORY: Inspect → Understand → Reuse → Update → Extend

Before modifying any existing code or documentation:

1. **Read** the existing file
2. **Understand** the intent
3. **Reuse** existing patterns
4. **Update** where necessary
5. **Extend** with new functionality

### DO NOT

- Delete working modules
- Rewrite the backend framework
- Replace the database technology
- Change the authentication architecture
- Duplicate existing documentation
- Create parallel task systems
- Introduce new frameworks without explicit approval
- Remove existing comments/docstrings unrelated to your changes

---

## 7. Backend Conventions

### Module Structure

Every backend module follows:
```
app/{module}/
├── __init__.py
├── models.py      # SQLAlchemy models
├── schemas.py     # Pydantic request/response schemas
├── service.py     # Business logic
└── router.py      # FastAPI endpoints
```

### Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| API | FastAPI + Uvicorn | Latest |
| ORM | SQLAlchemy 2.0 (async) | 2.0+ |
| Database | PostgreSQL | 15 |
| Cache/Broker | Redis | 7 |
| Jobs | Celery + Celery Beat | 5.4 |
| Auth | JWT (access + refresh) | — |
| SMS | MSG91 | — |
| Payments | Razorpay | — |
| Push | Firebase Cloud Messaging | — |

### API Conventions

- All endpoints prefixed: `/auth/`, `/users/`, `/admin/{module}/`
- Standard error envelope: `{ code, message, details }`
- Cursor-based pagination for list endpoints
- Offset-based pagination for admin/reports
- Idempotency keys on mutation endpoints
- All protected endpoints require `Authorization: Bearer <jwt>`

---

## 8. Frontend Conventions

### Application Routing

| App | Route Prefix | Target |
|-----|-------------|--------|
| Customer | `/(customer)/app/` | Mobile-first PWA |
| Driver | `/driver/` | Mobile-first portal |
| Admin | `/admin/` | Desktop dashboard |
| Auth | `/login/` | Shared login |

### Mock Data → Real API Migration

The current frontend uses hardcoded mock data. Migration rule:

```
1. Identify mock data in component
2. Identify corresponding backend API
3. Verify API contract (schemas match)
4. Replace mock with API call (using lib/api.ts)
5. Add loading state
6. Add empty state
7. Add error state
8. Add auth header
9. Test with real backend
```

Do NOT delete mock UI. Convert it to API-connected functionality.

---

## 9. Security Requirements

### Rate Limiting (Mandatory — Phase 1)

The platform MUST have rate limiting. See `docs/05-security/rate-limiting.md`.

No endpoint should be exposed without consideration for abuse.

### Demo Authentication Bypass

A temporary demo mode exists in `frontend/lib/auth.tsx` (lines 35-47).

This MUST be reverted as part of Phase 1. Do not leave it enabled.

### Authentication

- Customer: OTP-based (phone → SMS → verify → JWT)
- Admin/Driver: Email + password → JWT
- All tokens: short-lived access (1h) + long-lived refresh (30d)
- Server-side authorization enforcement (never client-only)

---

## 10. Water Type & Usage Purpose

The system supports configurable water purposes. Do NOT hardcode.

The catalog model supports:
```
Water Purpose    → Drinking, Construction, Daily Use, etc.
Quality Type     → RO+UV, Filtered, Bore, etc.
Delivery Method  → Tanker, Can, Pipeline, etc.
Water Variant    → Purpose × Quality × Method (with quantity ranges)
```

This concept is backend-authoritative. Do not duplicate catalog logic in frontend.

---

## 11. Testing Requirements

### Current State

Only 1 test exists (`tests/test_health.py`). Test infrastructure must be built in Phase 1.

### Test Hierarchy

```
Unit Tests         → Service layer logic
API Tests          → Router endpoints (httpx + AsyncClient)
Integration Tests  → Cross-module workflows
Frontend Tests     → Component + E2E (Playwright)
Security Tests     → Rate limiting, auth, authorization
```

### Rule

Do not claim a feature is complete without corresponding tests.

---

## 12. Change Impact Analysis

Before modifying a module, consider:

- Affected APIs
- Affected database models
- Affected frontend pages
- Affected tests
- Cross-module dependencies
- State machine implications
- Potential regressions

Document significant changes in the relevant phase/task docs.

---

## 13. Git Conventions

- Commit messages: `[phase] module: description`
  - Example: `[P1] auth: revert demo authentication bypass`
  - Example: `[P2] orders: connect order creation UI to backend API`
- Do not commit temporary/debug code
- Do not commit demo authentication bypasses
- Do not commit hardcoded credentials

---

## 14. Forbidden Actions

1. **Do not claim production readiness** without validation
2. **Do not mark tasks complete** without verifying implementation
3. **Do not skip phases** without documenting why
4. **Do not introduce "AquaSwift"** anywhere in new code
5. **Do not hardcode water types** — use the catalog system
6. **Do not duplicate business logic** in frontend
7. **Do not leave demo auth enabled** in any branch intended for deployment
8. **Do not create parallel documentation** that contradicts existing docs
9. **Do not implement Phase N+1 work** while Phase N exit criteria are unmet
10. **Do not invent task IDs** that conflict with existing ones

---

## 15. Decision-Making Process

When facing an ambiguous requirement:

1. Check `docs/01-requirements/SRS.md`
2. Check `docs/00-product/PRD.md`
3. Check relevant module docs in `docs/02-modules/`
4. Check architecture docs in `docs/03-architecture/`
5. If still ambiguous, document the decision and rationale
6. If high-impact, request project owner approval before implementing
