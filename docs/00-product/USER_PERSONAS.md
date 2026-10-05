# AquaSwift — User Personas

**Version:** 1.0
**Last Updated:** 2026-08-31

---

## P1 — Priya Sharma (Individual Customer)

### Demographics
- **Age:** 28–45
- **Location:** Urban/semi-urban India (Tier 1–2 city)
- **Tech comfort:** Moderate — uses food delivery apps, UPI payments daily
- **Device:** Android smartphone (mid-range), stable 4G connection

### Role
Residential customer ordering water for household use — drinking water (jars), daily use (overhead tank refills), or occasional special needs (e.g., RO water for an event).

### Goals
1. Order safe, clean drinking water quickly and reliably
2. Know the price before ordering — no surprises
3. Track when the delivery will arrive
4. Reorder easily when the water runs low
5. Trust the water quality (especially for drinking)

### Pain Points
1. Current suppliers require phone calls — no app, no price list, no tracking
2. Unreliable delivery times — "we'll come between 8 AM and 6 PM"
3. No way to verify water quality or source
4. Disputes about quantities delivered (especially tank refills)
5. Can't compare pricing across different water types/suppliers

### Behavior Patterns
- Orders 2–3 times per month (drinking jars), 1–2 times per month (tank refill)
- Prefers morning delivery (7–10 AM) before leaving for work
- Pays via UPI or credit/debit card — avoids cash
- Will switch suppliers for better reliability, even at a slight price premium
- Reads reviews before trying a new service

### Key Scenarios
- **First-time order:** Browses catalog, selects drinking water → RO+UV → 20L jar × 5 → scheduled for tomorrow morning → pays via Razorpay → receives OTP for delivery confirmation
- **Reorder:** Opens order history → taps "Reorder" on previous drinking water order → confirms address → pays → done in <60 seconds
- **Tank refill:** Selects Daily Use → Treated → 5,000L tanker → adds new address (terrace tank access instructions in notes) → gets price quote → pays → tracks tanker arrival
- **Issue resolution:** Delivery was 4,500L instead of 5,000L → sees "Partially Delivered" status → contacts support → receives automatic partial refund

### Relevant Modules
Auth, Catalog, Pricing, Orders, Deliveries, Payments, Notifications, Reviews, Address/Site Management

---

## P2 — Rajesh Patel (Business Customer)

### Demographics
- **Age:** 35–55
- **Location:** Urban India
- **Tech comfort:** Moderate — uses business apps, email, WhatsApp for work
- **Device:** Android smartphone + desktop for business operations

### Role
Procurement manager for a construction company. Needs regular bulk water delivery to multiple construction sites for concrete mixing, curing, and worker consumption.

### Goals
1. Set up recurring water deliveries to 3–5 active construction sites
2. Get predictable bulk pricing with invoicing (not per-order payment)
3. Track deliveries across all sites from one account
4. Add/remove sites as projects start and finish
5. Have multiple team members able to place orders under the company account

### Pain Points
1. Managing multiple suppliers for different sites — no consolidated view
2. Inconsistent pricing — negotiated verbally, changes without notice
3. No invoicing — pays cash or bank transfer per delivery, hard to track expenses
4. Can't delegate ordering to site supervisors without losing oversight
5. Water quality varies — no certificates or accountability

### Behavior Patterns
- Orders 10,000L–50,000L per site, 3–5 times per week
- Needs scheduled deliveries (same time, same quantity, recurring)
- Prefers monthly invoicing with 15–30 day payment terms
- Needs site supervisors to confirm delivery at site (delegated OTP)
- Reviews consumption reports monthly for project budgeting

### Key Scenarios (Phase 2 UI, ARCHITECTURE ONLY schema in V1)
- **Business registration:** Registers company → adds 3 construction sites with GPS coordinates → invites 2 site supervisors as employees
- **Bulk order request:** Requests quote for 50,000L/week × 12 weeks to Site A → admin sends quote → Rajesh accepts → recurring deliveries auto-generated
- **Multi-site management:** Views dashboard showing all active sites, pending deliveries, and consumption totals → clicks into Site B to see delivery history
- **Invoice review:** Downloads monthly invoice for all sites → cross-references with delivery confirmations → pays via bank transfer

### Relevant Modules
Auth, Businesses/B2B, Bulk Orders, Recurring Orders, Invoices, Address/Site Management, Orders, Deliveries, Payments, Notifications

---

## P3 — Suresh Kumar (Driver)

### Demographics
- **Age:** 25–40
- **Location:** Urban India
- **Tech comfort:** Basic to moderate — uses WhatsApp, Google Maps, UPI
- **Device:** Android smartphone (budget to mid-range), variable data connection

