# AquaSwift — Entity-Relationship Diagrams

**Version:** 1.0
**Status:** Draft
**Last Updated:** 2026-09-03

---

> All diagrams use Mermaid ER syntax. Diagrams are grouped by domain for readability. See `DATABASE_ARCHITECTURE.md` for full column definitions.

---

## 1. Identity & Access Domain

```mermaid
erDiagram
    users {
        UUID id PK
        VARCHAR phone UK
        VARCHAR email UK
        VARCHAR password_hash
        VARCHAR full_name
        BOOLEAN is_active
        TIMESTAMPTZ created_at
    }
    roles {
        UUID id PK
        VARCHAR name UK
        JSONB permissions
    }
    user_roles {
        UUID id PK
        UUID user_id FK
        UUID role_id FK
    }
    customer_profiles {
        UUID id PK
        UUID user_id FK
        VARCHAR customer_type
        UUID business_id FK
        JSONB preferences
    }
    driver_profiles {
        UUID id PK
        UUID user_id FK
        VARCHAR license_number
        VARCHAR status
        UUID current_vehicle_id FK
        DECIMAL gps_lat
        DECIMAL gps_lng
    }

    users ||--o{ user_roles : "has roles"
    roles ||--o{ user_roles : "assigned to"
    users ||--o| customer_profiles : "has profile"
    users ||--o| driver_profiles : "has profile"
    driver_profiles }o--o| vehicles : "assigned vehicle"
```

---

## 2. Catalog Domain

```mermaid
erDiagram
    water_purposes {
        UUID id PK
        VARCHAR name UK
        TEXT description
        VARCHAR icon_url
        INTEGER display_order
        BOOLEAN is_active
    }
    water_quality_types {
        UUID id PK
        VARCHAR name UK
        TEXT description
        BOOLEAN is_active
    }
    delivery_methods {
        UUID id PK
        VARCHAR name UK
        BOOLEAN is_active
    }
    water_purpose_qualities {
        UUID id PK
        UUID purpose_id FK
        UUID quality_id FK
    }
    water_variants {
        UUID id PK
        UUID purpose_id FK
        UUID quality_id FK
        UUID delivery_method_id FK
        BIGINT min_quantity_litres
        BIGINT max_quantity_litres
        BOOLEAN is_active
    }

    water_purposes ||--o{ water_purpose_qualities : "has qualities"
    water_quality_types ||--o{ water_purpose_qualities : "available for"
    water_purposes ||--o{ water_variants : "has variants"
    water_quality_types ||--o{ water_variants : "used in"
    delivery_methods ||--o{ water_variants : "used in"
```

---

## 3. Inventory Domain

```mermaid
erDiagram
    water_sources {
        UUID id PK
        VARCHAR name
        VARCHAR type
        DECIMAL gps_lat
        DECIMAL gps_lng
        BIGINT capacity_litres
        VARCHAR status
    }
    water_quality_records {
        UUID id PK
        UUID source_id FK
        DECIMAL ph_level
        INTEGER tds
        DECIMAL turbidity
        VARCHAR treatment_type
        DATE test_date
        VARCHAR certificate_url
        VARCHAR status
    }
    inventory_transactions {
        UUID id PK
        UUID source_id FK
        VARCHAR type
        BIGINT quantity_litres
        VARCHAR reference_type
        UUID reference_id
        TEXT notes
        UUID created_by FK
        TIMESTAMPTZ created_at
    }
    inventory_balances {
        UUID id PK
        UUID source_id FK
        BIGINT available_litres
        BIGINT reserved_litres
        BIGINT allocated_litres
        TIMESTAMPTZ last_reconciled_at
    }

    water_sources ||--o{ water_quality_records : "tested"
    water_sources ||--o{ inventory_transactions : "ledger"
    water_sources ||--|| inventory_balances : "balance cache"
    users ||--o{ inventory_transactions : "created by"
```

---

## 4. Commerce Domain

