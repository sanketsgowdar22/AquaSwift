# Phase 5 — Admin Dashboard

## 1. Phase Identity

- **Phase:** P5
- **Name:** Admin Dashboard
- **Status:** NOT STARTED
- **Depends On:** P4 (Customer + Driver Integration) validated

## 2. Objective

Connect the existing Admin Dashboard UI to real backend APIs. Deliver working management capabilities for customers, drivers, orders, catalog, inventory, pricing, service areas, and system configuration.

## 3. Scope

### P5.1 — Admin Authentication
- Email/password login (existing auth)
- RBAC-protected routes
- **Tasks:** T-AUTH-005

### P5.2 — Dashboard Overview
- Real-time metrics (orders, revenue, active deliveries)
- Alert system (low inventory, failed deliveries)
- **Tasks:** T-ADM-001

### P5.3 — Customer Management
- List/search/filter customers
- Customer detail (profile + orders + addresses)
- Deactivate customer
- **Tasks:** T-USR-005

### P5.4 — Driver Management
- List/search/filter drivers
- Driver detail (profile + deliveries + earnings)
- Create/update/deactivate drivers
- **Tasks:** T-DRV-001 through T-DRV-006

### P5.5 — Order Management
- List/filter orders by status, customer, date
- Order detail with full history
- Admin cancel with mandatory reason
- **Tasks:** T-ORD-009

### P5.6 — Delivery Management
- Monitor active deliveries
- Manual assign/reassign drivers
- View delivery events timeline
- **Tasks:** T-DEL-011, T-DEL-012

### P5.7 — Catalog Management
- CRUD water purposes, quality types, delivery methods
- Manage purpose-quality links
- CRUD water variants
- **Tasks:** T-CAT-003 through T-CAT-008

### P5.8 — Inventory Management
- View source balances
- Record received/adjusted/loss transactions
- Reconciliation
- **Tasks:** T-INV-001 through T-INV-012

### P5.9 — Pricing Management
- CRUD pricing rules (volume, distance, dynamic)
- CRUD delivery pricing rules
- **Tasks:** T-PRC-001 through T-PRC-008

### P5.10 — Service Areas (Leaflet)
- Polygon-based delivery zones
- Area CRUD on interactive map
- **Modules:** routes
- **Tasks:** T-RTE-001, T-RTE-002

### P5.11 — Reports & Analytics
- Sales reports (by period, purpose, quality)
- Inventory reports
- Delivery performance reports
- Customer metrics
- **Tasks:** T-RPT-001 through T-RPT-004, T-ANL-001 through T-ANL-002

### P5.12 — Audit Logs
- View audit trail (filterable by entity, actor, date)
- Entity-specific audit history
- **Tasks:** T-AUD-001 through T-AUD-005

### P5.13 — System Configuration
- Coupon management
- User & role management
- System settings
- **Tasks:** T-CPN-001 through T-CPN-007, T-RBAC-001 through T-RBAC-006

### P5.14 — B2B & Advanced (Deferred to Post-V1)
- Business management
- Bulk orders
- Recurring orders
- Invoices
- **Tasks:** T-BIZ-*, T-BULK-*, T-REC-*, T-INVC-*

## 4. Entry Gate

Before starting Phase 5, verify:
- [ ] Customer workflow validated (P2)
- [ ] Driver workflow validated (P3)
- [ ] Customer + Driver integration validated (P4)
- [ ] Order lifecycle stable
- [ ] Delivery lifecycle stable
- [ ] Core APIs tested

## 5. Existing Implementation

### Frontend (17 admin pages exist)
| Page | Route | Status |
|------|-------|--------|
| Dashboard | `/admin/dashboard` | ✅ UI (mock) |
| Orders | `/admin/orders` | ✅ UI (mock) |
| Catalog | `/admin/catalog` | ✅ UI (mock) |
| Inventory | `/admin/inventory` | ✅ UI (mock) |
| Coupons | `/admin/coupons` | ✅ UI (mock) |
| Reports | `/admin/reports` | ✅ UI (mock) |
| Areas | `/admin/areas` | ✅ Leaflet map (mock) |
| Settings | `/admin/settings` | ✅ UI (mock) |
| Customers | `/admin/customers` | ⬜ Placeholder |
| Drivers | `/admin/drivers` | ⬜ Placeholder |
| Deliveries | `/admin/deliveries` | ⬜ Placeholder |
| Payments | `/admin/payments` | ⬜ Placeholder |
| Pricing | `/admin/pricing` | ⬜ Placeholder |
| Vehicles | `/admin/vehicles` | ⬜ Placeholder |
| Sources | `/admin/sources` | ⬜ Placeholder |
| Audit | `/admin/audit` | ⬜ Placeholder |
| Businesses | `/admin/businesses` | ⬜ Placeholder |

## 6. Existing Tasks (Preserved)

56+ tasks across admin, inventory, catalog, pricing, reports, audit, etc. See `PHASE-MODULE-TASK-MATRIX.md`.

## 18. Acceptance Criteria

- [ ] Admin can log in and access dashboard
- [ ] Admin can manage customers
- [ ] Admin can manage drivers
- [ ] Admin can view and manage orders
- [ ] Admin can monitor deliveries
- [ ] Admin can manage catalog (purposes, qualities, variants)
- [ ] Admin can manage inventory
- [ ] Admin can manage pricing rules
- [ ] Admin can manage service areas on map
- [ ] Admin can view reports
- [ ] Admin can view audit logs
- [ ] RBAC prevents unauthorized access
- [ ] All mock data replaced with real API data

## 22. Exit Criteria

Admin dashboard is fully functional with real data. All CRUD operations work. RBAC enforced. Reports generate correctly.

**Phase 5 must be substantially complete before Phase 6 begins.**
