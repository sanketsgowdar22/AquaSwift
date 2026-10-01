# Phase → Module → Task Traceability Matrix

This document maps every existing task to its phase, module, and current implementation status.

**Total: 157 tasks across 27 modules**

---

## Phase 1 — Core Platform & Security

### auth (10 tasks, 5 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-AUTH-001 | Create Auth SQLAlchemy Models | IMPLEMENTED | None |
| T-AUTH-002 | Create Auth Pydantic Schemas | IMPLEMENTED | T-AUTH-001 |
| T-AUTH-003 | Implement OTP Request Service | IMPLEMENTED | T-AUTH-001, T-AUTH-002 |
| T-AUTH-004 | Implement OTP Verification Service | IMPLEMENTED | T-AUTH-003 |
| T-AUTH-005 | Implement Admin Login Service | IMPLEMENTED | T-AUTH-001 |
| T-AUTH-006 | Implement JWT & Refresh Token Utilities | IMPLEMENTED | T-AUTH-001 |
| T-AUTH-007 | Create Auth API Routes | IMPLEMENTED | T-AUTH-003–006 |
| T-AUTH-008 | Implement Rate Limiting Middleware | NOT_STARTED | T-AUTH-007, Redis |
| T-AUTH-009 | Implement OTP Fallback Channel | NOT_STARTED | T-AUTH-003 |
| T-AUTH-010 | Write Auth Unit & Integration Tests | NOT_STARTED | T-AUTH-007 |

### rbac (6 tasks, 4 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-RBAC-001 | Create Role & Permission Models | IMPLEMENTED | T-AUTH-001 |
| T-RBAC-002 | Create RBAC Schemas | IMPLEMENTED | T-RBAC-001 |
| T-RBAC-003 | Implement RBAC Service | IMPLEMENTED | T-RBAC-001 |
| T-RBAC-004 | Create RBAC Router | IMPLEMENTED | T-RBAC-003 |
| T-RBAC-005 | Implement Permission Decorators | IMPLEMENTED | T-RBAC-003 |
| T-RBAC-006 | Write RBAC Tests | NOT_STARTED | T-RBAC-004 |

### users (6 tasks, 3 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-USR-001 | Create User Models | IMPLEMENTED | T-AUTH-001 |
| T-USR-002 | Create User Schemas | IMPLEMENTED | T-USR-001 |
| T-USR-003 | Implement User Service | IMPLEMENTED | T-USR-001 |
| T-USR-004 | Create User Router | IMPLEMENTED | T-USR-003 |
| T-USR-005 | Implement Admin User Management | IMPLEMENTED | T-USR-003, T-RBAC-005 |
| T-USR-006 | Write User Tests | NOT_STARTED | T-USR-004 |

### New P1 Tasks

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-CORE-001 | Set up pytest async fixtures + test client | NOT_STARTED | None |
| T-CORE-002 | Create Alembic initial migration | NOT_STARTED | All models |
| T-CORE-003 | Implement rate limiting middleware | NOT_STARTED | T-AUTH-008 |
| T-CORE-004 | Revert demo authentication bypass | NOT_STARTED | T-AUTH-007 |
| T-CORE-005 | Add security headers middleware | NOT_STARTED | None |
| T-CORE-006 | Verify CORS configuration | NOT_STARTED | None |

---

## Phase 2 — Customer App

### addresses (5 tasks, 4 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-ADDR-001 | Create Address Models | IMPLEMENTED | T-AUTH-001 |
| T-ADDR-002 | Create Address Schemas | IMPLEMENTED | T-ADDR-001 |
| T-ADDR-003 | Implement Address Service | IMPLEMENTED | T-ADDR-001 |
| T-ADDR-004 | Create Address Router | IMPLEMENTED | T-ADDR-003 |
| T-ADDR-005 | Write Address Tests | NOT_STARTED | T-ADDR-004 |

