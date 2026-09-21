# AquaSwift — Software Requirements Specification (SRS)

**Version:** 1.0
**Status:** Draft
**Last Updated:** 2026-09-03
**Document Type:** Authoritative, complete requirements specification

---

> This document contains every functional requirement for AquaSwift, grouped by module, with each requirement individually phase-tagged. Requirements cover the full system across all phases (V1, Phase 2, Phase 3). V1 scoping is a build-sequencing decision captured in `PRODUCT_SCOPE.md`; it is not a reason to omit a requirement from this spec.

---

## Document Conventions

- **Requirement Format:** `<PREFIX>-<NNN>` followed by phase tag, testable statement, actors, preconditions, data involved, and source.
- **Phase Tags:** `[V1]` = MVP, `[PHASE 2]` = next major release, `[PHASE 3]` = future.
- **Module Prefixes:** See §2 of the Sub-Phase 0B prompt for the authoritative prefix table.
- **Source References:** PRD §X.Y, P1–P5 (persona IDs), J1–J10 (journey IDs), Master Prompt §N Rule M.

---

## 1. Authentication & Identity (AUTH)

---

AUTH-001
[V1]
The system shall allow customers and drivers to register and authenticate using OTP-based mobile number verification.

Actors: Customer (P1), Driver (P3)
Preconditions: User has a valid Indian mobile number and SMS reception capability
Data involved: `users`, OTP code, mobile number, JWT, refresh token
Source: PRD §5.1 (OTP-based registration/login), J1 Steps 2–3, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

AUTH-002
[V1]
The system shall send a 6-digit OTP to the user's mobile number via the SMS provider (MSG91 in V1) upon receiving an OTP request.

Actors: Customer (P1), Driver (P3)
Preconditions: Valid mobile number format provided
Data involved: OTP code, mobile number, SMS provider adapter
Source: PRD §5.1, GLOSSARY.md (OTP Login), J1 Step 2

---

AUTH-003
[V1]
The system shall verify the OTP entered by the user against the server-generated OTP and, upon successful verification, issue a JWT access token and a refresh token.

Actors: Customer (P1), Driver (P3)
Preconditions: OTP has been sent and is not expired
Data involved: `users`, JWT, refresh token, OTP code
Source: PRD §5.1, J1 Step 3, GLOSSARY.md (JWT)

---

AUTH-004
[V1]
The system shall support OTP expiry — an OTP not verified within a configurable time window (e.g., 5 minutes) shall be rejected.

Actors: Customer (P1), Driver (P3)
Preconditions: OTP has been generated
Data involved: OTP code, expiry timestamp
Source: GLOSSARY.md (OTP Login — "configurable expiry"), PRD §9.1 (SMS/OTP delivery failure risk)

---

AUTH-005
[V1]
The system shall allow admin and operations manager users to authenticate using email and password.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin account has been created with valid email and password
Data involved: `users`, email, hashed password, JWT, refresh token
Source: PRD §5.1 (Email+password login), PRODUCT_SCOPE.md (Admin — MUST HAVE — V1)

---

AUTH-006
[V1]
The system shall issue short-lived JWT access tokens and longer-lived refresh tokens, allowing clients to obtain new access tokens without re-authentication.

Actors: All authenticated users
Preconditions: User has a valid refresh token
Data involved: JWT, refresh token, token expiry
Source: GLOSSARY.md (JWT, Refresh Token), PRD §5.1

---

AUTH-007
[V1]
The system shall invalidate all refresh tokens for a user upon explicit logout or security events (e.g., password change, account deactivation).

Actors: All authenticated users, System
Preconditions: User is authenticated
Data involved: Refresh tokens, `users`
Source: GLOSSARY.md (Refresh Token — "invalidated on logout or security events")

---

AUTH-008
[V1]
The system shall create a new user record upon first successful OTP verification if no account exists for that mobile number.

Actors: Customer (P1), Driver (P3)
Preconditions: OTP verified, no existing user for this mobile number
Data involved: `users`, `customer_profiles` or `driver_profiles`
Source: J1 Step 3 ("creates user"), PRD §5.1

---

AUTH-009
[V1]
The system shall enforce rate limiting on OTP request and verification endpoints to prevent brute-force attacks.

Actors: System
Preconditions: None
Data involved: Request rate counters per IP/mobile number
Source: Master Prompt §10 Step 18 (rate limiting on auth/OTP endpoints)

---

AUTH-010
[V1]
The system shall support a retry mechanism with a fallback channel (e.g., email OTP) when primary SMS OTP delivery fails.

Actors: Customer (P1), Driver (P3), System
Preconditions: Primary SMS delivery has failed
Data involved: OTP code, fallback channel configuration
Source: PRD §9.1 (SMS/OTP delivery failure — "Retry with fallback channel")

---

## 2. RBAC & Permissions (RBAC)

---

RBAC-001
[V1]
The system shall enforce role-based access control (RBAC) on every protected API endpoint using a `require_permission()` server-side dependency.

Actors: System
Preconditions: User is authenticated with a valid JWT
Data involved: `roles`, `user_roles`, permission definitions
Source: Master Prompt §1 Rule 5 (server-side authority), PRD §5.1 (RBAC & permissions engine), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

RBAC-002
[V1]
The system shall support the following predefined platform roles: `CUSTOMER`, `DRIVER`, `OPS_MANAGER`, `SUPER_ADMIN`.

Actors: System
Preconditions: None
Data involved: `roles`, `user_roles`
Source: GLOSSARY.md (Role), PRD §4.1–4.5

---

RBAC-003
[V1]
The system shall assign each role a defined set of granular permissions (e.g., `orders:read`, `catalog:write`, `inventory:adjust`) and check the requesting user's permissions on every protected endpoint.

Actors: System
Preconditions: User has an assigned role
Data involved: `roles`, `user_roles`, permission definitions
Source: GLOSSARY.md (Permission — "require_permission() FastAPI dependency"), Master Prompt §7

---

RBAC-004
[V1]
The system shall return HTTP 403 Forbidden when an authenticated user attempts to access an endpoint for which their role does not grant the required permission.

Actors: All authenticated users
Preconditions: User is authenticated but lacks required permission
Data involved: JWT claims, role permissions
Source: Master Prompt §10 Step 4 ("role mismatch returns 403"), GLOSSARY.md (RBAC)

---

RBAC-005
[V1]
The system shall prevent customers from accessing admin-only endpoints (e.g., catalog write, pricing rule management, inventory adjustment).

Actors: Customer (P1)
Preconditions: Customer is authenticated
Data involved: `roles`, `user_roles`, endpoint permissions
Source: PRD §5.1 (separate admin/customer capabilities), Master Prompt §13 ("RBAC prevents every out-of-role action")

---

RBAC-006
[V1]
The system shall prevent drivers from accessing admin-only or customer-only endpoints (e.g., placing orders, modifying catalog).

Actors: Driver (P3)
Preconditions: Driver is authenticated
Data involved: `roles`, `user_roles`, endpoint permissions
Source: PRD §5.1, Master Prompt §13

---

RBAC-007
[PHASE 2]
The system shall support distinct permission scopes for a business's admin users versus its employee users, independent of platform-level RBAC roles.

Actors: Business Admin (P2), Business Employee
Preconditions: Business is registered; users are linked to the business
Data involved: `businesses`, `business_users`, business-level permission scopes
Source: Sub-Phase 0B §0 Correction 2, P2 scenario ("invites 2 site supervisors as employees"), GLOSSARY.md (Business)

---

RBAC-008
[V1]
The system shall allow the Super Admin to manage role assignments — assigning and revoking roles for other users.

Actors: Super Admin (P5)
Preconditions: Super Admin is authenticated
Data involved: `users`, `roles`, `user_roles`, `audit_logs`
Source: PRD §4.5 (full system access), P5 goals

---

## 3. User & Customer Management (USR)

---

USR-001
[V1]
The system shall allow authenticated customers to create and update their profile (name, email, phone number).

Actors: Customer (P1)
Preconditions: Customer is authenticated
Data involved: `users`, `customer_profiles`
Source: PRD §5.1 (Profile management), J1 Step 4, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

USR-002
[V1]
The system shall allow authenticated drivers to create and update their profile (name, phone number, vehicle information).

Actors: Driver (P3)
Preconditions: Driver is authenticated
Data involved: `users`, `driver_profiles`/`drivers`
Source: PRD §5.1 (Driver — Profile management), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

USR-003
[V1]
The system shall allow admin users to view and search the list of all customers with pagination, filtering, and sorting.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `customers:read` permission
Data involved: `users`, `customer_profiles`
Source: PRD §5.1 (Admin — Customer management), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

USR-004
[V1]
The system shall allow admin users to view detailed customer information including profile, order history, and addresses.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `customers:read` permission
Data involved: `users`, `customer_profiles`, `orders`, `addresses`
Source: PRD §5.1 (Admin — Customer list & detail), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

USR-005
[V1]
The system shall create a customer profile record automatically upon first registration via OTP.

Actors: System
Preconditions: New user created via OTP verification
Data involved: `users`, `customer_profiles`
Source: J1 Step 3–4, AUTH-008

---

USR-006
[V1]
The system shall allow admin users to deactivate a customer account, preventing further logins and order placement.

Actors: Super Admin (P5)
Preconditions: Admin is authenticated with `customers:write` permission
Data involved: `users`, `customer_profiles`, `audit_logs`
Source: PRD §4.5 (Super Admin — full system configuration)

---

## 4. Address & Site Management (ADDR)

---

ADDR-001
[V1]
The system shall allow authenticated customers to add, edit, and delete delivery addresses associated with their account.

Actors: Customer (P1)
Preconditions: Customer is authenticated
Data involved: `addresses`
Source: PRD §5.1 (Address/site management), J1 Step 10, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

ADDR-002
[V1]
The system shall geocode addresses using Google Maps Platform to store latitude and longitude coordinates.

Actors: System
Preconditions: Address text or map pin provided
Data involved: `addresses` (lat, lng, formatted_address)
Source: PRD §5.1 (Google Maps geocoding), J1 Step 10, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

ADDR-003
[V1]
The system shall allow customers to select a saved address or add a new address during the order placement flow.

Actors: Customer (P1)
Preconditions: Customer is authenticated and placing an order
Data involved: `addresses`
Source: J1 Step 10, PRD §6.1

