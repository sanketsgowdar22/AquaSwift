# AquaSwift — Database Architecture

**Version:** 1.0
**Status:** Draft
**Last Updated:** 2026-09-03

---

## 1. Design Principles

| Principle | Implementation |
|-----------|---------------|
| **UUID Primary Keys** | All tables use `UUID` PKs via `gen_random_uuid()` (DEC-DB-002) |
| **Integer Litres** | All quantity fields are `BIGINT` litres (RULE-002) |
| **Decimal Money** | All monetary fields are `DECIMAL(12,2)` in INR |
| **UTC Timestamps** | All timestamp columns are `TIMESTAMPTZ` (NFR-DATA-005) |
| **Soft Deletes** | Catalog entities use `is_active BOOLEAN` (RULE-010) |
| **Append-Only Ledger** | `inventory_transactions` and `audit_logs` — no UPDATE/DELETE (RULE-004, RULE-019) |
| **JSONB for Flexibility** | Pricing tiers, commercial snapshot details, audit before/after state |
| **Foreign Key Integrity** | All relationships enforced via FK constraints (NFR-DATA-006) |
| **Index Strategy** | Composite indexes on high-frequency query patterns |
| **Migration Tool** | Alembic — one migration per schema change, never auto-generate in production |

---

## 2. Table Definitions

### 2.1 Identity & Access Domain

---

#### `users`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK, DEFAULT gen_random_uuid() | |
| `phone` | `VARCHAR(15)` | UNIQUE, nullable | OTP auth (customers, drivers) |
| `email` | `VARCHAR(255)` | UNIQUE, nullable | Email auth (admins) |
| `password_hash` | `VARCHAR(255)` | nullable | bcrypt/Argon2; only for email-auth users |
| `full_name` | `VARCHAR(255)` | NOT NULL | |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | Deactivated = cannot login |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_users_phone` (UNIQUE), `idx_users_email` (UNIQUE)
**Constraints:** `CHECK(phone IS NOT NULL OR email IS NOT NULL)` — at least one auth method

---

#### `roles`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `name` | `VARCHAR(50)` | UNIQUE, NOT NULL | CUSTOMER, DRIVER, OPS_MANAGER, SUPER_ADMIN |
| `permissions` | `JSONB` | NOT NULL | Array of permission strings |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

#### `user_roles`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `user_id` | `UUID` | FK → users(id), NOT NULL | |
| `role_id` | `UUID` | FK → roles(id), NOT NULL | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_user_roles_user_id`, UNIQUE(`user_id`, `role_id`)

---

#### `customer_profiles`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `user_id` | `UUID` | FK → users(id), UNIQUE, NOT NULL | |
| `customer_type` | `VARCHAR(20)` | NOT NULL, DEFAULT 'INDIVIDUAL' | INDIVIDUAL, BUSINESS |
| `business_id` | `UUID` | FK → businesses(id), nullable | Set if customer_type = BUSINESS |
| `preferences` | `JSONB` | nullable | Notification preferences, etc. |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

#### `driver_profiles`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `user_id` | `UUID` | FK → users(id), UNIQUE, NOT NULL | |
| `license_number` | `VARCHAR(50)` | nullable | |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'UNAVAILABLE' | AVAILABLE, UNAVAILABLE, ON_DELIVERY |
| `current_vehicle_id` | `UUID` | FK → vehicles(id), nullable | |
| `gps_lat` | `DECIMAL(10,7)` | nullable | Last known location |
| `gps_lng` | `DECIMAL(10,7)` | nullable | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_driver_profiles_status`, `idx_driver_profiles_user_id`

---

### 2.2 Business / B2B Domain

---

#### `businesses`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `name` | `VARCHAR(255)` | NOT NULL | |
| `registration_number` | `VARCHAR(100)` | nullable | |
| `contact_email` | `VARCHAR(255)` | nullable | |
| `contact_phone` | `VARCHAR(15)` | nullable | |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

#### `business_users`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `business_id` | `UUID` | FK → businesses(id), NOT NULL | |
| `user_id` | `UUID` | FK → users(id), NOT NULL | |
| `role` | `VARCHAR(20)` | NOT NULL | ADMIN, EMPLOYEE |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** UNIQUE(`business_id`, `user_id`)

---

#### `business_sites`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `business_id` | `UUID` | FK → businesses(id), NOT NULL | |
| `address_id` | `UUID` | FK → addresses(id), NOT NULL | |
| `name` | `VARCHAR(255)` | NOT NULL | e.g., "Site A — Gachibowli" |
| `contact_person` | `VARCHAR(255)` | nullable | |
| `contact_phone` | `VARCHAR(15)` | nullable | |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_business_sites_business_id`

