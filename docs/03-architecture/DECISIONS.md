# AquaSwift — Architectural Decision Records

**Version:** 1.0
**Status:** Draft
**Last Updated:** 2026-09-03

---

> Every important architectural decision is recorded here with context, options considered, rationale, and consequences. Decisions are referenced by stable IDs (`DEC-XXX-NNN`) throughout the documentation.

---

## DEC-ARCH-001 — Modular Monolith Over Microservices

**Date:** 2026-09-03
**Status:** Accepted

**Problem:** AquaSwift has 27 identified modules with complex inter-module dependencies (e.g., order creation touches Catalog, Inventory, Pricing, Payments). Should the backend be structured as microservices or a monolith?

**Options Considered:**
1. **Microservices** — Each module as an independent deployable service with inter-service HTTP/gRPC calls.
2. **Modular monolith** — Single deployable unit with clearly separated module directories and in-process function calls.
3. **Hybrid** — Core modules as monolith, auxiliary (notifications, analytics) as separate services.

**Decision:** Modular monolith (Option 2).

**Rationale:**
- A small team building V1 cannot absorb the operational complexity of distributed systems (service discovery, distributed transactions, eventual consistency, network partition handling).
- Order creation requires atomic transactions spanning Inventory, Pricing, Payments — trivial in a monolith, extremely complex across services.
- Module boundaries are defined by directory structure (`backend/app/<module>/`), making future extraction straightforward if scale demands it.
- Master Prompt §1 Rule 7 explicitly mandates this.

**Consequences:**
- All modules share a single database — schema separation is by convention (module-prefixed tables), not enforcement.
- Module dependencies are in-process function imports — must be kept unidirectional to preserve extractability.
- Deployment is simpler (one container) but scaling is coarser (scale entire app, not individual modules).

**Affected Modules:** All

---

## DEC-ARCH-002 — FastAPI + SQLAlchemy + PostgreSQL Stack

**Date:** 2026-09-03
**Status:** Accepted

**Problem:** Which backend framework, ORM, and database to use?

**Options Considered:**
1. **Django + Django ORM + PostgreSQL** — Batteries-included, mature admin interface.
2. **FastAPI + SQLAlchemy + PostgreSQL** — Async-capable, auto-generated OpenAPI docs, explicit ORM.
3. **Flask + SQLAlchemy + PostgreSQL** — Lightweight, flexible.

**Decision:** FastAPI + SQLAlchemy + PostgreSQL (Option 2).

**Rationale:**
- FastAPI provides automatic OpenAPI/Swagger documentation from type hints — critical for a multi-client platform.
- Pydantic integration gives request/response validation with zero boilerplate.
- SQLAlchemy provides fine-grained control over queries and transactions needed for inventory ledger operations.
- PostgreSQL provides JSONB (for pricing snapshots, tiers), robust transaction isolation, and excellent indexing.
- Master Prompt §3 explicitly specifies this stack.

**Consequences:**
- No built-in admin interface (unlike Django) — admin dashboard built separately in Next.js.
- Must manually configure Alembic for migrations.
- SQLAlchemy's session management requires explicit transaction handling (a feature, not a bug, for this use case).

**Affected Modules:** All backend modules

---

## DEC-AUTH-001 — MSG91 for OTP with Adapter Pattern

**Date:** 2026-09-03
**Status:** Accepted

**Problem:** Which SMS/OTP provider to use for customer and driver authentication?

**Options Considered:**
1. **MSG91** — India-focused, DLT-compliant, dedicated OTP APIs.
2. **Twilio** — Global leader, but more expensive for India, requires DLT compliance setup.
3. **AWS SNS** — Low cost, but no dedicated OTP flow, DLT compliance manual.

**Decision:** MSG91 as V1 implementation behind an `SMSProvider` adapter interface.

**Rationale:**
- MSG91 is purpose-built for the Indian market with native DLT compliance (NFR-COMP-001).
- Dedicated OTP send/verify APIs reduce implementation complexity.
- Adapter pattern (`SMSProvider` interface with `send_otp()`, `verify_otp()` methods) allows swapping to Twilio or SNS later without changing business logic.
- Master Prompt §3 specifies MSG91.

**Consequences:**
- Vendor lock-in mitigated by adapter pattern.
- Must register DLT templates with telecom operators before production launch.
- Fallback channel (email OTP) needed for delivery failures (AUTH-010).

**Affected Modules:** AUTH, NTF

---

## DEC-PAY-001 — Razorpay with Webhook-Only Payment Confirmation

**Date:** 2026-09-03
**Status:** Accepted

**Problem:** How to handle payment processing and verification?

**Options Considered:**
1. **Client-reported payment status** — Client confirms payment success to server.
2. **Server-side polling** — Server polls gateway for payment status.
3. **Webhook-only** — Server receives payment events via webhook; webhook is the only writer of payment success.

