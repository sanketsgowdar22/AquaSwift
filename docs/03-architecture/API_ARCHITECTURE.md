# AquaSwift — API Architecture

**Version:** 1.0
**Status:** Draft
**Last Updated:** 2026-09-03

---

## 1. API Conventions

### 1.1 Base URL

```
Production: https://api.aquaswift.in/api/v1
Local Dev:  http://localhost:8000/api/v1
```

### 1.2 Authentication

All protected endpoints require a JWT access token in the `Authorization` header:

```
Authorization: Bearer <jwt_access_token>
```

Public endpoints (catalog browsing, OTP request/verify) do not require authentication.

### 1.3 Error Envelope

All error responses use a standardized JSON envelope. Clients must branch on `code`, never on `message`:

```json
{
  "code": "INVENTORY_INSUFFICIENT",
  "message": "Requested quantity exceeds available inventory.",
  "details": {
    "requested_litres": 5000,
    "max_available_litres": 3200
  }
}
```

| HTTP Status | Usage |
|-------------|-------|
| `400` | Business rule violation, invalid request data |
| `401` | Missing or invalid JWT |
| `403` | Insufficient RBAC permissions |
| `404` | Resource not found |
| `409` | Conflict (idempotency duplicate, illegal state transition) |
| `422` | Pydantic schema validation failure |
| `429` | Rate limit exceeded |
| `500` | Unexpected server error |

### 1.4 Pagination

List endpoints use **cursor-based pagination** for real-time data and **offset-based** for reports:

**Cursor-based (default for list endpoints):**
```
GET /orders?limit=20&cursor=<opaque_cursor>&sort=-created_at
```

Response includes:
```json
{
  "items": [...],
  "next_cursor": "eyJ...",
  "has_more": true
}
```

**Offset-based (for reports/admin):**
```
GET /admin/orders?page=1&page_size=50&sort=-created_at
```

Response includes:
```json
{
  "items": [...],
  "total": 1234,
  "page": 1,
  "page_size": 50,
  "total_pages": 25
}
```

### 1.5 Filtering

Standard query parameters for filtering:
```
GET /orders?status=CONFIRMED&customer_id=uuid&created_after=2026-01-01&created_before=2026-12-31
```

### 1.6 Idempotency

Mutation endpoints that must be idempotent accept an `Idempotency-Key` header:

```
POST /orders
Idempotency-Key: <client-generated-uuid>
```

If the same key is sent again, the server returns the original response with HTTP 200 (not 201).

### 1.7 Request/Response Content Type

All requests and responses use `Content-Type: application/json` unless explicitly noted (e.g., multipart file upload for delivery proof photos).

---

## 2. Endpoint Catalog

### 2.1 Authentication (AUTH)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `POST` | `/auth/otp/request` | Public | — | Request OTP for mobile number |
| `POST` | `/auth/otp/verify` | Public | — | Verify OTP, receive JWT + refresh token |
| `POST` | `/auth/login` | Public | — | Admin login with email + password |
| `POST` | `/auth/refresh` | Public | — | Refresh JWT using refresh token |
| `POST` | `/auth/logout` | Bearer | — | Invalidate refresh tokens |

**Request/Response Examples:**

```
POST /auth/otp/request
Request:  { "phone": "+919876543210" }
Response: { "message": "OTP sent", "expires_in_seconds": 300 }

POST /auth/otp/verify
Request:  { "phone": "+919876543210", "otp": "123456" }
Response: { "access_token": "...", "refresh_token": "...", "token_type": "bearer",
            "expires_in": 3600, "user": { "id": "uuid", "full_name": "...", "role": "CUSTOMER" } }
```

---

### 2.2 Users & Profiles (USR)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/users/me` | Bearer | — | Get current user profile |
| `PATCH` | `/users/me` | Bearer | — | Update current user profile |
| `GET` | `/admin/customers` | Bearer | `customers:read` | List all customers (paginated, filterable) |
| `GET` | `/admin/customers/{id}` | Bearer | `customers:read` | Get customer detail (profile + orders + addresses) |
| `PATCH` | `/admin/customers/{id}` | Bearer | `customers:write` | Update customer (e.g., deactivate) |

---