### catalog (9 tasks, 8 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-CAT-001 | Create Catalog Models | IMPLEMENTED | None |
| T-CAT-002 | Create Catalog Schemas | IMPLEMENTED | T-CAT-001 |
| T-CAT-003 | Implement Purpose Service | IMPLEMENTED | T-CAT-001 |
| T-CAT-004 | Implement Quality Type Service | IMPLEMENTED | T-CAT-001 |
| T-CAT-005 | Implement Delivery Method Service | IMPLEMENTED | T-CAT-001 |
| T-CAT-006 | Implement Variant Service | IMPLEMENTED | T-CAT-001 |
| T-CAT-007 | Implement Catalog Caching | NOT_STARTED | T-CAT-003–006, Redis |
| T-CAT-008 | Create Catalog Router | IMPLEMENTED | T-CAT-003–006 |
| T-CAT-009 | Write Catalog Tests | NOT_STARTED | T-CAT-008 |

### quality (5 tasks, 2 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-QUAL-001 | Create Quality Models | IMPLEMENTED | T-SRC-001 |
| T-QUAL-002 | Create Quality Schemas | IMPLEMENTED | T-QUAL-001 |
| T-QUAL-003 | Implement Quality Service | IMPLEMENTED | T-QUAL-001 |
| T-QUAL-004 | Create Quality Router | IMPLEMENTED | T-QUAL-003 |
| T-QUAL-005 | Write Quality Tests | NOT_STARTED | T-QUAL-004 |

### sources (4 tasks, 2 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-SRC-001 | Create Source Models | IMPLEMENTED | None |
| T-SRC-002 | Create Source Schemas | IMPLEMENTED | T-SRC-001 |
| T-SRC-003 | Implement Source Service | IMPLEMENTED | T-SRC-001 |
| T-SRC-004 | Create Source Router | IMPLEMENTED | T-SRC-003 |

### pricing (8 tasks, 7 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-PRC-001 | Create Pricing Models | IMPLEMENTED | T-CAT-001 |
| T-PRC-002 | Create Pricing Schemas | IMPLEMENTED | T-PRC-001 |
| T-PRC-003 | Implement Pricing Engine | IMPLEMENTED | T-PRC-001 |
| T-PRC-004 | Implement Delivery Pricing | IMPLEMENTED | T-PRC-001 |
| T-PRC-005 | Implement Dynamic Pricing | NOT_STARTED | T-PRC-003 |
| T-PRC-006 | Create Pricing Router | IMPLEMENTED | T-PRC-003 |
| T-PRC-007 | Implement Price Quoting | IMPLEMENTED | T-PRC-003, T-PRC-004 |
| T-PRC-008 | Write Pricing Tests | NOT_STARTED | T-PRC-006 |

### coupons (7 tasks, 4 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-CPN-001 | Create Coupon Models | IMPLEMENTED | None |
| T-CPN-002 | Create Coupon Schemas | IMPLEMENTED | T-CPN-001 |
| T-CPN-003 | Implement Coupon Validation | IMPLEMENTED | T-CPN-001 |
| T-CPN-004 | Implement Coupon Usage Tracking | IMPLEMENTED | T-CPN-003 |
| T-CPN-005 | Create Coupon Router | IMPLEMENTED | T-CPN-003 |
| T-CPN-006 | Implement Admin Coupon CRUD | IMPLEMENTED | T-CPN-003 |
| T-CPN-007 | Write Coupon Tests | NOT_STARTED | T-CPN-005 |

### orders (12 tasks, 10 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-ORD-001 | Create Order & OrderItem Models | IMPLEMENTED | T-AUTH-001, T-ADDR-001, T-CAT-001 |
| T-ORD-002 | Create Order Schemas | IMPLEMENTED | T-ORD-001 |
| T-ORD-003 | Implement Order Creation Service | IMPLEMENTED | T-PRC-003, T-INV-004, T-PAY-001 |
| T-ORD-004 | Implement Order State Machine | IMPLEMENTED | T-ORD-001 |
| T-ORD-005 | Implement Order Cancellation | IMPLEMENTED | T-ORD-004 |
| T-ORD-006 | Implement Delivery Generation | IMPLEMENTED | T-ORD-004 |
| T-ORD-007 | Implement Order Listing & Detail | IMPLEMENTED | T-ORD-001 |
| T-ORD-008 | Implement Reorder | IMPLEMENTED | T-ORD-003 |
| T-ORD-009 | Implement Admin Order Management | IMPLEMENTED | T-ORD-004 |
| T-ORD-010 | Create Order API Routes | IMPLEMENTED | T-ORD-003–009 |
| T-ORD-011 | Implement Order Number Generation | IMPLEMENTED | T-ORD-001 |
| T-ORD-012 | Write Order Tests | NOT_STARTED | T-ORD-010 |

