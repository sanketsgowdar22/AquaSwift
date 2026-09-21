# AquaSwift — User Journeys

**Version:** 1.0
**Last Updated:** 2026-08-31

---

## Journey Map Legend

Each journey documents:
- **Actor:** Which persona (P1–P5) performs this journey
- **Trigger:** What initiates the journey
- **Steps:** Sequential actions with touchpoints
- **System actions:** Backend processing at each step
- **Emotions:** User emotional state (😊 positive, 😐 neutral, 😟 concerned, 😠 frustrated)
- **V1 scope:** Whether this journey is fully supported in V1

---

## J1 — First-Time Customer Registration & First Order

**Actor:** P1 (Priya — Individual Customer)
**Trigger:** Priya downloads the AquaSwift app after seeing an ad
**V1 Scope:** ✅ Fully supported

### Steps

| # | Step | Touchpoint | User Action | System Action | Emotion |
|---|------|-----------|-------------|---------------|---------|
| 1 | App launch | Customer App | Opens app for the first time | Shows onboarding/welcome screen | 😊 Curious |
| 2 | Registration | Customer App | Enters mobile number | Sends OTP via MSG91 | 😐 Routine |
| 3 | OTP verification | Customer App | Enters 6-digit OTP | Verifies OTP → creates user → issues JWT | 😊 Quick |
| 4 | Profile setup | Customer App | Enters name, email (optional) | Saves customer profile | 😐 Routine |
| 5 | Home screen | Customer App | Sees purpose cards (Drinking, Daily Use, Construction, etc.) | Fetches `GET /catalog/purposes` → returns dynamic list | 😊 Clear options |
| 6 | Select purpose | Customer App | Taps "Drinking" | Fetches `GET /catalog/purposes/{id}/qualities` | 😊 Intuitive |
| 7 | Select quality | Customer App | Taps "RO+UV" | Shows available delivery methods for this combination | 😐 Expected |
| 8 | Select delivery method | Customer App | Taps "Jar (20L)" | Shows quantity selector with min/max from variant | 😐 Expected |
| 9 | Select quantity | Customer App | Selects 5 jars (100L total) | Validates against variant's min/max quantity | 😊 Flexible |
| 10 | Add address | Customer App | Enters address / selects on map | Geocodes via Google Maps → saves address | 😐 Standard |
| 11 | Select time slot | Customer App | Picks "Tomorrow 8–10 AM" | Checks available delivery windows | 😊 Convenient |
| 12 | View quote | Customer App | Sees price breakdown | `POST /orders/quote` → PricingService computes water price + delivery charge + tax | 😊 Transparent |
| 13 | Apply coupon | Customer App | Enters "FIRST50" coupon code | Validates coupon → recalculates quote with discount | 😊 Savings! |
| 14 | Confirm & pay | Customer App | Taps "Pay ₹450" | `POST /orders` → creates order + reserves inventory + creates payment intent (Razorpay) | 😐 Committed |
| 15 | Payment | Razorpay Checkout | Completes UPI/card payment | Razorpay processes → sends webhook → server verifies → payment SUCCESS | 😊 Done! |
| 16 | Order confirmed | Customer App | Sees "Order Confirmed" with details | Order transitions PENDING_PAYMENT → CONFIRMED; push notification sent | 😊 Confident |
| 17 | Status tracking | Customer App | Checks order status throughout the day | Polls `GET /orders/{id}` periodically; sees ASSIGNED → OUT_FOR_DELIVERY | 😊 Informed |
| 18 | Delivery arrival | Customer App + Push | Receives "Driver arrived" notification | Delivery transitions to ARRIVED; push notification sent | 😊 Ready |
| 19 | Delivery confirmation | In person | Gives OTP to driver; receives water | Driver enters OTP → verified → delivery DELIVERED → inventory DELIVER ledger entry | 😊 Satisfied |
| 20 | Rate & review | Customer App | Rates 5 stars, leaves comment | `POST /reviews` → saved | 😊 Complete |

