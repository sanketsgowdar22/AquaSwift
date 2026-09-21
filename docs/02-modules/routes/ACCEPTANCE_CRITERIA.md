# Routes Module — Acceptance Criteria

## AC-RTE-001: Stub Returns Deliveries in Order

**User Story:** US-RTE-001
**Given** the stub route optimizer is active, **When** route optimization is called with a list of deliveries, **Then** deliveries are returned in their original order (pass-through).

---

## AC-RTE-002: Optimized Route Reduces Distance (Phase 3)

**User Story:** US-RTE-002
**Given** a driver has 5 deliveries at different locations, **When** route optimization runs, **Then** the returned order minimizes total driving distance compared to original order.
