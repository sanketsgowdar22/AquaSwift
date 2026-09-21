# AquaSwift — Functional Requirements

**Version:** 1.0
**Status:** Draft
**Last Updated:** 2026-09-03

---

> Concise functional-only extract of `SRS.md`. Each entry contains only the requirement ID, phase tag, and "system shall" statement. For full detail (actors, preconditions, data dependencies), see `SRS.md`.

---

## 1. Authentication & Identity (AUTH)

| ID | Phase | Requirement |
|----|-------|-------------|
| AUTH-001 | V1 | The system shall allow customers and drivers to register and authenticate using OTP-based mobile number verification. |
| AUTH-002 | V1 | The system shall send a 6-digit OTP to the user's mobile number via the SMS provider (MSG91 in V1) upon receiving an OTP request. |
| AUTH-003 | V1 | The system shall verify the OTP entered by the user and, upon successful verification, issue a JWT access token and a refresh token. |
| AUTH-004 | V1 | The system shall support OTP expiry — an OTP not verified within a configurable time window shall be rejected. |
| AUTH-005 | V1 | The system shall allow admin and operations manager users to authenticate using email and password. |
| AUTH-006 | V1 | The system shall issue short-lived JWT access tokens and longer-lived refresh tokens, allowing clients to obtain new access tokens without re-authentication. |
| AUTH-007 | V1 | The system shall invalidate all refresh tokens for a user upon explicit logout or security events. |
| AUTH-008 | V1 | The system shall create a new user record upon first successful OTP verification if no account exists for that mobile number. |
| AUTH-009 | V1 | The system shall enforce rate limiting on OTP request and verification endpoints to prevent brute-force attacks. |
| AUTH-010 | V1 | The system shall support a retry mechanism with a fallback channel when primary SMS OTP delivery fails. |

---

## 2. RBAC & Permissions (RBAC)

| ID | Phase | Requirement |
|----|-------|-------------|
| RBAC-001 | V1 | The system shall enforce role-based access control (RBAC) on every protected API endpoint using a `require_permission()` server-side dependency. |
| RBAC-002 | V1 | The system shall support the following predefined platform roles: CUSTOMER, DRIVER, OPS_MANAGER, SUPER_ADMIN. |
| RBAC-003 | V1 | The system shall assign each role a defined set of granular permissions and check the requesting user's permissions on every protected endpoint. |
| RBAC-004 | V1 | The system shall return HTTP 403 Forbidden when an authenticated user lacks the required permission for an endpoint. |
| RBAC-005 | V1 | The system shall prevent customers from accessing admin-only endpoints. |
| RBAC-006 | V1 | The system shall prevent drivers from accessing admin-only or customer-only endpoints. |
| RBAC-007 | PHASE 2 | The system shall support distinct permission scopes for a business's admin users versus its employee users, independent of platform-level RBAC roles. |
| RBAC-008 | V1 | The system shall allow the Super Admin to manage role assignments — assigning and revoking roles for other users. |

---

## 3. User & Customer Management (USR)

| ID | Phase | Requirement |
|----|-------|-------------|
| USR-001 | V1 | The system shall allow authenticated customers to create and update their profile (name, email, phone number). |
| USR-002 | V1 | The system shall allow authenticated drivers to create and update their profile (name, phone number, vehicle information). |
| USR-003 | V1 | The system shall allow admin users to view and search the list of all customers with pagination, filtering, and sorting. |
| USR-004 | V1 | The system shall allow admin users to view detailed customer information including profile, order history, and addresses. |
| USR-005 | V1 | The system shall create a customer profile record automatically upon first registration via OTP. |
| USR-006 | V1 | The system shall allow admin users to deactivate a customer account, preventing further logins and order placement. |

---

## 4. Address & Site Management (ADDR)

| ID | Phase | Requirement |
|----|-------|-------------|
| ADDR-001 | V1 | The system shall allow authenticated customers to add, edit, and delete delivery addresses. |
| ADDR-002 | V1 | The system shall geocode addresses using Google Maps Platform to store latitude and longitude coordinates. |
| ADDR-003 | V1 | The system shall allow customers to select a saved address or add a new address during order placement. |
| ADDR-004 | V1 | The system shall allow customers to add delivery instructions/notes to an address. |
| ADDR-005 | V1 | The system shall allow admin users to view and manage customer addresses. |
| ADDR-006 | PHASE 2 | The system shall support business sites — delivery locations belonging to a business — manageable by business admin users. |
| ADDR-007 | V1 | The system shall store the schema for business_sites in V1 (ARCHITECTURE ONLY). |

