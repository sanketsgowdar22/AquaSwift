# AquaSwift — Glossary

**Version:** 1.0
**Last Updated:** 2026-08-31

---

This glossary defines domain-specific terminology used throughout AquaSwift's product and engineering documentation. Terms are grouped by domain and sorted alphabetically within each group.

---

## Water & Catalog Domain

| Term | Definition |
|------|-----------|
| **Catalog** | The complete set of orderable water offerings, composed from the four independent dimensions: Purpose, Quality, Delivery Method, and Variant. Entirely admin-configurable — no hard-coded product lists. |
| **Delivery Method** | How water is physically delivered to the customer. Examples: Jar (20L container), Can (50L container), Tanker (1,000–10,000L vehicle), Bulk Tanker (10,000–100,000L vehicle). Stored in `delivery_methods`. Admin-configurable. |
| **Dimension** | One of the four independent, composable axes that define a water offering: Purpose, Quality/Grade, Quantity, and Delivery Method. These are never collapsed into a single "water type" enum. |
| **Purpose** | The intended use of the water. Examples: Drinking, Daily Use, Construction, Cleaning, Industrial, Agriculture. Stored in `water_purposes`. Admin-configurable with icon, description, and display order. |
| **Quality / Grade** | The treatment or purity level of water. Examples: RO+UV, Purified, Treated, Utility Grade. Stored in `water_quality_types`. Admin-configurable. Linked to purposes via `water_purpose_qualities` join table. |
| **Quality Record** | A lab test result for water from a specific source, including pH, TDS, turbidity, treatment type, tester identity, test date, and certificate URL. Stored in `water_quality_records`. |
| **Variant** | A specific orderable combination of Purpose × Quality × Delivery Method, with defined minimum and maximum quantity ranges (in litres). Stored in `water_variants`. A variant is the atomic unit that a customer selects when placing an order. |
| **Water Source** | A physical location where water is produced, treated, or stored (e.g., a treatment plant, well, reservoir). Has a name, type, GPS location, capacity in litres, and operational status. Stored in `water_sources`. Inventory is tracked per source. |

---

## Inventory Domain

| Term | Definition |
|------|-----------|
| **Allocation** | The act of committing reserved inventory to a specific delivery vehicle/source for fulfilment. Transitions inventory from RESERVED to ALLOCATED. Occurs when dispatch assigns a driver/vehicle to a delivery. |
| **Available (Balance)** | The quantity of water at a source that is not reserved, allocated, or otherwise committed. Derived from the ledger, never stored as a mutable counter. `available = total_received - reserved - allocated - delivered - lost_wastage`. |
| **Inventory Balance** | A cached summary of a source's current inventory state: available, reserved, and allocated litres. Stored in `inventory_balances` as a **reconciled cache** — never the source of truth. Rebuilt from the ledger on demand or periodically. |
| **Inventory Ledger** | The `inventory_transactions` table — an **append-only** log of every inventory movement. Transaction types: RECEIVED, RESERVED, RELEASED, ALLOCATED, DELIVERED, ADJUSTED, LOST_WASTAGE. The ledger is the single source of truth for all inventory. Balances are always derivable by summing the ledger. |
| **Inventory Transaction** | A single row in the inventory ledger recording a quantity change (positive or negative) at a specific source, with a type, reference to the causing entity (order, delivery, adjustment), actor, timestamp, and optional notes. |
| **Reconciliation** | The process of recomputing `inventory_balances` by summing all transactions in the inventory ledger for a given source. Used to verify correctness and detect discrepancies. |
| **Release** | Returning previously reserved or allocated inventory back to available. Occurs on order cancellation, delivery failure, or reservation expiry. Creates a RELEASED transaction in the ledger. |
| **Reservation** | A soft hold on inventory when an order is confirmed. Reduces available balance; increases reserved balance. Prevents overselling but does not commit to a specific source/vehicle until allocation. Has a configurable expiry timeout. |
| **Reservation Expiry** | A Celery beat job that periodically checks for orders stuck in PENDING_PAYMENT beyond a configurable timeout. Expired reservations are released (reserved → available), and the associated order is marked FAILED. |

---

## Commerce Domain

