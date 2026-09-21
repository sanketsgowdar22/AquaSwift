# Orders Module — Tasks

## T-ORD-001: Create Order & OrderItem Models

**User Story:** US-ORD-001, US-ORD-007
**Type:** Backend
**Description:** Create `orders` model (order_number, customer_id, address_id, order_type, status, total_quantity_litres, scheduled windows, coupon_id, idempotency_key), `order_items` model (immutable commercial snapshot), `order_status_history` model.
**Files:** `backend/app/orders/models.py`
**Dependencies:** T-AUTH-001, T-ADDR-001, T-CAT-001, T-CPN-001
**Estimated Effort:** M

---

## T-ORD-002: Create Order Schemas

**User Story:** All order stories
**Type:** Backend
**Description:** Create schemas: OrderCreateRequest, OrderResponse, OrderDetailResponse (with items, deliveries, payments), OrderListResponse, OrderCancelRequest, ReorderRequest.
**Files:** `backend/app/orders/schemas.py`
**Dependencies:** T-ORD-001
**Estimated Effort:** M

---

## T-ORD-003: Implement Order Creation Service

**User Story:** US-ORD-001, US-ORD-002, US-ORD-007
**Type:** Backend
**Description:** Implement `create_order(data, user)` — atomic transaction: (1) check idempotency key, (2) call PricingService.quote() for fresh price, (3) compare with client-expected price, (4) create order + order_items with frozen snapshot, (5) reserve inventory, (6) create payment intent, (7) set status PENDING_PAYMENT. Return order + payment details.
**Files:** `backend/app/orders/service.py`
**Dependencies:** T-PRC-003, T-INV-004, T-PAY-001
**Estimated Effort:** XL

---

## T-ORD-004: Implement Order State Machine

**User Story:** US-ORD-005
**Type:** Backend
**Description:** Implement `transition_order(db, order, new_status, actor, reason)` with ALLOWED_TRANSITIONS map, validation, history writing, and side-effect dispatch.
**Files:** `backend/app/orders/state_machine.py`
**Dependencies:** T-ORD-001
**Estimated Effort:** L

---

## T-ORD-005: Implement Order Cancellation

**User Story:** US-ORD-004
**Type:** Backend
**Description:** Implement customer cancel (pre-OUT_FOR_DELIVERY only) and admin cancel (any status, mandatory reason). Release inventory, cancel pending deliveries, initiate refund.
**Files:** `backend/app/orders/service.py`
**Dependencies:** T-ORD-004, T-INV-006, T-RFD
**Estimated Effort:** M

---

## T-ORD-006: Implement Delivery Generation

**User Story:** US-ORD-006
**Type:** Backend
**Description:** When order transitions CONFIRMED → PROCESSING, auto-create delivery record(s) in PENDING_ASSIGNMENT status. For orders with quantity > vehicle capacity, split into multiple deliveries.
**Files:** `backend/app/orders/service.py`
**Dependencies:** T-ORD-004, T-DEL models
**Estimated Effort:** M

---

## T-ORD-007: Implement Order Listing & Detail

**User Story:** US-ORD-003
**Type:** Backend
**Description:** Implement customer-facing: list_orders(user, filters, cursor), get_order_detail(id, user). Include items, deliveries, payments, status history. Scope customer to own orders.
**Files:** `backend/app/orders/service.py`
**Dependencies:** T-ORD-001
**Estimated Effort:** M

---

## T-ORD-008: Implement Reorder

**User Story:** US-ORD-009
**Type:** Backend
**Description:** Implement `reorder(order_id, user)` — pre-fill new order from previous: same variant, quantity, address. Validate variant still active, re-quote for current price.
**Files:** `backend/app/orders/service.py`
**Dependencies:** T-ORD-003
**Estimated Effort:** S

---

## T-ORD-009: Implement Admin Order Management

**User Story:** US-ORD-008
**Type:** Backend
**Description:** Admin list with filters (status, customer, date range), admin detail view, admin cancel with mandatory reason.
**Files:** `backend/app/orders/service.py`
**Dependencies:** T-ORD-004
**Estimated Effort:** M

---

## T-ORD-010: Create Order API Routes

**User Story:** All order stories
**Type:** Backend
**Description:** Customer: POST /orders/quote, POST /orders, GET /orders, GET /orders/{id}, POST /orders/{id}/cancel, POST /orders/{id}/reorder. Admin: GET /admin/orders, GET /admin/orders/{id}, POST /admin/orders/{id}/cancel.
**Files:** `backend/app/orders/router.py`
**Dependencies:** T-ORD-003 through T-ORD-009
**Estimated Effort:** M

---

## T-ORD-011: Implement Order Number Generation

**User Story:** US-ORD-001
**Type:** Backend
**Description:** Generate human-readable order numbers: `AQ-{YYYYMMDD}-{sequential}` (e.g., AQ-20260904-001). Ensure uniqueness via DB constraint.
**Files:** `backend/app/orders/service.py`
**Dependencies:** T-ORD-001
**Estimated Effort:** S

---

## T-ORD-012: Write Order Tests

**User Story:** All order stories
**Type:** Backend
**Description:** Test: creation happy path, idempotency, stale price rejection, state machine transitions (all valid + all invalid), cancellation (customer pre/post OUT_FOR_DELIVERY, admin), delivery generation, reorder, commercial snapshot immutability.
**Files:** `backend/app/orders/tests/`
**Dependencies:** T-ORD-010
**Estimated Effort:** XL
