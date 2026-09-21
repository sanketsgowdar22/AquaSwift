# AquaSwift — Product Scope

**Version:** 1.0
**Last Updated:** 2026-08-31

---

## Scope Classification Framework

Every feature/capability is classified into one of four tiers:

| Tier | Meaning | Documentation | Implementation |
|------|---------|---------------|----------------|
| **MUST HAVE — V1** | Required for MVP launch | Full or Backend-only package | Fully built and tested |
| **SHOULD HAVE — V1** | Important for V1 completeness, not blocking launch | Full or Backend-only package | Built if time permits; may ship with reduced scope |
| **PHASE 2** | Planned for next major release | Deferred | Not implemented |
| **ARCHITECTURE ONLY** | Schema and stubs exist for forward compatibility | Reduced package (DATA_MODEL, API_SPEC, BUSINESS_RULES, STATE_MACHINE) | DB schema + basic CRUD endpoints, no customer-facing UI |

---

## V1 Scope — Detailed Breakdown

### Customer Mobile App (Flutter)

| Feature | Classification | Notes |
|---------|---------------|-------|
| OTP-based registration & login | MUST HAVE — V1 | MSG91 adapter |
| Home screen with dynamic purpose cards | MUST HAVE — V1 | Driven by catalog API, not hard-coded |
| Purpose → Quality → Quantity → Method selection | MUST HAVE — V1 | Full catalog browsing flow |
| Address/site management (add, edit, select) | MUST HAVE — V1 | Google Maps geocoding |
| Time slot / scheduling selection | MUST HAVE — V1 | Configurable delivery windows |
| Price quote preview | MUST HAVE — V1 | `PricingService.quote()` call |
| Coupon application | SHOULD HAVE — V1 | Coupon validation + discount display |
| Checkout & payment (Razorpay) | MUST HAVE — V1 | Server-side intent, gateway checkout |
| Order confirmation & summary | MUST HAVE — V1 | Commercial snapshot display |
| Order status tracking (polling) | MUST HAVE — V1 | Status polling, no WebSockets |
| Order history & detail view | MUST HAVE — V1 | Paginated list + detail |
| Reorder from history | SHOULD HAVE — V1 | Pre-fill from previous order |
| Rate & review delivery | SHOULD HAVE — V1 | Post-delivery rating flow |
| Profile management | MUST HAVE — V1 | Name, phone, email |
| Push notifications | MUST HAVE — V1 | FCM integration |
| Business registration (B2B) | ARCHITECTURE ONLY | Schema exists, no customer UI |
| Bulk order request | ARCHITECTURE ONLY | Schema exists, no customer UI |
| Recurring order setup | ARCHITECTURE ONLY | Schema exists, no customer UI |
| Real-time GPS tracking | PHASE 2 | WebSocket-based |

### Driver Mobile App (Flutter)

| Feature | Classification | Notes |
|---------|---------------|-------|
| OTP-based login | MUST HAVE — V1 | Shared auth with customer app |
| Availability toggle (online/offline) | MUST HAVE — V1 | Driver status management |
| Delivery offer notifications | MUST HAVE — V1 | Push notification + in-app |
| Accept/reject delivery offers | MUST HAVE — V1 | With timeout and reassignment |
| Active delivery view (details, navigation link) | MUST HAVE — V1 | Deep link to Google Maps |
| Trip status updates (started → arrived → delivered) | MUST HAVE — V1 | State machine transitions |
| OTP-based proof of delivery | MUST HAVE — V1 | Customer provides OTP to driver |
| Photo proof upload | SHOULD HAVE — V1 | S3 upload |
| Delivery history | MUST HAVE — V1 | Paginated list |
| Earnings summary & breakdown | MUST HAVE — V1 | Daily/weekly/monthly |
| Profile management | MUST HAVE — V1 | Name, phone, vehicle info |
| Push notifications | MUST HAVE — V1 | FCM integration |
| Live location sharing | PHASE 2 | WebSocket + Redis pub/sub |
| Route optimization | PHASE 2 | Multi-stop route planning |