---

## 5. Water Catalog (CAT)

| ID | Phase | Requirement |
|----|-------|-------------|
| CAT-001 | V1 | The system shall store water purposes as admin-configurable records — never as hard-coded enums or constants. |
| CAT-002 | V1 | The system shall store water quality types as admin-configurable records — never as hard-coded enums or constants. |
| CAT-003 | V1 | The system shall store delivery methods as admin-configurable records — never as hard-coded enums or constants. |
| CAT-004 | V1 | The system shall support a water_purpose_qualities join table controlling which quality types are available for each purpose. |
| CAT-005 | V1 | The system shall store water variants as orderable combinations of purpose × quality × delivery method, with admin-defined min/max quantity ranges in litres. |
| CAT-006 | V1 | The system shall store all catalog quantity fields as integer litres using BIGINT. |
| CAT-007 | V1 | The system shall support soft-delete (deactivation) for all catalog records; hard-deletion of records referenced by historical orders is prohibited. |
| CAT-008 | V1 | The system shall exclude deactivated catalog records from customer-facing browsing but retain them for historical order display. |
| CAT-009 | V1 | The system shall provide public read API endpoints for browsing the catalog. |
| CAT-010 | V1 | The system shall provide admin CRUD endpoints for all catalog entities with audit logging. |
| CAT-011 | V1 | The system shall apply a short-TTL Redis cache (≤ 60s) to catalog reads and invalidate on writes. |
| CAT-012 | V1 | The system shall validate that a variant's purpose-quality combination is valid via the join table before creation. |

---

## 6. Water Quality (QUAL)

| ID | Phase | Requirement |
|----|-------|-------------|
| QUAL-001 | V1 | The system shall store water quality test records (pH, TDS, turbidity, treatment type, tester, test date, certificate URL, status) for water sources. |
| QUAL-002 | V1 | The system shall allow admin users to create, view, and update quality test records. |
| QUAL-003 | V1 | The system shall allow customers to view quality information for the water they are ordering. |
| QUAL-004 | V1 | The system shall support approval/rejection status for quality records, showing only approved records to customers. |

---

## 7. Water Sources (SRC)

| ID | Phase | Requirement |
|----|-------|-------------|
| SRC-001 | V1 | The system shall store water source records with name, type, GPS location, capacity in litres (BIGINT), and status. |
| SRC-002 | V1 | The system shall allow admin users to CRUD water sources. |
| SRC-003 | V1 | The system shall track operational status of sources and prevent inventory operations on inactive sources. |
| SRC-004 | V1 | The system shall track inventory per source with independent balances. |

---

## 8. Inventory (INV)

| ID | Phase | Requirement |
|----|-------|-------------|
| INV-001 | V1 | The system shall store all inventory quantity fields as integer litres using BIGINT. |
| INV-002 | V1 | The system shall maintain an append-only inventory ledger where no row is ever updated or deleted. |
| INV-003 | V1 | The system shall support transaction types: RECEIVED, RESERVED, RELEASED, ALLOCATED, DELIVERED, ADJUSTED, LOST_WASTAGE. |
| INV-004 | V1 | The system shall maintain inventory_balances as a reconciled cache derived from the ledger — never the source of truth. |
| INV-005 | V1 | The system shall provide a reconciliation function that recomputes balances from the ledger and flags discrepancies. |
| INV-006 | V1 | The system shall use an explicit state-machine function for inventory transactions that validates legality. |
| INV-007 | V1 | The system shall reject DELIVER transactions where delivered quantity exceeds allocated quantity. |
| INV-008 | V1 | The system shall enforce the inventory conservation law: available + reserved + allocated + delivered + lost = total_received. |
| INV-009 | V1 | The system shall generate an alert when reconciliation detects a discrepancy. |
| INV-010 | V1 | The system shall allow admin users to create manual adjustments with mandatory reason and audit trail. |
| INV-011 | V1 | The system shall auto-release expired inventory reservations via Celery beat, marking orders as FAILED. |
| INV-012 | V1 | The system shall create RESERVED transactions atomically within the order creation transaction. |
| INV-013 | V1 | The system shall create RELEASED transactions on order cancellation or delivery failure. |
| INV-014 | V1 | The system shall create ALLOCATED transactions when a delivery is assigned to a driver. |
| INV-015 | V1 | The system shall create DELIVERED transactions when proof of delivery is confirmed. |
| INV-016 | V1 | The system shall provide admin endpoints to view the inventory ledger with filtering. |
| INV-017 | V1 | The system shall reject orders when requested quantity exceeds available inventory. |
| INV-018 | V1 | The system shall use row-level locking during reservation to prevent race conditions. |

