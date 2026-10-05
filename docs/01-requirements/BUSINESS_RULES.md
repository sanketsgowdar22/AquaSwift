# AquaSwift — Business Rules (Master, System-Level)

**Version:** 1.0
**Status:** Draft
**Last Updated:** 2026-09-03

---

> This document formalizes system-level, cross-cutting business rules that span multiple modules. Module-specific business rules belong in each module's own `BUSINESS_RULES.md` in Sub-Phase 0D (`docs/02-modules/<module>/BUSINESS_RULES.md`). Module-level docs should reference rules here by stable ID (`RULE-XXX`) rather than restating them.

---

## Part A — Non-Negotiable Architectural Rules

These are the ten inviolable architectural rules from the Master Build Prompt §2. Violating any of these is a critical defect.

---

### RULE-001 — Admin-Configurable Catalog Dimensions

**Rule:** Water Purpose, Quality/Grade, Quantity, and Delivery Method are four independent, admin-configurable dimensions. No backend or frontend code shall contain a hard-coded list of water types, purposes, qualities, or delivery methods.

**Rationale:** The platform must support arbitrary expansion of the water catalog — adding a new purpose (e.g., "Swimming Pool") and having it appear in the customer app with zero app rebuild or redeploy. Hard-coding defeats the platform's core value proposition of data-driven configurability.

**Constrained Modules:** CAT (Catalog), ORD (Orders), PRC (Pricing), DEL (Deliveries), INV (Inventory), all frontend applications (Customer App, Driver App, Admin Dashboard)

**Testable Requirements:** CAT-001, CAT-002, CAT-003, CAT-004, CAT-005

---

### RULE-002 — Litres as Canonical Unit

**Rule:** Litres are the canonical quantity unit, stored as integers (`BIGINT`) everywhere in the database and in all business logic. UI layers may format values for display (e.g., "10 KL") but must never store or calculate using formatted strings.

**Rationale:** Integer arithmetic eliminates floating-point rounding errors in inventory accounting and pricing calculations. A single canonical unit prevents unit-conversion bugs across modules.

**Constrained Modules:** CAT (Catalog), INV (Inventory), ORD (Orders), DEL (Deliveries), PRC (Pricing), BULK (Bulk Orders), REC (Recurring Orders), SRC (Water Sources)

**Testable Requirements:** CAT-006, INV-001, ORD-003, DEL-003

---

### RULE-003 — One-to-Many Order-Delivery Relationship

**Rule:** One order can have many deliveries. The system shall always model the order-delivery relationship as `orders (1) → (N) deliveries`, even when N=1. No code path shall assume exactly one delivery per order.

**Rationale:** Bulk orders, partial deliveries, and delivery failures that spawn remainder deliveries all produce multiple deliveries for a single order. Assuming 1:1 creates data model and business logic bugs that are expensive to fix later.

**Constrained Modules:** ORD (Orders), DEL (Deliveries), INV (Inventory), PAY (Payments), NTF (Notifications)

**Testable Requirements:** ORD-004, DEL-001, DEL-002

---

### RULE-004 — Append-Only Inventory Ledger

**Rule:** Inventory is tracked through an append-only ledger (`inventory_transactions`). No code path shall `UPDATE` or `DELETE` rows in the inventory ledger. Balances are derived by summing the ledger and stored in `inventory_balances` as a reconciled cache — never the source of truth.

**Rationale:** An append-only ledger provides a complete audit trail, enables point-in-time reconciliation, and prevents the class of bugs where a mutable counter silently drifts out of sync with reality.

**Constrained Modules:** INV (Inventory), ORD (Orders), DEL (Deliveries), SRC (Water Sources), AUD (Audit)

**Testable Requirements:** INV-002, INV-003, INV-004, INV-005

---

### RULE-005 — Server-Side Authority

**Rule:** All pricing, inventory availability, payment verification, and permission/authorization logic shall execute server-side. Mobile and web clients display server-returned data; they shall never independently compute a final price, determine their own permissions, or make inventory availability decisions.

**Rationale:** Client-side business logic is trivially bypassable, leading to price manipulation, permission escalation, and inventory overselling. The server is the single source of truth for all business decisions.

**Constrained Modules:** PRC (Pricing), INV (Inventory), PAY (Payments), RBAC (Permissions), ORD (Orders), all frontend applications