---

### 2.3 Location Domain

---

#### `addresses`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `user_id` | `UUID` | FK → users(id), NOT NULL | |
| `label` | `VARCHAR(50)` | nullable | "Home", "Office", etc. |
| `address_line_1` | `VARCHAR(255)` | NOT NULL | |
| `address_line_2` | `VARCHAR(255)` | nullable | |
| `city` | `VARCHAR(100)` | NOT NULL | |
| `state` | `VARCHAR(100)` | NOT NULL | |
| `pincode` | `VARCHAR(10)` | NOT NULL | |
| `lat` | `DECIMAL(10,7)` | nullable | Geocoded latitude |
| `lng` | `DECIMAL(10,7)` | nullable | Geocoded longitude |
| `formatted_address` | `TEXT` | nullable | Google Maps formatted |
| `notes` | `TEXT` | nullable | Delivery instructions |
| `is_default` | `BOOLEAN` | NOT NULL, DEFAULT false | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_addresses_user_id`

---

### 2.4 Catalog Domain

---

#### `water_purposes`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `name` | `VARCHAR(100)` | UNIQUE, NOT NULL | e.g., "Drinking", "Construction" |
| `description` | `TEXT` | nullable | |
| `icon_url` | `VARCHAR(500)` | nullable | |
| `display_order` | `INTEGER` | NOT NULL, DEFAULT 0 | Sorting in UI |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | Soft-delete (RULE-010) |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

#### `water_quality_types`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `name` | `VARCHAR(100)` | UNIQUE, NOT NULL | e.g., "RO+UV Purified", "Raw Municipal" |
| `description` | `TEXT` | nullable | |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

#### `delivery_methods`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `name` | `VARCHAR(100)` | UNIQUE, NOT NULL | e.g., "Tanker Truck", "20L Jar" |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

#### `water_purpose_qualities`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `purpose_id` | `UUID` | FK → water_purposes(id), NOT NULL | |
| `quality_id` | `UUID` | FK → water_quality_types(id), NOT NULL | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Constraints:** UNIQUE(`purpose_id`, `quality_id`)

---

#### `water_variants`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `purpose_id` | `UUID` | FK → water_purposes(id), NOT NULL | |
| `quality_id` | `UUID` | FK → water_quality_types(id), NOT NULL | |
| `delivery_method_id` | `UUID` | FK → delivery_methods(id), NOT NULL | |
| `min_quantity_litres` | `BIGINT` | NOT NULL | Integer litres (RULE-002) |
| `max_quantity_litres` | `BIGINT` | NOT NULL | |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Constraints:** UNIQUE(`purpose_id`, `quality_id`, `delivery_method_id`), CHECK(`min_quantity_litres > 0`), CHECK(`max_quantity_litres >= min_quantity_litres`)
**Indexes:** `idx_variants_purpose_quality`

---

### 2.5 Resource & Inventory Domain

---

#### `water_sources`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `name` | `VARCHAR(255)` | NOT NULL | |
| `type` | `VARCHAR(50)` | NOT NULL | e.g., "Borewell", "Municipal", "Treatment Plant" |
| `gps_lat` | `DECIMAL(10,7)` | nullable | |
| `gps_lng` | `DECIMAL(10,7)` | nullable | |
| `capacity_litres` | `BIGINT` | NOT NULL | Total capacity of this source |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'ACTIVE' | ACTIVE, INACTIVE, MAINTENANCE |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

#### `water_quality_records`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `source_id` | `UUID` | FK → water_sources(id), NOT NULL | |
| `ph_level` | `DECIMAL(4,2)` | nullable | |
| `tds` | `INTEGER` | nullable | Total dissolved solids (ppm) |
| `turbidity` | `DECIMAL(6,2)` | nullable | NTU |
| `treatment_type` | `VARCHAR(100)` | nullable | |
| `tested_by` | `VARCHAR(255)` | nullable | |
| `test_date` | `DATE` | NOT NULL | |
| `certificate_url` | `VARCHAR(500)` | nullable | S3 URL |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'PENDING' | PENDING, APPROVED, REJECTED |
| `notes` | `TEXT` | nullable | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_quality_records_source_id`