---

ADDR-004
[V1]
The system shall allow customers to add delivery instructions/notes to an address (e.g., "terrace tank access from back gate").

Actors: Customer (P1)
Preconditions: Customer is authenticated
Data involved: `addresses` (notes field)
Source: P1 Key Scenario (tank refill — "terrace tank access instructions in notes")

---

ADDR-005
[V1]
The system shall allow admin users to view and manage customer addresses.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `addresses:read` permission
Data involved: `addresses`, `users`
Source: PRD §5.1 (Admin — Address/site management)

---

ADDR-006
[PHASE 2]
The system shall support business sites — delivery locations belonging to a business — linked to addresses and manageable by business admin users.

Actors: Business Admin (P2)
Preconditions: Business is registered
Data involved: `business_sites`, `addresses`, `businesses`
Source: GLOSSARY.md (Business Site), P2 scenario ("adds 3 construction sites"), PRODUCT_SCOPE.md (ARCHITECTURE ONLY in V1)

---

ADDR-007
[V1]
The system shall store the schema for `business_sites` in V1, supporting the relationship between businesses, sites, and addresses, even though customer-facing UI is deferred to Phase 2.

Actors: System
Preconditions: None (schema-only)
Data involved: `business_sites`, `addresses`, `businesses`
Source: PRODUCT_SCOPE.md (ARCHITECTURE ONLY — "Schema exists, no customer UI"), Master Prompt §6

---

## 5. Water Catalog (CAT)

---

CAT-001
[V1]
The system shall store water purposes as admin-configurable records with name, description, icon URL, display order, and active status — never as hard-coded enums or constants.

Actors: Super Admin (P5)
Preconditions: None
Data involved: `water_purposes`
Source: Master Prompt §1 Rule 1 (RULE-001), PRD §7.1, GLOSSARY.md (Purpose)

---

CAT-002
[V1]
The system shall store water quality types as admin-configurable records with name, description, and active status — never as hard-coded enums or constants.

Actors: Super Admin (P5)
Preconditions: None
Data involved: `water_quality_types`
Source: Master Prompt §1 Rule 1 (RULE-001), PRD §7.1, GLOSSARY.md (Quality/Grade)

---

CAT-003
[V1]
The system shall store delivery methods as admin-configurable records with name and active status — never as hard-coded enums or constants.

Actors: Super Admin (P5)
Preconditions: None
Data involved: `delivery_methods`
Source: Master Prompt §1 Rule 1 (RULE-001), PRD §7.1, GLOSSARY.md (Delivery Method)

---

CAT-004
[V1]
The system shall support a `water_purpose_qualities` join table that controls which quality types are available for each purpose, configurable by admin users.

Actors: Super Admin (P5)
Preconditions: Purposes and quality types exist
Data involved: `water_purpose_qualities`, `water_purposes`, `water_quality_types`
Source: PRD §7.1 ("water_purpose_qualities join table"), J7 Step 4

---

CAT-005
[V1]
The system shall store water variants as orderable combinations of purpose × quality × delivery method, with admin-defined minimum and maximum quantity ranges in litres.

Actors: Super Admin (P5)
Preconditions: Valid purpose, quality, and delivery method records exist
Data involved: `water_variants` (purpose_id, quality_id, delivery_method_id, min_quantity_litres, max_quantity_litres, is_active)
Source: PRD §7.1, GLOSSARY.md (Variant), J7 Step 5, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

CAT-006
[V1]
The system shall store all catalog quantity fields (min_quantity_litres, max_quantity_litres in variants) as integer litres using BIGINT.

Actors: System
Preconditions: None
Data involved: `water_variants`
Source: Master Prompt §1 Rule 2 (RULE-002)

---

CAT-007
[V1]
The system shall support soft-delete (deactivation via `is_active = false`) for all catalog records (purposes, quality types, delivery methods, variants). Hard-deletion of records referenced by historical orders is prohibited.

Actors: Super Admin (P5)
Preconditions: Catalog record exists
Data involved: `water_purposes`, `water_quality_types`, `delivery_methods`, `water_variants`
Source: Master Prompt §1 Rule 10 (RULE-010)

---

CAT-008
[V1]
The system shall exclude deactivated catalog records from customer-facing catalog browsing endpoints but retain them for historical order display.

Actors: Customer (P1), System
Preconditions: Catalog record has been deactivated
Data involved: `water_purposes`, `water_quality_types`, `delivery_methods`, `water_variants`
Source: Master Prompt §1 Rule 10 (RULE-010)

---

CAT-009
[V1]
The system shall provide public read API endpoints for browsing the catalog: purposes list, qualities for a purpose, delivery methods, and available variants.

Actors: Customer (P1), Business Customer (P2)
Preconditions: None (public endpoints)
Data involved: `water_purposes`, `water_quality_types`, `delivery_methods`, `water_variants`, `water_purpose_qualities`
Source: PRD §5.1 (Browse dynamic water catalog), J1 Steps 5–9, Master Prompt §7

---

CAT-010
[V1]
The system shall provide admin CRUD endpoints for creating, reading, updating, and deactivating purposes, quality types, delivery methods, purpose-quality links, and variants.

Actors: Super Admin (P5)
Preconditions: Admin is authenticated with `catalog:write` permission
Data involved: `water_purposes`, `water_quality_types`, `delivery_methods`, `water_purpose_qualities`, `water_variants`, `audit_logs`
Source: PRD §5.1 (Admin — Full CRUD for water catalog), J7, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

CAT-011
[V1]
The system shall apply a short-TTL Redis cache (≤ 60 seconds) to catalog read endpoints and invalidate the cache on any catalog write operation, ensuring changes are visible in the customer app within the cache TTL with no redeploy.

Actors: System
Preconditions: Redis is available
Data involved: Catalog API responses, Redis cache
Source: Master Prompt §9 (Catalog — "short-TTL Redis cache, invalidate on write"), J7 Step 8 ("visible within cache TTL"), Master Prompt §10 Step 5

---

CAT-012
[V1]
The system shall validate that a water variant's combination of purpose, quality, and delivery method is valid (quality is linked to purpose via `water_purpose_qualities`) before allowing creation.

Actors: Super Admin (P5)
Preconditions: Purpose-quality link exists
Data involved: `water_variants`, `water_purpose_qualities`
Source: J7 Step 5 ("validates combination"), PRD §7.1

---

## 6. Water Quality (QUAL)

---

QUAL-001
[V1]
The system shall store water quality test records (pH, TDS, turbidity, treatment type, tester, test date, certificate URL, status) associated with water sources.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Water source exists
Data involved: `water_quality_records`, `water_sources`
Source: GLOSSARY.md (Quality Record), Master Prompt §6, PRODUCT_SCOPE.md (SHOULD HAVE — V1)

---

QUAL-002
[V1]
The system shall allow admin users to create, view, and update quality test records for each water source.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `quality:write` permission; source exists
Data involved: `water_quality_records`, `water_sources`, `audit_logs`
Source: PRODUCT_SCOPE.md (Admin — Water quality record management — SHOULD HAVE — V1)

---

QUAL-003
[V1]
The system shall allow customers to view quality information (test results, certificates) for the water they are ordering.

Actors: Customer (P1), Business Customer (P2)
Preconditions: Quality records exist for the relevant source
Data involved: `water_quality_records`, `water_sources`
Source: P1 goals ("Trust the water quality"), PRODUCT_VISION.md ("Quality certificates... build trust")

---

QUAL-004
[V1]
The system shall support approval/rejection status for quality records, allowing only approved records to be visible to customers.

Actors: Super Admin (P5), System
Preconditions: Quality record has been created
Data involved: `water_quality_records` (status field)
Source: GLOSSARY.md (Quality Record — "status"), Master Prompt §6

---

## 7. Water Sources (SRC)

---

SRC-001
[V1]
The system shall store water source records with name, type, GPS location, capacity in litres (integer BIGINT), and operational status.

Actors: Super Admin (P5)
Preconditions: None
Data involved: `water_sources`
Source: GLOSSARY.md (Water Source), Master Prompt §6, PRD §7.4

---

SRC-002
[V1]
The system shall allow admin users to create, read, update, and deactivate water sources.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `sources:write` permission
Data involved: `water_sources`, `audit_logs`
Source: PRODUCT_SCOPE.md (Admin — Water source management — MUST HAVE — V1)

---

SRC-003
[V1]
The system shall track the operational status of each water source (e.g., ACTIVE, INACTIVE, MAINTENANCE) and prevent inventory operations on inactive sources.

Actors: System, Operations Manager (P4)
Preconditions: Source exists
Data involved: `water_sources` (status)
Source: Master Prompt §6 (water_sources — status), GLOSSARY.md (Water Source)

---

SRC-004
[V1]
The system shall track inventory per source — each source has independent available, reserved, and allocated balances derived from its inventory transactions.

Actors: System
Preconditions: Source exists
Data involved: `water_sources`, `inventory_transactions`, `inventory_balances`
Source: PRD §7.4, GLOSSARY.md (Water Source — "Inventory is tracked per source")

---

## 8. Inventory (INV)

---

INV-001
[V1]
The system shall store all inventory quantity fields as integer litres using BIGINT, including transaction quantities and balance fields.

Actors: System
Preconditions: None
Data involved: `inventory_transactions` (quantity_litres), `inventory_balances`
Source: Master Prompt §1 Rule 2 (RULE-002)

---

INV-002
[V1]
The system shall maintain an append-only inventory ledger (`inventory_transactions`) where each transaction records: source_id, transaction type, quantity_litres (signed BIGINT), reference_type, reference_id, created_by, created_at, and notes. No row in this table shall ever be updated or deleted.

Actors: System
Preconditions: Source exists
Data involved: `inventory_transactions`
Source: Master Prompt §1 Rule 4 (RULE-004), PRD §7.4, GLOSSARY.md (Inventory Ledger)

---

INV-003
[V1]
The system shall support the following inventory transaction types: RECEIVED, RESERVED, RELEASED, ALLOCATED, DELIVERED, ADJUSTED, LOST_WASTAGE.

Actors: System, Operations Manager (P4)
Preconditions: Source exists
Data involved: `inventory_transactions` (type)
Source: PRD §7.4, GLOSSARY.md (Inventory Transaction), Master Prompt §6