**Testable Requirements:** PRC-001, RBAC-001, PAY-004, ORD-005

---

### RULE-006 — Commercial Snapshot Immutability

**Rule:** Every order shall store a frozen commercial snapshot (purpose name, quality name, quantity, unit price, all charges, delivery charge, discount, tax, final total) at creation time in `order_items`. Subsequent changes to catalog configuration, pricing rules, or coupon definitions shall never alter any field of any historical order's snapshot.

**Rationale:** Historical orders are financial records. Retroactive price changes would corrupt revenue reporting, break customer trust, and create accounting/audit failures.

**Constrained Modules:** ORD (Orders), PRC (Pricing), CAT (Catalog), CPN (Coupons), RPT (Reporting), AUD (Audit)

**Testable Requirements:** ORD-006, ORD-007, PRC-002

---

### RULE-007 — Modular Monolith Architecture

**Rule:** The backend shall be structured as a modular monolith — a single deployable unit with clearly separated module directories (`backend/app/<module>/`) that could be extracted into independent services later. No microservices, no inter-module HTTP calls, no separate deployable services per module.

**Rationale:** A modular monolith provides the clean separation benefits of microservices without the operational complexity of distributed systems. It is the correct starting architecture for a V1 platform with a small team.

**Constrained Modules:** All backend modules, Infrastructure/Platform

**Testable Requirements:** ADM-001 (implicitly tested through module structure, not a functional requirement per se)

---

### RULE-008 — State Machine Enforcement

**Rule:** Orders, Deliveries, and Inventory transactions shall use explicit state machines — an `transition(entity, new_status, actor, reason)` function that (a) validates legality against an allow-list of permitted transitions, (b) applies the change inside a DB transaction, (c) writes a history/audit row, and (d) triggers relevant side effects. Arbitrary status writes bypassing the state machine are prohibited.

**Rationale:** State machines prevent illegal business states (e.g., a CANCELLED order being marked DELIVERED), ensure audit trail completeness, and centralize side-effect triggering so that notifications, inventory adjustments, and payment actions cannot be skipped.

**Constrained Modules:** ORD (Orders), DEL (Deliveries), INV (Inventory), PAY (Payments), BULK (Bulk Orders), REC (Recurring Orders)

**Testable Requirements:** ORD-008, ORD-009, DEL-004, DEL-005, INV-006

---

### RULE-009 — Server-to-Server Payment Verification

**Rule:** The system shall never trust client-reported payment success. Payment status shall only be written to `SUCCESS` by the server-side webhook handler after verifying the payment gateway's cryptographic signature server-to-server. The webhook handler shall be idempotent.

**Rationale:** Clients can be spoofed, tampered with, or simply wrong about payment outcomes. Only the payment gateway, verified server-to-server, is authoritative. Idempotent webhook handling prevents double-processing on gateway retries.

**Constrained Modules:** PAY (Payments), ORD (Orders)

**Testable Requirements:** PAY-001, PAY-002, PAY-003, PAY-004

---

### RULE-010 — Soft-Delete for Referenced Catalog Records

**Rule:** The system shall never hard-delete catalog records (water purposes, quality types, delivery methods, water variants) that are referenced by historical orders. Deactivation (`is_active = false`) is the only permitted removal mechanism. Deactivated records shall not appear in customer-facing catalog browsing but shall remain queryable for historical order display.

**Rationale:** Hard-deleting a catalog record that is referenced by an order's commercial snapshot would break foreign key integrity, corrupt order history display, and violate the commercial snapshot immutability rule (RULE-006).

**Constrained Modules:** CAT (Catalog), ORD (Orders), ADM (Admin Operations), AUD (Audit)

**Testable Requirements:** CAT-007, CAT-008, ADM-002

---

## Part B — Cross-Cutting Domain Rules

These rules span multiple modules and do not fit cleanly in any single module's own `BUSINESS_RULES.md`. They govern cross-module interactions and data integrity constraints.

---

### RULE-011 — Delivery Quantity Ceiling

**Rule:** A delivery's `delivered_quantity_litres` shall never exceed its `allocated` quantity (i.e., the `quantity_litres` assigned to that delivery). If the driver reports a delivered quantity greater than the allocated amount, the system shall reject the completion request.

**Constrained Modules:** DEL (Deliveries), INV (Inventory)

**Testable Requirements:** DEL-006, INV-007

---