### 2.3 Addresses (ADDR)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/addresses` | Bearer | — | List current user's addresses |
| `POST` | `/addresses` | Bearer | — | Add a new address (auto-geocode) |
| `PATCH` | `/addresses/{id}` | Bearer | — | Update an address |
| `DELETE` | `/addresses/{id}` | Bearer | — | Delete an address |
| `GET` | `/admin/addresses` | Bearer | `addresses:read` | List addresses (admin, filterable by user) |

---

### 2.4 Catalog (CAT)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/catalog/purposes` | Public | — | List active water purposes |
| `GET` | `/catalog/purposes/{id}/qualities` | Public | — | List quality types for a purpose |
| `GET` | `/catalog/delivery-methods` | Public | — | List active delivery methods |
| `GET` | `/catalog/variants` | Public | — | List active variants (filter by purpose, quality, method) |
| `GET` | `/catalog/variants/{id}` | Public | — | Get variant detail |
| `POST` | `/admin/catalog/purposes` | Bearer | `catalog:write` | Create water purpose |
| `PATCH` | `/admin/catalog/purposes/{id}` | Bearer | `catalog:write` | Update/deactivate purpose |
| `POST` | `/admin/catalog/quality-types` | Bearer | `catalog:write` | Create quality type |
| `PATCH` | `/admin/catalog/quality-types/{id}` | Bearer | `catalog:write` | Update/deactivate quality type |
| `POST` | `/admin/catalog/delivery-methods` | Bearer | `catalog:write` | Create delivery method |
| `PATCH` | `/admin/catalog/delivery-methods/{id}` | Bearer | `catalog:write` | Update/deactivate method |
| `POST` | `/admin/catalog/purpose-qualities` | Bearer | `catalog:write` | Link quality to purpose |
| `DELETE` | `/admin/catalog/purpose-qualities/{id}` | Bearer | `catalog:write` | Unlink quality from purpose |
| `POST` | `/admin/catalog/variants` | Bearer | `catalog:write` | Create water variant |
| `PATCH` | `/admin/catalog/variants/{id}` | Bearer | `catalog:write` | Update/deactivate variant |

---

### 2.5 Water Quality (QUAL)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/quality/records` | Public | — | List approved quality records (filterable by source) |
| `GET` | `/quality/records/{id}` | Public | — | Get quality record detail |
| `POST` | `/admin/quality/records` | Bearer | `quality:write` | Create quality record |
| `PATCH` | `/admin/quality/records/{id}` | Bearer | `quality:write` | Update/approve/reject |

---

### 2.6 Water Sources (SRC)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/admin/sources` | Bearer | `sources:read` | List water sources |
| `GET` | `/admin/sources/{id}` | Bearer | `sources:read` | Get source detail + inventory balance |
| `POST` | `/admin/sources` | Bearer | `sources:write` | Create water source |
| `PATCH` | `/admin/sources/{id}` | Bearer | `sources:write` | Update/deactivate source |

---

### 2.7 Inventory (INV)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/admin/inventory/balances` | Bearer | `inventory:read` | List all source balances |
| `GET` | `/admin/inventory/balances/{source_id}` | Bearer | `inventory:read` | Get balance for a source |
| `GET` | `/admin/inventory/transactions` | Bearer | `inventory:read` | List inventory ledger (filterable by source, type, date) |
| `POST` | `/admin/inventory/receive` | Bearer | `inventory:adjust` | Record RECEIVED transaction |
| `POST` | `/admin/inventory/adjust` | Bearer | `inventory:adjust` | Manual ADJUSTED transaction (mandatory reason) |
| `POST` | `/admin/inventory/loss` | Bearer | `inventory:adjust` | Record LOST_WASTAGE transaction (mandatory reason) |
| `POST` | `/admin/inventory/reconcile/{source_id}` | Bearer | `inventory:adjust` | Run reconciliation check |

---