### payments (7 tasks, 5 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-PAY-001 | Create Payment Models | IMPLEMENTED | T-ORD-001 |
| T-PAY-002 | Create Payment Schemas | IMPLEMENTED | T-PAY-001 |
| T-PAY-003 | Implement Razorpay Integration | IMPLEMENTED | T-PAY-001 |
| T-PAY-004 | Implement Webhook Handler | IMPLEMENTED | T-PAY-003 |
| T-PAY-005 | Implement Payment Retry | IMPLEMENTED | T-PAY-003 |
| T-PAY-006 | Create Payment Router | IMPLEMENTED | T-PAY-003 |
| T-PAY-007 | Write Payment Tests | NOT_STARTED | T-PAY-006 |

### refunds (5 tasks, 3 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-RFD-001 | Create Refund Models | IMPLEMENTED | T-PAY-001, T-ORD-001 |
| T-RFD-002 | Create Refund Schemas | IMPLEMENTED | T-RFD-001 |
| T-RFD-003 | Implement Refund Service | IMPLEMENTED | T-RFD-001, T-PAY-003 |
| T-RFD-004 | Create Refund Router | IMPLEMENTED | T-RFD-003 |
| T-RFD-005 | Write Refund Tests | NOT_STARTED | T-RFD-004 |

### notifications (7 tasks, 6 user stories) — Shared P2/P3

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-NTF-001 | Create Notification Models | IMPLEMENTED | T-AUTH-001 |
| T-NTF-002 | Implement FCM Push Service | NOT_STARTED | T-NTF-001, FCM |
| T-NTF-003 | Implement SMS Notification Service | NOT_STARTED | T-NTF-001, MSG91 |
| T-NTF-004 | Implement In-App Notifications | IMPLEMENTED | T-NTF-001 |
| T-NTF-005 | Create Notification Router | IMPLEMENTED | T-NTF-004 |
| T-NTF-006 | Implement Device Registration | NOT_STARTED | T-NTF-002 |
| T-NTF-007 | Write Notification Tests | NOT_STARTED | T-NTF-005 |

### reviews (3 tasks, 3 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-REV-001 | Create Review Models | IMPLEMENTED | T-ORD-001 |
| T-REV-002 | Implement Review Service + Router | IMPLEMENTED | T-REV-001 |
| T-REV-003 | Write Review Tests | NOT_STARTED | T-REV-002 |

### New P2 Tasks (Frontend Integration)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-FE-CUS-001 | Wire Customer Home to catalog API | NOT_STARTED | T-CAT-008 |
| T-FE-CUS-002 | Wire Product page to variant API | NOT_STARTED | T-CAT-002, T-PRC-007 |
| T-FE-CUS-003 | Wire Checkout to order creation API | NOT_STARTED | T-ORD-003 |
| T-FE-CUS-004 | Wire Orders page to order list API | NOT_STARTED | T-ORD-007 |
| T-FE-CUS-005 | Wire Tracking page to delivery status API | NOT_STARTED | T-DEL-012 |
| T-FE-CUS-006 | Wire Review page to review API | NOT_STARTED | T-REV-002 |
| T-FE-CUS-007 | Implement customer OTP login flow | NOT_STARTED | T-AUTH-003, T-AUTH-004 |
| T-FE-CUS-008 | Implement address management UI | NOT_STARTED | T-ADDR-004 |

---

## Phase 3 — Driver App

### drivers (6 tasks, 4 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-DRV-001 | Create Driver Models | IMPLEMENTED | T-AUTH-001 |
| T-DRV-002 | Create Driver Schemas | NOT_STARTED | T-DRV-001 |
| T-DRV-003 | Implement Driver Service | NOT_STARTED | T-DRV-001 |
| T-DRV-004 | Create Driver Router | IMPLEMENTED | T-DRV-003 |
| T-DRV-005 | Implement Driver Earnings | NOT_STARTED | T-DRV-001, T-DEL-008 |
| T-DRV-006 | Write Driver Tests | NOT_STARTED | T-DRV-004 |

