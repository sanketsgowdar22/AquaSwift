# AquaSwift — Non-Functional Requirements

**Version:** 1.0
**Status:** Draft
**Last Updated:** 2026-09-03

---

> Non-functional requirements covering performance, scalability, availability, security, compliance, auditability, and data integrity. Each NFR has a unique ID (`NFR-<CAT>-<NNN>`), a phase tag, and a measurable target where PRD §8 provides one.

---

## 1. Performance (NFR-PERF)

---

NFR-PERF-001
[V1]
The system shall respond to all API requests with a P95 latency of less than 500ms under normal operational load.

Measurement: Application performance monitoring (APM) — P95 response time across all endpoints
Target: < 500ms (P95)
Source: PRD §8 (API response time P95 < 500ms)

---

NFR-PERF-002
[V1]
The system shall serve catalog browsing endpoints (GET /catalog/purposes, GET /catalog/variants) with a P95 latency of less than 300ms.

Measurement: APM — catalog endpoint P95 response time
Target: < 300ms (P95)
Source: PRD §5.1 (Browse dynamic water catalog), Sub-Phase 0B §5

---

NFR-PERF-003
[V1]
The system shall serve inventory availability checks with a P95 latency of less than 200ms.

Measurement: APM — inventory availability check P95 response time
Target: < 200ms (P95)
Source: Sub-Phase 0B §5, PRD §7.4 (real-time availability)

---

NFR-PERF-004
[V1]
The system shall complete the full order creation flow (validate → quote → create → reserve → payment intent) within 2 seconds under normal load.

Measurement: End-to-end order creation timing
Target: < 2 seconds
Source: PRD §8 (API response time), Master Prompt §10 Step 8

---

NFR-PERF-005
[V1]
The system shall render the admin dashboard summary within 3 seconds of login, including aggregated metrics.

Measurement: Dashboard load time
Target: < 3 seconds
Source: P4 scenario (morning review), PRD §5.1

---

NFR-PERF-006
[V1]
The system shall support the reorder flow completing in less than 60 seconds from app open to payment confirmation.

Measurement: End-to-end reorder flow timing
Target: < 60 seconds
Source: J2 ("Reorder flow completes in < 60 seconds")

---

NFR-PERF-007
[V1]
The system shall use short-TTL Redis caching (≤ 60 seconds) for catalog data to reduce database load while ensuring changes are visible within the cache TTL.

Measurement: Cache hit rate, staleness window
Target: ≤ 60 second cache TTL; > 90% cache hit rate for catalog reads
Source: Master Prompt §9 (Catalog), J7 Step 8

---

NFR-PERF-008
[V1]
The system shall process payment gateway webhooks within 5 seconds of receipt, ensuring timely order status transitions.

Measurement: Webhook processing time
Target: < 5 seconds from receipt to completion
Source: PRD §6.6, Master Prompt §10 Step 10

---

## 2. Scalability (NFR-SCALE)

---

NFR-SCALE-001
[V1]
The system shall handle a minimum of 100 concurrent order placements without degradation beyond the P95 latency target.

Measurement: Load testing with concurrent order creation requests
Target: 100 concurrent orders, P95 < 500ms
Source: PRD §3.2 (capture market), PRD §8

---

NFR-SCALE-002
[V1]
The system shall handle inventory reservation contention on a single source with proper locking (SELECT ... FOR UPDATE or equivalent), preventing overselling while minimizing lock contention.

Measurement: Concurrent reservation tests against same source — zero oversell, acceptable throughput
Target: Zero overselling; < 1% reservation failure rate under 50 concurrent requests
Source: Master Prompt §10 Step 17 (reservation race conditions), Sub-Phase 0B §5

---

NFR-SCALE-003
[V1]
The system shall support proper database indexing on high-query tables (orders, deliveries, inventory_transactions) to maintain performance as data grows.

Measurement: Query explain plans; no full table scans on indexed columns
Target: All list/search queries use appropriate indexes
Source: PRD §9.1 (Database performance at scale — "Proper indexing"), Master Prompt §6

---

NFR-SCALE-004
[V1]
The system shall support read replicas for reporting queries to prevent reporting workloads from degrading operational endpoint performance.

Measurement: Reporting queries routed to read replica; primary write latency unaffected
Target: Reporting queries on read replica
Source: PRD §9.1 ("read replicas for reporting queries")

---

NFR-SCALE-005
[PHASE 2]
The system shall support multi-city operations with area/zone-based partitioning of pricing, inventory, and dispatch rules without architectural changes.

Measurement: Multi-city configuration functional test
Target: New city added via configuration only
Source: PRD §5.2 (Phase 2 — Multi-city), PRODUCT_SCOPE.md

---

## 3. Availability (NFR-AVAIL)

---

NFR-AVAIL-001
[V1]
The system shall maintain 99.5% uptime for all customer-facing and driver-facing API endpoints, measured monthly.

Measurement: Uptime monitoring and alerting
Target: 99.5% monthly uptime
Source: PRD §8 (System uptime — 99.5%)