---

#### `inventory_transactions`

**APPEND-ONLY — no UPDATE or DELETE permitted (RULE-004)**

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `source_id` | `UUID` | FK → water_sources(id), NOT NULL | |
| `type` | `VARCHAR(20)` | NOT NULL | RECEIVED, RESERVED, RELEASED, ALLOCATED, DELIVERED, ADJUSTED, LOST_WASTAGE |
| `quantity_litres` | `BIGINT` | NOT NULL | Signed: positive = increase, negative = decrease |
| `reference_type` | `VARCHAR(30)` | nullable | "order", "delivery", "adjustment" |
| `reference_id` | `UUID` | nullable | FK to the source entity |
| `notes` | `TEXT` | nullable | Mandatory for ADJUSTED and LOST_WASTAGE |
| `created_by` | `UUID` | FK → users(id), NOT NULL | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_inv_txn_source_id`, `idx_inv_txn_source_type` (source_id, type), `idx_inv_txn_reference` (reference_type, reference_id), `idx_inv_txn_created_at`
**Constraints:** No UPDATE/DELETE triggers or application-level enforcement

---

#### `inventory_balances`

**Reconciled cache — not the source of truth (RULE-004)**

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `source_id` | `UUID` | FK → water_sources(id), UNIQUE, NOT NULL | One row per source |
| `available_litres` | `BIGINT` | NOT NULL, DEFAULT 0 | |
| `reserved_litres` | `BIGINT` | NOT NULL, DEFAULT 0 | |
| `allocated_litres` | `BIGINT` | NOT NULL, DEFAULT 0 | |
| `last_reconciled_at` | `TIMESTAMPTZ` | nullable | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_inv_balances_source_id` (UNIQUE)

---

### 2.6 Commerce Domain

---

#### `pricing_rules`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `version` | `INTEGER` | NOT NULL, DEFAULT 1 | Incremented on update |
| `purpose_id` | `UUID` | FK → water_purposes(id), nullable | null = applies to all |
| `quality_id` | `UUID` | FK → water_quality_types(id), nullable | |
| `customer_type` | `VARCHAR(20)` | nullable | INDIVIDUAL, BUSINESS |
| `area_id` | `UUID` | nullable | For Phase 2 multi-city |
| `pricing_model` | `VARCHAR(20)` | NOT NULL | FIXED, PER_LITRE, TIERED |
| `base_price` | `DECIMAL(12,2)` | NOT NULL | |
| `tiers` | `JSONB` | nullable | For TIERED: [{min_litres, max_litres, price_per_litre}] |
| `active_from` | `TIMESTAMPTZ` | NOT NULL | |
| `active_to` | `TIMESTAMPTZ` | nullable | null = no expiry |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_pricing_rules_lookup` (purpose_id, quality_id, customer_type, is_active, active_from)

---

#### `delivery_pricing_rules`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `delivery_method_id` | `UUID` | FK → delivery_methods(id), nullable | |
| `pricing_model` | `VARCHAR(20)` | NOT NULL | FLAT, PER_KM, DISTANCE_BAND |
| `base_price` | `DECIMAL(12,2)` | NOT NULL | |
| `bands` | `JSONB` | nullable | For DISTANCE_BAND: [{min_km, max_km, price}] |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

#### `coupons`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `code` | `VARCHAR(50)` | UNIQUE, NOT NULL | e.g., "FIRST50" |
| `discount_type` | `VARCHAR(20)` | NOT NULL | PERCENTAGE, FIXED_AMOUNT |
| `discount_value` | `DECIMAL(12,2)` | NOT NULL | % or amount in INR |
| `min_order_amount` | `DECIMAL(12,2)` | nullable | |
| `max_discount_amount` | `DECIMAL(12,2)` | nullable | Cap for PERCENTAGE |
| `valid_from` | `TIMESTAMPTZ` | NOT NULL | |
| `valid_to` | `TIMESTAMPTZ` | NOT NULL | |
| `total_usage_limit` | `INTEGER` | nullable | null = unlimited |
| `per_customer_limit` | `INTEGER` | NOT NULL, DEFAULT 1 | |
| `current_usage_count` | `INTEGER` | NOT NULL, DEFAULT 0 | |
| `is_active` | `BOOLEAN` | NOT NULL, DEFAULT true | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_coupons_code` (UNIQUE)

---

