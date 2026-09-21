# Reports Module — Acceptance Criteria

## AC-RPT-001: Sales Report Returns Aggregated Data

**User Story:** US-RPT-001
**Given** completed orders exist for September 2026,
**When** admin GET /admin/reports/sales?date_from=2026-09-01&date_to=2026-09-30,
**Then** the response includes total_revenue, total_volume_litres, order_count, and breakdown by purpose.

---

## AC-RPT-002: Inventory Report Shows Supply/Consumption

**User Story:** US-RPT-002
**Given** inventory transactions exist,
**When** admin GET /admin/reports/inventory,
**Then** the response shows total received, total delivered, current balances per source.

---

## AC-RPT-003: Delivery Report Shows Performance

**User Story:** US-RPT-003
**Given** completed deliveries exist,
**When** admin GET /admin/reports/deliveries,
**Then** the response includes avg completion time, success rate, delivery count by driver.

---

## AC-RPT-004: Reports Use Read Replica

**User Story:** US-RPT-005
**Given** a read replica is configured,
**When** any report query executes,
**Then** it runs against the read replica, not the primary database.