---

NFR-AVAIL-002
[V1]
The system shall degrade gracefully when the payment gateway is temporarily unavailable — queuing payment intents for retry and showing helpful error messages to customers, without blocking non-payment-related functionality.

Measurement: Payment gateway outage simulation; other endpoints continue to function
Target: Non-payment functionality unaffected during gateway downtime
Source: PRD §9.1 (Payment gateway downtime — "Queue failed payment intents for retry"), Sub-Phase 0B §5

---

NFR-AVAIL-003
[V1]
The system shall degrade gracefully when the maps API (Google Maps) is temporarily unavailable — allowing order placement with previously geocoded addresses and degrading gracefully for new address geocoding.

Measurement: Maps API outage simulation
Target: Orders to existing addresses unaffected; new address geocoding queued for retry
Source: Sub-Phase 0B §5, PRD §9.3 (Google Maps dependency)

---

NFR-AVAIL-004
[V1]
The system shall implement health check endpoints for monitoring system component availability (database, Redis, Celery, external services).

Measurement: Health check endpoint responses
Target: Health checks detect component failures within 30 seconds
Source: Master Prompt §10 Step 1 ("health check"), Master Prompt §10 Step 19

---

NFR-AVAIL-005
[V1]
The system shall implement monitoring and alerting for critical failure conditions: 5xx error rate, webhook processing failures, Celery task backlog, and inventory reconciliation mismatches.

Measurement: Alert trigger accuracy and response time
Target: Alerts fire within 5 minutes of threshold breach
Source: Master Prompt §10 Step 19 (monitoring/alarms), PRODUCT_SCOPE.md (Monitoring & alerting — MUST HAVE — V1)

---

## 4. Security (NFR-SEC)

---

NFR-SEC-001
[V1]
The system shall enforce RBAC permission checks on every protected API endpoint — no endpoint shall be accessible without proper authentication and authorization.

Measurement: Security audit — every endpoint has require_permission() or explicit public marker
Target: 100% endpoint coverage
Source: Master Prompt §10 Step 18 (RBAC audit across every endpoint), Sub-Phase 0B §5

---

NFR-SEC-002
[V1]
The system shall enforce rate limiting on authentication and OTP endpoints to prevent brute-force attacks.

Measurement: Rate limit testing — excessive requests are throttled
Target: OTP request: max 5/minute per number; OTP verify: max 10/minute per number
Source: Master Prompt §10 Step 18 (rate limiting on auth/OTP endpoints), Sub-Phase 0B §5

---

NFR-SEC-003
[V1]
The system shall never store card/payment instrument data — all payment data shall be handled through gateway-hosted fields only (no PCI scope expansion).

Measurement: Security audit — no card data in database, logs, or application memory
Target: Zero card data storage
Source: Sub-Phase 0B §5, Master Prompt §3 ("no PAN storage")

---

NFR-SEC-004
[V1]
The system shall encrypt all data in transit using TLS 1.2 or higher for all client-server and server-server communications.

Measurement: TLS configuration audit
Target: All endpoints accessible only via HTTPS; TLS 1.2+ enforced
Source: Sub-Phase 0B §5, security best practices

---

NFR-SEC-005
[V1]
The system shall manage all secrets (API keys, database credentials, JWT signing keys) via environment variables loaded through a typed settings module — no secrets in code, configuration files, or version control history.

Measurement: Secrets audit — no secrets in repository or commit history
Target: Zero secrets in codebase
Source: Master Prompt §10 Step 18 (secrets audit), Master Prompt §5 ("No secrets in code or repo"), PRODUCT_SCOPE.md (Environment configuration — MUST HAVE — V1)

---

NFR-SEC-006
[V1]
The system shall configure CORS with an explicit allow-list of permitted origins — no wildcard CORS in production.

Measurement: CORS header audit
Target: Only whitelisted origins allowed
Source: Master Prompt §10 Step 18 (CORS allow-list)

---

NFR-SEC-007
[V1]
The system shall perform a dependency vulnerability scan and remediate critical/high vulnerabilities before production deployment.

Measurement: Dependency scan results
Target: Zero critical/high vulnerabilities in production dependencies
Source: Master Prompt §10 Step 18 (dependency vulnerability scan)

---

NFR-SEC-008
[V1]
The system shall hash all passwords using a strong, adaptive hashing algorithm (e.g., bcrypt, Argon2) with appropriate work factors.

Measurement: Password storage audit
Target: All passwords hashed with bcrypt/Argon2; no plaintext or weak hashes
Source: Security best practices, PRD §5.1 (email+password auth)

---

NFR-SEC-009
[V1]
The system shall enforce that all mutating endpoints are wrapped in explicit database transactions with full rollback on any failure — no partial writes.

Measurement: Code review — all mutating endpoints use transaction context managers
Target: Zero partial-write scenarios
Source: Master Prompt §5 ("Every mutating endpoint wrapped in an explicit DB transaction")

---

## 5. Compliance (NFR-COMP)

---