---

## 9. Pricing (PRC)

| ID | Phase | Requirement |
|----|-------|-------------|
| PRC-001 | V1 | The system shall compute all prices through a single PricingService.quote() function — the only place price is calculated. |
| PRC-002 | V1 | The system shall store the pricing rule version used for each order item in the commercial snapshot. |
| PRC-003 | V1 | The system shall support FIXED, PER_LITRE, and TIERED pricing models. |
| PRC-004 | V1 | The system shall re-compute price at order creation and require re-confirmation if it differs from the quote. |
| PRC-005 | V1 | The system shall support purpose-specific and quality-specific pricing rules. |
| PRC-006 | V1 | The system shall support customer-type-specific pricing rules. |
| PRC-007 | PHASE 2 | The system shall support area-based pricing rules for multi-city operations. |
| PRC-008 | V1 | The system shall provide admin CRUD endpoints for pricing rules with audit logging. |
| PRC-009 | V1 | The system shall support pricing rule versioning with activation periods. |
| PRC-010 | V1 | The system shall compute delivery charges based on configurable delivery pricing rules. |
| PRC-011 | V1 | The system shall return a non-binding price quote via POST /orders/quote with complete breakdown. |

---

## 10. Coupons / Promotions (CPN)

| ID | Phase | Requirement |
|----|-------|-------------|
| CPN-001 | V1 | The system shall support coupon codes with discount type, value, min order amount, validity window, and usage limits. |
| CPN-002 | V1 | The system shall validate coupon codes server-side during quote and order creation. |
| CPN-003 | V1 | The system shall apply validated coupon discounts within PricingService.quote(). |
| CPN-004 | V1 | The system shall provide admin CRUD endpoints for coupons. |
| CPN-005 | V1 | The system shall reject coupons exceeding total or per-customer usage limits. |
| CPN-006 | V1 | The system shall reject coupons outside their validity window. |

---

## 11. Orders (ORD)

| ID | Phase | Requirement |
|----|-------|-------------|
| ORD-001 | V1 | The system shall allow customers to create standard orders by selecting variant, quantity, address, and time slot. |
| ORD-002 | V1 | The system shall support order types: STANDARD, SCHEDULED, RECURRING, BULK. |
| ORD-003 | V1 | The system shall store all order quantity fields as integer litres using BIGINT. |
| ORD-004 | V1 | The system shall model every order as having one or more deliveries (1:N), even when N=1. |
| ORD-005 | V1 | The system shall compute order price server-side via PricingService.quote(), never accepting client-provided prices. |
| ORD-006 | V1 | The system shall store a complete commercial snapshot in order_items at creation time. |
| ORD-007 | V1 | The system shall ensure catalog/pricing changes never alter historical order snapshots. |
| ORD-008 | V1 | The system shall implement the order state machine with all defined states. |
| ORD-009 | V1 | The system shall reject illegal order status transitions using a transition() function. |
| ORD-010 | V1 | The system shall transition a parent order to DELIVERED only when all child deliveries are DELIVERED. |
| ORD-011 | V1 | The system shall mark orders as FAILED when inventory reservation expires. |
| ORD-012 | V1 | The system shall support Idempotency-Key header on POST /orders. |
| ORD-013 | V1 | The system shall allow customer cancellation only before OUT_FOR_DELIVERY status. |
| ORD-014 | V1 | The system shall allow admin cancellation at any status with mandatory reason. |
| ORD-015 | V1 | The system shall re-compute price at order creation and require re-confirmation if changed. |
| ORD-016 | V1 | The system shall create orders in a single atomic transaction (validate → quote → create → snapshot → reserve → pay). |
| ORD-017 | V1 | The system shall allow customers to view order history with pagination and filtering. |
| ORD-018 | V1 | The system shall allow customers to view detailed order information. |
| ORD-019 | V1 | The system shall support reordering from history with pre-filled details. |
| ORD-020 | V1 | The system shall allow admin users to view all orders with filtering, sorting, and pagination. |
| ORD-021 | V1 | The system shall support configurable delivery time slots/windows. |
| ORD-022 | V1 | The system shall allow customers to track order status via polling. |