#### `orders`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `order_number` | `VARCHAR(20)` | UNIQUE, NOT NULL | Human-readable (e.g., AQ-20260903-001) |
| `customer_id` | `UUID` | FK → users(id), NOT NULL | |
| `address_id` | `UUID` | FK → addresses(id), NOT NULL | |
| `order_type` | `VARCHAR(20)` | NOT NULL | STANDARD, SCHEDULED, RECURRING, BULK |
| `status` | `VARCHAR(30)` | NOT NULL, DEFAULT 'PENDING_PAYMENT' | See state machine |
| `total_quantity_litres` | `BIGINT` | NOT NULL | Integer litres (RULE-002) |
| `scheduled_window_start` | `TIMESTAMPTZ` | nullable | For scheduled orders |
| `scheduled_window_end` | `TIMESTAMPTZ` | nullable | |
| `coupon_id` | `UUID` | FK → coupons(id), nullable | |
| `idempotency_key` | `VARCHAR(64)` | UNIQUE, nullable | Client-provided (RULE-016) |
| `notes` | `TEXT` | nullable | Customer notes |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_orders_customer_id`, `idx_orders_status`, `idx_orders_created_at`, `idx_orders_idempotency_key` (UNIQUE)

---

#### `order_items`

**Commercial snapshot — immutable after creation (RULE-006)**

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `order_id` | `UUID` | FK → orders(id), NOT NULL | |
| `variant_id` | `UUID` | FK → water_variants(id), NOT NULL | |
| `purpose_name` | `VARCHAR(100)` | NOT NULL | Frozen snapshot |
| `quality_name` | `VARCHAR(100)` | NOT NULL | Frozen snapshot |
| `delivery_method_name` | `VARCHAR(100)` | NOT NULL | Frozen snapshot |
| `quantity_litres` | `BIGINT` | NOT NULL | |
| `unit_price` | `DECIMAL(12,2)` | NOT NULL | Per litre or per unit |
| `water_total` | `DECIMAL(12,2)` | NOT NULL | |
| `delivery_charge` | `DECIMAL(12,2)` | NOT NULL, DEFAULT 0 | |
| `discount_total` | `DECIMAL(12,2)` | NOT NULL, DEFAULT 0 | |
| `tax_total` | `DECIMAL(12,2)` | NOT NULL, DEFAULT 0 | |
| `final_total` | `DECIMAL(12,2)` | NOT NULL | |
| `pricing_rule_version_id` | `UUID` | nullable | FK-like reference (PRC-002) |
| `pricing_snapshot` | `JSONB` | nullable | Full pricing computation details |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_order_items_order_id`

---

#### `order_status_history`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `order_id` | `UUID` | FK → orders(id), NOT NULL | |
| `from_status` | `VARCHAR(30)` | NOT NULL | |
| `to_status` | `VARCHAR(30)` | NOT NULL | |
| `actor_id` | `UUID` | FK → users(id), nullable | null for system actions |
| `reason` | `TEXT` | nullable | Mandatory for cancellation |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_order_history_order_id`

---

### 2.7 Fulfilment Domain

---

#### `deliveries`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `order_id` | `UUID` | FK → orders(id), NOT NULL | 1:N (RULE-003) |
| `source_id` | `UUID` | FK → water_sources(id), nullable | Assigned source |
| `driver_id` | `UUID` | FK → driver_profiles(id), nullable | |
| `vehicle_id` | `UUID` | FK → vehicles(id), nullable | |
| `status` | `VARCHAR(25)` | NOT NULL, DEFAULT 'PENDING_ASSIGNMENT' | See state machine |
| `quantity_litres` | `BIGINT` | NOT NULL | Allocated quantity |
| `delivered_quantity_litres` | `BIGINT` | nullable | Actual delivered |
| `otp_code` | `VARCHAR(6)` | nullable | Proof of delivery OTP |
| `proof_photo_url` | `VARCHAR(500)` | nullable | S3 URL |
| `gps_lat` | `DECIMAL(10,7)` | nullable | At delivery completion |
| `gps_lng` | `DECIMAL(10,7)` | nullable | |
| `parent_delivery_id` | `UUID` | FK → deliveries(id), nullable | For remainder deliveries |
| `scheduled_at` | `TIMESTAMPTZ` | nullable | |
| `completed_at` | `TIMESTAMPTZ` | nullable | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_deliveries_order_id`, `idx_deliveries_driver_id`, `idx_deliveries_status`, `idx_deliveries_scheduled_at`

