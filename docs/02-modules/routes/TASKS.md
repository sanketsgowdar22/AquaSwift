# Routes Module — Tasks

## T-RTE-001: Define Route Optimization Interface

**User Story:** US-RTE-001
**Type:** Backend
**Description:** Define `RouteOptimizer` ABC with `optimize_route(deliveries, driver_location)` → ordered list. Stub implementation that returns deliveries in original order (no optimization).
**Files:** `backend/app/routes/service.py`
**Dependencies:** T-DEL-001, T-ADDR-001
**Estimated Effort:** S

---

## T-RTE-002: Implement Route Optimization (Phase 3)

**User Story:** US-RTE-002
**Type:** Backend
**Description:** Implement real route optimization using Google Directions API or OR-Tools for TSP solving.
**Files:** `backend/app/routes/service.py`
**Dependencies:** T-RTE-001, Google Maps adapter
**Estimated Effort:** XL
