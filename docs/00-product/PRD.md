# AquaSwift — Product Requirements Document (PRD)

**Version:** 1.0
**Status:** Draft
**Last Updated:** 2026-08-31
**Owner:** AquaSwift Product Team

---

## 1. Product Vision

AquaSwift is a **production-grade Water Supply, Resource, Inventory, Order, Fleet & Delivery Management Platform** serving the Indian water supply market. It enables customers to order water in any quantity — from a 20-litre jar to a 100,000-litre bulk tanker supply — while operators manage water sources, inventory, pricing, fleet, and delivery from a single integrated system.

The platform comprises three client applications backed by a single modular-monolith backend:
- **Customer Mobile App** (Flutter — Android + iOS): Browse, order, pay, track
- **Driver Mobile App** (Flutter — Android first, iOS-ready): Accept deliveries, navigate, confirm delivery
- **Admin Web Dashboard** (Next.js + TypeScript): Full operational control

---

## 2. Problem Statement

India's water supply industry — especially bulk and tanker delivery — operates with fragmented, manual workflows:

- **Customers** have no transparent way to compare water quality, see real-time availability, or track deliveries. Ordering is done via phone calls, WhatsApp messages, or walk-ins, with no price visibility.
- **Water suppliers** manage orders on paper or basic spreadsheets, leading to lost orders, double-booking, inventory miscounts, and inability to scale.
- **Drivers** receive delivery instructions verbally, with no route optimization, delivery proof, or earnings tracking.
- **Business customers** (construction sites, factories, hotels) need recurring/bulk orders with credit terms and invoicing, which manual processes cannot reliably support.

AquaSwift digitizes the entire workflow end-to-end, providing transparency, reliability, and scalability for all participants.

---

## 3. Product & Business Goals

### 3.1 Product Goals
1. **Unified ordering experience** — A single app for all water needs, from drinking jars to industrial tankers, driven entirely by admin-configurable data (not hard-coded product lists).
2. **Operational efficiency** — Automated inventory tracking, pricing, dispatch, and delivery proof replace manual coordination.
3. **Transparency** — Real-time order status, delivery tracking, pricing breakdown, and water quality information available to all stakeholders.
4. **Scalability** — Modular architecture supporting multi-city expansion, new water types, and B2B workflows without code changes.
5. **Reliability** — Append-only inventory ledger, server-side pricing, state-machine-enforced workflows prevent data corruption and business logic bypasses.

### 3.2 Business Goals
1. Capture India's fragmented water delivery market starting with a single city.
2. Achieve high order completion rates (>95%) through automated dispatch and driver management.
3. Enable B2B revenue streams (construction, hospitality, industrial) through bulk/recurring order infrastructure.
4. Reduce operational overhead by 60%+ vs. manual operations through automation.
5. Build a data foundation (analytics, reporting) for pricing optimization and market expansion.

---

## 4. Target Users & Personas