---

#### `delivery_assignments`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `delivery_id` | `UUID` | FK → deliveries(id), NOT NULL | |
| `driver_id` | `UUID` | FK → driver_profiles(id), NOT NULL | |
| `status` | `VARCHAR(20)` | NOT NULL | OFFERED, ACCEPTED, REJECTED, TIMED_OUT |
| `offered_at` | `TIMESTAMPTZ` | NOT NULL | |
| `responded_at` | `TIMESTAMPTZ` | nullable | |
| `rejection_reason` | `TEXT` | nullable | |
| `attempt_number` | `INTEGER` | NOT NULL | |

**Indexes:** `idx_del_assignments_delivery_id`, `idx_del_assignments_driver_id`

---

#### `delivery_events`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `delivery_id` | `UUID` | FK → deliveries(id), NOT NULL | |
| `event_type` | `VARCHAR(30)` | NOT NULL | CREATED, OFFERED, ACCEPTED, REJECTED, STARTED, ARRIVED, DELIVERED, etc. |
| `actor_id` | `UUID` | FK → users(id), nullable | |
| `metadata` | `JSONB` | nullable | Event-specific data |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_del_events_delivery_id`

---

#### `vehicles`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `registration_number` | `VARCHAR(20)` | UNIQUE, NOT NULL | |
| `type` | `VARCHAR(50)` | NOT NULL | e.g., "Water Tanker", "Mini Truck" |
| `capacity_litres` | `BIGINT` | NOT NULL | Integer litres (RULE-002) |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'ACTIVE' | ACTIVE, INACTIVE, MAINTENANCE |
| `current_driver_id` | `UUID` | FK → driver_profiles(id), nullable | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

### 2.8 Payment Domain

---

#### `payments`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `order_id` | `UUID` | FK → orders(id), NOT NULL | |
| `amount` | `DECIMAL(12,2)` | NOT NULL | |
| `currency` | `VARCHAR(3)` | NOT NULL, DEFAULT 'INR' | |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'INITIATED' | INITIATED, PENDING, SUCCESS, FAILED, REFUNDED |
| `gateway` | `VARCHAR(30)` | NOT NULL | "razorpay" |
| `gateway_order_id` | `VARCHAR(100)` | nullable | Razorpay order ID |
| `gateway_payment_id` | `VARCHAR(100)` | nullable | Razorpay payment ID |
| `idempotency_key` | `VARCHAR(64)` | UNIQUE, nullable | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_payments_order_id`, `idx_payments_gateway_order_id`, `idx_payments_idempotency_key` (UNIQUE)

---

#### `payment_transactions`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `payment_id` | `UUID` | FK → payments(id), NOT NULL | |
| `gateway_reference_id` | `VARCHAR(100)` | nullable | |
| `event_type` | `VARCHAR(50)` | NOT NULL | e.g., "payment.captured", "refund.processed" |
| `raw_payload` | `JSONB` | NOT NULL | Full gateway response |
| `verified_at` | `TIMESTAMPTZ` | nullable | Signature verification timestamp |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_pay_txns_payment_id`

---

#### `refunds`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `payment_id` | `UUID` | FK → payments(id), NOT NULL | |
| `amount` | `DECIMAL(12,2)` | NOT NULL | |
| `reason` | `TEXT` | NOT NULL | |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'INITIATED' | INITIATED, PROCESSING, COMPLETED, FAILED |
| `gateway_refund_id` | `VARCHAR(100)` | nullable | |
| `initiated_by` | `UUID` | FK → users(id), nullable | null = auto (system) |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_refunds_payment_id`

---

### 2.9 B2B Extensions Domain

---

#### `bulk_requests`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `business_id` | `UUID` | FK → businesses(id), NOT NULL | |
| `site_id` | `UUID` | FK → business_sites(id), nullable | |
| `purpose_id` | `UUID` | FK → water_purposes(id), NOT NULL | |
| `quality_id` | `UUID` | FK → water_quality_types(id), NOT NULL | |
| `total_quantity_litres` | `BIGINT` | NOT NULL | |
| `frequency` | `VARCHAR(20)` | nullable | DAILY, WEEKLY, BIWEEKLY, MONTHLY |
| `schedule_start` | `DATE` | NOT NULL | |
| `schedule_end` | `DATE` | nullable | |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'PENDING' | PENDING, QUOTED, ACCEPTED, REJECTED, ACTIVE, COMPLETED |
| `notes` | `TEXT` | nullable | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