**Decision:** Razorpay as V1 gateway behind `PaymentGatewayAdapter`, with webhook-only payment confirmation (Option 3).

**Rationale:**
- Client-reported status is trivially spoofable (RULE-009, Master Prompt §1 Rule 9).
- Server polling introduces latency and complexity (race conditions, missed events).
- Webhooks are push-based, idempotent, and cryptographically verifiable via Razorpay's signature.
- The webhook handler is the single code path writing `payments.status = SUCCESS`, eliminating duplicate-payment bugs.

**Consequences:**
- Must handle webhook delivery failures (retry from Razorpay, idempotent handler).
- Order stays in PENDING_PAYMENT until webhook arrives — reservation expiry job handles abandoned payments.
- Must verify webhook signature server-to-server before trusting any event.
- Gateway-hosted checkout fields mean zero PCI scope (NFR-SEC-003).

**Affected Modules:** PAY, ORD

---

## DEC-DB-001 — Append-Only Inventory Ledger Over Mutable Counters

**Date:** 2026-09-03
**Status:** Accepted

**Problem:** How to track inventory — a single mutable balance counter or an append-only transaction log?

**Options Considered:**
1. **Mutable counter** — `UPDATE inventory SET available = available - quantity` on each operation.
2. **Append-only ledger** — Insert a new transaction row for every movement; derive balances by summing.

**Decision:** Append-only ledger (`inventory_transactions`) with a reconciled cache (`inventory_balances`).

**Rationale:**
- Mutable counters silently drift when bugs skip an update or concurrent writes race — there's no way to answer "where did the water go?"
- The ledger provides a complete, immutable audit trail of every litre from RECEIVED to DELIVERED.
- Balances are derivable at any time by summing the ledger — the `inventory_balances` table is a performance optimization cache, never the source of truth.
- Conservation law (`available + reserved + allocated + delivered + lost = total_received`) is verifiable by summing the ledger (RULE-013, INV-008).
- Master Prompt §1 Rule 4 mandates this.

**Consequences:**
- INSERT-only operations are faster than UPDATE under contention (no row-level locks on the transaction table itself).
- Balance cache must be kept in sync — reconciliation function rebuilds it from ledger on demand.
- Row-level locking moves to `inventory_balances` during reservation (`SELECT ... FOR UPDATE`) to prevent overselling (INV-018).
- Ledger table grows linearly with operations — proper indexing and potential partitioning by source_id required.

**Affected Modules:** INV, ORD, DEL, SRC

---

## DEC-DB-002 — UUID Primary Keys

**Date:** 2026-09-03
**Status:** Accepted

**Problem:** Should entities use auto-increment integers or UUIDs as primary keys?

**Options Considered:**
1. **Auto-increment BIGINT** — Simple, compact, ordered.
2. **UUID v4** — Globally unique, non-sequential, no collision risk.
3. **ULID / UUID v7** — Globally unique, time-sortable.

**Decision:** UUID v4 (Option 2) for all entity primary keys.

**Rationale:**
- Globally unique IDs prevent conflicts during potential future multi-city/multi-instance deployments.
- Non-sequential IDs prevent information leakage (competitor cannot infer order volume from sequential IDs).
- Master Prompt §6 specifies UUID PKs.
- PostgreSQL's `uuid-ossp` or `gen_random_uuid()` extension provides native support.

**Consequences:**
- Slightly larger index sizes compared to BIGINT (16 bytes vs 8 bytes).
- No natural ordering — must use `created_at` for chronological queries.
- Need to ensure proper indexing on UUID columns used in JOINs and lookups.

**Affected Modules:** All (NFR-DATA-004)

---

## DEC-DB-003 — Commercial Snapshot Immutability

**Date:** 2026-09-03
**Status:** Accepted

**Problem:** How to ensure historical orders retain correct pricing when catalog/pricing rules change?

**Options Considered:**
1. **Foreign key to pricing rule** — Order references current pricing rule; display recalculates from rule.
2. **Snapshot at creation** — Copy all pricing details into `order_items` at creation time.
3. **Versioned pricing with FK** — Order references a specific pricing rule version (immutable).

**Decision:** Snapshot at creation (Option 2), with pricing rule version ID stored for audit traceability.

**Rationale:**
- Option 1 means changing a pricing rule retroactively changes all historical orders — a financial integrity violation (RULE-006).
- Option 2 makes each order self-contained — `order_items` contains purpose_name, quality_name, quantity, unit_price, all charges, final_total as frozen values.
- Storing `pricing_rule_version_id` alongside the snapshot provides traceability without dependency (PRC-002).
- Master Prompt §1 Rule 6 mandates snapshot immutability.

**Consequences:**
- Slightly denormalized — purpose/quality names duplicated in order_items.
- Reporting must aggregate from snapshots, not from current catalog/pricing configuration.
- No migration needed when pricing rules change — old orders are self-contained.

