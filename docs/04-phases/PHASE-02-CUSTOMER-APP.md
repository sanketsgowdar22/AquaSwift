# Phase 2 — Customer App

## 1. Phase Identity

- **Phase:** P2
- **Name:** Customer App
- **Status:** NOT STARTED
- **Depends On:** P1 (Core Platform & Security) complete

## 2. Objective

Connect the existing Customer App UI to real backend APIs, replacing mock data with live functionality. Deliver a working customer journey from login through order creation, payment, tracking, and review.

## 3. Scope

### P2.1 — Customer Authentication
- OTP login flow (phone → SMS → verify → JWT)
- Session management (token storage, refresh, expiry)
- Protected route guards
- **Modules:** auth
- **Tasks:** T-AUTH-003, T-AUTH-004, T-AUTH-006, T-AUTH-007

### P2.2 — Customer Profile
- View/edit profile (name, email)
- **Modules:** users
- **Tasks:** T-USR-001 through T-USR-004

### P2.3 — Address Management
- Add/edit/delete delivery addresses
- Auto-geocode (Google Maps API)
- Default address selection
- **Modules:** addresses
- **Tasks:** T-ADDR-001 through T-ADDR-005

### P2.4 — Water Catalog
- Browse water purposes, quality types, delivery methods
- View available variants
- **Modules:** catalog
- **Tasks:** T-CAT-001, T-CAT-002, T-CAT-009

### P2.5 — Water Type & Usage Purpose
- Select purpose (Drinking, Construction, Daily Use, etc.)
- Filter quality types by purpose
- Backend-driven catalog (not hardcoded)
- **Modules:** catalog, quality
- **Tasks:** T-CAT-001 through T-CAT-005

### P2.6 — Pricing & Quote
- Request non-binding price quote
- Volume-based pricing
- Delivery fee calculation
- Coupon application
- **Modules:** pricing, coupons
- **Tasks:** T-PRC-001 through T-PRC-008, T-CPN-001 through T-CPN-007

### P2.7 — Order Creation
- Select variant, quantity, address, time window
- Apply coupon code
- Create order with idempotency key
- Handle PENDING_PAYMENT state
- **Modules:** orders
- **Tasks:** T-ORD-001 through T-ORD-006, T-ORD-010, T-ORD-011

### P2.8 — Payment
- Razorpay payment intent creation
- Payment completion callback
- Payment status polling
- Failed payment retry
- **Modules:** payments
- **Tasks:** T-PAY-001 through T-PAY-007

### P2.9 — Order History
- List past orders (paginated, filterable by status)
- Order detail view (items, deliveries, payments)
- **Modules:** orders
- **Tasks:** T-ORD-007

### P2.10 — Order Cancellation
- Cancel order (pre-OUT_FOR_DELIVERY only)
- Cancellation confirmation
- Refund initiation
- **Modules:** orders, refunds
- **Tasks:** T-ORD-005, T-RFD-001 through T-RFD-005

### P2.11 — Real-Time Tracking
- Order status updates
- Delivery driver location (if assigned)
- Leaflet map integration (already exists)
- **Modules:** orders, deliveries
- **Tasks:** T-ORD-007 (detail view), T-DEL-007

### P2.12 — Notifications
- Order status notifications
- Delivery updates
- FCM push registration
- **Modules:** notifications
- **Tasks:** T-NTF-001 through T-NTF-007

### P2.13 — Reviews
- Submit order review (rating + text)
- View review history
- **Modules:** reviews
- **Tasks:** T-REV-001 through T-REV-003

## 4. Out of Scope

- Driver app functionality (Phase 3)
- Admin dashboard functionality (Phase 5)
- B2B orders (Phase 5+)
- Recurring orders (Phase 5+)
- Invoice generation (Phase 5+)

## 5. Existing Implementation

### Backend (API Ready)
All backend modules have router + model + service + schema files. APIs exist but need verification against frontend contracts.

### Frontend (UI Exists — Mock Data)
| Page | Route | Status |
|------|-------|--------|
| Home | `/app` | ✅ UI with mock water types |
| Product | `/app/product` | ✅ UI with mock product data |
| Checkout | `/app/checkout` | ✅ UI with mock pricing |
| Confirmed | `/app/confirmed` | ✅ UI with mock order |
| Orders | `/app/orders` | ✅ UI with mock order list |
| Order Detail | `/app/orders/[id]` | ✅ UI with mock order |
| Tracking | `/app/tracking` | ✅ Leaflet map with mock location |
| Profile | `/app/profile` | ⬜ Placeholder |
| Review | `/app/review` | ✅ UI with mock review |

## 6. Existing Modules

addresses (5 tasks), catalog (9 tasks), coupons (7 tasks), notifications (7 tasks), orders (12 tasks), payments (7 tasks), pricing (8 tasks), quality (5 tasks), refunds (5 tasks), reviews (3 tasks), sources (4 tasks)

## 7. Existing Tasks (Preserved)

71 tasks across the above modules. See `PHASE-MODULE-TASK-MATRIX.md` for full mapping.

## 8. New Tasks

| Task | Description | Dependencies |
|------|------------|-------------|
| T-FE-CUS-001 | Wire Customer Home to catalog API | T-CAT-009 |
| T-FE-CUS-002 | Wire Product page to variant API | T-CAT-002, T-PRC-003 |
| T-FE-CUS-003 | Wire Checkout to order creation API | T-ORD-003 |
| T-FE-CUS-004 | Wire Orders page to order list API | T-ORD-007 |
| T-FE-CUS-005 | Wire Tracking page to delivery status API | T-DEL-007 |
| T-FE-CUS-006 | Wire Review page to review API | T-REV-001 |
| T-FE-CUS-007 | Implement customer OTP login flow | T-AUTH-003, T-AUTH-004 |
| T-FE-CUS-008 | Implement address management UI | T-ADDR-001 through T-ADDR-004 |

## 9–22. [Standard sections follow Phase Document Template]

## 18. Acceptance Criteria

- [ ] Customer can log in via OTP
- [ ] Customer can browse real water catalog
- [ ] Customer can manage addresses
- [ ] Customer can create an order with real pricing
- [ ] Customer can complete payment
- [ ] Customer can view order history
- [ ] Customer can cancel pre-delivery orders
- [ ] Customer can track delivery on map
- [ ] Customer receives notifications
- [ ] Customer can submit reviews
- [ ] All mock data replaced with real API data
- [ ] Error states handled (loading, empty, error)
- [ ] Rate limiting applies to customer endpoints

## 22. Exit Criteria

The complete customer journey works end-to-end:
```
Login → Browse → Select → Quote → Order → Pay → Track → Review
```
All acceptance criteria pass. All customer-facing APIs tested. Mock data fully replaced.

**Phase 2 must be substantially complete before Phase 3 (Driver App) begins.**