### 2.8 Pricing (PRC)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/admin/pricing/rules` | Bearer | `pricing:read` | List pricing rules |
| `GET` | `/admin/pricing/rules/{id}` | Bearer | `pricing:read` | Get pricing rule detail |
| `POST` | `/admin/pricing/rules` | Bearer | `pricing:write` | Create pricing rule |
| `PATCH` | `/admin/pricing/rules/{id}` | Bearer | `pricing:write` | Update/deactivate pricing rule |
| `GET` | `/admin/pricing/delivery-rules` | Bearer | `pricing:read` | List delivery pricing rules |
| `POST` | `/admin/pricing/delivery-rules` | Bearer | `pricing:write` | Create delivery pricing rule |
| `PATCH` | `/admin/pricing/delivery-rules/{id}` | Bearer | `pricing:write` | Update delivery pricing rule |

---

### 2.9 Coupons (CPN)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `POST` | `/coupons/validate` | Bearer | — | Validate a coupon code for the current user |
| `GET` | `/admin/coupons` | Bearer | `coupons:read` | List all coupons |
| `GET` | `/admin/coupons/{id}` | Bearer | `coupons:read` | Get coupon detail |
| `POST` | `/admin/coupons` | Bearer | `coupons:write` | Create coupon |
| `PATCH` | `/admin/coupons/{id}` | Bearer | `coupons:write` | Update/deactivate coupon |

---

### 2.10 Orders (ORD)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `POST` | `/orders/quote` | Bearer | — | Get non-binding price quote |
| `POST` | `/orders` | Bearer | — | Create order (Idempotency-Key supported) |
| `GET` | `/orders` | Bearer | — | List current user's orders (paginated, filterable by status) |
| `GET` | `/orders/{id}` | Bearer | — | Get order detail (items, deliveries, payments) |
| `POST` | `/orders/{id}/cancel` | Bearer | — | Cancel order (customer — pre-OUT_FOR_DELIVERY) |
| `POST` | `/orders/{id}/reorder` | Bearer | — | Pre-fill new order from previous order |
| `GET` | `/admin/orders` | Bearer | `orders:read` | List all orders (admin, filterable) |
| `GET` | `/admin/orders/{id}` | Bearer | `orders:read` | Get order detail (admin view) |
| `POST` | `/admin/orders/{id}/cancel` | Bearer | `orders:cancel` | Admin cancel (mandatory reason) |

**Order Creation Flow:**
```
POST /orders
Idempotency-Key: <uuid>
{
  "variant_id": "uuid",
  "quantity_litres": 5000,
  "address_id": "uuid",
  "scheduled_window_start": "2026-09-04T08:00:00Z",
  "scheduled_window_end": "2026-09-04T10:00:00Z",
  "coupon_code": "FIRST50",
  "notes": "Terrace tank, back gate access"
}

Response (201):
{
  "order": {
    "id": "uuid",
    "order_number": "AQ-20260904-001",
    "status": "PENDING_PAYMENT",
    "items": [{ "purpose_name": "Drinking", "quality_name": "RO+UV", ... }],
    "total": 2250.00,
    ...
  },
  "payment": {
    "gateway_order_id": "order_xyz",
    "amount": 2250.00,
    "currency": "INR",
    "key": "rzp_live_xxx"
  }
}
```

---

### 2.11 Deliveries (DEL)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/deliveries/active` | Bearer (Driver) | — | Get driver's active delivery |
| `POST` | `/deliveries/{id}/respond` | Bearer (Driver) | — | Accept or reject delivery offer |
| `POST` | `/deliveries/{id}/start` | Bearer (Driver) | — | Start trip (en route) |
| `POST` | `/deliveries/{id}/arrive` | Bearer (Driver) | — | Mark arrived at customer |
| `POST` | `/deliveries/{id}/complete` | Bearer (Driver) | — | Complete delivery (OTP + quantity + optional photo) |
| `GET` | `/admin/deliveries` | Bearer | `deliveries:read` | List all deliveries (admin, filterable) |
| `GET` | `/admin/deliveries/{id}` | Bearer | `deliveries:read` | Get delivery detail + events + assignments |
| `POST` | `/admin/deliveries/{id}/assign` | Bearer | `deliveries:assign` | Manual driver assignment |
| `POST` | `/admin/deliveries/{id}/reassign` | Bearer | `deliveries:assign` | Reassign to different driver |

**Delivery Completion:**
```
POST /deliveries/{id}/complete
Content-Type: multipart/form-data

{
  "otp_code": "482910",
  "delivered_quantity_litres": 5000,
  "gps_lat": 17.385044,
  "gps_lng": 78.486671,
  "proof_photo": <file>  (optional)
}
```