---

INV-004
[V1]
The system shall maintain `inventory_balances` as a reconciled cache (available_litres, reserved_litres, allocated_litres) derived from summing the inventory ledger — never as the source of truth.

Actors: System
Preconditions: Inventory transactions exist
Data involved: `inventory_balances`, `inventory_transactions`
Source: Master Prompt §1 Rule 4 (RULE-004), PRD §7.4, GLOSSARY.md (Inventory Balance)

---

INV-005
[V1]
The system shall provide a reconciliation function that recomputes `inventory_balances` by summing all transactions in the inventory ledger for a given source, detecting and flagging any discrepancies.

Actors: System, Operations Manager (P4), Super Admin (P5)
Preconditions: Inventory transactions exist for the source
Data involved: `inventory_transactions`, `inventory_balances`
Source: PRD §7.4, GLOSSARY.md (Reconciliation), J9

---

INV-006
[V1]
The system shall use an explicit state-machine function for inventory transaction processing that validates the legality of each transaction (e.g., cannot ALLOCATE more than RESERVED, cannot DELIVER more than ALLOCATED), writes the transaction inside a DB transaction, and writes an audit row.

Actors: System
Preconditions: Transaction request is received
Data involved: `inventory_transactions`, `inventory_balances`
Source: Master Prompt §1 Rule 8 (RULE-008), PRD §6.5

---

INV-007
[V1]
The system shall reject any DELIVER transaction where the delivered quantity exceeds the allocated quantity for that delivery.

Actors: System
Preconditions: Delivery is being completed; allocated quantity is known
Data involved: `inventory_transactions`, `deliveries`
Source: RULE-011 (Delivery Quantity Ceiling)

---

INV-008
[V1]
The system shall enforce the inventory conservation law: for every source, `available + reserved + allocated + delivered + lost_wastage = total_received`, verifiable by summing the ledger.

Actors: System
Preconditions: Inventory transactions exist
Data involved: `inventory_transactions`, `inventory_balances`
Source: PRD §7.4, Master Prompt §13, RULE-013

---

INV-009
[V1]
The system shall generate an alert when a reconciliation check detects a discrepancy between computed balances and the cached balances.

Actors: System
Preconditions: Reconciliation has been run
Data involved: `inventory_balances`, computed values
Source: RULE-013, PRD §8 (Inventory accuracy — 100% reconciliation)

---

INV-010
[V1]
The system shall allow admin users to create manual inventory adjustments with a mandatory reason and notes, recording the adjustment as an ADJUSTED or LOST_WASTAGE transaction in the ledger with full audit trail.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `inventory:adjust` permission; source exists
Data involved: `inventory_transactions`, `inventory_balances`, `audit_logs`
Source: PRD §5.1 (Inventory manual adjustment), J9 Steps 3–4, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

INV-011
[V1]
The system shall automatically release expired inventory reservations via a Celery beat job that detects orders stuck in PENDING_PAYMENT beyond a configurable timeout, creates RELEASED transactions, and marks the orders as FAILED.

Actors: System (Celery beat)
Preconditions: Orders in PENDING_PAYMENT state past timeout
Data involved: `inventory_transactions`, `orders`, `inventory_balances`
Source: RULE-015, PRD §6.5 (Cancellation Creates RELEASE), GLOSSARY.md (Reservation Expiry), J10 Edge Case, Master Prompt §8, PRODUCT_SCOPE.md (Reservation expiry Celery job — MUST HAVE — V1)

---

INV-012
[V1]
The system shall create a RESERVED inventory transaction atomically as part of the order creation transaction. If inventory reservation fails, the entire order creation shall roll back.

Actors: System
Preconditions: Order is being created; sufficient available inventory
Data involved: `inventory_transactions`, `orders`, `inventory_balances`
Source: RULE-023, PRD §6.5, Master Prompt §9 (Orders)

---

INV-013
[V1]
The system shall create a RELEASED inventory transaction when an order is cancelled or a delivery fails, returning the reserved or allocated quantity to available.

Actors: System
Preconditions: Order is cancelled or delivery fails
Data involved: `inventory_transactions`, `inventory_balances`
Source: PRD §6.5 (Cancellation Creates RELEASE), GLOSSARY.md (Release), J3 Step 3a

---

INV-014
[V1]
The system shall create an ALLOCATED inventory transaction when a delivery is assigned to a driver, transitioning inventory from reserved to allocated.

Actors: System
Preconditions: Delivery has been assigned a driver; inventory is reserved
Data involved: `inventory_transactions`, `deliveries`, `inventory_balances`
Source: PRD §6.5 (Dispatch Creates ALLOCATE), GLOSSARY.md (Allocation)

---

INV-015
[V1]
The system shall create a DELIVERED inventory transaction when proof of delivery is confirmed, recording the final delivered quantity as a deduction.

Actors: System
Preconditions: Delivery is being completed with OTP verification
Data involved: `inventory_transactions`, `deliveries`, `inventory_balances`
Source: PRD §6.5 (Delivery Creates DELIVER deduction), J1 Step 19

---

INV-016
[V1]
The system shall provide admin endpoints to view the inventory ledger (transaction history) for a source with filtering by transaction type, date range, and reference.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `inventory:read` permission
Data involved: `inventory_transactions`
Source: PRD §5.1 (Inventory ledger viewer), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

INV-017
[V1]
The system shall reject an order when the requested quantity exceeds the available inventory at any source, returning an error with the `INVENTORY_INSUFFICIENT` code.

Actors: System
Preconditions: Customer is placing an order
Data involved: `inventory_balances`, `orders`
Source: Master Prompt §12 (Edge case — insufficient inventory), Master Prompt §10 Step 8

---

INV-018
[V1]
The system shall use `SELECT ... FOR UPDATE` or equivalent row-level locking on the source balance during inventory reservation to prevent race conditions under concurrent order placement.

Actors: System
Preconditions: Concurrent orders targeting the same source
Data involved: `inventory_balances`, `inventory_transactions`
Source: Master Prompt §10 Step 17 (reservation race conditions)

---

## 9. Pricing (PRC)

---

PRC-001
[V1]
The system shall compute all prices through a single `PricingService.quote()` function that is the only place price is calculated. Both the pre-checkout quote preview and the order creation shall use the same function.

Actors: System
Preconditions: Variant, quantity, and customer context are provided
Data involved: `pricing_rules`, `coupons`, `water_variants`
Source: Master Prompt §1 Rule 5 (RULE-005), PRD §7.5, RULE-014, Master Prompt §9 (Pricing)

---

PRC-002
[V1]
The system shall store the pricing rule version used for each order item in the commercial snapshot, ensuring historical traceability of the price computation.

Actors: System
Preconditions: Order is being created
Data involved: `order_items` (pricing_rule_version_id), `pricing_rules`
Source: Master Prompt §1 Rule 6 (RULE-006), PRD §7.5

---

PRC-003
[V1]
The system shall support three pricing models: FIXED (flat price regardless of quantity), PER_LITRE (unit price × quantity), and TIERED (different price per litre at different quantity thresholds), configurable via `pricing_rules`.

Actors: Super Admin (P5)
Preconditions: None
Data involved: `pricing_rules` (pricing_model, tiers JSONB)
Source: PRD §7.5, GLOSSARY.md (Pricing Model), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

PRC-004
[V1]
The system shall re-compute the price at order creation time and require the customer to re-confirm if the price differs from a previously viewed quote due to intervening pricing or catalog changes.

Actors: Customer (P1), System
Preconditions: Customer has viewed a quote; pricing/catalog has changed since
Data involved: `pricing_rules`, `water_variants`, quote response
Source: RULE-020, Master Prompt §12 (price/config change after cart creation)

---

PRC-005
[V1]
The system shall support purpose-specific and quality-specific pricing rules, allowing different prices for different water purpose and quality combinations.

Actors: Super Admin (P5)
Preconditions: Purposes and quality types exist
Data involved: `pricing_rules` (purpose_id, quality_id)
Source: PRD §7.5 ("purpose/quality-specific pricing"), Master Prompt §6

---

PRC-006
[V1]
The system shall support customer-type-specific pricing rules, allowing different prices for individual versus business customers.

Actors: Super Admin (P5)
Preconditions: None
Data involved: `pricing_rules` (customer_type)
Source: PRD §7.5 ("customer-type pricing"), Master Prompt §6

---

PRC-007
[PHASE 2]
The system shall support area-based pricing rules for multi-city operations, allowing different prices by geographical area/zone.

Actors: Super Admin (P5)
Preconditions: Area/zone definitions exist
Data involved: `pricing_rules` (area_id)
Source: PRD §7.5 ("area-based pricing"), PRD §5.2 (Phase 2 — Multi-city support)

---

PRC-008
[V1]
The system shall provide admin CRUD endpoints for creating, reading, updating, and deactivating pricing rules, with audit logging for all changes.

Actors: Super Admin (P5)
Preconditions: Admin is authenticated with `pricing:write` permission
Data involved: `pricing_rules`, `audit_logs`
Source: PRD §5.1 (Admin — Pricing rule management), J7 Step 6, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

PRC-009
[V1]
The system shall support pricing rule versioning with activation periods (active_from, active_to), ensuring new rules take effect at a defined time without affecting existing orders.

Actors: Super Admin (P5)
Preconditions: Pricing rule exists
Data involved: `pricing_rules` (version, active_from, active_to)
Source: P5 scenario ("sets activation date → existing orders keep old pricing → new orders use new pricing"), GLOSSARY.md (Pricing Rule)

---

PRC-010
[V1]
The system shall compute delivery charges based on configurable delivery pricing rules (distance bands, vehicle type multipliers, or flat rate).

Actors: System
Preconditions: Delivery pricing rules configured
Data involved: `delivery_pricing_rules`, quote computation
Source: GLOSSARY.md (Delivery Charge), PRD §7.5, Master Prompt §6

---

PRC-011
[V1]
The system shall return a non-binding price quote via `POST /orders/quote` showing the complete price breakdown (water total, delivery charge, discount, tax, final total) using the same `PricingService.quote()` function used for order creation.