### Role
Tanker/delivery vehicle driver employed or contracted by the water supply operator. Responsible for loading water at the source, transporting it to customer sites, and confirming delivery.

### Goals
1. Get clear delivery instructions — where to go, how much to deliver, customer contact
2. Maximize daily deliveries (earnings are delivery-based)
3. Complete delivery proof quickly and move to the next one
4. Track daily/weekly/monthly earnings accurately
5. Have flexibility to go offline when not available

### Pain Points
1. Currently receives instructions by phone call — no written record, easy to miscommunicate
2. Doesn't know delivery location until dispatch calls — can't plan route
3. Customer disputes about quantity delivered — no proof system
4. No visibility into earnings — gets paid monthly with no breakdown
5. Can't reject a delivery that's too far away without calling dispatch

### Behavior Patterns
- Works 6–7 days/week, 8–12 hours/day
- Handles 5–15 deliveries per day depending on size
- Goes online at start of shift, offline at end
- Prefers to accept deliveries in his familiar area
- Checks earnings at end of each day

### Key Scenarios
- **Start of day:** Opens app → toggles "Online" → receives first delivery offer (2,000L to location 3km away) → reviews details → accepts → sees loading instructions (Source: Plant A, Bay 3)
- **En route:** Starts trip → app shows navigation link to Google Maps → arrives at customer site → taps "Arrived"
- **Delivery completion:** Customer provides 4-digit OTP → driver enters OTP → app confirms match → driver takes photo of tank/delivery point → taps "Complete" → delivery marked DELIVERED
- **Rejection/reassignment:** Receives offer for delivery 15km away → rejects → offer goes to next eligible driver → Suresh receives closer delivery within 2 minutes
- **Earnings check:** At end of day, views 8 completed deliveries → sees total earnings → views weekly trend

### Relevant Modules
Auth, Drivers, Deliveries (incl. Dispatch/Assignment), Vehicles, Notifications, Payments (earnings)

---

## P4 — Anita Desai (Operations Manager)

### Demographics
- **Age:** 30–45
- **Location:** Urban India (office-based)
- **Tech comfort:** High — proficient with web apps, dashboards, spreadsheets
- **Device:** Desktop/laptop (primary), smartphone (alerts)

### Role
Day-to-day operations manager responsible for order processing, dispatch, driver management, inventory monitoring, and exception handling. Reports to the business owner (Super Admin).

### Goals
1. Process all incoming orders within SLA (< 30 minutes to assign)
2. Keep inventory levels above safety thresholds across all sources
3. Resolve delivery exceptions quickly (driver rejection, customer unavailable, vehicle breakdown)
4. Monitor driver availability and performance
5. Generate daily/weekly operational reports for management

### Pain Points
1. Currently manages operations via phone calls and WhatsApp groups — no single dashboard
2. No visibility into real-time inventory — has to call each source to check levels
3. When a driver rejects a delivery, manual phone tree to find replacement
4. No way to spot patterns (frequent failures at certain locations, underperforming drivers)
5. Report generation is manual — compiling data from multiple paper/spreadsheet sources

### Behavior Patterns
- First thing in morning: reviews overnight orders, checks inventory levels, reviews driver availability
- Throughout day: monitors order queue, handles exceptions, coordinates with drivers
- End of day: reviews completion rates, flags issues, prepares summary
- Escalates to Super Admin only for pricing changes, major policy decisions, or system issues

### Key Scenarios
- **Morning review:** Logs into admin dashboard → sees 12 pending orders, 2 low-inventory alerts, 1 driver unavailable → starts processing
- **Manual assignment:** Auto-offer timed out for a large delivery → reviews available drivers with compatible vehicles → manually assigns → driver receives notification
- **Exception handling:** Delivery failed (customer unavailable) → reviews driver's GPS confirmation of arrival → contacts customer → reschedules delivery → updates status
- **Inventory alert:** Source A below 20% capacity → creates purchase order (external) → records incoming RECEIVED transaction when water arrives → balance updates
- **End-of-day report:** Views dashboard → 45/47 deliveries completed (95.7%) → 2 failed (1 customer unavailable, 1 vehicle issue) → exports daily summary

### Relevant Modules
Admin Operations (cross-cutting), Orders, Deliveries, Inventory, Drivers, Vehicles, Notifications, Reporting, Audit

---

## P5 — Vikram Mehta (Super Admin / Business Owner)

### Demographics
- **Age:** 35–55
- **Location:** Urban India
- **Tech comfort:** High — runs a technology-forward business
- **Device:** Desktop/laptop (primary), smartphone (monitoring)