NFR-COMP-001
[V1]
The system shall comply with India's DLT (Distributed Ledger Technology) requirements for commercial SMS, ensuring all SMS templates are registered with telecom operators via the SMS provider (MSG91).

Measurement: DLT registration audit; SMS delivery success rate
Target: 100% DLT-compliant SMS templates; > 95% SMS delivery rate
Source: Sub-Phase 0B §5, PRD §9.2 (DLT-compliant SMS), GLOSSARY.md (DLT)

---

NFR-COMP-002
[V1]
The system shall handle payment data exclusively through gateway-hosted fields (Razorpay checkout), never expanding PCI scope by processing or storing raw card data.

Measurement: PCI scope audit
Target: No PCI DSS scope expansion; all payment data handled by gateway
Source: Sub-Phase 0B §5, Master Prompt §3

---

NFR-COMP-003
[V1]
The system shall store all monetary values in INR (Indian Rupees) using integer paise or Decimal types — never floating-point.

Measurement: Code review — monetary field types
Target: All monetary fields use integer/Decimal types
Source: PRD §9.2 (Indian market — INR currency), Master Prompt §5

---

## 6. Auditability (NFR-AUD)

---

NFR-AUD-001
[V1]
The system shall log every admin mutation to catalog, pricing, and inventory as an immutable audit record with actor identity, timestamp, action, entity reference, and before/after state.

Measurement: Audit log coverage audit — all admin mutations produce audit rows
Target: 100% coverage of admin catalog/pricing/inventory mutations
Source: Sub-Phase 0B §5, RULE-019, Master Prompt §13

---

NFR-AUD-002
[V1]
The system shall ensure audit log records are immutable — no UPDATE or DELETE operations permitted on the audit_logs table.

Measurement: Database constraint audit; application code review
Target: Zero update/delete paths to audit_logs
Source: Sub-Phase 0B §5, RULE-019, GLOSSARY.md (Audit Log)

---

NFR-AUD-003
[V1]
The system shall provide the ability to reconstruct the complete history of any order, delivery, catalog item, or pricing rule through audit log and history table queries.

Measurement: Audit trail reconstruction test
Target: Complete history retrievable for any entity
Source: P5 scenario (audit investigation), PRODUCT_VISION.md ("Audit everything")

---

NFR-AUD-004
[V1]
The system shall resolve admin task escalations within 15 minutes for standard operational issues (as measured from alert generation to resolution action in audit log).

Measurement: Alert-to-resolution time from audit log
Target: < 15 minutes
Source: PRD §8 (Admin task resolution time < 15 min)

---

## 7. Data Integrity (NFR-DATA)

---

NFR-DATA-001
[V1]
The system shall maintain the inventory conservation law at all times: for every source, `available + reserved + allocated + delivered + lost_wastage = total_received`, verifiable by summing the inventory ledger.

Measurement: Automated reconciliation checks (Celery scheduled job)
Target: 100% reconciliation accuracy
Source: Sub-Phase 0B §5, PRD §7.4, PRD §8 (Inventory accuracy — 100%), RULE-013

---

NFR-DATA-002
[V1]
The system shall ensure commercial snapshot immutability — no catalog or pricing change shall alter any field of any existing order's order_items snapshot.

Measurement: Integration test — modify pricing after order creation; verify snapshot unchanged
Target: Zero historical order mutations from config changes
Source: Sub-Phase 0B §5, RULE-006, Master Prompt §13

---

NFR-DATA-003
[V1]
The system shall prevent inventory overselling through row-level locking during reservation, ensuring that concurrent orders cannot reserve more inventory than is available.

Measurement: Concurrent reservation load test — verify sum(reserved) ≤ available at all times
Target: Zero overselling incidents
Source: Master Prompt §10 Step 17, INV-018

---

NFR-DATA-004
[V1]
The system shall use UUIDs as primary keys for all entities to ensure globally unique identifiers.

Measurement: Schema review
Target: All tables use UUID primary keys
Source: Master Prompt §6 ("appropriate PKs (UUID)")

---

NFR-DATA-005
[V1]
The system shall store all timestamps as UTC, timezone-aware datetimes.

Measurement: Schema and code review
Target: All timestamp fields are timezone-aware UTC
Source: Master Prompt §5 ("All timestamps: UTC, timezone-aware datetimes")

---

NFR-DATA-006
[V1]
The system shall use foreign key constraints to maintain referential integrity across all entity relationships.

Measurement: Schema review — all relationships have FK constraints
Target: 100% FK coverage for documented relationships
Source: Master Prompt §6 ("appropriate FKs"), database best practices

---

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Performance (NFR-PERF) | 8 |
| Scalability (NFR-SCALE) | 5 |
| Availability (NFR-AVAIL) | 5 |
| Security (NFR-SEC) | 9 |
| Compliance (NFR-COMP) | 3 |
| Auditability (NFR-AUD) | 4 |
| Data Integrity (NFR-DATA) | 6 |
| **Total NFRs** | **40** |
| V1 NFRs | 39 |
| Phase 2 NFRs | 1 |