Actors: Customer (P1), Business Customer (P2)
Preconditions: Valid variant, quantity, delivery details provided
Data involved: `pricing_rules`, `delivery_pricing_rules`, `coupons`
Source: PRD §5.1 (Price quote preview), J1 Step 12, GLOSSARY.md (Quote), Master Prompt §7

---

## 10. Coupons / Promotions (CPN)

---

CPN-001
[V1]
The system shall support promotional coupon codes with configurable attributes: discount type (percentage or fixed amount), discount value, minimum order amount, validity window (valid_from, valid_to), total usage limit, and per-customer usage limit.

Actors: Super Admin (P5)
Preconditions: None
Data involved: `coupons`
Source: PRD §7.5, GLOSSARY.md (Coupon), PRODUCT_SCOPE.md (SHOULD HAVE — V1)

---

CPN-002
[V1]
The system shall validate coupon codes server-side during quote and order creation, checking: code existence, active status, validity window, minimum order amount, total usage count, and per-customer usage count.

Actors: System
Preconditions: Customer provides a coupon code
Data involved: `coupons`, `orders` (usage counts)
Source: PRD §7.5, J1 Step 13, GLOSSARY.md (Coupon — "Validated and applied server-side only")

---

CPN-003
[V1]
The system shall apply validated coupon discounts to the price computation within `PricingService.quote()`, reflecting the discount in both the quote preview and the final order price.

Actors: System
Preconditions: Coupon is valid for the order
Data involved: `coupons`, `pricing_rules`, quote computation
Source: J1 Step 13 ("recalculates quote with discount"), PRD §7.5

---

CPN-004
[V1]
The system shall provide admin CRUD endpoints for creating, reading, updating, and deactivating coupons.

Actors: Super Admin (P5), Operations Manager (P4)
Preconditions: Admin is authenticated with `coupons:write` permission
Data involved: `coupons`, `audit_logs`
Source: PRODUCT_SCOPE.md (Admin — Coupon/promotion management — SHOULD HAVE — V1)

---

CPN-005
[V1]
The system shall reject a coupon code that has exceeded its total usage limit or the per-customer usage limit, returning an appropriate error.

Actors: System
Preconditions: Coupon code submitted with order
Data involved: `coupons`, usage tracking
Source: GLOSSARY.md (Coupon — "usage limits, per-customer limits"), Master Prompt §12 (coupon expiration)

---

CPN-006
[V1]
The system shall reject a coupon code that is outside its validity window (before valid_from or after valid_to).

Actors: System
Preconditions: Coupon code submitted
Data involved: `coupons` (valid_from, valid_to)
Source: Master Prompt §12 (coupon expiration), GLOSSARY.md (Coupon)

---

## 11. Orders (ORD)

---

ORD-001
[V1]
The system shall allow an authenticated customer to create a standard order by selecting a water variant, quantity (within variant min/max), delivery address, and time slot.

Actors: Customer (P1)
Preconditions: Customer is authenticated; variant is active; quantity is within range
Data involved: `orders`, `order_items`, `water_variants`, `addresses`
Source: PRD §5.1 (Place standard orders), J1 Steps 6–14, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

ORD-002
[V1]
The system shall support four order types: STANDARD (one-time), SCHEDULED (specific future time), RECURRING (repeating schedule), and BULK (large quantity).

Actors: System
Preconditions: None
Data involved: `orders` (order_type)
Source: PRD §7.2, GLOSSARY.md (Order Type)

---

ORD-003
[V1]
The system shall store all order quantity fields as integer litres using BIGINT.

Actors: System
Preconditions: None
Data involved: `orders` (total_quantity_litres), `order_items` (quantity_litres)
Source: Master Prompt §1 Rule 2 (RULE-002)

---

ORD-004
[V1]
The system shall model every order as having one or more deliveries (1:N relationship), even when the order results in a single delivery.

Actors: System
Preconditions: Order is created
Data involved: `orders`, `deliveries`
Source: Master Prompt §1 Rule 3 (RULE-003), PRD §7.2, PRD §7.3

---

ORD-005
[V1]
The system shall compute the order price server-side via `PricingService.quote()` during order creation, never accepting a client-provided price.

Actors: System
Preconditions: Order creation request received
Data involved: `pricing_rules`, `order_items`
Source: Master Prompt §1 Rule 5 (RULE-005), RULE-014

---

ORD-006
[V1]
The system shall store a complete commercial snapshot in `order_items` at creation time, including: purpose name, quality name, quantity in litres, unit price, water total, delivery charge, discount total, tax total, final total, and pricing rule version ID.

Actors: System
Preconditions: Order is being created
Data involved: `order_items`
Source: Master Prompt §1 Rule 6 (RULE-006), PRD §7.2, GLOSSARY.md (Commercial Snapshot)

---

ORD-007
[V1]
The system shall ensure that subsequent changes to catalog configuration, pricing rules, or coupon definitions never alter any field of any historical order's commercial snapshot.

Actors: System
Preconditions: Order exists with snapshot
Data involved: `order_items`, `pricing_rules`, `water_variants`
Source: Master Prompt §1 Rule 6 (RULE-006), PRD §7.2

---

ORD-008
[V1]
The system shall implement an explicit order state machine with the following states: PENDING_PAYMENT, CONFIRMED, PROCESSING, ALLOCATED, ASSIGNED, OUT_FOR_DELIVERY, ARRIVED, PARTIALLY_DELIVERED, DELIVERED, CANCELLED, FAILED, REFUNDED, REJECTED.

Actors: System
Preconditions: None
Data involved: `orders` (status), `order_status_history`
Source: Master Prompt §8 (Order state machine), Master Prompt §1 Rule 8 (RULE-008)

---

ORD-009
[V1]
The system shall reject any order status transition that is not in the allowed transition list, using a `transition(order, new_status, actor, reason)` function that validates legality, applies the change in a DB transaction, writes a history row, and triggers side effects.

Actors: System
Preconditions: Order exists with current status
Data involved: `orders`, `order_status_history`
Source: Master Prompt §1 Rule 8 (RULE-008), Master Prompt §8

---

ORD-010
[V1]
The system shall transition a parent order to DELIVERED status only when all of its child deliveries have reached DELIVERED status.

Actors: System
Preconditions: All child deliveries are DELIVERED
Data involved: `orders`, `deliveries`
Source: RULE-012, PRD §7.3, Master Prompt §8

---

ORD-011
[V1]
The system shall mark an order as FAILED when its inventory reservation expires (PENDING_PAYMENT past configurable timeout) and notify the customer.

Actors: System (Celery beat)
Preconditions: Order in PENDING_PAYMENT past timeout
Data involved: `orders`, `inventory_transactions`, `notifications`
Source: RULE-015, J10 Edge Case, GLOSSARY.md (Reservation Expiry)

---

ORD-012
[V1]
The system shall support an `Idempotency-Key` header on `POST /orders` to prevent duplicate order creation on client retry, returning the original response for repeated keys.

Actors: Customer (P1), System
Preconditions: Client sends Idempotency-Key header
Data involved: `orders`, idempotency key store
Source: RULE-016, PRD §7.2, Master Prompt §7

---

ORD-013
[V1]
The system shall allow a customer to cancel an order only before it reaches OUT_FOR_DELIVERY status.

Actors: Customer (P1)
Preconditions: Order is in a cancellable status (pre-OUT_FOR_DELIVERY)
Data involved: `orders`, `order_status_history`
Source: RULE-017, J3, PRD §5.1

---

ORD-014
[V1]
The system shall allow admin/ops users to cancel an order at any status with a mandatory reason, triggering appropriate inventory releases and refund processing.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `orders:cancel` permission
Data involved: `orders`, `order_status_history`, `inventory_transactions`, `refunds`, `audit_logs`
Source: RULE-017, PRD §5.1 (Admin — Order lifecycle management)

---

ORD-015
[V1]
The system shall re-compute the price at order creation time using the current pricing rules and require re-confirmation if the price differs from a previously viewed quote.

Actors: Customer (P1), System
Preconditions: Quote was viewed; pricing may have changed
Data involved: `pricing_rules`, quote, `orders`
Source: RULE-020, Master Prompt §12

---

ORD-016
[V1]
The system shall create orders within a single database transaction encompassing: availability validation, price computation, order record creation, order_items snapshot, inventory reservation, and payment intent creation. Any failure shall roll back the entire transaction.

Actors: System
Preconditions: Order creation request received
Data involved: `orders`, `order_items`, `inventory_transactions`, `payments`
Source: RULE-023, Master Prompt §9 (Orders), Master Prompt §5

---

ORD-017
[V1]
The system shall allow authenticated customers to view their order history with pagination and filtering by status.

Actors: Customer (P1)
Preconditions: Customer is authenticated
Data involved: `orders`, `order_items`
Source: PRD §5.1 (Order history & detail view), J2 Step 2, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

ORD-018
[V1]
The system shall allow authenticated customers to view detailed information for a specific order, including commercial snapshot, status, deliveries, and payment status.

Actors: Customer (P1)
Preconditions: Customer is authenticated; order belongs to the customer
Data involved: `orders`, `order_items`, `deliveries`, `payments`
Source: PRD §5.1 (Order history & detail view), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

ORD-019
[V1]
The system shall support reordering from order history by pre-filling a new order with the purpose, quality, quantity, delivery method, and address from a previous order.

Actors: Customer (P1)
Preconditions: Customer has a completed previous order
Data involved: `orders`, `order_items`, `addresses`
Source: PRD §5.1 (Reorder from history), J2 Steps 3–4, PRODUCT_SCOPE.md (SHOULD HAVE — V1)

---

ORD-020
[V1]
The system shall allow admin/ops users to view all orders with filtering, sorting, and pagination, and view detailed order information.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `orders:read` permission
Data involved: `orders`, `order_items`, `deliveries`, `payments`
Source: PRD §5.1 (Admin — Order list & detail view), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

ORD-021
[V1]
The system shall support configurable delivery time slots/windows that customers select during order placement.

Actors: Customer (P1), System
Preconditions: Delivery windows are configured
Data involved: `orders` (scheduled_window_start, scheduled_window_end)
Source: PRD §5.1 (Time slot / scheduling selection), J1 Step 11, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

ORD-022
[V1]
The system shall allow customers to track order status via polling (GET /orders/{id}).