### Key Moments of Truth
- **Step 12:** Price transparency builds trust — no hidden charges
- **Step 15:** Payment must be seamless — any friction here causes abandonment
- **Step 19:** OTP verification proves delivery happened — resolves disputes

---

## J2 — Returning Customer Reorder

**Actor:** P1 (Priya)
**Trigger:** Priya's drinking water supply is running low
**V1 Scope:** ✅ Fully supported

### Steps

| # | Step | Touchpoint | User Action | System Action | Emotion |
|---|------|-----------|-------------|---------------|---------|
| 1 | Open app | Customer App | Opens app, already logged in | JWT refresh if needed | 😊 Quick |
| 2 | View history | Customer App | Taps "Orders" → sees past orders | `GET /orders?status=DELIVERED&sort=-created_at` | 😊 Easy |
| 3 | Reorder | Customer App | Taps "Reorder" on previous drinking water order | Pre-fills purpose, quality, quantity, delivery method, address from previous order | 😊 Effortless |
| 4 | Confirm details | Customer App | Verifies pre-filled details, adjusts quantity if needed | Re-fetches quote with current pricing | 😐 Quick check |
| 5 | Pay | Customer App | Taps "Pay" → UPI payment | Same flow as J1 steps 14–15 | 😊 Familiar |
| 6 | Track & receive | Customer App | Tracks → receives delivery → confirms with OTP | Same flow as J1 steps 16–19 | 😊 Reliable |

**Target:** Reorder flow completes in < 60 seconds from app open to payment.

---

## J3 — Customer Order Cancellation & Refund

**Actor:** P1 (Priya)
**Trigger:** Priya placed an order but plans changed — she needs to cancel
**V1 Scope:** ✅ Fully supported (cancellation before OUT_FOR_DELIVERY)

### Steps

| # | Step | Touchpoint | User Action | System Action | Emotion |
|---|------|-----------|-------------|---------------|---------|
| 1 | View active order | Customer App | Opens order detail | Shows current status (e.g., CONFIRMED) | 😟 Need to cancel |
| 2 | Cancel order | Customer App | Taps "Cancel Order" → confirms | `POST /orders/{id}/cancel` → validates cancellation is allowed (pre-OUT_FOR_DELIVERY) | 😐 Hopeful |
| 3a | **Allowed** | Customer App | Sees "Order Cancelled" confirmation | Order → CANCELLED; inventory RELEASE (reserved→available); refund initiated via gateway | 😊 Relieved |
| 3b | **Not allowed** | Customer App | Sees "Cannot cancel — delivery in progress" | Returns error: order is OUT_FOR_DELIVERY or later | 😟 Frustrated |
| 4 | Refund processing | Push notification | Receives "Refund of ₹450 initiated" | Gateway processes refund → webhook confirms → payment REFUNDED → push notification | 😊 Trust maintained |
| 5 | Refund confirmation | Customer App + Bank | Sees refund in order history; amount appears in bank (2–5 days) | Refund record created with gateway reference | 😊 Resolved |

### Key Moments of Truth
- **Step 2:** Cancellation window is clear — customer knows *before* tapping whether cancellation is possible
- **Step 4:** Automatic refund without manual intervention builds trust

---

## J4 — Partial Delivery Handling

**Actor:** P1 (Priya) + P3 (Suresh — Driver)
**Trigger:** Driver arrives at customer site but can only deliver 4,000L of a 5,000L order (vehicle issue)
**V1 Scope:** ✅ Fully supported

### Steps