```mermaid
erDiagram
    orders {
        UUID id PK
        VARCHAR order_number UK
        UUID customer_id FK
        UUID address_id FK
        VARCHAR order_type
        VARCHAR status
        BIGINT total_quantity_litres
        TIMESTAMPTZ scheduled_window_start
        TIMESTAMPTZ scheduled_window_end
        UUID coupon_id FK
        VARCHAR idempotency_key UK
    }
    order_items {
        UUID id PK
        UUID order_id FK
        UUID variant_id FK
        VARCHAR purpose_name
        VARCHAR quality_name
        BIGINT quantity_litres
        DECIMAL unit_price
        DECIMAL water_total
        DECIMAL delivery_charge
        DECIMAL discount_total
        DECIMAL tax_total
        DECIMAL final_total
        UUID pricing_rule_version_id
        JSONB pricing_snapshot
    }
    order_status_history {
        UUID id PK
        UUID order_id FK
        VARCHAR from_status
        VARCHAR to_status
        UUID actor_id FK
        TEXT reason
        TIMESTAMPTZ created_at
    }
    pricing_rules {
        UUID id PK
        INTEGER version
        UUID purpose_id FK
        UUID quality_id FK
        VARCHAR customer_type
        VARCHAR pricing_model
        DECIMAL base_price
        JSONB tiers
        TIMESTAMPTZ active_from
        TIMESTAMPTZ active_to
        BOOLEAN is_active
    }
    coupons {
        UUID id PK
        VARCHAR code UK
        VARCHAR discount_type
        DECIMAL discount_value
        DECIMAL min_order_amount
        INTEGER total_usage_limit
        INTEGER per_customer_limit
        TIMESTAMPTZ valid_from
        TIMESTAMPTZ valid_to
        BOOLEAN is_active
    }

    users ||--o{ orders : "places"
    addresses ||--o{ orders : "delivers to"
    orders ||--o{ order_items : "contains"
    orders ||--o{ order_status_history : "history"
    water_variants ||--o{ order_items : "ordered variant"
    coupons ||--o{ orders : "applied to"
    users ||--o{ order_status_history : "acted by"
```

---

## 5. Fulfilment Domain

```mermaid
erDiagram
    deliveries {
        UUID id PK
        UUID order_id FK
        UUID source_id FK
        UUID driver_id FK
        UUID vehicle_id FK
        VARCHAR status
        BIGINT quantity_litres
        BIGINT delivered_quantity_litres
        VARCHAR otp_code
        VARCHAR proof_photo_url
        DECIMAL gps_lat
        DECIMAL gps_lng
        UUID parent_delivery_id FK
    }
    delivery_assignments {
        UUID id PK
        UUID delivery_id FK
        UUID driver_id FK
        VARCHAR status
        TIMESTAMPTZ offered_at
        TIMESTAMPTZ responded_at
        TEXT rejection_reason
        INTEGER attempt_number
    }
    delivery_events {
        UUID id PK
        UUID delivery_id FK
        VARCHAR event_type
        UUID actor_id FK
        JSONB metadata
        TIMESTAMPTZ created_at
    }
    vehicles {
        UUID id PK
        VARCHAR registration_number UK
        VARCHAR type
        BIGINT capacity_litres
        VARCHAR status
        UUID current_driver_id FK
    }

    orders ||--o{ deliveries : "fulfilled by (1:N)"
    water_sources ||--o{ deliveries : "sourced from"
    driver_profiles ||--o{ deliveries : "assigned to"
    vehicles ||--o{ deliveries : "carried by"
    deliveries ||--o{ delivery_assignments : "assignment history"
    deliveries ||--o{ delivery_events : "lifecycle events"
    driver_profiles ||--o{ delivery_assignments : "offered to"
    deliveries ||--o{ deliveries : "parent/remainder"
```

---

## 6. Payment Domain

```mermaid
erDiagram
    payments {
        UUID id PK
        UUID order_id FK
        DECIMAL amount
        VARCHAR currency
        VARCHAR status
        VARCHAR gateway
        VARCHAR gateway_order_id
        VARCHAR gateway_payment_id
        VARCHAR idempotency_key UK
    }
    payment_transactions {
        UUID id PK
        UUID payment_id FK
        VARCHAR gateway_reference_id
        VARCHAR event_type
        JSONB raw_payload
        TIMESTAMPTZ verified_at
    }
    refunds {
        UUID id PK
        UUID payment_id FK
        DECIMAL amount
        TEXT reason
        VARCHAR status
        VARCHAR gateway_refund_id
        UUID initiated_by FK
    }

    orders ||--o{ payments : "paid via"
    payments ||--o{ payment_transactions : "gateway events"
    payments ||--o{ refunds : "refunded"
    users ||--o{ refunds : "initiated by"
```

---

## 7. B2B Extensions Domain