Actors: Customer (P1)
Preconditions: Customer is authenticated; order exists
Data involved: `orders` (status)
Source: PRD §5.1 (Track order status — polling), J1 Step 17, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

## 12. Deliveries (DEL)

---

DEL-001
[V1]
The system shall create one or more delivery records for each order, always modeling the order-delivery relationship as 1:N.

Actors: System
Preconditions: Order is confirmed
Data involved: `orders`, `deliveries`
Source: Master Prompt §1 Rule 3 (RULE-003), PRD §7.3

---

DEL-002
[V1]
The system shall treat each delivery as independently trackable with its own state machine, assigned driver, assigned vehicle, quantity, OTP code, and proof.

Actors: System
Preconditions: Delivery record exists
Data involved: `deliveries`
Source: PRD §7.3, GLOSSARY.md (Delivery)

---

DEL-003
[V1]
The system shall store all delivery quantity fields as integer litres using BIGINT.

Actors: System
Preconditions: None
Data involved: `deliveries` (quantity_litres, delivered_quantity_litres)
Source: Master Prompt §1 Rule 2 (RULE-002)

---

DEL-004
[V1]
The system shall implement an explicit delivery state machine with states: PENDING_ASSIGNMENT, OFFERED, ASSIGNED, STARTED, ARRIVED, DELIVERED, PARTIALLY_DELIVERED, FAILED, with a REASSIGNING loop on reject/timeout back to OFFERED.

Actors: System
Preconditions: None
Data involved: `deliveries` (status), `delivery_events`
Source: Master Prompt §8 (Delivery state machine), Master Prompt §1 Rule 8 (RULE-008)

---

DEL-005
[V1]
The system shall reject any delivery status transition not in the allowed transition list, using a `transition(delivery, new_status, actor, reason)` function.

Actors: System
Preconditions: Delivery exists with current status
Data involved: `deliveries`, `delivery_events`
Source: Master Prompt §1 Rule 8 (RULE-008), Master Prompt §8

---

DEL-006
[V1]
The system shall reject delivery completion when the reported delivered quantity exceeds the allocated quantity for that delivery.

Actors: System
Preconditions: Driver is completing a delivery
Data involved: `deliveries` (quantity_litres, delivered_quantity_litres)
Source: RULE-011

---

DEL-007
[V1]
The system shall ensure a parent order transitions to DELIVERED only when all its child deliveries have reached DELIVERED status.

Actors: System
Preconditions: A delivery is being marked DELIVERED
Data involved: `orders`, `deliveries`
Source: RULE-012, PRD §7.3

---

DEL-008
[V1]
The system shall support partial delivery: when a driver delivers less than the full allocated quantity, the delivery is marked PARTIALLY_DELIVERED with the actual quantity, and a new delivery is automatically created for the remaining quantity in PENDING_ASSIGNMENT status.

Actors: Driver (P3), System
Preconditions: Delivery is being completed with quantity less than allocated
Data involved: `deliveries`
Source: RULE-018, J4 Steps 2–4, GLOSSARY.md (Partial Delivery)

---

DEL-009
[V1]
The system shall keep the parent order in PROCESSING status when a partial delivery occurs, until all deliveries (including remainder deliveries) are complete.

Actors: System
Preconditions: Partial delivery has occurred
Data involved: `orders`, `deliveries`
Source: RULE-018, J4 Step 4

---

DEL-010
[V1]
The system shall use an offer/accept/reject assignment pattern with a configurable timeout for driver delivery offers.

Actors: Driver (P3), System
Preconditions: Delivery is in PENDING_ASSIGNMENT status; eligible drivers exist
Data involved: `deliveries`, `delivery_assignments`, `drivers`
Source: PRD §7.3, J5 Steps 3–4, J6, GLOSSARY.md (Assignment)

---

DEL-011
[V1]
The system shall automatically re-offer a delivery to the next eligible driver when the current driver rejects the offer or the offer times out, recording the rejection in `delivery_assignments`.

Actors: System
Preconditions: Driver has rejected or timed out
Data involved: `deliveries`, `delivery_assignments`, `drivers`
Source: RULE-022, J6 Steps 2–3, GLOSSARY.md (Reassignment)

---

DEL-012
[V1]
The system shall generate an alert for the ops team when no driver accepts a delivery after a configurable number of offer attempts, making the delivery available for manual assignment.

Actors: System, Operations Manager (P4)
Preconditions: Delivery has been rejected by N drivers
Data involved: `deliveries`, `delivery_assignments`, alerts
Source: RULE-022, J6 Step 5

---

DEL-013
[V1]
The system shall allow ops/admin users to manually assign a delivery to a specific driver, overriding the automatic offer pattern.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `deliveries:assign` permission; delivery is in assignable state
Data involved: `deliveries`, `delivery_assignments`, `drivers`
Source: PRD §5.1 (Admin — Manual delivery assignment), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

DEL-014
[V1]
The system shall allow ops/admin users to reassign a delivery from one driver to another with a reason.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated; delivery is assigned
Data involved: `deliveries`, `delivery_assignments`, `audit_logs`
Source: PRD §5.1 (Admin — Delivery reassignment), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

DEL-015
[V1]
The system shall generate a unique OTP code for each delivery and share it with the customer (via push/SMS) for proof of delivery verification.

Actors: System
Preconditions: Delivery is assigned
Data involved: `deliveries` (otp_code), `notifications`
Source: PRD §7.3, J5 Step 11, GLOSSARY.md (OTP Delivery), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

DEL-016
[V1]
The system shall verify the OTP entered by the driver against the delivery's OTP code before marking the delivery as complete.

Actors: Driver (P3), Customer (P1)
Preconditions: Driver has arrived and is completing delivery
Data involved: `deliveries` (otp_code)
Source: PRD §5.1 (OTP-based proof of delivery), J5 Step 12, J1 Step 19

---

DEL-017
[V1]
The system shall support optional photo upload as additional proof of delivery, stored in object storage (S3).

Actors: Driver (P3)
Preconditions: Delivery is being completed
Data involved: `deliveries` (proof_photo_url)
Source: PRD §5.1 (Driver — Photo proof upload), PRODUCT_SCOPE.md (SHOULD HAVE — V1)

---

DEL-018
[V1]
The system shall record GPS coordinates at the time of delivery completion.

Actors: Driver (P3), System
Preconditions: Delivery is being completed; GPS is available
Data involved: `deliveries` (gps_lat, gps_lng)
Source: GLOSSARY.md (Proof of Delivery — "GPS coordinates at delivery time")

---

DEL-019
[V1]
The system shall record timestamped delivery lifecycle events (offered, accepted, started, arrived, delivered, etc.) in `delivery_events` for timeline display.

Actors: System
Preconditions: Delivery status changes
Data involved: `delivery_events`
Source: GLOSSARY.md (Delivery Event), Master Prompt §6

---

DEL-020
[V1]
The system shall support driver trip status updates: STARTED (en route to source/customer), ARRIVED (at customer location).

Actors: Driver (P3)
Preconditions: Delivery is assigned to driver
Data involved: `deliveries`, `delivery_events`
Source: PRD §5.1 (Driver — Trip status updates), J5 Steps 6, 9, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

DEL-021
[V1]
The system shall allow admin users to view all deliveries with filtering, sorting, and pagination, and view detailed delivery information including assignment history and events.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `deliveries:read` permission
Data involved: `deliveries`, `delivery_events`, `delivery_assignments`
Source: PRD §5.1 (Admin — Delivery list & detail view), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

DEL-022
[PHASE 2]
The system shall support real-time WebSocket-based live delivery tracking with GPS updates from the driver, visible to the customer.

Actors: Customer (P1), Driver (P3)
Preconditions: Delivery is in progress
Data involved: Driver GPS location, WebSocket connection
Source: PRD §5.2 (Phase 2 — Real-time tracking), PRODUCT_SCOPE.md (PHASE 2)

---

## 13. Driver Management (DRV)

---

DRV-001
[V1]
The system shall allow drivers to toggle their availability status between AVAILABLE (online) and UNAVAILABLE (offline).

Actors: Driver (P3)
Preconditions: Driver is authenticated
Data involved: `drivers` (status)
Source: PRD §5.1 (Driver — Set availability status), J5 Step 2, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

DRV-002
[V1]
The system shall present delivery offers only to drivers whose status is AVAILABLE and whose assigned vehicle has sufficient capacity for the delivery.

Actors: System
Preconditions: Delivery needs assignment; eligible drivers exist
Data involved: `drivers`, `vehicles`, `deliveries`
Source: J5 Step 3, GLOSSARY.md (Assignment)

---

DRV-003
[V1]
The system shall allow drivers to view their delivery history with pagination.

Actors: Driver (P3)
Preconditions: Driver is authenticated
Data involved: `deliveries`, `delivery_events`
Source: PRD §5.1 (Driver — Delivery history), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

DRV-004
[V1]
The system shall allow drivers to view their earnings summary and breakdown (daily, weekly, monthly).

Actors: Driver (P3)
Preconditions: Driver is authenticated
Data involved: `deliveries` (completed), earnings calculations
Source: PRD §5.1 (Driver — Earnings summary and history), J5 Step 14, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

DRV-005
[V1]
The system shall allow admin users to create, read, update, and deactivate driver profiles.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `drivers:write` permission
Data involved: `drivers`, `users`, `audit_logs`
Source: PRD §5.1 (Admin — Driver CRUD), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

DRV-006
[V1]
The system shall allow drivers to receive and respond to (accept/reject) delivery offer notifications.

Actors: Driver (P3)
Preconditions: Driver is AVAILABLE; delivery offer sent
Data involved: `deliveries`, `delivery_assignments`
Source: PRD §5.1 (Driver — Accept/reject delivery offers), J5 Steps 3–4, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

DRV-007
[V1]
The system shall provide a deep link to Google Maps navigation from the driver's active delivery view.

Actors: Driver (P3)
Preconditions: Delivery is assigned and started
Data involved: `deliveries`, `addresses` (lat, lng)
Source: PRD §5.1 (Driver — Active delivery view with navigation link), J5 Step 8, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

## 14. Vehicle / Fleet Management (VEH)

---

VEH-001
[V1]
The system shall store vehicle records with registration number, type, capacity in litres (integer BIGINT), operational status, and current assigned driver.