| # | Step | Touchpoint | User Action | System Action | Emotion |
|---|------|-----------|-------------|---------------|---------|
| 1 | Driver arrives | Driver App | Taps "Arrived" at customer location | Delivery → ARRIVED | 😐 |
| 2 | Partial delivery | Driver App | Enters actual quantity delivered: 4,000L (of 5,000L) | Validates: delivered < expected | 😟 Issue |
| 3 | Customer confirms | In person | Customer provides OTP for received quantity | OTP verified; delivery marked PARTIALLY_DELIVERED with `delivered_quantity_litres = 4000` | 😟 Incomplete |
| 4 | System creates remainder | Backend | — | Creates new delivery for remaining 1,000L (PENDING_ASSIGNMENT); order stays PROCESSING | 😐 Automatic |
| 5 | Customer notified | Push notification | Receives "Partial delivery: 4,000L delivered. Remaining 1,000L will be delivered separately." | Push + SMS notification | 😐 Informed |
| 6 | Remainder assigned | Admin Dashboard | Ops manager assigns remainder to next available driver | New delivery goes through standard assignment flow | 😐 |
| 7 | Remainder delivered | Customer App | Receives remaining 1,000L; confirms with OTP | Delivery 2 DELIVERED; **all deliveries done** → parent order → DELIVERED | 😊 Complete |

---

## J5 — Driver Delivery Flow (Full Cycle)

**Actor:** P3 (Suresh — Driver)
**Trigger:** Start of Suresh's work day
**V1 Scope:** ✅ Fully supported

### Steps

| # | Step | Touchpoint | User Action | System Action | Emotion |
|---|------|-----------|-------------|---------------|---------|
| 1 | Login | Driver App | Opens app, enters phone, verifies OTP | Auth → JWT issued; driver profile loaded | 😐 Routine |
| 2 | Go online | Driver App | Toggles availability to "Online" | `POST /drivers/availability` → driver status AVAILABLE | 😊 Ready |
| 3 | Receive offer | Driver App + Push | Push notification: "New delivery — 2,000L to Sector 15 (3.2 km)" | Delivery OFFERED to this driver; timer starts (configurable timeout) | 😊 Opportunity |
| 4a | **Accept** | Driver App | Taps "Accept" | `POST /deliveries/{id}/respond` (accept) → delivery ASSIGNED to driver; driver linked to delivery | 😊 Committed |
| 4b | **Reject** | Driver App | Taps "Reject" (optional reason) | Delivery back to PENDING_ASSIGNMENT → OFFERED to next eligible driver | 😐 Pass |
| 4c | **Timeout** | Driver App | No response within timeout period | Same as reject — auto-reassign to next driver | — |
| 5 | View details | Driver App | Sees delivery details: customer name, address, quantity, source, vehicle | Full delivery info displayed | 😊 Clear |
| 6 | Start trip | Driver App | Taps "Start Trip" | `POST /deliveries/{id}/start` → delivery STARTED | 😊 Moving |
| 7 | Load water | Physical | Loads water at source facility | (Manual process; source staff may verify via separate flow) | 😐 Physical work |
| 8 | Navigate | Driver App | Taps "Navigate" → opens Google Maps | Deep link to Google Maps with customer coordinates | 😊 Guided |
| 9 | Arrive | Driver App | Taps "Arrived" at customer location | `POST /deliveries/{id}/arrive` → delivery ARRIVED; customer notified | 😐 Waiting |
| 10 | Deliver | Physical | Delivers water to customer's tank/location | Physical process | 😐 Physical work |
| 11 | Get OTP | In person | Asks customer for delivery OTP | Customer reads 4-digit code from app/SMS | 😐 Verification |
| 12 | Complete | Driver App | Enters OTP + optional photo → taps "Complete" | `POST /deliveries/{id}/complete` → OTP verified → delivery DELIVERED → inventory DELIVER entry → customer notified | 😊 Done! |
| 13 | Next delivery | Driver App | Returns to available state → receives next offer | Automatically eligible for new offers | 😊 Productive |
| 14 | End of day | Driver App | Toggles "Offline" → checks earnings | Views daily summary: deliveries completed, total earnings | 😊 Earned |

---

## J6 — Driver Rejection & Reassignment

**Actor:** P3 (Suresh) → P3b (another driver)
**Trigger:** Suresh rejects a delivery offer
**V1 Scope:** ✅ Fully supported

### Steps