**Affected Modules:** ORD, PRC, RPT

---

## DEC-API-001 — Server-Side Pricing Authority

**Date:** 2026-09-03
**Status:** Accepted

**Problem:** Should the client or server compute the final order price?

**Decision:** Server-only. A single `PricingService.quote()` function is the sole authority for price computation. Clients display the server-returned price but never independently calculate it.

**Rationale:**
- Client-side pricing is bypassable — a modified client could send arbitrary prices (RULE-005).
- Using the same function for both quote preview and order creation guarantees the quoted price equals the charged price (RULE-014).
- Centralizing pricing logic in one function eliminates the class of bugs where price computation diverges between endpoints.

**Consequences:**
- Every order placement requires a server round-trip for pricing.
- Price changes between quote and order creation trigger re-confirmation (RULE-020, PRC-004).

**Affected Modules:** PRC, ORD, CPN

---

## DEC-CACHE-001 — Short-TTL Redis Cache for Catalog

**Date:** 2026-09-03
**Status:** Accepted

**Problem:** Catalog data is read frequently (every customer browse) but changes rarely. How to balance performance and freshness?

**Decision:** Redis cache with ≤ 60-second TTL on catalog read endpoints, with cache invalidation on any catalog write operation.

**Rationale:**
- Catalog data is the most-read, least-written dataset — ideal for caching.
- 60-second TTL ensures new catalog entries (e.g., new water purpose) are visible within one minute with no redeploy (CAT-011).
- Write-through invalidation ensures changes are visible faster than TTL expiry in most cases.
- Master Prompt §9 specifies this approach.

**Consequences:**
- Redis becomes a runtime dependency for catalog reads — graceful fallback to direct DB reads needed.
- Cache invalidation logic must be called from every catalog write endpoint.
- Cache keys must include enough context (purpose_id, quality filters) to avoid stale partial results.

**Affected Modules:** CAT, ADM

---

## DEC-STATE-001 — Explicit State Machine Functions

**Date:** 2026-09-03
**Status:** Accepted

**Problem:** How to enforce valid status transitions for Orders, Deliveries, and Inventory?

**Decision:** Explicit `transition(entity, new_status, actor, reason)` functions that validate against an allow-list, apply changes in a DB transaction, write history/audit rows, and trigger side effects.

**Rationale:**
- Direct status writes (`order.status = 'DELIVERED'`) bypass validation and skip side effects (notifications, inventory adjustments).
- A centralized transition function ensures: (a) illegal transitions are rejected, (b) audit trail is always written, (c) side effects always fire, (d) transitions are always transactional.
- Master Prompt §1 Rule 8 and §8 mandate this pattern.

**Consequences:**
- All status changes must go through the transition function — no direct attribute writes on status fields.
- Side effects are coupled to transitions — must be carefully designed to avoid circular dependencies.
- Testing is focused: test the transition function's allow-list, history writing, and side-effect triggering.

**Affected Modules:** ORD, DEL, INV, BULK, REC

---

## DEC-NOTIFY-001 — Channel-Agnostic Notification Service

**Date:** 2026-09-03
**Status:** Accepted

**Problem:** The system needs to send notifications via Push, SMS, and Email. How to structure this?

**Decision:** A channel-agnostic `NotificationService.send(user, event, context)` with adapter-pattern channel implementations (Push via FCM, SMS via MSG91, Email via SendGrid/SES).

**Rationale:**
- Call sites should not know or care about delivery channels — they just emit an event.
- Adding a new channel (e.g., WhatsApp) should not require changing any call site.
- Channel selection, templating, and delivery tracking are centralized in the notification service.
- Master Prompt §9 specifies this pattern.

**Consequences:**
- Each channel adapter implements a common interface (`send()`, `get_status()`).
- Template management centralizes message content by event type.
- Retry and fallback logic lives in the notification service, not in call sites (RULE-021).

**Affected Modules:** NTF, all modules that emit lifecycle events

---

## Decision Index

| Decision ID | Short Name | Category |
|-------------|-----------|----------|
| DEC-ARCH-001 | Modular Monolith | Architecture |
| DEC-ARCH-002 | FastAPI + SQLAlchemy + PostgreSQL | Technology |
| DEC-AUTH-001 | MSG91 OTP with Adapter | Integration |
| DEC-PAY-001 | Razorpay Webhook-Only | Integration |
| DEC-DB-001 | Append-Only Inventory Ledger | Database |
| DEC-DB-002 | UUID Primary Keys | Database |
| DEC-DB-003 | Commercial Snapshot Immutability | Database |
| DEC-API-001 | Server-Side Pricing Authority | API |
| DEC-CACHE-001 | Short-TTL Redis Cache | Performance |
| DEC-STATE-001 | Explicit State Machine Functions | Architecture |
| DEC-NOTIFY-001 | Channel-Agnostic Notifications | Architecture |
