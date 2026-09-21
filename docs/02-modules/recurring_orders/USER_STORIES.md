# Recurring Orders Module — User Stories

## US-REC-001: Customer Creates Recurring Order

**As a** customer (P1), **I want to** set up a recurring water delivery (e.g., weekly drinking water), **So that** I receive water automatically without re-ordering.
**SRS Requirements:** REC-001, REC-002, REC-003 **Priority:** MUST **Phase:** Phase 2

---

## US-REC-002: Recurring Order Instance Generation

**As a** system, **I want** the Celery beat job to generate individual orders from recurring schedules, **So that** deliveries happen on schedule without manual intervention.
**SRS Requirements:** REC-004, REC-005 **Priority:** MUST **Phase:** Phase 2

---

## US-REC-003: Customer Manages Recurring Orders

**As a** customer (P1), **I want to** pause, resume, or cancel my recurring order, **So that** I can adjust deliveries as needed.
**SRS Requirements:** REC-006, REC-007 **Priority:** MUST **Phase:** Phase 2