| # | Step | Touchpoint | User Action | System Action | Emotion |
|---|------|-----------|-------------|---------------|---------|
| 1 | Offer received | Driver App (Suresh) | Sees delivery offer (15km away) | Delivery OFFERED to Suresh | 😟 Too far |
| 2 | Reject | Driver App (Suresh) | Taps "Reject" → selects reason "Too far" | Delivery status → REASSIGNING; rejection recorded in `delivery_assignments` | 😐 Passed |
| 3 | Re-offer | Driver App (Driver B) | Different driver receives the offer | System selects next eligible driver → delivery OFFERED again | 😊 New chance |
| 4 | Accept | Driver App (Driver B) | Accepts the delivery | Delivery ASSIGNED to Driver B; normal flow continues | 😊 |
| 5 | Ops alert (if needed) | Admin Dashboard | If no driver accepts after N attempts → ops manager alerted | Alert generated; manual assignment option available | 😟 Escalation |

---

## J7 — Admin: New Water Purpose Creation

**Actor:** P5 (Vikram — Super Admin)
**Trigger:** Vikram wants to add "Swimming Pool" as a new water purpose
**V1 Scope:** ✅ Fully supported

### Steps

| # | Step | Touchpoint | User Action | System Action | Emotion |
|---|------|-----------|-------------|---------------|---------|
| 1 | Login | Admin Dashboard | Logs in with email + password | JWT issued with admin role | 😐 Routine |
| 2 | Navigate to Catalog | Admin Dashboard | Clicks "Catalog" → "Water Purposes" | Fetches current purposes list | 😐 |
| 3 | Add purpose | Admin Dashboard | Clicks "Add Purpose" → enters name "Swimming Pool", description, uploads icon | `POST /admin/water-purposes` → creates purpose; audit log entry | 😊 Easy |
| 4 | Add quality types | Admin Dashboard | Links quality types: "Chlorinated", "pH-Balanced" | Creates `water_purpose_qualities` records | 😊 Configurable |
| 5 | Create variants | Admin Dashboard | Creates variants: Swimming Pool + Chlorinated + Tanker (5,000L–20,000L) | Creates `water_variants` records; validates combination | 😊 Flexible |
| 6 | Set pricing | Admin Dashboard | Creates pricing rule: ₹0.45/litre for Swimming Pool + Chlorinated | `POST /admin/pricing-rules` → creates rule; audit log entry | 😊 Control |
| 7 | Activate | Admin Dashboard | Activates all new records | `is_active = true`; Redis cache invalidated | 😊 Done |
| 8 | Verify | Customer App | Opens customer app → sees "Swimming Pool" purpose card on home screen | `GET /catalog/purposes` returns new purpose (cache TTL ≤ 60s) | 😊 Instant! |

**Key Moment:** Step 8 — zero app rebuild, zero redeploy, visible within cache TTL.

---

## J8 — Admin: Order Exception Handling

**Actor:** P4 (Anita — Operations Manager)
**Trigger:** A delivery failed because the customer was unavailable
**V1 Scope:** ✅ Fully supported

### Steps

| # | Step | Touchpoint | User Action | System Action | Emotion |
|---|------|-----------|-------------|---------------|---------|
| 1 | Alert received | Admin Dashboard | Sees "Delivery Failed" alert in dashboard | Delivery marked FAILED by driver; alert generated | 😟 Issue |
| 2 | Review details | Admin Dashboard | Clicks into delivery detail | Sees: driver GPS confirmed arrival, customer not present, driver waited 15 min | 😐 Investigating |
| 3 | Contact customer | Phone | Calls customer to reschedule | — | 😐 Manual step |
| 4 | Reschedule | Admin Dashboard | Creates new delivery for the same order, new time slot | New delivery created (PENDING_ASSIGNMENT); order stays PROCESSING | 😐 Resolved |
| 5 | Reassign | Admin Dashboard | Assigns new delivery to available driver | Manual assignment → delivery ASSIGNED → driver notified | 😊 Moving |
| 6 | Successful delivery | System | Driver completes rescheduled delivery | Standard delivery completion flow; parent order → DELIVERED | 😊 Resolved |

---

## J9 — Admin: Inventory Adjustment