Actors: Super Admin (P5)
Preconditions: None
Data involved: `vehicles`
Source: Master Prompt §6, GLOSSARY.md, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

VEH-002
[V1]
The system shall allow admin users to create, read, update, and deactivate vehicle records.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `vehicles:write` permission
Data involved: `vehicles`, `audit_logs`
Source: PRD §5.1 (Admin — Vehicle CRUD), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

VEH-003
[V1]
The system shall assign a vehicle to a driver and track the current vehicle-driver mapping.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Vehicle and driver exist
Data involved: `vehicles` (current_driver_id), `drivers` (current_vehicle_id)
Source: Master Prompt §6, GLOSSARY.md

---

VEH-004
[V1]
The system shall prevent assignment of deliveries to drivers whose vehicle capacity (in litres) is less than the delivery quantity.

Actors: System
Preconditions: Delivery assignment is being processed
Data involved: `vehicles` (capacity_litres), `deliveries` (quantity_litres)
Source: Master Prompt §12 (insufficient vehicle capacity)

---

VEH-005
[PHASE 3]
The system shall support predictive maintenance tracking, fuel tracking, and compliance automation for the vehicle fleet.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Vehicle records exist
Data involved: `vehicles`, maintenance records
Source: PRD §5.3 (Phase 3 — Advanced fleet management)

---

## 15. Payments (PAY)

---

PAY-001
[V1]
The system shall create payment intents server-side via a generic `PaymentGatewayAdapter` interface (Razorpay implementation in V1) during order creation.

Actors: System
Preconditions: Order is being created
Data involved: `payments`, gateway adapter
Source: PRD §7.6, GLOSSARY.md (Payment Intent, Gateway Adapter), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

PAY-002
[V1]
The system shall process payment status updates exclusively through a server-side webhook handler that verifies the payment gateway's cryptographic signature. The webhook handler is the only code path that writes `payments.status = SUCCESS`.

Actors: System (Webhook)
Preconditions: Payment gateway sends webhook callback
Data involved: `payments`, `payment_transactions`
Source: Master Prompt §1 Rule 9 (RULE-009), PRD §7.6, PRD §6.6

---

PAY-003
[V1]
The system shall implement an idempotent webhook handler — receiving the same webhook event twice shall not create duplicate records or trigger duplicate side effects.

Actors: System
Preconditions: Webhook received
Data involved: `payments`, `payment_transactions`
Source: Master Prompt §1 Rule 9 (RULE-009), PRD §7.6 ("Idempotent webhook handler"), Master Prompt §9

---

PAY-004
[V1]
The system shall never trust client-reported payment success and shall never transition an order from PENDING_PAYMENT to CONFIRMED based on a client callback alone.

Actors: System
Preconditions: Payment flow in progress
Data involved: `payments`, `orders`
Source: Master Prompt §1 Rule 9 (RULE-009), Master Prompt §10 Step 10

---

PAY-005
[V1]
The system shall support an `Idempotency-Key` header on payment verification endpoints to prevent duplicate payment processing on client retry.

Actors: System
Preconditions: Client retries payment
Data involved: `payments`, idempotency key store
Source: RULE-016, Master Prompt §7

---

PAY-006
[V1]
The system shall store raw gateway interaction records in `payment_transactions`, including gateway reference ID, raw response payload (JSONB), and verification timestamp.

Actors: System
Preconditions: Gateway interaction occurs
Data involved: `payment_transactions`
Source: GLOSSARY.md (Payment Transaction), Master Prompt §6

---

PAY-007
[V1]
The system shall transition the order from PENDING_PAYMENT to CONFIRMED upon successful payment verification via webhook.

Actors: System
Preconditions: Payment webhook confirms success
Data involved: `payments`, `orders`, `order_status_history`
Source: PRD §6.6, J1 Step 16, J10 Step 4

---

PAY-008
[V1]
The system shall allow admin users to view payment records with status and details.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `payments:read` permission
Data involved: `payments`, `payment_transactions`
Source: PRD §5.1 (Admin — Payment list & detail), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

PAY-009
[V1]
The system shall support payment retry when the initial payment attempt fails, creating a new payment intent with the same idempotency key to prevent duplicate orders.

Actors: Customer (P1), System
Preconditions: Previous payment attempt failed; order is still in PENDING_PAYMENT
Data involved: `payments`, `orders`
Source: J10 Steps 2–4, PRD §9.1 (payment gateway downtime)

---

PAY-010
[V1]
The system shall queue failed payment intents for retry when the payment gateway is temporarily down, showing helpful error messages to the customer.

Actors: System
Preconditions: Payment gateway is unavailable
Data involved: `payments`, error queue
Source: PRD §9.1 (Payment gateway downtime — "Queue failed payment intents for retry")

---

## 16. Refunds (RFD)

---

RFD-001
[V1]
The system shall initiate a refund automatically when a paid order is cancelled by the customer (pre-OUT_FOR_DELIVERY), processing the refund through the payment gateway adapter.

Actors: System
Preconditions: Order is cancelled; payment was successful
Data involved: `refunds`, `payments`, gateway adapter
Source: RULE-017, J3 Steps 3a–4, PRD §6.6

---

RFD-002
[V1]
The system shall allow admin users to manually initiate a refund for an order with a mandatory reason.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `refunds:write` permission; payment exists
Data involved: `refunds`, `payments`, `audit_logs`
Source: PRD §5.1 (Admin — Refund management), PRODUCT_SCOPE.md (SHOULD HAVE — V1)

---

RFD-003
[V1]
The system shall track refund status (INITIATED, PROCESSING, COMPLETED, FAILED) and update the payment status to REFUNDED upon successful refund confirmation via gateway webhook.

Actors: System
Preconditions: Refund has been initiated
Data involved: `refunds`, `payments`
Source: PRD §6.6, J3 Steps 4–5, GLOSSARY.md (Refund)

---

RFD-004
[V1]
The system shall store refund records with payment reference, refund amount, reason, and status.

Actors: System
Preconditions: Refund initiated
Data involved: `refunds`
Source: Master Prompt §6, GLOSSARY.md (Refund)

---

RFD-005
[V1]
The system shall notify the customer when a refund is initiated and when it is completed.

Actors: System
Preconditions: Refund status changes
Data involved: `refunds`, `notifications`
Source: J3 Step 4 ("Receives 'Refund of ₹450 initiated'"), J3 Step 5

---

RFD-006
[V1]
The system shall allow admin users to view refund records and their status.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `refunds:read` permission
Data involved: `refunds`, `payments`
Source: PRODUCT_SCOPE.md (Admin — Refund management — SHOULD HAVE — V1)

---

## 17. Notifications (NTF)

---

NTF-001
[V1]
The system shall send notifications to customers when their order's inventory reservation expires and the order is marked FAILED.

Actors: System
Preconditions: Reservation has expired
Data involved: `notifications`, `orders`
Source: RULE-015, J10 Edge Case ("Customer notified: 'Your order has expired'")

---

NTF-002
[V1]
The system shall implement a channel-agnostic `NotificationService.send(user, event, context)` with adapter pattern for Push, SMS (MSG91), and Email channels, allowing channels to be added without touching call sites.

Actors: System
Preconditions: None
Data involved: `notifications`
Source: PRD §7.7, GLOSSARY.md (Notification), Master Prompt §9 (Notifications), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

NTF-003
[V1]
The system shall retry failed notification delivery and, for critical events (payment success, delivery arrival, order cancellation), attempt a fallback channel.

Actors: System
Preconditions: Primary notification delivery has failed
Data involved: `notifications`
Source: RULE-021, Master Prompt §12 (notification delivery failure)

---

NTF-004
[V1]
The system shall send push notifications to customers at key order/delivery lifecycle transitions: order confirmed, delivery assigned, driver en route, driver arrived, delivery completed.

Actors: System
Preconditions: Customer has FCM token registered
Data involved: `notifications`, `orders`, `deliveries`
Source: PRD §5.1 (Push notifications), J1 Steps 16–18, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

NTF-005
[V1]
The system shall send push notifications to drivers for new delivery offers.

Actors: System
Preconditions: Driver has FCM token registered; delivery is being offered
Data involved: `notifications`, `deliveries`, `drivers`
Source: PRD §5.1 (Driver — Delivery offer notifications), J5 Step 3, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

NTF-006
[V1]
The system shall send notifications to customers for partial delivery events, including the quantity delivered and the remainder scheduled.

Actors: System
Preconditions: Partial delivery has occurred
Data involved: `notifications`, `deliveries`
Source: J4 Step 5 ("Push + SMS notification")

---

NTF-007
[V1]
The system shall send the delivery OTP to the customer via push notification and/or SMS before the driver arrives.

Actors: System
Preconditions: Delivery is assigned
Data involved: `notifications`, `deliveries` (otp_code)
Source: DEL-015, J5 Step 11, GLOSSARY.md (OTP Delivery)

---

NTF-008
[V1]
The system shall store notification records with user, channel, template, payload (JSONB), delivery status, and sent timestamp.

Actors: System
Preconditions: Notification sent
Data involved: `notifications`
Source: Master Prompt §6, GLOSSARY.md (Notification)

---

NTF-009
[V1]
The system shall send notifications to the ops team when delivery assignment escalation occurs (no driver accepts after N attempts).

Actors: System
Preconditions: Delivery has been rejected by N drivers
Data involved: `notifications`, `deliveries`
Source: RULE-022, J6 Step 5

---

## 18. Reviews / Ratings (REV)

---

REV-001
[V1]
The system shall allow authenticated customers to rate and review a completed delivery (1–5 stars with optional text comment).

Actors: Customer (P1)
Preconditions: Delivery is DELIVERED; customer has not already reviewed this delivery
Data involved: `reviews`
Source: PRD §5.1 (Rate and review completed deliveries), J1 Step 20, PRODUCT_SCOPE.md (SHOULD HAVE — V1)

---

REV-002
[V1]
The system shall store reviews with order reference, customer reference, rating value, and comment text.

Actors: System
Preconditions: Review submitted
Data involved: `reviews`
Source: Master Prompt §6

---

REV-003
[V1]
The system shall allow admin users to view all reviews with filtering and pagination.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated
Data involved: `reviews`
Source: P5 scenario (business review — driver performance), PRODUCT_SCOPE.md (SHOULD HAVE — V1)

