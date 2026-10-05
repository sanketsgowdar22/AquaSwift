# Phase 4 — Customer + Driver Integration

## 1. Phase Identity

- **Phase:** P4
- **Name:** Customer + Driver Integration
- **Status:** NOT STARTED
- **Depends On:** P2 (Customer App) + P3 (Driver App) substantially complete

## 2. Objective

Validate the complete order→delivery lifecycle across Customer and Driver applications through the shared backend. Ensure state consistency, notification delivery, and error recovery.

## 3. Scope

### P4.1 — Order Lifecycle Validation
```
Customer Creates Order → Payment → Confirmed
→ Backend generates Delivery → PENDING_ASSIGNMENT
→ Auto-offer to Driver → Driver Accepts → ASSIGNED
→ Driver starts → STARTED → Customer notified
→ Driver arrives → ARRIVED → Customer notified
→ Driver delivers (OTP) → DELIVERED → Customer notified
→ All deliveries done → Order COMPLETED
→ Customer submits review
```

### P4.2 — Cancellation Flows
- Customer cancels before OUT_FOR_DELIVERY
- Admin cancels with reason
- Inventory release verification
- Refund initiation verification

### P4.3 — Assignment & Reassignment
- Auto-offer timeout → reassign to next driver
- Driver rejects → reassign
- Max attempts → escalate to admin
- Admin manual assign/reassign

### P4.4 — Notification Verification
- Customer receives order status updates
- Driver receives delivery assignments
- Push notification delivery (FCM)
- In-app notification state

### P4.5 — Error Recovery
- Payment failure → retry
- Driver unavailable → reassign
- Network failure → resume state
- Duplicate request → idempotency
- Invalid state transition → rejection

### P4.6 — State Consistency
- Order state machine validates all transitions
- Delivery state machine validates all transitions
- Parent order status derived from child deliveries
- Inventory transactions match delivery states

## 4. Existing Tasks (Preserved)

Integration tasks drawn from existing modules:
- T-ORD-004 (Order State Machine)
- T-ORD-005 (Order Cancellation)
- T-ORD-006 (Delivery Generation)
- T-DEL-003 (Delivery State Machine)
- T-DEL-004 (Auto-Offer Service)
- T-DEL-005 (Offer Timeout Handler)
- T-DEL-006 (Driver Response Handler)
- T-DEL-008 (Delivery Completion)
- T-DEL-009 (Partial Delivery)
- T-DEL-010 (Failed Delivery)
- T-INV-004 through T-INV-007 (Inventory transactions)

## 5. New Tasks

| Task | Description | Dependencies |
|------|------------|-------------|
| T-INT-001 | End-to-end order lifecycle test | T-ORD-004, T-DEL-003 |
| T-INT-002 | Cancellation + refund integration test | T-ORD-005, T-RFD |
| T-INT-003 | Assignment cascade test (offer→timeout→reassign) | T-DEL-004, T-DEL-005 |
| T-INT-004 | Notification delivery verification | T-NTF |
| T-INT-005 | State consistency audit | T-ORD-004, T-DEL-003, T-INV |

## 18. Acceptance Criteria

- [ ] Complete order→delivery lifecycle works end-to-end
- [ ] Customer sees real-time status updates
- [ ] Driver assignment and acceptance work
- [ ] Cancellation releases inventory and initiates refund
- [ ] Reassignment works on rejection/timeout
- [ ] Notifications delivered to both Customer and Driver
- [ ] State machines reject invalid transitions
- [ ] Inventory transactions are consistent
- [ ] Idempotency prevents duplicate orders

## 22. Exit Criteria

The full Customer→Backend→Driver lifecycle works reliably. All integration tests pass. Error scenarios handled gracefully.

**Phase 4 must be complete before Phase 5 (Admin Dashboard) becomes the primary focus.**