### deliveries (13 tasks, 9 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-DEL-001 | Create Delivery Models | IMPLEMENTED | T-ORD-001, T-DRV-001 |
| T-DEL-002 | Create Delivery Schemas | IMPLEMENTED | T-DEL-001 |
| T-DEL-003 | Implement Delivery State Machine | IMPLEMENTED | T-DEL-001 |
| T-DEL-004 | Implement Auto-Offer Service | NOT_STARTED | T-DEL-003, T-DRV-001, FCM |
| T-DEL-005 | Implement Offer Timeout Handler | NOT_STARTED | T-DEL-004 |
| T-DEL-006 | Implement Driver Response Handler | NOT_STARTED | T-DEL-003 |
| T-DEL-007 | Implement Delivery Execution Endpoints | IMPLEMENTED | T-DEL-003 |
| T-DEL-008 | Implement Delivery Completion | NOT_STARTED | T-DEL-003, OTP |
| T-DEL-009 | Implement Partial Delivery | NOT_STARTED | T-DEL-008 |
| T-DEL-010 | Implement Failed Delivery | NOT_STARTED | T-DEL-003 |
| T-DEL-011 | Implement Admin Assign/Reassign | NOT_STARTED | T-DEL-003 |
| T-DEL-012 | Create Delivery API Routes | IMPLEMENTED | T-DEL-004–011 |
| T-DEL-013 | Write Delivery Tests | NOT_STARTED | T-DEL-012 |

### vehicles (4 tasks, 2 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-VEH-001 | Create Vehicle Models | IMPLEMENTED | None |
| T-VEH-002 | Create Vehicle Schemas | IMPLEMENTED | T-VEH-001 |
| T-VEH-003 | Implement Vehicle Service + Router | IMPLEMENTED | T-VEH-001 |
| T-VEH-004 | Write Vehicle Tests | NOT_STARTED | T-VEH-003 |

### New P3 Tasks (Frontend Integration)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-FE-DRV-001 | Wire Driver Dashboard to delivery API | NOT_STARTED | T-DEL-012 |
| T-FE-DRV-002 | Wire Earnings page to driver earnings API | NOT_STARTED | T-DRV-005 |
| T-FE-DRV-003 | Implement driver login flow | NOT_STARTED | T-AUTH-005 |
| T-FE-DRV-004 | Implement delivery accept/reject UI | NOT_STARTED | T-DEL-006 |
| T-FE-DRV-005 | Implement delivery completion UI | NOT_STARTED | T-DEL-008 |

---

## Phase 4 — Customer + Driver Integration

### New P4 Tasks

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-INT-001 | End-to-end order lifecycle test | NOT_STARTED | T-ORD-004, T-DEL-003 |
| T-INT-002 | Cancellation + refund integration test | NOT_STARTED | T-ORD-005, T-RFD |
| T-INT-003 | Assignment cascade test | NOT_STARTED | T-DEL-004, T-DEL-005 |
| T-INT-004 | Notification delivery verification | NOT_STARTED | T-NTF |
| T-INT-005 | State consistency audit | NOT_STARTED | T-ORD-004, T-DEL-003 |

---

## Phase 5 — Admin Dashboard

### inventory (12 tasks, 11 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-INV-001 | Create Inventory Models | IMPLEMENTED | T-SRC-001 |
| T-INV-002 | Create Inventory Schemas | IMPLEMENTED | T-INV-001 |
| T-INV-003 | Implement Balance Query | IMPLEMENTED | T-INV-001 |
| T-INV-004 | Implement RECEIVED Transaction | IMPLEMENTED | T-INV-001 |
| T-INV-005 | Implement ALLOCATED Transaction | IMPLEMENTED | T-INV-001 |
| T-INV-006 | Implement RELEASED Transaction | IMPLEMENTED | T-INV-001 |
| T-INV-007 | Implement DELIVERED Transaction | IMPLEMENTED | T-INV-001 |
| T-INV-008 | Implement ADJUSTED Transaction | IMPLEMENTED | T-INV-001 |
| T-INV-009 | Implement LOST_WASTAGE Transaction | IMPLEMENTED | T-INV-001 |
| T-INV-010 | Implement Reconciliation | NOT_STARTED | T-INV-003 |
| T-INV-011 | Create Inventory Router | IMPLEMENTED | T-INV-003–009 |
| T-INV-012 | Write Inventory Tests | NOT_STARTED | T-INV-011 |