---

## 12. Deliveries (DEL)

| ID | Phase | Requirement |
|----|-------|-------------|
| DEL-001 | V1 | The system shall create one or more delivery records for each order, always modeling 1:N. |
| DEL-002 | V1 | The system shall treat each delivery as independently trackable with its own state machine. |
| DEL-003 | V1 | The system shall store all delivery quantity fields as integer litres using BIGINT. |
| DEL-004 | V1 | The system shall implement the delivery state machine with all defined states and REASSIGNING loop. |
| DEL-005 | V1 | The system shall reject illegal delivery status transitions using a transition() function. |
| DEL-006 | V1 | The system shall reject delivery completion when delivered quantity exceeds allocated quantity. |
| DEL-007 | V1 | The system shall ensure parent order reaches DELIVERED only when all child deliveries are DELIVERED. |
| DEL-008 | V1 | The system shall support partial delivery with automatic remainder delivery creation. |
| DEL-009 | V1 | The system shall keep orders in PROCESSING when partial delivery occurs. |
| DEL-010 | V1 | The system shall use offer/accept/reject assignment pattern with configurable timeout. |
| DEL-011 | V1 | The system shall auto-re-offer deliveries on driver rejection or timeout. |
| DEL-012 | V1 | The system shall alert ops when no driver accepts after N attempts. |
| DEL-013 | V1 | The system shall allow admin manual delivery assignment. |
| DEL-014 | V1 | The system shall allow admin delivery reassignment with reason. |
| DEL-015 | V1 | The system shall generate a unique OTP per delivery for proof of delivery. |
| DEL-016 | V1 | The system shall verify OTP before marking delivery complete. |
| DEL-017 | V1 | The system shall support optional photo upload as delivery proof. |
| DEL-018 | V1 | The system shall record GPS coordinates at delivery completion. |
| DEL-019 | V1 | The system shall record timestamped delivery lifecycle events. |
| DEL-020 | V1 | The system shall support driver trip status updates (STARTED, ARRIVED). |
| DEL-021 | V1 | The system shall allow admin to view all deliveries with filtering and details. |
| DEL-022 | PHASE 2 | The system shall support real-time WebSocket-based live delivery tracking. |

---

## 13. Driver Management (DRV)

| ID | Phase | Requirement |
|----|-------|-------------|
| DRV-001 | V1 | The system shall allow drivers to toggle availability (AVAILABLE/UNAVAILABLE). |
| DRV-002 | V1 | The system shall present delivery offers only to available drivers with sufficient vehicle capacity. |
| DRV-003 | V1 | The system shall allow drivers to view delivery history with pagination. |
| DRV-004 | V1 | The system shall allow drivers to view earnings summary and breakdown. |
| DRV-005 | V1 | The system shall allow admin to CRUD driver profiles. |
| DRV-006 | V1 | The system shall allow drivers to receive and respond to delivery offer notifications. |
| DRV-007 | V1 | The system shall provide Google Maps navigation deep link from active delivery view. |

---

## 14. Vehicle / Fleet Management (VEH)

| ID | Phase | Requirement |
|----|-------|-------------|
| VEH-001 | V1 | The system shall store vehicle records with registration, type, capacity (BIGINT litres), status, and current driver. |
| VEH-002 | V1 | The system shall allow admin to CRUD vehicle records. |
| VEH-003 | V1 | The system shall assign vehicles to drivers and track vehicle-driver mapping. |
| VEH-004 | V1 | The system shall prevent delivery assignment to drivers with insufficient vehicle capacity. |
| VEH-005 | PHASE 3 | The system shall support predictive maintenance, fuel tracking, and compliance automation. |

---

## 15. Payments (PAY)