### RULE-012 — Order Completion Requires All Deliveries Complete

**Rule:** A parent order shall only transition to `DELIVERED` status when **all** of its child deliveries have reached `DELIVERED` status. No partial set of completed deliveries shall cause the parent order to be marked as delivered.

**Constrained Modules:** ORD (Orders), DEL (Deliveries)

**Testable Requirements:** ORD-010, DEL-007

---

### RULE-013 — Inventory Conservation Law

**Rule:** For every water source, the following conservation equation must hold at all times, verifiable by summing the inventory ledger: `available + reserved + allocated + delivered + lost_wastage = total_received`. Any discrepancy detected by reconciliation must generate an alert and be resolvable only through an explicit `ADJUSTED` or `LOST_WASTAGE` transaction with a mandatory reason.

**Constrained Modules:** INV (Inventory), SRC (Water Sources), AUD (Audit), ADM (Admin Operations)

**Testable Requirements:** INV-008, INV-009, INV-010

---

### RULE-014 — Single Pricing Authority

**Rule:** The `PricingService.quote()` function is the single, authoritative place where price is computed. Both the pre-checkout quote preview endpoint and the order creation endpoint shall call the same function. No other code path shall independently compute or override a price.

**Constrained Modules:** PRC (Pricing), ORD (Orders), CPN (Coupons)

**Testable Requirements:** PRC-001, PRC-003, ORD-005

---

### RULE-015 — Reservation Expiry and Auto-Release

**Rule:** Inventory reservations created for orders in `PENDING_PAYMENT` status shall be automatically released if the order does not transition to `CONFIRMED` within a configurable timeout. A Celery beat job shall detect expired reservations, release the reserved inventory (creating a `RELEASED` transaction), and mark the order as `FAILED` (payment timeout). The customer shall be notified.

**Constrained Modules:** INV (Inventory), ORD (Orders), NTF (Notifications)

**Testable Requirements:** INV-011, ORD-011, NTF-001

---

### RULE-016 — Idempotent Order and Payment Processing

**Rule:** `POST /orders` and `POST /payments/verify` endpoints shall support an `Idempotency-Key` header. If the same idempotency key is received again, the server shall return the original response without creating a duplicate order or processing a duplicate payment.

**Constrained Modules:** ORD (Orders), PAY (Payments)

**Testable Requirements:** ORD-012, PAY-005

---

### RULE-017 — Cancellation Window Enforcement

**Rule:** A customer may cancel an order only before it reaches `OUT_FOR_DELIVERY` status. Once a delivery has started (driver en route), cancellation is no longer permitted through the customer-facing interface. Admin/Ops users may cancel at any status with a mandatory reason.

**Constrained Modules:** ORD (Orders), DEL (Deliveries), RFD (Refunds), INV (Inventory)

**Testable Requirements:** ORD-013, ORD-014, RFD-001

---

### RULE-018 — Partial Delivery Creates Remainder

**Rule:** When a driver delivers less than the full allocated quantity for a delivery, the system shall mark the delivery as `PARTIALLY_DELIVERED` with the actual delivered quantity, and automatically create a new delivery for the remaining quantity in `PENDING_ASSIGNMENT` status. The parent order shall remain in `PROCESSING` status until all deliveries (including remainder deliveries) are complete.

**Constrained Modules:** DEL (Deliveries), ORD (Orders), INV (Inventory), NTF (Notifications)

**Testable Requirements:** DEL-008, DEL-009, ORD-010

---

### RULE-019 — Audit Trail for Admin Mutations

**Rule:** Every admin write operation to catalog, pricing, inventory, or user/role data shall create an immutable `audit_logs` row recording the actor, action, entity type/ID, before state, after state, metadata, and timestamp. Audit log rows shall never be updated or deleted.

**Constrained Modules:** AUD (Audit), CAT (Catalog), PRC (Pricing), INV (Inventory), ADM (Admin Operations), RBAC (Permissions), USR (Users)

**Testable Requirements:** AUD-001, AUD-002, AUD-003

---

### RULE-020 — Re-Quote on Stale Cart

**Rule:** If catalog configuration or pricing rules change between the time a customer views a price quote and the time they confirm an order, the system shall re-compute the price at order creation time. If the new price differs from the quoted price, the system shall require the customer to re-confirm before proceeding.