| Term | Definition |
|------|-----------|
| **Commercial Snapshot** | A frozen copy of all pricing and product details stored within `order_items` at order creation time. Includes purpose name, quality name, quantity, unit price, delivery charge, discount, tax, and final total. Subsequent changes to catalog or pricing configuration never alter historical snapshots. |
| **Coupon** | A promotional code offering a discount (percentage or fixed amount) on an order. Has validity dates, usage limits, per-customer limits, and minimum order amount thresholds. Stored in `coupons`. Validated and applied server-side only. |
| **Delivery Charge** | A fee added to an order for transporting water from source to customer site. May be based on distance bands, vehicle type, or flat rate. Defined in `delivery_pricing_rules`. Computed server-side as part of the pricing quote. |
| **Idempotency Key** | A client-generated unique identifier sent in the `Idempotency-Key` HTTP header with `POST /orders` and `POST /payments/verify` requests. Prevents duplicate order creation or payment verification on client retry. The server returns the original response if the same key is seen again. |
| **Order** | A customer's request to purchase water. Contains: customer, variant, order type, quantity, pricing snapshot, status, scheduled delivery window. One order can generate multiple deliveries. Stored in `orders` with line items in `order_items`. |
| **Order Item** | A line item within an order storing the commercial snapshot: purpose name, quality name, quantity in litres, unit price, water total, delivery charge, discount total, tax total, and final total for that line. The pricing rule version used is also recorded. |
| **Order Type** | Classification of an order: STANDARD (one-time, immediate/scheduled), SCHEDULED (specific future date/time), RECURRING (repeating schedule), or BULK (large quantity, potentially multi-delivery). |
| **Pricing Model** | The method used to calculate water price: FIXED (flat price regardless of quantity), PER_LITRE (price × quantity), or TIERED (different price per litre at different quantity thresholds). Configured in `pricing_rules`. |
| **Pricing Rule** | A configurable rule defining how to price a specific combination of purpose, quality, customer type, and/or area. Has a version, activation period, and pricing model (fixed/per-litre/tiered). Stored in `pricing_rules`. |
| **Quote** | A non-binding price and availability preview returned by `POST /orders/quote`. Shows the price breakdown the customer will pay if they proceed. Computed by `PricingService.quote()` — the same function used during actual order creation, ensuring the quoted price equals the charged price. |

---

## Fulfilment Domain

| Term | Definition |
|------|-----------|
| **Assignment** | The process of matching a delivery to a driver. Can be automatic (offer/accept pattern) or manual (ops manager assigns directly). Tracked in `delivery_assignments` for audit. |
| **Delivery** | A single physical trip to transport water from a source to a customer site. One order can have multiple deliveries (1:N relationship). Each delivery has its own state machine, assigned driver, assigned vehicle, quantity, OTP code, and proof. Stored in `deliveries`. |
| **Delivery Event** | A timestamped lifecycle event for a delivery (e.g., "offered to driver X", "driver accepted", "driver departed", "arrived at site"). Stored in `delivery_events` for timeline display. |
| **Dispatch** | The cross-cutting process of processing confirmed orders into deliveries and assigning them to drivers. Not a standalone backend module — the logic lives in the Deliveries module (`deliveries/service.py`). |
| **OTP (Delivery)** | A one-time password generated for each delivery, shared with the customer (via push/SMS), and entered by the driver at delivery time to prove the delivery was received by the correct person. Different from login OTP. |
| **Partial Delivery** | When a driver delivers less than the full quantity for a delivery (e.g., vehicle capacity issue). The delivery is marked PARTIALLY_DELIVERED with the actual quantity, and a new delivery is created for the remainder. |
| **Proof of Delivery** | Evidence that a delivery was completed: OTP verification (mandatory), photo upload (optional), GPS coordinates at delivery time, and delivered quantity. Stored on the delivery record. |
| **Reassignment** | When a driver rejects a delivery offer or fails to respond within the timeout, the delivery returns to the assignment pool and is offered to the next eligible driver. The rejection is recorded in `delivery_assignments`. |

---

## Identity & Access Domain

| Term | Definition |
|------|-----------|
| **Actor** | Any user performing an action in the system: Customer, Driver, Operations Manager, or Super Admin. Identified by `user_id`. All audit records reference the actor. |
| **Customer Profile** | Additional customer-specific data linked to a user: delivery addresses, order history, preferences. Stored in `customer_profiles`. |
| **Driver Profile** | Additional driver-specific data linked to a user: availability status, current vehicle, service area, earnings. Stored in `driver_profiles` / `drivers`. |
| **JWT (JSON Web Token)** | The authentication token issued after successful login. Contains user identity and role claims. Short-lived; refreshed via refresh token. Used in `Authorization: Bearer <token>` header. |
| **OTP (Login)** | A one-time password sent via SMS (MSG91) for customer and driver authentication. 6-digit code with configurable expiry. Different from delivery OTP. |
| **Permission** | A granular access right (e.g., `orders:read`, `catalog:write`, `inventory:adjust`). Checked by the `require_permission()` FastAPI dependency on every protected endpoint. |
| **RBAC (Role-Based Access Control)** | The authorization model. Users are assigned roles (e.g., CUSTOMER, DRIVER, OPS_MANAGER, SUPER_ADMIN). Each role grants a set of permissions. Permissions are checked server-side on every request. |
| **Refresh Token** | A long-lived token used to obtain a new JWT without re-authentication. Stored securely; invalidated on logout or security events. |
| **Role** | A named collection of permissions assigned to users. Predefined roles: CUSTOMER, DRIVER, OPS_MANAGER, SUPER_ADMIN. Stored in `roles`; user-role linkage in `user_roles`. |

---

## B2B Domain