| ID | Phase | Requirement |
|----|-------|-------------|
| PAY-001 | V1 | The system shall create payment intents server-side via PaymentGatewayAdapter (Razorpay V1). |
| PAY-002 | V1 | The system shall process payment status exclusively via webhook with signature verification. |
| PAY-003 | V1 | The system shall implement an idempotent webhook handler. |
| PAY-004 | V1 | The system shall never trust client-reported payment success. |
| PAY-005 | V1 | The system shall support Idempotency-Key on payment verification endpoints. |
| PAY-006 | V1 | The system shall store raw gateway interaction records in payment_transactions. |
| PAY-007 | V1 | The system shall transition orders PENDING_PAYMENT → CONFIRMED on successful webhook. |
| PAY-008 | V1 | The system shall allow admin to view payment records. |
| PAY-009 | V1 | The system shall support payment retry on failure. |
| PAY-010 | V1 | The system shall queue failed payment intents for retry on gateway downtime. |

---

## 16. Refunds (RFD)

| ID | Phase | Requirement |
|----|-------|-------------|
| RFD-001 | V1 | The system shall auto-initiate refund on customer cancellation (pre-OUT_FOR_DELIVERY). |
| RFD-002 | V1 | The system shall allow admin to manually initiate refunds with mandatory reason. |
| RFD-003 | V1 | The system shall track refund status and update payment to REFUNDED on confirmation. |
| RFD-004 | V1 | The system shall store refund records with payment ref, amount, reason, status. |
| RFD-005 | V1 | The system shall notify customers on refund initiation and completion. |
| RFD-006 | V1 | The system shall allow admin to view refund records and status. |

---

## 17. Notifications (NTF)

| ID | Phase | Requirement |
|----|-------|-------------|
| NTF-001 | V1 | The system shall notify customers when inventory reservation expires and order fails. |
| NTF-002 | V1 | The system shall implement channel-agnostic NotificationService with Push/SMS/Email adapters. |
| NTF-003 | V1 | The system shall retry failed notifications and use fallback channels for critical events. |
| NTF-004 | V1 | The system shall send push notifications at key order/delivery lifecycle transitions. |
| NTF-005 | V1 | The system shall send push notifications to drivers for delivery offers. |
| NTF-006 | V1 | The system shall notify customers for partial delivery events. |
| NTF-007 | V1 | The system shall send delivery OTP to customer via push/SMS. |
| NTF-008 | V1 | The system shall store notification records with delivery status. |
| NTF-009 | V1 | The system shall notify ops team on delivery assignment escalation. |

---

## 18. Reviews / Ratings (REV)

| ID | Phase | Requirement |
|----|-------|-------------|
| REV-001 | V1 | The system shall allow customers to rate and review completed deliveries (1–5 stars + comment). |
| REV-002 | V1 | The system shall store reviews with order ref, customer ref, rating, and comment. |
| REV-003 | V1 | The system shall allow admin to view all reviews with filtering. |
| REV-004 | V1 | The system shall allow drivers to view reviews for their deliveries. |

---

## 19. Admin Operations (ADM)

| ID | Phase | Requirement |
|----|-------|-------------|
| ADM-001 | V1 | The system shall provide a dashboard summary with key operational metrics and alerts. |
| ADM-002 | V1 | The system shall enforce soft-delete semantics for admin catalog operations. |
| ADM-003 | V1 | The system shall generate alerts when critical operational thresholds are breached. |
| ADM-004 | V1 | The system shall allow admin manual interventions on orders. |
| ADM-005 | V1 | The system shall log every admin mutation in audit_logs. |

---

## 20. Reporting (RPT)

| ID | Phase | Requirement |
|----|-------|-------------|
| RPT-001 | V1 | The system shall provide sales report views (revenue by period, purpose, quality, customer type). |
| RPT-002 | V1 | The system shall provide water supply/consumption report views. |
| RPT-003 | V1 | The system shall provide delivery performance report views. |
| RPT-004 | V1 | The system shall provide customer report views (retention, order patterns). |
| RPT-005 | V1 | The system shall use scheduled Celery aggregation jobs for report data. |

---

## 21. Analytics (ANL)

| ID | Phase | Requirement |
|----|-------|-------------|
| ANL-001 | PHASE 2 | The system shall provide an advanced analytics dashboard. |
| ANL-002 | PHASE 2 | The system shall support demand trend analysis. |
| ANL-003 | PHASE 2 | The system shall support customer cohort analysis. |
| ANL-004 | PHASE 3 | The system shall support ML-based demand forecasting. |
| ANL-005 | PHASE 3 | The system shall support ML-based dynamic pricing recommendations. |

---