### 4.1 Individual Customer
- **Who:** Residential users, small office/shop owners
- **Needs:** Reliable drinking/daily-use water delivery, easy ordering, price transparency, delivery tracking
- **Order profile:** Small to medium orders (20L–2,000L), standard frequency
- **See:** [USER_PERSONAS.md](file:///d:/Aquaswift/docs/00-product/USER_PERSONAS.md) — Persona P1 (Priya)

### 4.2 Business Customer
- **Who:** Construction site managers, hotel/restaurant procurement, factory managers, housing societies
- **Needs:** Bulk orders, recurring schedules, site-specific delivery, invoicing, credit terms
- **Order profile:** Large orders (5,000L–100,000L), recurring/scheduled
- **See:** [USER_PERSONAS.md](file:///d:/Aquaswift/docs/00-product/USER_PERSONAS.md) — Persona P2 (Rajesh)

### 4.3 Driver
- **Who:** Tanker/delivery vehicle operators (employed or contracted)
- **Needs:** Clear delivery instructions, GPS navigation, delivery proof workflow, earnings visibility
- **See:** [USER_PERSONAS.md](file:///d:/Aquaswift/docs/00-product/USER_PERSONAS.md) — Persona P3 (Suresh)

### 4.4 Operations Manager
- **Who:** Day-to-day operational staff managing orders, dispatch, inventory, drivers
- **Needs:** Dashboard visibility, manual override capabilities, alert management
- **See:** [USER_PERSONAS.md](file:///d:/Aquaswift/docs/00-product/USER_PERSONAS.md) — Persona P4 (Anita)

### 4.5 Super Admin
- **Who:** Business owner / platform administrator
- **Needs:** Full system configuration, pricing control, catalog management, reporting, audit visibility
- **See:** [USER_PERSONAS.md](file:///d:/Aquaswift/docs/00-product/USER_PERSONAS.md) — Persona P5 (Vikram)

---

## 5. Product Scope

### 5.1 V1 Scope (MVP)

**Customer experience:**
- OTP-based registration/login
- Browse dynamic water catalog (purposes → qualities → delivery methods → variants)
- Address/site management
- Place standard orders (select purpose → quality → quantity → delivery method → time slot)
- View pricing quote before checkout
- Pay via integrated payment gateway (Razorpay V1 adapter)
- Track order status in real-time (polling-based)
- View order history, reorder
- Rate and review completed deliveries

**Driver experience:**
- OTP-based login
- Set availability status
- Receive and accept/reject delivery offers
- Trip status updates (started → arrived → delivered)
- OTP-based proof of delivery
- Earnings summary and history

**Admin/Ops experience:**
- Email+password login
- Dashboard with key metrics and alerts
- Full CRUD for water catalog (purposes, quality types, delivery methods, variants)
- Pricing rule management (fixed, per-litre, tiered models)
- Coupon/promotion management
- Inventory management (sources, ledger viewer, manual adjustments)
- Order management (view, status tracking, manual interventions)
- Delivery management (view, manual assignment, reassignment)
- Driver and vehicle CRUD
- Customer management
- Payment and refund visibility
- Audit log viewer
- Basic reports (sales, water, delivery, customer)

**Platform:**
- Modular monolith backend (FastAPI + PostgreSQL)
- State-machine-enforced order/delivery/inventory workflows
- Append-only inventory ledger
- Server-side pricing engine
- Notification service (push, SMS, email adapters)
- Audit logging for all admin mutations
- Docker-based local development
- CI/CD pipeline (GitHub Actions)

### 5.2 Phase 2 Scope

- **Real-time tracking:** WebSocket-based live delivery tracking with GPS updates
- **B2B customer-facing UI:** Business registration, employee management, site management in customer app
- **Bulk order customer flow:** Request → quote → accept → fulfilment workflow in customer app
- **Recurring order customer flow:** Set up recurring deliveries with schedule management
- **Invoicing:** Period-based invoice generation for B2B customers
- **Route optimization:** Algorithmic route planning for multi-stop deliveries
- **Analytics dashboard:** Advanced operational and business analytics
- **Multi-city support:** Area/zone-based pricing, inventory, and dispatch

### 5.3 Phase 3 Scope

- **Marketplace model:** Multiple water suppliers on a single platform
- **Subscription plans:** Prepaid subscription packages with automatic renewal
- **IoT integration:** Smart water level sensors for automatic reorder triggers
- **Advanced fleet management:** Predictive maintenance, fuel tracking, compliance automation
- **Customer loyalty program:** Points, rewards, referral bonuses
- **White-label capabilities:** Brandable instances for enterprise customers
- **Machine learning:** Demand forecasting, dynamic pricing, route optimization

### 5.4 Explicit Non-Goals (V1)

1. **No real-time GPS tracking** — Status polling only; WebSockets deferred to Phase 2.
2. **No customer-facing B2B workflows** — Backend schema exists; UI deferred to Phase 2.
3. **No customer-facing bulk/recurring order UI** — Backend CRUD exists; customer app UI deferred to Phase 2.
4. **No route optimization** — Manual dispatch only; algorithmic routing deferred to Phase 2.
5. **No multi-city operations** — Single-city deployment in V1.
6. **No marketplace/multi-supplier** — Single operator model in V1.
7. **No IoT integration** — All inventory managed manually or via admin adjustments.
8. **No machine learning** — Static pricing rules, manual dispatch.
9. **No subscription plans** — One-off and scheduled orders only.
10. **No white-labeling** — Single brand, single deployment.

---

## 6. Core Workflows

### 6.1 Customer Ordering Flow
```
Register/Login (OTP) → Browse Catalog → Select Purpose → Select Quality → Select Quantity
→ Select Delivery Method → Choose Time Slot → View Address/Add New → Get Price Quote
→ Apply Coupon (optional) → Confirm & Pay → Order Created → Track Status → Receive Delivery
→ Rate & Review
```

### 6.2 Driver Delivery Flow
```
Login (OTP) → Set Availability → Receive Delivery Offer → Accept/Reject → Start Trip
→ Navigate to Source (load) → Navigate to Customer Site → Arrive → Customer Verifies (OTP)
→ Deliver → Upload Proof → Complete Delivery → View Earnings
```

### 6.3 Admin Order Management Flow
```
Login (Email+Password) → View Dashboard (pending orders, alerts) → Review Orders → Assign
to Driver (manual or auto-offer) → Monitor Delivery Progress → Handle Exceptions
(reassignment, cancellation, refund) → View Reports
```

### 6.4 Admin Catalog Management Flow
```
Login → Navigate to Catalog → Add/Edit Water Purpose → Add/Edit Quality Type → Add/Edit
Delivery Method → Create Water Variant (purpose × quality × delivery method × quantity range)
→ Set Pricing Rule for Variant → Activate → Visible in Customer App
```

### 6.5 Inventory Management Flow
```
Water Source Setup → Record Incoming Water (RECEIVED transaction) → View Available Balance
→ Order Creates RESERVE → Dispatch Creates ALLOCATE → Delivery Creates DELIVER deduction
→ Cancellation Creates RELEASE → Manual Adjustment with Reason → Reconciliation Check
```

### 6.6 Payment Flow
```
Order Created → Payment Intent Created (server-side) → Customer Pays (gateway checkout)
→ Gateway Webhook Received → Server Verifies Signature → Payment Marked SUCCESS
→ Order Transitions to CONFIRMED → (On cancellation: Refund Initiated → Gateway Processes
→ Refund Webhook → Payment Marked REFUNDED)
```

---

## 7. Product Models

### 7.1 Water Catalog Model
Four **independent, admin-configurable dimensions** — never hard-coded:

| Dimension | Entity | Example Values |
|-----------|--------|---------------|
| **Purpose** | `water_purposes` | Drinking, Daily Use, Construction, Cleaning, Industrial, Agriculture |
| **Quality/Grade** | `water_quality_types` | RO+UV, Purified, Treated, Utility Grade |
| **Delivery Method** | `delivery_methods` | Jar, Can, Tanker, Bulk Tanker |
| **Variant** | `water_variants` | Purpose × Quality × Delivery Method × Quantity Range |

A `water_variant` is an orderable combination. Admins create variants by selecting valid combinations of purpose, quality, and delivery method, and defining min/max quantity ranges. The `water_purpose_qualities` join table controls which quality types are available for each purpose.

### 7.2 Ordering Model
- **Order types:** STANDARD, SCHEDULED, RECURRING, BULK
- **One order → many deliveries** (always modeled as 1:N, even when N=1)
- **Commercial snapshot:** Every order stores a frozen copy of purpose name, quality name, quantity, unit price, all charges, and final total at creation time. Subsequent catalog/pricing changes never alter historical orders.
- **Idempotency:** `POST /orders` supports `Idempotency-Key` header to prevent duplicate orders on client retry.

### 7.3 Delivery Model
- Each delivery is independently trackable with its own state machine.
- Parent order reaches DELIVERED only when **all** child deliveries are DELIVERED.
- Assignment uses an offer/accept/reject pattern with timeout and reassignment.
- Proof of delivery via OTP verification + optional photo upload.

### 7.4 Inventory Model
- **Append-only ledger** (`inventory_transactions`) — never a mutable counter.
- Transaction types: RECEIVED, RESERVED, RELEASED, ALLOCATED, DELIVERED, ADJUSTED, LOST_WASTAGE.
- `inventory_balances` is a **reconciled cache** rebuilt from the ledger — never the source of truth.
- Conservation law: `available + reserved + allocated + delivered + lost = total_received` (verifiable by summing the ledger).

### 7.5 Pricing Model
- Single `PricingService.quote()` function is the **only** place price is computed.
- Models: FIXED, PER_LITRE, TIERED (configurable via `pricing_rules`).
- Supports: purpose/quality-specific pricing, customer-type pricing, area-based pricing.
- Coupon system with discount types, validity windows, usage limits.
- The same service call powers both the pre-checkout quote preview and the actual order creation price.

### 7.6 Payment Model
- Server-side payment intent creation via generic `PaymentGatewayAdapter` (Razorpay V1).
- **Webhook is the only writer of payment success** — never trust client-reported payment status.
- Idempotent webhook handler (safe to receive same event twice).
- Refund flow triggered on eligible cancellations, processed through the same gateway adapter.

### 7.7 Notification Model
- Channel-agnostic `NotificationService.send(user, event, context)`.
- Adapter pattern: Push, SMS (MSG91 V1), Email adapters behind a common interface.
- Channels can be added/changed without touching call sites.
- Event-driven: wired into order/delivery/payment lifecycle transitions.

### 7.8 Reporting Model
- Scheduled aggregation jobs feeding dashboard views.
- Report categories: Sales, Water supply/consumption, Delivery performance, Customer metrics.
- V1: pre-defined report views, not ad-hoc querying.

---

## 8. Success Metrics & KPIs

| Metric | Target (V1) | Measurement |
|--------|-------------|-------------|
| Order completion rate | >95% | Confirmed orders reaching DELIVERED / total confirmed |
| Average delivery time | <2 hours (standard) | Order confirmed → delivery completed timestamp delta |
| Payment success rate | >98% | Successful payments / total payment attempts |
| Inventory accuracy | 100% reconciliation | Ledger sum matches balance cache (automated check) |
| Customer reorder rate | >40% within 30 days | Repeat orders from same customer_id |
| Driver acceptance rate | >80% | Accepted offers / total offers sent |
| System uptime | 99.5% | Monitoring/alerting |
| API response time (P95) | <500ms | Application performance monitoring |
| Admin task resolution time | <15 min for standard ops | Time from alert to resolution in audit log |

---

## 9. Risks, Assumptions, Dependencies & Extensibility

### 9.1 Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Payment gateway downtime | Orders blocked | Queue failed payment intents for retry; show helpful error messages |
| SMS/OTP delivery failure | Login blocked | Retry with fallback channel (email OTP); MSG91 DLT compliance reduces failures |
| Driver supply shortage | Delivery delays | Alert ops team when acceptance rate drops; manual assignment fallback |
| Inventory data entry errors | Incorrect availability | Mandatory reason + audit log for adjustments; periodic reconciliation checks |
| Database performance at scale | Slow queries | Proper indexing; read replicas for reporting queries; caching strategy |

### 9.2 Assumptions
1. Single-city, single-operator deployment for V1.
2. Indian market — INR currency, Indian payment gateway, DLT-compliant SMS.
3. Water sources are managed by the same operator (no marketplace model).
4. Customers have smartphones with internet access for mobile ordering.
5. Drivers have smartphones with GPS for navigation and delivery proof.
6. Admin staff have desktop/laptop access for the web dashboard.

### 9.3 Dependencies
- **Razorpay** — Payment processing (V1 adapter)
- **MSG91** — OTP/SMS delivery (V1 adapter)
- **Google Maps Platform** — Geocoding, distance calculation
- **AWS** — Cloud infrastructure (ECS/Fargate, RDS, ElastiCache, S3)
- **Firebase Cloud Messaging** — Push notifications
- **SendGrid / AWS SES** — Transactional email (to be decided in implementation)

### 9.4 Extensibility Design
- **Adapter pattern** for all external integrations (payment, SMS, maps, push, email, storage)
- **Admin-configurable catalog** — new water purposes, qualities, delivery methods added without code changes
- **Modular monolith** — cleanly separated modules can be extracted to services if/when needed
- **Feature flags** — Phase 2/3 features can be toggled without deployment
- **Multi-tenant readiness** — schema design accommodates future multi-city/multi-operator expansion