---

REV-004
[V1]
The system shall allow drivers to view reviews associated with their deliveries.

Actors: Driver (P3)
Preconditions: Driver is authenticated
Data involved: `reviews`, `deliveries`
Source: USER_PERSONAS.md (P3 — Reviews/Ratings: view)

---

## 19. Admin Operations (ADM)

---

ADM-001
[V1]
The system shall provide a dashboard summary endpoint returning key operational metrics: pending orders count, active deliveries, revenue summary, low-inventory alerts, and driver availability.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated
Data involved: `orders`, `deliveries`, `inventory_balances`, `drivers`, aggregated metrics
Source: PRD §5.1 (Admin — Dashboard summary), P4 scenario (morning review), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

ADM-002
[V1]
The system shall enforce soft-delete semantics for all admin catalog operations — deactivation only, no hard-deletion of records referenced by historical orders.

Actors: System
Preconditions: Admin attempts to delete a catalog record
Data involved: `water_purposes`, `water_quality_types`, `delivery_methods`, `water_variants`
Source: Master Prompt §1 Rule 10 (RULE-010)

---

ADM-003
[V1]
The system shall generate alerts for operations managers when critical operational thresholds are breached (low inventory, high rejection rate, unassigned deliveries).

Actors: System
Preconditions: Operational data exists
Data involved: `inventory_balances`, `deliveries`, `delivery_assignments`, alerts
Source: P4 scenario (morning review — "2 low-inventory alerts"), PRD §5.1 (Dashboard — alerts)

---

ADM-004
[V1]
The system shall allow admin users to perform manual interventions on orders: cancel, reschedule delivery, and create replacement deliveries.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with appropriate permissions
Data involved: `orders`, `deliveries`, `order_status_history`, `audit_logs`
Source: PRD §5.1 (Admin — Order lifecycle management), J8, PRODUCT_SCOPE.md (MUST HAVE — V1)

---

ADM-005
[V1]
The system shall log every admin mutation to catalog, pricing, inventory, user, and role data in `audit_logs` with the acting admin's identity.

Actors: System
Preconditions: Admin performs a write operation
Data involved: `audit_logs`
Source: RULE-019, PRD §5.1 (Audit logging for all admin mutations), Master Prompt §9

---

## 20. Reporting (RPT)

---

RPT-001
[V1]
The system shall provide pre-built sales report views showing revenue by period, by water purpose, by quality, and by customer type.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `reports:read` permission; order data exists
Data involved: `orders`, `order_items`, aggregated data
Source: PRD §5.1 (Admin — Sales reports), PRD §7.8, P5 scenario (monthly sales by purpose), PRODUCT_SCOPE.md (SHOULD HAVE — V1)

---

RPT-002
[V1]
The system shall provide water supply/consumption report views showing source utilization, consumption by purpose, and inventory movements.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated; inventory data exists
Data involved: `inventory_transactions`, `water_sources`, aggregated data
Source: PRD §5.1 (Admin — Water supply/consumption reports), PRD §7.8, PRODUCT_SCOPE.md (SHOULD HAVE — V1)

---

RPT-003
[V1]
The system shall provide delivery performance report views showing driver completion rates, delivery times, failure rates, and vehicle utilization.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated; delivery data exists
Data involved: `deliveries`, `drivers`, `vehicles`, aggregated data
Source: PRD §5.1 (Admin — Delivery performance reports), PRD §7.8, P5 scenario (driver 92% completion rate), PRODUCT_SCOPE.md (SHOULD HAVE — V1)

---

RPT-004
[V1]
The system shall provide customer report views showing retention rates, order patterns, reorder rates, and customer acquisition.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated; customer and order data exists
Data involved: `users`, `customer_profiles`, `orders`, aggregated data
Source: PRD §5.1 (Admin — Customer reports), PRD §7.8, PRD §8 (Customer reorder rate > 40%), PRODUCT_SCOPE.md (SHOULD HAVE — V1)

---

RPT-005
[V1]
The system shall use scheduled aggregation jobs (Celery) to pre-compute report data for dashboard views, avoiding real-time heavy queries.

Actors: System
Preconditions: Celery beat is running
Data involved: Aggregation tables, `orders`, `deliveries`, `inventory_transactions`
Source: PRD §7.8 ("Scheduled aggregation jobs"), PRODUCT_SCOPE.md (Backend — Reporting — SHOULD HAVE — V1)

---

## 21. Analytics (ANL)

---

ANL-001
[PHASE 2]
The system shall provide an advanced analytics dashboard with operational analytics, trend analysis, and cohort analysis.

Actors: Super Admin (P5)
Preconditions: Sufficient historical data exists
Data involved: Aggregated operational data
Source: PRD §5.2 (Phase 2 — Analytics dashboard), PRODUCT_SCOPE.md (PHASE 2)

---

ANL-002
[PHASE 2]
The system shall support demand trend analysis showing order volume patterns by time of day, day of week, and seasonal trends.

Actors: Super Admin (P5)
Preconditions: Sufficient order history exists
Data involved: `orders`, time-series aggregations
Source: PRD §5.2 (Analytics — trend analysis)

---

ANL-003
[PHASE 2]
The system shall support customer cohort analysis showing retention, lifetime value, and ordering behavior by acquisition period.

Actors: Super Admin (P5)
Preconditions: Sufficient customer data exists
Data involved: `users`, `customer_profiles`, `orders`, cohort calculations
Source: PRD §5.2 (Analytics — cohort analysis)

---

ANL-004
[PHASE 3]
The system shall support demand forecasting using machine learning to predict order volumes by area, purpose, and time period.

Actors: System, Super Admin (P5)
Preconditions: Sufficient historical data; ML model trained
Data involved: Historical order data, ML model outputs
Source: PRD §5.3 (Phase 3 — Machine learning — Demand forecasting)

---

ANL-005
[PHASE 3]
The system shall support dynamic pricing recommendations using machine learning, suggesting optimal price points based on demand, supply, and competition.

Actors: Super Admin (P5)
Preconditions: ML model trained; sufficient pricing data
Data involved: `pricing_rules`, order data, ML model outputs
Source: PRD §5.3 (Phase 3 — Machine learning — Dynamic pricing)

---

## 22. Businesses / B2B (BIZ)

---

BIZ-001
[V1]
The system shall store the database schema for businesses, business users, and business sites in V1 (ARCHITECTURE ONLY), even though customer-facing B2B UI is deferred to Phase 2.

Actors: System
Preconditions: None (schema only)
Data involved: `businesses`, `business_users`, `business_sites`
Source: PRODUCT_SCOPE.md (ARCHITECTURE ONLY), Master Prompt §6, Master Prompt §9

---

BIZ-002
[PHASE 2]
The system shall allow business customers to register their company with business name, registration details, and contact information.

Actors: Business Customer (P2)
Preconditions: User is authenticated
Data involved: `businesses`, `business_users`, `users`
Source: PRD §5.2 (Phase 2 — B2B customer-facing UI), P2 scenario ("Registers company"), PRODUCT_SCOPE.md (PHASE 2)

---

BIZ-003
[PHASE 2]
The system shall support distinct roles within a business: business admin (manages all sites, views all orders, invites/removes employees) and business employee (places orders for assigned sites, views own orders only).

Actors: Business Admin (P2), Business Employee
Preconditions: Business is registered
Data involved: `business_users`, business-level permissions
Source: Sub-Phase 0B §0 Correction 2, RULE-024, P2 goals ("have multiple team members able to place orders")

---

BIZ-004
[PHASE 2]
The system shall allow business admins to invite employees by mobile number and assign them to specific sites.

Actors: Business Admin (P2)
Preconditions: Business is registered; sites exist
Data involved: `business_users`, `business_sites`, `users`
Source: P2 scenario ("invites 2 site supervisors as employees"), RULE-024

---

BIZ-005
[PHASE 2]
The system shall allow business admins to manage multiple delivery sites (add, edit, deactivate) with GPS coordinates and site-specific delivery instructions.

Actors: Business Admin (P2)
Preconditions: Business is registered
Data involved: `business_sites`, `addresses`
Source: P2 goals ("Add/remove sites as projects start and finish"), P2 scenario ("adds 3 construction sites")

---

BIZ-006
[PHASE 2]
The system shall allow business admins to view a consolidated dashboard showing all active sites, pending deliveries, consumption totals, and order history across sites.

Actors: Business Admin (P2)
Preconditions: Business is registered; orders/deliveries exist
Data involved: `businesses`, `business_sites`, `orders`, `deliveries`
Source: P2 scenario ("Views dashboard showing all active sites")

---

BIZ-007
[V1]
The system shall provide basic CRUD backend endpoints for businesses, business users, and business sites in V1, usable by admin users even though customer-facing UI is deferred.

Actors: Super Admin (P5)
Preconditions: Admin is authenticated
Data involved: `businesses`, `business_users`, `business_sites`
Source: PRODUCT_SCOPE.md (Backend — Business/B2B endpoints — ARCHITECTURE ONLY), Master Prompt §7

---

## 23. Bulk Orders (BULK)

---

BULK-001
[V1]
The system shall store the database schema for bulk requests and bulk quotes in V1 (ARCHITECTURE ONLY), supporting the full request → quote → accept → fulfilment workflow.

Actors: System
Preconditions: None (schema only)
Data involved: `bulk_requests`, `bulk_quotes`
Source: PRODUCT_SCOPE.md (ARCHITECTURE ONLY), Master Prompt §6

---

BULK-002
[PHASE 2]
The system shall allow business customers to submit a bulk order request specifying purpose, quality, total quantity, site, schedule period (start/end), frequency, and notes.

Actors: Business Customer (P2)
Preconditions: Business is registered; site exists
Data involved: `bulk_requests`
Source: PRD §5.2 (Phase 2 — Bulk order customer flow), P2 scenario ("Requests quote for 50,000L/week"), GLOSSARY.md (Bulk Request)

---

BULK-003
[PHASE 2]
The system shall allow admin users to review bulk requests and create a quote with price details and an expiry date.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Bulk request exists; admin is authenticated
Data involved: `bulk_requests`, `bulk_quotes`
Source: PRD §5.2, P2 scenario ("admin sends quote"), GLOSSARY.md (Bulk Quote)