### Role
Business owner and platform administrator with full system access. Responsible for business strategy, pricing, catalog configuration, and overall platform governance.

### Goals
1. Grow revenue by expanding the water catalog and optimizing pricing
2. Maintain full visibility into all business operations
3. Ensure system integrity — accurate inventory, proper audit trails, RBAC enforcement
4. Scale operations (new areas, new water types, more drivers) without system changes
5. Make data-driven decisions using reports and analytics

### Pain Points
1. Currently has no real-time visibility into business performance — relies on end-of-day summaries
2. Changing pricing requires manually updating rate cards and informing all staff
3. No audit trail — can't trace who did what or when
4. Adding a new water type requires calling the app developer — not self-service
5. Financial reconciliation is manual — payment records don't match delivery records

### Behavior Patterns
- Reviews dashboard and key metrics 2–3 times daily
- Adjusts pricing quarterly (or when costs change)
- Adds new catalog items when expanding service offering (1–2 times per quarter)
- Reviews audit logs when investigating issues or complaints
- Monthly: deep dive into financial reports, customer retention, driver performance

### Key Scenarios
- **New water purpose:** Navigates to Catalog → adds "Swimming Pool" purpose with icon and description → adds quality types (Chlorinated, pH-Balanced) → creates variants for tanker delivery → sets pricing rules → activates → appears in customer app within 60 seconds
- **Pricing update:** Navigates to Pricing → selects "Construction" purpose → creates new tiered pricing rule (₹0.50/L for first 10,000L, ₹0.40/L for 10,001–50,000L) → sets activation date → existing orders keep old pricing → new orders use new pricing → audit log records the change
- **Business review:** Opens Reports → views monthly sales by purpose → sees Construction water grew 35% → views delivery performance → identifies driver with 92% completion rate (below 95% target) → reviews that driver's failed deliveries
- **Audit investigation:** Customer complaint about overcharging → opens Audit Log → searches by order ID → sees complete price computation (variant, quantity, coupon, delivery charge, tax) → verifies pricing rule version used → resolves complaint with evidence
- **Inventory reconciliation:** Monthly check → views Inventory → runs reconciliation for each source → ledger sum matches balance cache → one source shows 500L discrepancy → reviews adjustment history → finds unexplained loss → creates LOST_WASTAGE adjustment with documented reason

### Relevant Modules
All modules (full system access via Super Admin role)

---

## Persona-Module Matrix

| Module | P1 (Customer) | P2 (Business) | P3 (Driver) | P4 (Ops Mgr) | P5 (Super Admin) |
|--------|:---:|:---:|:---:|:---:|:---:|
| Auth & Identity | ✅ | ✅ | ✅ | ✅ | ✅ |
| User & Customer Mgmt | ✅ | ✅ | — | ✅ | ✅ |
| RBAC & Permissions | — | — | — | ✅ | ✅ |
| Address & Site Mgmt | ✅ | ✅ | — | ✅ | ✅ |
| Water Catalog | ✅ | ✅ | — | — | ✅ |
| Water Quality | ✅ (view) | ✅ (view) | — | ✅ | ✅ |
| Water Sources | — | — | — | ✅ | ✅ |
| Inventory | — | — | — | ✅ | ✅ |
| Pricing | ✅ (view) | ✅ (view) | — | — | ✅ |
| Coupons/Promotions | ✅ | ✅ | — | ✅ | ✅ |
| Orders | ✅ | ✅ | — | ✅ | ✅ |
| Deliveries (+ Dispatch) | ✅ (track) | ✅ (track) | ✅ | ✅ | ✅ |
| Driver Management | — | — | ✅ | ✅ | ✅ |
| Vehicle/Fleet | — | — | ✅ (view) | ✅ | ✅ |
| Payments | ✅ | ✅ | ✅ (earnings) | ✅ | ✅ |
| Refunds | ✅ (receive) | ✅ (receive) | — | ✅ | ✅ |
| Notifications | ✅ | ✅ | ✅ | ✅ | ✅ |
| Reviews/Ratings | ✅ | ✅ | ✅ (view) | ✅ | ✅ |
| Admin Ops (cross-cutting) | — | — | — | ✅ | ✅ |
| Reporting | — | — | — | ✅ | ✅ |
| Businesses/B2B | — | ✅ | — | ✅ | ✅ |
| Bulk Orders | — | ✅ | — | ✅ | ✅ |
| Recurring Orders | ✅ | ✅ | — | ✅ | ✅ |
| Invoices | — | ✅ | — | ✅ | ✅ |
| Audit/Compliance | — | — | — | ✅ | ✅ |