## 22. Businesses / B2B (BIZ)

| ID | Phase | Requirement |
|----|-------|-------------|
| BIZ-001 | V1 | The system shall store database schema for businesses, business users, and business sites (ARCHITECTURE ONLY). |
| BIZ-002 | PHASE 2 | The system shall allow business customer registration. |
| BIZ-003 | PHASE 2 | The system shall support distinct business admin vs. employee roles. |
| BIZ-004 | PHASE 2 | The system shall allow business admins to invite employees and assign them to sites. |
| BIZ-005 | PHASE 2 | The system shall allow business admins to manage multiple delivery sites. |
| BIZ-006 | PHASE 2 | The system shall provide a consolidated business dashboard. |
| BIZ-007 | V1 | The system shall provide basic CRUD backend endpoints for B2B entities. |

---

## 23. Bulk Orders (BULK)

| ID | Phase | Requirement |
|----|-------|-------------|
| BULK-001 | V1 | The system shall store database schema for bulk requests and quotes (ARCHITECTURE ONLY). |
| BULK-002 | PHASE 2 | The system shall allow business customers to submit bulk order requests. |
| BULK-003 | PHASE 2 | The system shall allow admin to create quotes for bulk requests. |
| BULK-004 | PHASE 2 | The system shall allow customers to accept/reject bulk quotes. |
| BULK-005 | PHASE 2 | The system shall generate orders/deliveries from accepted bulk requests. |
| BULK-006 | V1 | The system shall provide basic CRUD backend endpoints for bulk requests/quotes. |
| BULK-007 | PHASE 2 | The system shall handle bulk request rejection with notification. |

---

## 24. Recurring Orders (REC)

| ID | Phase | Requirement |
|----|-------|-------------|
| REC-001 | V1 | The system shall store database schema for recurring orders and instances (ARCHITECTURE ONLY). |
| REC-002 | PHASE 2 | The system shall allow business customers to set up recurring deliveries. |
| REC-003 | PHASE 2 | The system shall allow individual customers to set up recurring deliveries. |
| REC-004 | PHASE 2 | The system shall auto-generate order instances from recurring orders on schedule. |
| REC-005 | PHASE 2 | The system shall allow pause, skip, and cancel of recurring orders. |
| REC-006 | PHASE 2 | The system shall flag and notify on recurring instance generation failure. |
| REC-007 | V1 | The system shall provide basic CRUD backend endpoints for recurring orders. |

---

## 25. Invoices (INVC)

| ID | Phase | Requirement |
|----|-------|-------------|
| INVC-001 | V1 | The system shall store database schema for invoices (ARCHITECTURE ONLY). |
| INVC-002 | PHASE 2 | The system shall support period-based B2B invoice generation. |
| INVC-003 | PHASE 2 | The system shall allow business customers to view/download invoices. |
| INVC-004 | PHASE 2 | The system shall track invoice payment status and due dates. |
| INVC-005 | PHASE 2 | The system shall generate statement summaries for business customers. |

---

## 26. Routes (RTE)

| ID | Phase | Requirement |
|----|-------|-------------|
| RTE-001 | V1 | The system shall store database schema stub for routes (ARCHITECTURE ONLY). |
| RTE-002 | PHASE 2 | The system shall support algorithmic multi-stop route planning. |
| RTE-003 | PHASE 2 | The system shall provide a route management UI in admin dashboard. |
| RTE-004 | PHASE 2 | The system shall provide distance-based dispatch suggestions. |

---

## 27. Audit / Compliance (AUD)

| ID | Phase | Requirement |
|----|-------|-------------|
| AUD-001 | V1 | The system shall maintain an immutable audit log for every admin action. |
| AUD-002 | V1 | The system shall never update or delete audit log rows. |
| AUD-003 | V1 | The system shall log all admin mutations to catalog, pricing, and inventory. |
| AUD-004 | V1 | The system shall provide an admin audit log viewer with filtering and search. |
| AUD-005 | V1 | The system shall record order status transition history. |
| AUD-006 | V1 | The system shall support audit trail queries for complete entity history reconstruction. |
| AUD-007 | V1 | The system shall comply with DLT requirements for commercial SMS in India. |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total Requirements | 203 |
| V1 Requirements | 170 |
| Phase 2 Requirements | 29 |
| Phase 3 Requirements | 4 |
| Modules Covered | 27/27 |