#### `bulk_quotes`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `bulk_request_id` | `UUID` | FK → bulk_requests(id), NOT NULL | |
| `price_per_litre` | `DECIMAL(12,4)` | NOT NULL | |
| `total_price` | `DECIMAL(12,2)` | NOT NULL | |
| `delivery_charge` | `DECIMAL(12,2)` | NOT NULL, DEFAULT 0 | |
| `valid_until` | `TIMESTAMPTZ` | NOT NULL | Quote expiry |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'PENDING' | PENDING, ACCEPTED, REJECTED, EXPIRED |
| `created_by` | `UUID` | FK → users(id), NOT NULL | Admin who created |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

#### `recurring_orders`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `customer_id` | `UUID` | FK → users(id), NOT NULL | |
| `variant_id` | `UUID` | FK → water_variants(id), NOT NULL | |
| `address_id` | `UUID` | FK → addresses(id), NOT NULL | |
| `quantity_litres` | `BIGINT` | NOT NULL | |
| `frequency` | `VARCHAR(20)` | NOT NULL | DAILY, WEEKLY, BIWEEKLY, MONTHLY |
| `schedule_days` | `JSONB` | nullable | e.g., [1, 3, 5] for Mon/Wed/Fri |
| `preferred_window_start` | `TIME` | nullable | |
| `preferred_window_end` | `TIME` | nullable | |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'ACTIVE' | ACTIVE, PAUSED, CANCELLED |
| `next_instance_date` | `DATE` | nullable | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

#### `recurring_order_instances`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `recurring_order_id` | `UUID` | FK → recurring_orders(id), NOT NULL | |
| `order_id` | `UUID` | FK → orders(id), nullable | Generated order |
| `scheduled_date` | `DATE` | NOT NULL | |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'PENDING' | PENDING, GENERATED, SKIPPED, FAILED |
| `failure_reason` | `TEXT` | nullable | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

#### `invoices`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `invoice_number` | `VARCHAR(30)` | UNIQUE, NOT NULL | |
| `business_id` | `UUID` | FK → businesses(id), NOT NULL | |
| `billing_period_start` | `DATE` | NOT NULL | |
| `billing_period_end` | `DATE` | NOT NULL | |
| `subtotal` | `DECIMAL(12,2)` | NOT NULL | |
| `tax_total` | `DECIMAL(12,2)` | NOT NULL, DEFAULT 0 | |
| `total` | `DECIMAL(12,2)` | NOT NULL | |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'PENDING' | PENDING, PAID, OVERDUE |
| `due_date` | `DATE` | NOT NULL | |
| `payment_terms_days` | `INTEGER` | NOT NULL, DEFAULT 30 | |
| `pdf_url` | `VARCHAR(500)` | nullable | Generated PDF in S3 |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

---

### 2.10 Platform Domain

---

#### `notifications`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `user_id` | `UUID` | FK → users(id), NOT NULL | |
| `channel` | `VARCHAR(10)` | NOT NULL | PUSH, SMS, EMAIL |
| `event_type` | `VARCHAR(50)` | NOT NULL | e.g., "order_confirmed", "delivery_arrived" |
| `template` | `VARCHAR(100)` | nullable | Template identifier |
| `payload` | `JSONB` | NOT NULL | Channel-specific content |
| `status` | `VARCHAR(20)` | NOT NULL, DEFAULT 'PENDING' | PENDING, SENT, DELIVERED, FAILED |
| `sent_at` | `TIMESTAMPTZ` | nullable | |
| `failure_reason` | `TEXT` | nullable | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_notifications_user_id`, `idx_notifications_status`

---

#### `reviews`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `order_id` | `UUID` | FK → orders(id), NOT NULL | |
| `delivery_id` | `UUID` | FK → deliveries(id), nullable | |
| `customer_id` | `UUID` | FK → users(id), NOT NULL | |
| `rating` | `INTEGER` | NOT NULL | 1–5, CHECK(rating >= 1 AND rating <= 5) |
| `comment` | `TEXT` | nullable | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_reviews_order_id`, `idx_reviews_customer_id`
**Constraints:** UNIQUE(`order_id`, `customer_id`) — one review per order per customer

---

#### `audit_logs`