### admin (3 tasks, 3 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-ADM-001 | Implement Dashboard Aggregation | NOT_STARTED | Multiple modules |
| T-ADM-002 | Implement Admin Role Management | IMPLEMENTED | T-RBAC-003 |
| T-ADM-003 | Write Admin Tests | NOT_STARTED | T-ADM-001 |

### reports (4 tasks, 5 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-RPT-001 | Implement Sales Report | NOT_STARTED | T-ORD, T-PAY |
| T-RPT-002 | Implement Inventory Report | NOT_STARTED | T-INV |
| T-RPT-003 | Implement Delivery Report | NOT_STARTED | T-DEL |
| T-RPT-004 | Implement Customer Report | NOT_STARTED | T-USR, T-ORD |

### audit (5 tasks, 4 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-AUD-001 | Create Audit Log Models | IMPLEMENTED | None |
| T-AUD-002 | Implement Audit Log Writer | IMPLEMENTED | T-AUD-001 |
| T-AUD-003 | Implement Audit Log Query | NOT_STARTED | T-AUD-001 |
| T-AUD-004 | Create Audit Router | NOT_STARTED | T-AUD-003 |
| T-AUD-005 | Write Audit Tests | NOT_STARTED | T-AUD-004 |

### routes (2 tasks, 2 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-RTE-001 | Create Service Area Models | NOT_STARTED | None |
| T-RTE-002 | Implement Service Area CRUD | NOT_STARTED | T-RTE-001 |

### analytics (2 tasks, 5 user stories)

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-ANL-001 | Implement Analytics Aggregation | NOT_STARTED | Multiple modules |
| T-ANL-002 | Write Analytics Tests | NOT_STARTED | T-ANL-001 |

### businesses (3 tasks, 4 user stories) — Deferred to post-V1

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-BIZ-001 | Create Business Models | IMPLEMENTED | T-AUTH-001 |
| T-BIZ-002 | Implement Business Service + Router | NOT_STARTED | T-BIZ-001 |
| T-BIZ-003 | Write Business Tests | NOT_STARTED | T-BIZ-002 |

### bulk_orders (3 tasks, 4 user stories) — Deferred to post-V1

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-BULK-001 | Create Bulk Order Models | NOT_STARTED | T-ORD-001 |
| T-BULK-002 | Implement Bulk Order Service + Router | NOT_STARTED | T-BULK-001 |
| T-BULK-003 | Write Bulk Order Tests | NOT_STARTED | T-BULK-002 |

### recurring_orders (4 tasks, 3 user stories) — Deferred to post-V1

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-REC-001 | Create Recurring Order Models | NOT_STARTED | T-ORD-001 |
| T-REC-002 | Implement Recurring Order Service | NOT_STARTED | T-REC-001 |
| T-REC-003 | Create Recurring Order Router | NOT_STARTED | T-REC-002 |
| T-REC-004 | Write Recurring Order Tests | NOT_STARTED | T-REC-003 |

### invoices (3 tasks, 3 user stories) — Deferred to post-V1

| Task | Description | Status | Dependencies |
|------|------------|--------|-------------|
| T-INVC-001 | Create Invoice Models | NOT_STARTED | T-ORD-001 |
| T-INVC-002 | Implement Invoice Service + Router | NOT_STARTED | T-INVC-001 |
| T-INVC-003 | Write Invoice Tests | NOT_STARTED | T-INVC-002 |

---

## Summary

| Phase | Existing Tasks | New Tasks | Total | Implemented | Not Started |
|-------|---------------|-----------|-------|-------------|-------------|
| P1 | 22 | 6 | 28 | 16 | 12 |
| P2 | 71 | 8 | 79 | 53 | 26 |
| P3 | 23 | 5 | 28 | 10 | 18 |
| P4 | 0 | 5 | 5 | 0 | 5 |
| P5 | 41 | 0 | 41 | 18 | 23 |
| P6 | 0 | — | — | — | — |
| P7 | 0 | — | — | — | — |
| **TOTAL** | **157** | **24** | **181** | **97** | **84** |
