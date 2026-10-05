# Phase 3 — Driver App

## 1. Phase Identity

- **Phase:** P3
- **Name:** Driver App
- **Status:** NOT STARTED
- **Depends On:** P2 (Customer App) substantially complete

## 2. Objective

Connect the existing Driver App UI to real backend APIs. Deliver a working driver journey from login through delivery assignment, navigation, completion, and earnings tracking.

## 3. Scope

### P3.1 — Driver Authentication
- Email/password login → JWT
- Session management
- Protected route guards
- **Tasks:** T-AUTH-005, T-AUTH-006, T-AUTH-007

### P3.2 — Driver Profile
- View/update driver profile
- Vehicle assignment display
- **Tasks:** T-DRV-001 through T-DRV-003

### P3.3 — Availability Toggle
- Set AVAILABLE / UNAVAILABLE status
- Backend status tracking
- **Tasks:** T-DRV-004

### P3.4 — Assignment Notifications
- Receive delivery offer via push notification
- View offer details (customer, address, quantity)
- **Tasks:** T-DEL-004, T-NTF-002

### P3.5 — Accept / Reject Delivery
- Accept delivery offer → ASSIGNED status
- Reject with reason → auto-reassign
- Offer timeout handling
- **Tasks:** T-DEL-005, T-DEL-006

### P3.6 — Navigation / Location
- Leaflet map with pickup → delivery route
- GPS location updates to backend
- **Tasks:** T-DEL-007

### P3.7 — Delivery Progress
- Start trip → STARTED status
- Arrive at customer → ARRIVED status
- Status updates to customer
- **Tasks:** T-DEL-007

### P3.8 — Delivery Completion
- Verify customer OTP
- Record delivered quantity
- Upload proof photo (optional)
- → DELIVERED status
- **Tasks:** T-DEL-008

### P3.9 — Partial & Failed Delivery
- Handle partial quantity delivery
- Handle delivery failure (retry/escalation)
- **Tasks:** T-DEL-009, T-DEL-010

### P3.10 — Earnings
- Daily/weekly/monthly earnings view
- Delivery history list
- **Tasks:** T-DRV-005, T-DRV-006

## 4. Out of Scope

- Customer app changes (Phase 2)
- Admin dashboard (Phase 5)
- Route optimization (Phase 5+)

## 5. Existing Implementation

### Backend
| Module | Status |
|--------|--------|
| drivers (models, router) | ✅ Partial (2 .py files) |
| deliveries (models, router, service, schemas) | ✅ Implemented |
| vehicles (models, router, service, schemas) | ✅ Implemented |

### Frontend
| Page | Route | Status |
|------|-------|--------|
| Dashboard | `/driver` | ✅ UI with mock delivery data |
| Earnings | `/driver/earnings` | ✅ UI with mock earnings data |
| Profile | `/driver/profile` | ⬜ Placeholder |

## 6. Existing Modules

deliveries (13 tasks), drivers (6 tasks), vehicles (4 tasks), notifications (7 tasks — shared)

## 7. Existing Tasks (Preserved)

30 tasks across the above modules. See `PHASE-MODULE-TASK-MATRIX.md`.

## 8. New Tasks

| Task | Description | Dependencies |
|------|------------|-------------|
| T-FE-DRV-001 | Wire Driver Dashboard to delivery API | T-DEL-004 |
| T-FE-DRV-002 | Wire Earnings page to driver earnings API | T-DRV-005 |
| T-FE-DRV-003 | Implement driver login flow | T-AUTH-005 |
| T-FE-DRV-004 | Implement delivery accept/reject UI | T-DEL-006 |
| T-FE-DRV-005 | Implement delivery completion UI (OTP + photo) | T-DEL-008 |

## 9. Entry Gate (Prerequisites)

Before starting Phase 3, verify:
- [ ] Customer authentication stable
- [ ] Order creation works end-to-end
- [ ] Order state machine defined and tested
- [ ] Delivery state machine defined and tested
- [ ] Driver assignment model implemented
- [ ] Cancellation rules defined
- [ ] Relevant backend APIs available and tested

## 18. Acceptance Criteria

- [ ] Driver can log in via email/password
- [ ] Driver can toggle availability
- [ ] Driver receives delivery assignments
- [ ] Driver can accept/reject deliveries
- [ ] Driver can navigate to customer (Leaflet)
- [ ] Driver can complete delivery with OTP verification
- [ ] Driver can view earnings summary
- [ ] Driver can view delivery history
- [ ] All mock data replaced with real API data
- [ ] Rate limiting applies to driver endpoints

## 22. Exit Criteria

The complete driver journey works end-to-end:
```
Login → Available → Assignment → Accept → Navigate → Deliver → OTP → Complete → Earnings
```

**Phase 3 must be substantially complete before Phase 4 begins.**