**APPEND-ONLY — no UPDATE or DELETE permitted (RULE-019)**

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK | |
| `actor_id` | `UUID` | FK → users(id), NOT NULL | Admin who performed action |
| `action` | `VARCHAR(50)` | NOT NULL | e.g., "CREATE", "UPDATE", "DEACTIVATE" |
| `entity_type` | `VARCHAR(50)` | NOT NULL | e.g., "water_purpose", "pricing_rule" |
| `entity_id` | `UUID` | NOT NULL | |
| `before_state` | `JSONB` | nullable | null for CREATE |
| `after_state` | `JSONB` | nullable | null for DELETE |
| `metadata` | `JSONB` | nullable | Additional context |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT now() | |

**Indexes:** `idx_audit_logs_entity` (entity_type, entity_id), `idx_audit_logs_actor_id`, `idx_audit_logs_created_at`

---

## 3. Indexing Strategy

### 3.1 High-Priority Indexes

| Table | Index | Columns | Purpose |
|-------|-------|---------|---------|
| `orders` | `idx_orders_customer_status` | (customer_id, status) | Customer order list with status filter |
| `orders` | `idx_orders_status_created` | (status, created_at) | Ops dashboard: orders by status |
| `deliveries` | `idx_deliveries_driver_status` | (driver_id, status) | Driver's active/pending deliveries |
| `deliveries` | `idx_deliveries_status_scheduled` | (status, scheduled_at) | Dispatch queue |
| `inventory_transactions` | `idx_inv_txn_source_type_created` | (source_id, type, created_at) | Ledger queries per source by type |
| `audit_logs` | `idx_audit_entity_created` | (entity_type, entity_id, created_at) | Entity history reconstruction |

### 3.2 Partitioning Considerations (Future)

| Table | Strategy | Trigger |
|-------|----------|---------|
| `inventory_transactions` | Range partition by `created_at` (monthly) | When table exceeds 10M rows |
| `audit_logs` | Range partition by `created_at` (monthly) | When table exceeds 10M rows |
| `order_status_history` | Range partition by `created_at` (quarterly) | When table exceeds 5M rows |
| `delivery_events` | Range partition by `created_at` (quarterly) | When table exceeds 5M rows |

---

## 4. Migration Strategy (Alembic)

1. **One migration per logical change** — never batch unrelated changes.
2. **Forward-only** — every migration has a `downgrade()`, but production never downgrades.
3. **Non-destructive** — column additions use `nullable=True` or `server_default`; never drop columns in production without a deprecation period.
4. **Seed data** — initial roles, permissions, and system configuration loaded via `scripts/seed_data.py`, not migrations.
5. **Review process** — every migration reviewed for index impact and lock duration before production deployment.

---

## 5. Connection Pooling

| Environment | Pool Size | Max Overflow | Pool Timeout |
|-------------|-----------|-------------|--------------|
| Local Dev | 5 | 10 | 30s |
| Staging | 10 | 20 | 30s |
| Production | 20 | 40 | 30s |

Configuration via `DATABASE_POOL_SIZE`, `DATABASE_MAX_OVERFLOW` environment variables.

---

## 6. Read Replica Strategy

| Query Type | Target |
|-----------|--------|
| All write operations | Primary |
| Transactional reads (orders, inventory) | Primary |
| Reporting queries | Read Replica |
| Dashboard aggregations | Read Replica |
| Audit log queries | Read Replica |
| Customer order history | Primary (for consistency) |

Implementation: SQLAlchemy `Session` binds configured with `bind_key` for read replica routing.

---

## Table Summary

| Domain | Tables | Count |
|--------|--------|-------|
| Identity & Access | users, roles, user_roles, customer_profiles, driver_profiles | 5 |
| Business / B2B | businesses, business_users, business_sites | 3 |
| Location | addresses | 1 |
| Catalog | water_purposes, water_quality_types, delivery_methods, water_purpose_qualities, water_variants | 5 |
| Resource & Inventory | water_sources, water_quality_records, inventory_transactions, inventory_balances | 4 |
| Commerce | pricing_rules, delivery_pricing_rules, coupons, orders, order_items, order_status_history | 6 |
| Fulfilment | deliveries, delivery_assignments, delivery_events, vehicles | 4 |
| Payment | payments, payment_transactions, refunds | 3 |
| B2B Extensions | bulk_requests, bulk_quotes, recurring_orders, recurring_order_instances, invoices | 5 |
| Platform | notifications, reviews, audit_logs | 3 |
| **TOTAL** | | **39** |