---

### 2.12 Drivers (DRV)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/drivers/me` | Bearer (Driver) | — | Get driver profile + status |
| `PATCH` | `/drivers/me/status` | Bearer (Driver) | — | Toggle availability (AVAILABLE/UNAVAILABLE) |
| `GET` | `/drivers/me/deliveries` | Bearer (Driver) | — | Delivery history (paginated) |
| `GET` | `/drivers/me/earnings` | Bearer (Driver) | — | Earnings summary (daily/weekly/monthly) |
| `GET` | `/admin/drivers` | Bearer | `drivers:read` | List all drivers |
| `GET` | `/admin/drivers/{id}` | Bearer | `drivers:read` | Get driver detail |
| `POST` | `/admin/drivers` | Bearer | `drivers:write` | Create driver profile |
| `PATCH` | `/admin/drivers/{id}` | Bearer | `drivers:write` | Update/deactivate driver |

---

### 2.13 Vehicles (VEH)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/admin/vehicles` | Bearer | `vehicles:read` | List all vehicles |
| `GET` | `/admin/vehicles/{id}` | Bearer | `vehicles:read` | Get vehicle detail |
| `POST` | `/admin/vehicles` | Bearer | `vehicles:write` | Create vehicle |
| `PATCH` | `/admin/vehicles/{id}` | Bearer | `vehicles:write` | Update/deactivate vehicle |
| `POST` | `/admin/vehicles/{id}/assign-driver` | Bearer | `vehicles:write` | Assign driver to vehicle |

---

### 2.14 Payments (PAY)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `POST` | `/payments/webhook` | Public* | — | Gateway webhook (signature verified) |
| `POST` | `/payments/{id}/retry` | Bearer | — | Retry failed payment |
| `GET` | `/admin/payments` | Bearer | `payments:read` | List payments (filterable) |
| `GET` | `/admin/payments/{id}` | Bearer | `payments:read` | Get payment detail + transactions |

*Webhook endpoint is public but verifies Razorpay's cryptographic signature server-side.

---

### 2.15 Refunds (RFD)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/admin/refunds` | Bearer | `refunds:read` | List refunds |
| `GET` | `/admin/refunds/{id}` | Bearer | `refunds:read` | Get refund detail |
| `POST` | `/admin/refunds` | Bearer | `refunds:write` | Initiate manual refund (mandatory reason) |

---

### 2.16 Notifications (NTF)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/notifications` | Bearer | — | List current user's notifications |
| `POST` | `/notifications/register-device` | Bearer | — | Register FCM token for push notifications |

---

### 2.17 Reviews (REV)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `POST` | `/orders/{id}/reviews` | Bearer | — | Submit a review for a completed order |
| `GET` | `/drivers/me/reviews` | Bearer (Driver) | — | Driver's received reviews |
| `GET` | `/admin/reviews` | Bearer | `reviews:read` | List all reviews (filterable) |

---

### 2.18 Admin Operations (ADM)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/admin/dashboard` | Bearer | `dashboard:read` | Dashboard summary (metrics + alerts) |
| `GET` | `/admin/roles` | Bearer | `roles:read` | List all roles |
| `POST` | `/admin/users/{id}/roles` | Bearer | `roles:write` | Assign role to user |
| `DELETE` | `/admin/users/{id}/roles/{role_id}` | Bearer | `roles:write` | Revoke role from user |

---

### 2.19 Reporting (RPT)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/admin/reports/sales` | Bearer | `reports:read` | Sales report (by period, purpose, quality) |
| `GET` | `/admin/reports/inventory` | Bearer | `reports:read` | Water supply/consumption report |
| `GET` | `/admin/reports/deliveries` | Bearer | `reports:read` | Delivery performance report |
| `GET` | `/admin/reports/customers` | Bearer | `reports:read` | Customer metrics report |

---