---

BULK-004
[PHASE 2]
The system shall allow business customers to accept or reject a bulk quote before its expiry date.

Actors: Business Customer (P2)
Preconditions: Quote exists and is not expired
Data involved: `bulk_quotes`
Source: PRD §5.2, Master Prompt §12 (bulk quote expiration), GLOSSARY.md (Bulk Quote)

---

BULK-005
[PHASE 2]
The system shall generate individual orders and deliveries from an accepted bulk request, splitting the total quantity across the scheduled delivery period.

Actors: System
Preconditions: Bulk quote has been accepted
Data involved: `bulk_requests`, `orders`, `deliveries`
Source: P2 scenario ("recurring deliveries auto-generated"), PRD §5.2

---

BULK-006
[V1]
The system shall provide basic CRUD and state-flow backend endpoints for bulk requests and quotes in V1.

Actors: Super Admin (P5)
Preconditions: Admin is authenticated
Data involved: `bulk_requests`, `bulk_quotes`
Source: PRODUCT_SCOPE.md (Backend — Bulk order endpoints — ARCHITECTURE ONLY), Master Prompt §7

---

BULK-007
[PHASE 2]
The system shall handle bulk request rejection by admin with a reason, notifying the customer.

Actors: Operations Manager (P4), System
Preconditions: Bulk request exists
Data involved: `bulk_requests`, `notifications`
Source: Master Prompt §12 (bulk request rejection)

---

## 24. Recurring Orders (REC)

---

REC-001
[V1]
The system shall store the database schema for recurring orders and recurring order instances in V1 (ARCHITECTURE ONLY).

Actors: System
Preconditions: None (schema only)
Data involved: `recurring_orders`, `recurring_order_instances`
Source: PRODUCT_SCOPE.md (ARCHITECTURE ONLY), Master Prompt §6

---

REC-002
[PHASE 2]
The system shall allow business customers to set up recurring water deliveries with a schedule (frequency, day(s) of week, time window), variant, quantity, and site.

Actors: Business Customer (P2)
Preconditions: Business is registered; variant and site exist
Data involved: `recurring_orders`, `water_variants`, `business_sites`
Source: PRD §5.2 (Phase 2 — Recurring order customer flow), P2 goals ("Set up recurring water deliveries"), GLOSSARY.md (Recurring Order)

---

REC-003
[PHASE 2]
The system shall allow individual customers to set up recurring water deliveries for personal use (e.g., weekly drinking water jars).

Actors: Customer (P1)
Preconditions: Customer is authenticated; variant exists
Data involved: `recurring_orders`, `water_variants`, `addresses`
Source: Sub-Phase 0B §0 Correction 1, USER_PERSONAS.md (P1 ✅ Recurring Orders), P1 behavior ("Orders 2–3 times per month")

---

REC-004
[PHASE 2]
The system shall auto-generate individual order instances from a recurring order on schedule, creating each instance on or before its scheduled date.

Actors: System (Celery beat)
Preconditions: Recurring order is active; scheduled date reached
Data involved: `recurring_orders`, `recurring_order_instances`, `orders`
Source: GLOSSARY.md (Recurring Instance), PRD §5.2

---

REC-005
[PHASE 2]
The system shall allow customers to pause, skip individual instances, or cancel a recurring order.

Actors: Customer (P1), Business Customer (P2)
Preconditions: Recurring order exists and is active
Data involved: `recurring_orders`, `recurring_order_instances`
Source: PRD §5.2 (schedule management), Master Prompt §7 (PATCH recurring-orders — pause/skip/cancel)

---

REC-006
[PHASE 2]
The system shall flag for ops review and notify the customer when a recurring instance generation fails (e.g., insufficient inventory), never silently dropping the instance.

Actors: System
Preconditions: Instance generation failed
Data involved: `recurring_order_instances`, `notifications`
Source: Master Prompt §12 (recurring instance generation failure — "flag for ops, notify customer, never silently drop")

---

REC-007
[V1]
The system shall provide basic CRUD backend endpoints for recurring orders in V1.

Actors: Super Admin (P5)
Preconditions: Admin is authenticated
Data involved: `recurring_orders`, `recurring_order_instances`
Source: PRODUCT_SCOPE.md (Backend — Recurring order endpoints — ARCHITECTURE ONLY), Master Prompt §7

---

## 25. Invoices (INVC)

---

INVC-001
[V1]
The system shall store the database schema for invoices in V1 (ARCHITECTURE ONLY), linking invoices to businesses and orders.

Actors: System
Preconditions: None (schema only)
Data involved: `invoices`
Source: PRODUCT_SCOPE.md (ARCHITECTURE ONLY), Master Prompt §6

---

INVC-002
[PHASE 2]
The system shall support period-based invoice generation for B2B customers, covering a billing period (start/end dates) with line items from all deliveries in that period.

Actors: System, Super Admin (P5)
Preconditions: Business has completed deliveries in the billing period
Data involved: `invoices`, `businesses`, `orders`, `deliveries`
Source: PRD §5.2 (Phase 2 — Invoicing), P2 goals ("monthly invoicing with 15–30 day payment terms"), GLOSSARY.md (Invoice)

---

INVC-003
[PHASE 2]
The system shall allow business customers to view and download invoices for their account.

Actors: Business Customer (P2)
Preconditions: Invoices exist for the business
Data involved: `invoices`, `businesses`
Source: P2 scenario ("Downloads monthly invoice"), PRD §5.2

---

INVC-004
[PHASE 2]
The system shall track invoice payment status (PENDING, PAID, OVERDUE) and due dates with configurable payment terms.

Actors: System, Super Admin (P5)
Preconditions: Invoice exists
Data involved: `invoices` (status, due_date)
Source: P2 goals ("15–30 day payment terms"), GLOSSARY.md (Invoice — "due date, payment status")

---

INVC-005
[PHASE 2]
The system shall generate statement summaries for business customers showing all invoices, payments, and outstanding balances.

Actors: Business Customer (P2), Super Admin (P5)
Preconditions: Business has invoice history
Data involved: `invoices`, `payments`
Source: PRD §5.2 (Invoicing — statement generation)

---

## 26. Routes (RTE)

---

RTE-001
[V1]
The system shall store the database schema stub for routes in V1, supporting future route optimization capabilities.

Actors: System
Preconditions: None (schema only)
Data involved: Route schema (stub)
Source: PRODUCT_SCOPE.md (Backend — Route endpoints — ARCHITECTURE ONLY), Master Prompt §4

---

RTE-002
[PHASE 2]
The system shall support algorithmic multi-stop route planning for drivers with multiple deliveries, optimizing for distance and time.

Actors: System, Operations Manager (P4)
Preconditions: Multiple deliveries assigned to a driver
Data involved: Route data, `deliveries`, `addresses`
Source: PRD §5.2 (Phase 2 — Route optimization), PRODUCT_SCOPE.md (PHASE 2)

---

RTE-003
[PHASE 2]
The system shall provide a route management UI in the admin dashboard for viewing and editing planned routes.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Routes exist
Data involved: Route data, `deliveries`
Source: PRODUCT_SCOPE.md (Admin — Route management — PHASE 2)

---

RTE-004
[PHASE 2]
The system shall provide distance-based dispatch suggestions, recommending driver assignments based on proximity to the delivery location.

Actors: System, Operations Manager (P4)
Preconditions: Driver locations and delivery addresses are known
Data involved: `drivers`, `addresses`, distance calculations
Source: PRD §5.2 (Route optimization — distance-based dispatch suggestions)

---

## 27. Audit / Compliance (AUD)

---

AUD-001
[V1]
The system shall maintain an immutable audit log recording every admin action with: actor ID, action type, entity type, entity ID, before state (JSONB), after state (JSONB), metadata (JSONB), and timestamp.

Actors: System
Preconditions: Admin performs a write operation
Data involved: `audit_logs`
Source: RULE-019, PRD §5.1 (Audit logging), GLOSSARY.md (Audit Log), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

AUD-002
[V1]
The system shall never update or delete rows in the `audit_logs` table — audit records are immutable and append-only.

Actors: System
Preconditions: None
Data involved: `audit_logs`
Source: RULE-019, GLOSSARY.md (Audit Log — "immutable record"), PRODUCT_VISION.md ("Audit everything — immutable record")

---

AUD-003
[V1]
The system shall log all admin mutations to catalog (purposes, quality types, delivery methods, variants), pricing rules, and inventory adjustments.

Actors: System
Preconditions: Admin performs a catalog/pricing/inventory write
Data involved: `audit_logs`, affected entity tables
Source: RULE-019, Master Prompt §9 (Admin — "Every admin write to catalog, pricing, or inventory must call the audit logger"), Master Prompt §13

---

AUD-004
[V1]
The system shall provide an admin-facing audit log viewer with filtering by action type, entity type, actor, and date range, with search capability.

Actors: Operations Manager (P4), Super Admin (P5)
Preconditions: Admin is authenticated with `audit:read` permission
Data involved: `audit_logs`
Source: PRD §5.1 (Admin — Audit log viewer), P5 scenario (audit investigation), PRODUCT_SCOPE.md (MUST HAVE — V1)

---

AUD-005
[V1]
The system shall record order status transition history in `order_status_history` with from_status, to_status, actor, reason, and timestamp.

Actors: System
Preconditions: Order status changes
Data involved: `order_status_history`
Source: Master Prompt §6, Master Prompt §8 (state machine writes history row)

---

AUD-006
[V1]
The system shall support audit trail queries that reconstruct the complete history of any entity (order, delivery, catalog item, pricing rule) for dispute resolution and compliance.

Actors: Super Admin (P5)
Preconditions: Audit data exists
Data involved: `audit_logs`, `order_status_history`, `delivery_events`
Source: P5 scenario ("searches by order ID → sees complete price computation"), PRODUCT_VISION.md ("Audit everything")

---

AUD-007
[V1]
The system shall comply with DLT (Distributed Ledger Technology) requirements for commercial SMS delivery in India, ensuring all SMS templates are registered with telecom operators.

Actors: System
Preconditions: SMS templates registered
Data involved: SMS templates, MSG91 configuration
Source: PRD §9.2 (Indian market — DLT-compliant SMS), GLOSSARY.md (DLT)

---