**Constrained Modules:** PRC (Pricing), ORD (Orders), CAT (Catalog)

**Testable Requirements:** PRC-004, ORD-015

---

### RULE-021 — Notification Delivery Resilience

**Rule:** If a notification fails to deliver on the primary channel, the system shall retry and, for critical events (payment success, delivery arrival, order cancellation), attempt a fallback channel. The system shall never silently drop a notification for a critical lifecycle event.

**Constrained Modules:** NTF (Notifications)

**Testable Requirements:** NTF-002, NTF-003

---

### RULE-022 — Driver Assignment Escalation

**Rule:** If a delivery offer is rejected by a driver or times out without response, the system shall automatically re-offer to the next eligible driver. If no driver accepts after a configurable number of attempts, the system shall generate an alert for the ops team and the delivery shall be available for manual assignment.

**Constrained Modules:** DEL (Deliveries), DRV (Drivers), NTF (Notifications), ADM (Admin Operations)

**Testable Requirements:** DEL-010, DEL-011, DRV-001

---

### RULE-023 — Transaction Atomicity for Order Creation

**Rule:** Order creation is a single database transaction comprising: availability validation → price computation → order record creation → order_items snapshot → inventory reservation → payment intent creation. If any step fails, the entire transaction rolls back — no partial writes (e.g., no order without a reservation, no reservation without an order).

**Constrained Modules:** ORD (Orders), INV (Inventory), PAY (Payments), PRC (Pricing)

**Testable Requirements:** ORD-016, INV-012

---

### RULE-024 — Business Permission Scoping

**Rule:** The system shall support distinct permission scopes for a business's admin users versus its employee users. A business admin may manage all sites, view all orders, and invite/remove employees. A business employee may only place orders for sites they are assigned to and view only their own orders. This scoping is independent of the platform-level RBAC roles.

**Rationale:** B2B customers (e.g., construction companies with multiple sites) need to delegate ordering to site supervisors without granting full business-level visibility and control.

**Constrained Modules:** BIZ (Businesses/B2B), RBAC (Permissions), ORD (Orders), ADDR (Address/Site Management)

**Testable Requirements:** RBAC-007, BIZ-001, BIZ-002, BIZ-003

---

## Appendix — Rule Index

| Rule ID | Short Name | Part |
|---------|-----------|------|
| RULE-001 | Admin-Configurable Catalog Dimensions | A (Non-Negotiable) |
| RULE-002 | Litres as Canonical Unit | A (Non-Negotiable) |
| RULE-003 | One-to-Many Order-Delivery | A (Non-Negotiable) |
| RULE-004 | Append-Only Inventory Ledger | A (Non-Negotiable) |
| RULE-005 | Server-Side Authority | A (Non-Negotiable) |
| RULE-006 | Commercial Snapshot Immutability | A (Non-Negotiable) |
| RULE-007 | Modular Monolith Architecture | A (Non-Negotiable) |
| RULE-008 | State Machine Enforcement | A (Non-Negotiable) |
| RULE-009 | Server-to-Server Payment Verification | A (Non-Negotiable) |
| RULE-010 | Soft-Delete for Referenced Catalog Records | A (Non-Negotiable) |
| RULE-011 | Delivery Quantity Ceiling | B (Cross-Cutting) |
| RULE-012 | Order Completion Requires All Deliveries | B (Cross-Cutting) |
| RULE-013 | Inventory Conservation Law | B (Cross-Cutting) |
| RULE-014 | Single Pricing Authority | B (Cross-Cutting) |
| RULE-015 | Reservation Expiry and Auto-Release | B (Cross-Cutting) |
| RULE-016 | Idempotent Order and Payment Processing | B (Cross-Cutting) |
| RULE-017 | Cancellation Window Enforcement | B (Cross-Cutting) |
| RULE-018 | Partial Delivery Creates Remainder | B (Cross-Cutting) |
| RULE-019 | Audit Trail for Admin Mutations | B (Cross-Cutting) |
| RULE-020 | Re-Quote on Stale Cart | B (Cross-Cutting) |
| RULE-021 | Notification Delivery Resilience | B (Cross-Cutting) |
| RULE-022 | Driver Assignment Escalation | B (Cross-Cutting) |
| RULE-023 | Transaction Atomicity for Order Creation | B (Cross-Cutting) |
| RULE-024 | Business Permission Scoping | B (Cross-Cutting) |