### Admin Web Dashboard (Next.js)

| Feature | Classification | Notes |
|---------|---------------|-------|
| Email + password login | MUST HAVE — V1 | JWT-based, RBAC-enforced |
| Dashboard summary (orders, revenue, alerts) | MUST HAVE — V1 | Aggregated metrics |
| Water catalog CRUD (purposes, qualities, methods) | MUST HAVE — V1 | Admin-configurable |
| Water variant management | MUST HAVE — V1 | Combination builder |
| Pricing rule management (fixed/per-litre/tiered) | MUST HAVE — V1 | Rule builder UI |
| Coupon/promotion management | SHOULD HAVE — V1 | CRUD + validation |
| Order list & detail view | MUST HAVE — V1 | Filterable, sortable |
| Order lifecycle management (cancel, refund) | MUST HAVE — V1 | Admin manual actions |
| Delivery list & detail view | MUST HAVE — V1 | Status tracking |
| Manual delivery assignment | MUST HAVE — V1 | Admin assigns driver |
| Delivery reassignment | MUST HAVE — V1 | Override current assignment |
| Customer list & detail | MUST HAVE — V1 | View + search |
| Driver CRUD | MUST HAVE — V1 | Add, edit, activate/deactivate |
| Vehicle CRUD | MUST HAVE — V1 | Registration, type, capacity |
| Water source management | MUST HAVE — V1 | Source CRUD + status |
| Inventory ledger viewer | MUST HAVE — V1 | Filterable transaction log |
| Inventory manual adjustment | MUST HAVE — V1 | With mandatory reason + audit |
| Water quality record management | SHOULD HAVE — V1 | Test results, certificates |
| Payment list & detail | MUST HAVE — V1 | View + status |
| Refund management | SHOULD HAVE — V1 | Initiate + track |
| Audit log viewer | MUST HAVE — V1 | Filterable, searchable |
| Sales reports | SHOULD HAVE — V1 | Pre-built report views |
| Water supply/consumption reports | SHOULD HAVE — V1 | Source utilization |
| Delivery performance reports | SHOULD HAVE — V1 | Driver/vehicle metrics |
| Customer reports | SHOULD HAVE — V1 | Retention, order patterns |
| Business/B2B management | ARCHITECTURE ONLY | Schema exists, admin view deferred |
| Bulk order management | ARCHITECTURE ONLY | Schema exists, admin view deferred |
| Recurring order management | ARCHITECTURE ONLY | Schema exists, admin view deferred |
| Invoice management | ARCHITECTURE ONLY | Schema exists, admin view deferred |
| Analytics dashboard | PHASE 2 | Advanced insights |
| Route management | PHASE 2 | Route planning UI |

### Backend (FastAPI)

| Feature | Classification | Notes |
|---------|---------------|-------|
| Auth module (OTP + email/password, JWT, refresh) | MUST HAVE — V1 | |
| RBAC & permissions engine | MUST HAVE — V1 | `require_permission()` dependency |
| User/customer/driver profile management | MUST HAVE — V1 | |
| Address/site management | MUST HAVE — V1 | |
| Water catalog (purposes, qualities, methods, variants) | MUST HAVE — V1 | Admin CRUD + public read |
| Water quality records | SHOULD HAVE — V1 | Source quality tracking |
| Water source management | MUST HAVE — V1 | |
| Inventory ledger (append-only) | MUST HAVE — V1 | Core architectural requirement |
| Inventory balance reconciliation | MUST HAVE — V1 | Derived from ledger |
| Pricing engine (`PricingService.quote()`) | MUST HAVE — V1 | Fixed/per-litre/tiered |
| Coupon system | SHOULD HAVE — V1 | Validation + application |
| Order system (state machine, snapshot, idempotency) | MUST HAVE — V1 | |
| Delivery system (N per order, state machine, OTP) | MUST HAVE — V1 | Includes dispatch/assignment |
| Payment system (intent, webhook, verification) | MUST HAVE — V1 | Razorpay adapter |
| Refund system | SHOULD HAVE — V1 | Gateway-processed refunds |
| Notification service (channel-agnostic) | MUST HAVE — V1 | Push, SMS (MSG91), Email |
| Review/rating system | SHOULD HAVE — V1 | |
| Audit logging | MUST HAVE — V1 | All admin mutations |
| Reporting (scheduled aggregation) | SHOULD HAVE — V1 | |
| Business/B2B endpoints | ARCHITECTURE ONLY | Schema + basic CRUD |
| Bulk order endpoints | ARCHITECTURE ONLY | Schema + state flow |
| Recurring order endpoints | ARCHITECTURE ONLY | Schema + instance generation |
| Invoice endpoints | ARCHITECTURE ONLY | Schema only |
| Route endpoints | ARCHITECTURE ONLY | Stub |
| Analytics | PHASE 2 | |
| Reservation expiry Celery job | MUST HAVE — V1 | Auto-release on timeout |
| Background job infrastructure (Celery + Beat) | MUST HAVE — V1 | |