| Term | Definition |
|------|-----------|
| **Bulk Order** | A large-quantity water order (typically business customers) that may require multiple deliveries over a period. Initiated via a request/quote/accept workflow. Schema in `bulk_requests` and `bulk_quotes`. ARCHITECTURE ONLY in V1. |
| **Bulk Quote** | A price proposal from the admin in response to a bulk order request. Contains price details, expiry date, and status. The customer can accept or reject. Stored in `bulk_quotes`. |
| **Bulk Request** | A business customer's request for a large quantity of water over a period. Contains purpose, quality, quantity, site, schedule, and frequency. Sent to admin for quoting. Stored in `bulk_requests`. |
| **Business** | A company or organization registered on the platform for B2B water supply. Has a profile, employees (linked users), and sites (delivery locations). Stored in `businesses`. |
| **Business Site** | A delivery location belonging to a business (e.g., a construction site, factory floor, hotel property). Linked to an address. Stored in `business_sites`. |
| **Invoice** | A billing document for business customers, covering a period or specific order. Contains line items, amounts, due date, and payment status. Stored in `invoices`. ARCHITECTURE ONLY in V1. |
| **Recurring Order** | An order that repeats on a schedule (e.g., "500L every Monday and Thursday"). The system auto-generates individual order instances on schedule. Stored in `recurring_orders` with instances in `recurring_order_instances`. ARCHITECTURE ONLY in V1. |
| **Recurring Instance** | A single scheduled occurrence of a recurring order. Has a scheduled date and may link to a generated order once created. Stored in `recurring_order_instances`. |

---

## Payment Domain

| Term | Definition |
|------|-----------|
| **Gateway Adapter** | An abstraction layer (`PaymentGatewayAdapter` interface) that decouples payment logic from a specific provider. Methods: `create_intent`, `verify_webhook`, `refund`. Razorpay is the V1 concrete implementation. See ADR DEC-PAY-001. |
| **Payment** | A record of a financial transaction for an order. Tracks amount, method, and status (INITIATED → SUCCESS / FAILED / REFUNDED). Stored in `payments`. |
| **Payment Intent** | A server-side request to the payment gateway to prepare a payment session. Created when the customer initiates checkout. The gateway returns a session/order ID that the client uses to complete payment. |
| **Payment Transaction** | The raw gateway interaction record: gateway reference ID, raw response payload (JSONB), and verification timestamp. Stored in `payment_transactions` for audit and reconciliation. |
| **Refund** | A reversal of a successful payment, processed through the payment gateway. Triggered by order cancellation or admin action. Tracked in `refunds` with amount, reason, and status. |
| **Webhook** | An HTTP callback from the payment gateway (Razorpay) notifying the server of payment events (success, failure, refund). The webhook handler is **idempotent** and is the **only** code path that writes `payments.status = SUCCESS`. |

---

## Platform Domain

| Term | Definition |
|------|-----------|
| **Adapter Pattern** | A design pattern used throughout AquaSwift for external integrations. A generic interface defines the contract; a concrete implementation handles a specific provider. Allows swapping providers without changing business logic. Used for: payments (Razorpay), SMS (MSG91), push, email, storage. |
| **Audit Log** | An immutable record of an action performed in the system: actor, action, entity type/ID, before/after state (JSONB), metadata, and timestamp. Stored in `audit_logs`. Required for all admin mutations to catalog, pricing, and inventory. |
| **Celery** | The distributed task queue used for background jobs (e.g., reservation expiry, notification sending, report generation). Workers process tasks; Beat schedules periodic tasks. |
| **Modular Monolith** | The architectural pattern for AquaSwift's backend. All modules run in a single deployable unit but are structured as clearly separated packages that could be extracted into independent services later. Module boundaries follow the `backend/app/<module>/` directory structure. |
| **Notification** | A message sent to a user via one or more channels (push, SMS, email). Sent through the channel-agnostic `NotificationService.send(user, event, context)`. Stored in `notifications` with channel, template, payload, and delivery status. |
| **SMS Provider** | An abstraction layer (`SMSProvider` interface) for SMS/OTP delivery. Methods: `send_otp`, `verify_otp`. MSG91 is the V1 implementation (India-focused, DLT-compliant). See ADR DEC-AUTH-001. |
| **State Machine** | An explicit function `transition(entity, new_status, actor, reason)` that validates whether a status transition is legal (against an allow-list), applies the change inside a DB transaction, writes a history/audit row, and triggers side effects. Used for Orders, Deliveries, and Inventory transactions. |

---

## Abbreviations

| Abbreviation | Full Form |
|-------------|-----------|
| ADR | Architectural Decision Record |
| API | Application Programming Interface |
| CRUD | Create, Read, Update, Delete |
| DLT | Distributed Ledger Technology (in SMS context: India's telecom regulatory requirement for commercial SMS) |
| ERD | Entity-Relationship Diagram |
| FCM | Firebase Cloud Messaging |
| GPS | Global Positioning System |
| JWT | JSON Web Token |
| OTP | One-Time Password |
| PRD | Product Requirements Document |
| RBAC | Role-Based Access Control |
| RDS | Relational Database Service (AWS) |
| SMS | Short Message Service |
| SRS | Software Requirements Specification |
| TDS | Total Dissolved Solids (water quality metric) |
| TTL | Time To Live (cache expiry duration) |
| UPI | Unified Payments Interface (India's instant payment system) |
| UUID | Universally Unique Identifier |