### 2.20 Audit (AUD)

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/admin/audit-logs` | Bearer | `audit:read` | List audit logs (filterable by entity, actor, date, action) |
| `GET` | `/admin/audit-logs/{entity_type}/{entity_id}` | Bearer | `audit:read` | Get complete audit trail for a specific entity |

---

### 2.21 B2B — Businesses (BIZ) [V1 Backend / Phase 2 UI]

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/admin/businesses` | Bearer | `businesses:read` | List businesses |
| `GET` | `/admin/businesses/{id}` | Bearer | `businesses:read` | Get business detail |
| `POST` | `/admin/businesses` | Bearer | `businesses:write` | Create business |
| `PATCH` | `/admin/businesses/{id}` | Bearer | `businesses:write` | Update business |
| `GET` | `/admin/businesses/{id}/users` | Bearer | `businesses:read` | List business users |
| `POST` | `/admin/businesses/{id}/users` | Bearer | `businesses:write` | Add user to business |
| `GET` | `/admin/businesses/{id}/sites` | Bearer | `businesses:read` | List business sites |
| `POST` | `/admin/businesses/{id}/sites` | Bearer | `businesses:write` | Add business site |

---

### 2.22 Bulk Orders (BULK) [V1 Backend / Phase 2 UI]

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/admin/bulk-requests` | Bearer | `bulk:read` | List bulk requests |
| `GET` | `/admin/bulk-requests/{id}` | Bearer | `bulk:read` | Get bulk request detail |
| `POST` | `/admin/bulk-requests/{id}/quote` | Bearer | `bulk:write` | Create quote for request |
| `PATCH` | `/admin/bulk-requests/{id}` | Bearer | `bulk:write` | Update status |

---

### 2.23 Recurring Orders (REC) [V1 Backend / Phase 2 UI]

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/admin/recurring-orders` | Bearer | `recurring:read` | List recurring orders |
| `GET` | `/admin/recurring-orders/{id}` | Bearer | `recurring:read` | Get recurring order detail + instances |
| `POST` | `/admin/recurring-orders` | Bearer | `recurring:write` | Create recurring order |
| `PATCH` | `/admin/recurring-orders/{id}` | Bearer | `recurring:write` | Pause / cancel recurring order |

---

### 2.24 Invoices (INVC) [V1 Backend / Phase 2 UI]

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/admin/invoices` | Bearer | `invoices:read` | List invoices |
| `GET` | `/admin/invoices/{id}` | Bearer | `invoices:read` | Get invoice detail |
| `POST` | `/admin/invoices` | Bearer | `invoices:write` | Generate invoice |
| `PATCH` | `/admin/invoices/{id}` | Bearer | `invoices:write` | Update invoice status |

---

### 2.25 Health & System

| Method | Path | Auth | Permission | Description |
|--------|------|------|------------|-------------|
| `GET` | `/health` | Public | — | System health check (DB, Redis, Celery) |
| `GET` | `/health/ready` | Public | — | Readiness probe |

---

## 3. Endpoint Summary

| Domain | Customer-Facing | Driver-Facing | Admin | Total |
|--------|----------------|---------------|-------|-------|
| Auth | 5 | — | — | 5 |
| Users | 2 | — | 3 | 5 |
| Addresses | 4 | — | 1 | 5 |
| Catalog | 5 | — | 10 | 15 |
| Quality | 2 | — | 2 | 4 |
| Sources | — | — | 4 | 4 |
| Inventory | — | — | 7 | 7 |
| Pricing | — | — | 7 | 7 |
| Coupons | 1 | — | 4 | 5 |
| Orders | 6 | — | 3 | 9 |
| Deliveries | — | 5 | 4 | 9 |
| Drivers | — | 4 | 4 | 8 |
| Vehicles | — | — | 5 | 5 |
| Payments | 1 | — | 3 | 4 |
| Refunds | — | — | 3 | 3 |
| Notifications | 2 | — | — | 2 |
| Reviews | 1 | 1 | 1 | 3 |
| Admin Ops | — | — | 4 | 4 |
| Reporting | — | — | 4 | 4 |
| Audit | — | — | 2 | 2 |
| B2B | — | — | 8 | 8 |
| Bulk | — | — | 4 | 4 |
| Recurring | — | — | 4 | 4 |
| Invoices | — | — | 4 | 4 |
| Health | 2 | — | — | 2 |
| **TOTAL** | **31** | **10** | **91** | **132** |