### Infrastructure & Platform

| Feature | Classification | Notes |
|---------|---------------|-------|
| Docker + docker-compose (local dev) | MUST HAVE — V1 | Postgres, Redis, backend, admin_web |
| GitHub Actions CI/CD | MUST HAVE — V1 | Lint, test, build |
| Environment configuration (`.env.example`, typed settings) | MUST HAVE — V1 | No secrets in code |
| AWS deployment (ECS/Fargate, RDS, ElastiCache, S3) | MUST HAVE — V1 | Production infra |
| Monitoring & alerting (CloudWatch, Sentry) | MUST HAVE — V1 | 5xx rate, webhook failures, etc. |
| Runbook | MUST HAVE — V1 | `docs/RUNBOOK.md` |

---

## Phase 2 Scope — Summary

| Feature Area | Key Capabilities |
|-------------|-----------------|
| Real-time tracking | WebSocket + Redis pub/sub, live driver location on customer map |
| B2B customer UI | Business registration, employee accounts, site management |
| Bulk orders UI | Customer request → admin quote → accept → fulfilment |
| Recurring orders UI | Schedule setup, pause/skip/cancel, instance tracking |
| Invoicing | Period-based B2B invoices, payment terms, statement generation |
| Route optimization | Multi-stop route planning, distance-based dispatch suggestions |
| Analytics | Operational analytics dashboard, trend analysis, cohort analysis |
| Multi-city | Area/zone-based pricing, inventory, dispatch rules |

---

## Phase 3 Scope — Summary

| Feature Area | Key Capabilities |
|-------------|-----------------|
| Marketplace | Multi-supplier model, supplier onboarding, commission structure |
| Subscriptions | Prepaid packages, auto-renewal, credit-based ordering |
| IoT | Smart water level sensors, automatic reorder triggers |
| Advanced fleet | Predictive maintenance, fuel tracking, compliance automation |
| Loyalty | Points, rewards, referral bonuses |
| White-label | Brandable instances, multi-tenant SaaS |
| ML/AI | Demand forecasting, dynamic pricing, intelligent dispatch |

---

## Explicit Non-Goals (V1)

These are **intentionally excluded** from V1 and should not be built, designed for, or discussed as V1 requirements:

1. Real-time GPS tracking (WebSockets)
2. Customer-facing B2B workflows (UI only; backend schema exists)
3. Customer-facing bulk/recurring order UI
4. Algorithmic route optimization
5. Multi-city/multi-operator operations
6. Marketplace / multi-supplier model
7. IoT sensor integration
8. Machine learning / AI features
9. Subscription plans
10. White-label / multi-tenant deployment
11. Social login (Google, Apple, Facebook)
12. Multi-language support (English only for V1)
13. Offline-first mobile app capabilities
14. Third-party delivery partner integration
15. Customer loyalty/rewards program