```mermaid
erDiagram
    businesses {
        UUID id PK
        VARCHAR name
        VARCHAR registration_number
        VARCHAR contact_email
        VARCHAR contact_phone
        BOOLEAN is_active
    }
    business_users {
        UUID id PK
        UUID business_id FK
        UUID user_id FK
        VARCHAR role
        BOOLEAN is_active
    }
    business_sites {
        UUID id PK
        UUID business_id FK
        UUID address_id FK
        VARCHAR name
        VARCHAR contact_person
        VARCHAR contact_phone
        BOOLEAN is_active
    }
    bulk_requests {
        UUID id PK
        UUID business_id FK
        UUID site_id FK
        UUID purpose_id FK
        UUID quality_id FK
        BIGINT total_quantity_litres
        VARCHAR frequency
        VARCHAR status
    }
    bulk_quotes {
        UUID id PK
        UUID bulk_request_id FK
        DECIMAL price_per_litre
        DECIMAL total_price
        TIMESTAMPTZ valid_until
        VARCHAR status
    }
    recurring_orders {
        UUID id PK
        UUID customer_id FK
        UUID variant_id FK
        UUID address_id FK
        BIGINT quantity_litres
        VARCHAR frequency
        JSONB schedule_days
        VARCHAR status
    }
    recurring_order_instances {
        UUID id PK
        UUID recurring_order_id FK
        UUID order_id FK
        DATE scheduled_date
        VARCHAR status
    }
    invoices {
        UUID id PK
        VARCHAR invoice_number UK
        UUID business_id FK
        DATE billing_period_start
        DATE billing_period_end
        DECIMAL total
        VARCHAR status
        DATE due_date
    }

    businesses ||--o{ business_users : "has members"
    users ||--o{ business_users : "belongs to"
    businesses ||--o{ business_sites : "has sites"
    addresses ||--o{ business_sites : "located at"
    businesses ||--o{ bulk_requests : "requests"
    bulk_requests ||--o{ bulk_quotes : "quoted"
    users ||--o{ recurring_orders : "subscribes"
    recurring_orders ||--o{ recurring_order_instances : "generates"
    orders ||--o{ recurring_order_instances : "generated order"
    businesses ||--o{ invoices : "billed"
    customer_profiles }o--o| businesses : "linked to"
```

---

## 8. Platform Domain

```mermaid
erDiagram
    notifications {
        UUID id PK
        UUID user_id FK
        VARCHAR channel
        VARCHAR event_type
        VARCHAR template
        JSONB payload
        VARCHAR status
        TIMESTAMPTZ sent_at
    }
    reviews {
        UUID id PK
        UUID order_id FK
        UUID delivery_id FK
        UUID customer_id FK
        INTEGER rating
        TEXT comment
    }
    audit_logs {
        UUID id PK
        UUID actor_id FK
        VARCHAR action
        VARCHAR entity_type
        UUID entity_id
        JSONB before_state
        JSONB after_state
        JSONB metadata
        TIMESTAMPTZ created_at
    }

    users ||--o{ notifications : "receives"
    orders ||--o{ reviews : "reviewed"
    deliveries ||--o{ reviews : "reviewed"
    users ||--o{ reviews : "by customer"
    users ||--o{ audit_logs : "acted by"
```

---

## 9. Full System Overview (Simplified)

```mermaid
erDiagram
    users ||--o{ orders : "places"
    users ||--o| customer_profiles : "profile"
    users ||--o| driver_profiles : "profile"
    users ||--o{ user_roles : "roles"
    users ||--o{ addresses : "addresses"

    orders ||--|{ order_items : "snapshot"
    orders ||--o{ deliveries : "1:N deliveries"
    orders ||--o{ payments : "payment"
    orders ||--o{ order_status_history : "history"

    deliveries ||--o{ delivery_events : "events"
    deliveries ||--o{ delivery_assignments : "offers"
    driver_profiles ||--o{ deliveries : "delivers"
    vehicles ||--o{ deliveries : "carries"

    water_sources ||--o{ inventory_transactions : "ledger"
    water_sources ||--|| inventory_balances : "cache"

    water_purposes ||--o{ water_variants : "variants"
    water_quality_types ||--o{ water_variants : "variants"
    delivery_methods ||--o{ water_variants : "variants"

    payments ||--o{ refunds : "refunds"
    businesses ||--o{ business_sites : "sites"
    businesses ||--o{ invoices : "invoices"
```