**Actor:** P4 (Anita — Operations Manager)
**Trigger:** Monthly reconciliation reveals 500L discrepancy at Source A
**V1 Scope:** ✅ Fully supported

### Steps

| # | Step | Touchpoint | User Action | System Action | Emotion |
|---|------|-----------|-------------|---------------|---------|
| 1 | View inventory | Admin Dashboard | Navigates to Inventory → Source A → Ledger | Shows transaction history + current balance | 😐 |
| 2 | Identify discrepancy | Admin Dashboard | Compares expected vs. actual balance | Reconciliation shows 500L unaccounted | 😟 Issue |
| 3 | Adjust | Admin Dashboard | Clicks "Adjust" → enters -500L → selects reason "LOST_WASTAGE" → adds notes "Monthly reconciliation — suspected leak in storage tank Bay 2" | `POST /admin/inventory/{source_id}/adjust` → creates LOST_WASTAGE transaction; audit log with actor, reason, notes | 😐 Documented |
| 4 | Verify | Admin Dashboard | Refreshes balance → sees updated available quantity | Balance reconciled from ledger | 😊 Accurate |
| 5 | Report | Admin Dashboard | Flags issue for Super Admin review | Audit log entry visible to Super Admin | 😐 Escalated |

---

## J10 — Payment Failure & Retry

**Actor:** P1 (Priya — Customer)
**Trigger:** Payment fails during checkout (bank timeout)
**V1 Scope:** ✅ Fully supported

### Steps

| # | Step | Touchpoint | User Action | System Action | Emotion |
|---|------|-----------|-------------|---------------|---------|
| 1 | Pay | Razorpay Checkout | Selects UPI → payment times out | No webhook received; order stays PENDING_PAYMENT | 😠 Frustrated |
| 2 | Error shown | Customer App | Sees "Payment failed — please try again" | Client callback indicates failure (but server does NOT trust this) | 😟 Worried |
| 3 | Retry | Customer App | Taps "Retry Payment" | New payment intent created (same idempotency key prevents duplicate order); same Razorpay checkout | 😐 Trying again |
| 4 | Success | Razorpay Checkout | Completes payment via card this time | Webhook received → verified → payment SUCCESS → order CONFIRMED | 😊 Relief |
| 5 | Reservation intact | Backend | — | Inventory reservation was held during retry window (not released yet — expiry timeout hasn't passed) | — |

### Edge Case: Abandoned Payment
If Priya never retries and the reservation expiry timeout passes:
- Celery beat job detects PENDING_PAYMENT order past timeout
- Inventory reservation RELEASED (reserved → available)
- Order marked FAILED (payment timeout)
- Customer notified: "Your order has expired. Please place a new order."

---

## Journey Coverage Matrix

| Journey | P1 | P2 | P3 | P4 | P5 | V1 | Key Modules |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|------------|
| J1 — First Order | ✅ | — | — | — | — | ✅ | Auth, Catalog, Pricing, Orders, Payments, Deliveries |
| J2 — Reorder | ✅ | — | — | — | — | ✅ | Orders, Pricing, Payments |
| J3 — Cancellation & Refund | ✅ | — | — | — | — | ✅ | Orders, Payments, Refunds, Inventory |
| J4 — Partial Delivery | ✅ | — | ✅ | — | — | ✅ | Deliveries, Inventory, Orders, Notifications |
| J5 — Driver Full Cycle | — | — | ✅ | — | — | ✅ | Auth, Drivers, Deliveries, Inventory |
| J6 — Driver Reassignment | — | — | ✅ | ✅ | — | ✅ | Deliveries, Drivers, Notifications |
| J7 — New Purpose Creation | — | — | — | — | ✅ | ✅ | Catalog, Pricing, Audit |
| J8 — Exception Handling | — | — | — | ✅ | — | ✅ | Deliveries, Orders, Notifications |
| J9 — Inventory Adjustment | — | — | — | ✅ | ✅ | ✅ | Inventory, Audit |
| J10 — Payment Failure | ✅ | — | — | — | — | ✅ | Payments, Orders, Inventory |
