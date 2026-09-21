# AquaSwift — Traceability Matrix

**Version:** 2.0
**Status:** Draft (0D columns filled — Implementation/Test columns pending)
**Last Updated:** 2026-09-04

---

> This matrix provides bidirectional traceability from PRD sections to SRS requirements, user stories, tasks, and acceptance criteria. Columns marked `(pending)` will be filled during Section 10's implementation steps.

---

## Authentication & Identity (AUTH)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §5.1 (OTP-based registration/login) | AUTH-001 | US-AUTH-001 | T-AUTH-003 | (pending) | (pending) | AC-AUTH-001 |
| PRD §5.1, GLOSSARY (OTP Login) | AUTH-002 | US-AUTH-001 | T-AUTH-003 | (pending) | (pending) | AC-AUTH-001 |
| PRD §5.1, J1 Step 3 | AUTH-003 | US-AUTH-001 | T-AUTH-004 | (pending) | (pending) | AC-AUTH-002 |
| GLOSSARY (OTP Login — configurable expiry) | AUTH-004 | US-AUTH-001 | T-AUTH-003 | (pending) | (pending) | AC-AUTH-003 |
| PRD §5.1 (Email+password login) | AUTH-005 | US-AUTH-002 | T-AUTH-005 | (pending) | (pending) | AC-AUTH-007 |
| GLOSSARY (JWT, Refresh Token) | AUTH-006 | US-AUTH-003 | T-AUTH-006 | (pending) | (pending) | AC-AUTH-009 |
| GLOSSARY (Refresh Token — invalidation) | AUTH-007 | US-AUTH-003 | T-AUTH-006 | (pending) | (pending) | AC-AUTH-010, AC-AUTH-011 |
| J1 Step 3 (creates user) | AUTH-008 | US-AUTH-001 | T-AUTH-004 | (pending) | (pending) | AC-AUTH-005 |
| Master Prompt §10 Step 18 | AUTH-009 | US-AUTH-004 | T-AUTH-008 | (pending) | (pending) | AC-AUTH-012, AC-AUTH-013 |
| PRD §9.1 (SMS/OTP failure) | AUTH-010 | US-AUTH-005 | T-AUTH-009 | (pending) | (pending) | AC-AUTH-014 |

---

## RBAC & Permissions (RBAC)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| Master Prompt §1 Rule 5, PRD §5.1 | RBAC-001 | US-RBAC-001 | T-RBAC-003 | (pending) | (pending) | AC-RBAC-001, AC-RBAC-002 |
| GLOSSARY (Role), PRD §4.1–4.5 | RBAC-002 | US-RBAC-002 | T-RBAC-001 | (pending) | (pending) | AC-RBAC-003 |
| GLOSSARY (Permission), Master Prompt §7 | RBAC-003 | US-RBAC-001 | T-RBAC-002 | (pending) | (pending) | AC-RBAC-001 |
| Master Prompt §10 Step 4 | RBAC-004 | US-RBAC-001 | T-RBAC-003 | (pending) | (pending) | AC-RBAC-008 |
| PRD §5.1, Master Prompt §13 | RBAC-005 | US-RBAC-001 | T-RBAC-003 | (pending) | (pending) | AC-RBAC-004 |
| PRD §5.1, Master Prompt §13 | RBAC-006 | US-RBAC-001 | T-RBAC-003 | (pending) | (pending) | AC-RBAC-003 |
| Sub-Phase 0B §0 Correction 2, P2 | RBAC-007 | US-RBAC-004 | T-RBAC-005 | (pending) | (pending) | — (Phase 2) |
| PRD §5.1 (role assignment) | RBAC-008 | US-RBAC-003 | T-RBAC-004 | (pending) | (pending) | AC-RBAC-005, AC-RBAC-006 |

---

## User & Customer Management (USR)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §4.1, J1 Step 3 | USR-001 | US-USR-001 | T-USR-003 | (pending) | (pending) | AC-USR-001, AC-USR-002 |
| PRD §4.3, Master Prompt §10 Step 20 | USR-002 | US-USR-002 | T-USR-003 | (pending) | (pending) | AC-USR-003 |
| PRD §5.3 (customer management) | USR-003 | US-USR-003 | T-USR-004 | (pending) | (pending) | AC-USR-004 |
| PRD §5.3, Master Prompt §10 Step 7 | USR-004 | US-USR-003 | T-USR-004 | (pending) | (pending) | AC-USR-005 |
| PRD §4.1 (profile updates) | USR-005 | US-USR-001 | T-USR-003 | (pending) | (pending) | AC-USR-002 |
| PRD §5.3, Master Prompt §10 Step 7 | USR-006 | US-USR-003 | T-USR-004 | (pending) | (pending) | AC-USR-006 |

---

## Address & Site Management (ADDR)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| J1 Step 4, PRD §5.2 | ADDR-001 | US-ADDR-001 | T-ADDR-003 | (pending) | (pending) | AC-ADDR-001 |
| J1 Step 4, PRD §5.2 | ADDR-002 | US-ADDR-001 | T-ADDR-003 | (pending) | (pending) | AC-ADDR-002, AC-ADDR-003 |
| J1 Step 5 | ADDR-003 | US-ADDR-002 | T-ADDR-003 | (pending) | (pending) | AC-ADDR-005 |
| PRD §5.2 (geocoding) | ADDR-004 | US-ADDR-001 | T-ADDR-003 | (pending) | (pending) | AC-ADDR-001, AC-ADDR-006 |
| PRD §5.3 | ADDR-005 | US-ADDR-003 | T-ADDR-004 | (pending) | (pending) | AC-ADDR-007 |
| PRD §4.2 (business sites) | ADDR-006 | US-ADDR-004 | T-ADDR-001 | (pending) | (pending) | — (Phase 2 UI) |
| PRD §4.2, §5.2 (site management) | ADDR-007 | US-ADDR-004 | T-ADDR-001 | (pending) | (pending) | — (Phase 2 UI) |

---

## Water Catalog (CAT)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §5.2 (water purposes) | CAT-001 | US-CAT-002 | T-CAT-004 | (pending) | (pending) | AC-CAT-004 |
| PRD §5.2 (quality types) | CAT-002 | US-CAT-003 | T-CAT-004 | (pending) | (pending) | AC-CAT-004 |
| PRD §5.2 (delivery methods) | CAT-003 | US-CAT-004 | T-CAT-004 | (pending) | (pending) | AC-CAT-004 |
| PRD §5.2 (purpose-quality links) | CAT-004 | US-CAT-005 | T-CAT-004 | (pending) | (pending) | AC-CAT-012 |
| PRD §5.2, Master Prompt §6 | CAT-005 | US-CAT-006 | T-CAT-006 | (pending) | (pending) | AC-CAT-006 |
| Master Prompt §1 Rule 2 | CAT-006 | US-CAT-006 | T-CAT-006 | (pending) | (pending) | AC-CAT-008 |
| Master Prompt §1 Rule 10 | CAT-007 | US-CAT-007 | T-CAT-005 | (pending) | (pending) | AC-CAT-005 |
| Master Prompt §1 Rule 10 | CAT-008 | US-CAT-007 | T-CAT-005 | (pending) | (pending) | AC-CAT-005 |
| J1 Step 4, PRD §5.2 | CAT-009 | US-CAT-001 | T-CAT-003 | (pending) | (pending) | AC-CAT-001, AC-CAT-002, AC-CAT-003 |
| Master Prompt §10 Step 6 | CAT-010 | US-CAT-002 | T-CAT-004 | (pending) | (pending) | AC-CAT-004 |
| Master Prompt §9 (Redis cache) | CAT-011 | US-CAT-008 | T-CAT-007 | (pending) | (pending) | AC-CAT-010, AC-CAT-011 |
| PRD §5.3 (admin catalog) | CAT-012 | US-CAT-005 | T-CAT-004 | (pending) | (pending) | AC-CAT-006, AC-CAT-007, AC-CAT-009 |

---

## Water Quality (QUAL)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §5.2, Master Prompt §6 | QUAL-001 | US-QUAL-002 | T-QUAL-003 | (pending) | (pending) | AC-QUAL-002 |
| PRD §5.3, Master Prompt §10 Step 8 | QUAL-002 | US-QUAL-002 | T-QUAL-003 | (pending) | (pending) | AC-QUAL-003, AC-QUAL-004 |
| PRD §5.2 (customer views quality) | QUAL-003 | US-QUAL-001 | T-QUAL-004 | (pending) | (pending) | AC-QUAL-001 |
| PRD §5.3 (admin quality management) | QUAL-004 | US-QUAL-002 | T-QUAL-003 | (pending) | (pending) | AC-QUAL-002 |

---

## Water Sources (SRC)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| Master Prompt §6, §10 Step 9 | SRC-001 | US-SRC-001 | T-SRC-002 | (pending) | (pending) | AC-SRC-001 |
| PRD §5.3 | SRC-002 | US-SRC-001 | T-SRC-002 | (pending) | (pending) | AC-SRC-001 |
| Master Prompt §6 (capacity) | SRC-003 | US-SRC-002 | T-SRC-001 | (pending) | (pending) | AC-SRC-002 |
| PRD §5.3, Master Prompt §10 | SRC-004 | US-SRC-002 | T-SRC-002 | (pending) | (pending) | AC-SRC-003, AC-SRC-004 |

---

## Inventory (INV)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| Master Prompt §1 Rule 4, §6 | INV-001 | US-INV-001 | T-INV-003 | (pending) | (pending) | AC-INV-001 |
| Master Prompt §6 (balances) | INV-002 | US-INV-008 | T-INV-011 | (pending) | (pending) | AC-INV-015 |
| Master Prompt §1 Rule 4 | INV-003 | US-INV-001 | T-INV-001 | (pending) | (pending) | AC-INV-011 |
| J1 Step 7, Master Prompt §8 | INV-004 | US-INV-002 | T-INV-004 | (pending) | (pending) | AC-INV-002 |
| J1 Step 7 (availability check) | INV-005 | US-INV-002 | T-INV-004 | (pending) | (pending) | AC-INV-003 |
| Master Prompt §8 (RESERVE) | INV-006 | US-INV-002 | T-INV-004 | (pending) | (pending) | AC-INV-002 |
| Master Prompt §8 (ALLOCATE) | INV-007 | US-INV-003 | T-INV-005 | (pending) | (pending) | AC-INV-005 |
| Master Prompt §8 (RELEASE) | INV-008 | US-INV-004 | T-INV-006 | (pending) | (pending) | AC-INV-006 |
| Master Prompt §8 (DELIVER) | INV-009 | US-INV-005 | T-INV-007 | (pending) | (pending) | AC-INV-007 |
| PRD §5.3 (manual adjustment) | INV-010 | US-INV-006 | T-INV-008 | (pending) | (pending) | AC-INV-008, AC-INV-009 |
| PRD §5.3 (mandatory reason) | INV-011 | US-INV-006 | T-INV-008 | (pending) | (pending) | AC-INV-008 |
| PRD §5.3 (loss/wastage) | INV-012 | US-INV-007 | T-INV-008 | (pending) | (pending) | AC-INV-010 |
| PRD §5.3 (admin view) | INV-013 | US-INV-008 | T-INV-011 | (pending) | (pending) | AC-INV-015 |
| PRD §5.3 (ledger view) | INV-014 | US-INV-008 | T-INV-011 | (pending) | (pending) | AC-INV-015 |
| Master Prompt §8 (expiry) | INV-015 | US-INV-009 | T-INV-009 | (pending) | (pending) | AC-INV-012 |
| Master Prompt §9 (Celery beat) | INV-016 | US-INV-009 | T-INV-009 | (pending) | (pending) | AC-INV-012 |
| RULE-013 (conservation law) | INV-017 | US-INV-010 | T-INV-010 | (pending) | (pending) | AC-INV-013, AC-INV-014 |
| Master Prompt §6 (FOR UPDATE) | INV-018 | US-INV-011 | T-INV-004 | (pending) | (pending) | AC-INV-004 |

---

## Pricing (PRC)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| Master Prompt §1 Rule 3, J1 Step 6 | PRC-001 | US-PRC-001 | T-PRC-003 | (pending) | (pending) | AC-PRC-001 |
| Master Prompt §6 (version) | PRC-002 | US-PRC-002 | T-PRC-006 | (pending) | (pending) | AC-PRC-007, AC-PRC-008 |
| PRD §5.2, GLOSSARY (tiered) | PRC-003 | US-PRC-003 | T-PRC-003 | (pending) | (pending) | AC-PRC-003 |
| RULE-020 (stale cart) | PRC-004 | US-PRC-004 | T-PRC-005 | (pending) | (pending) | AC-PRC-005 |
| PRD §5.3 (admin pricing) | PRC-005 | US-PRC-005 | T-PRC-006 | (pending) | (pending) | AC-PRC-007 |
| PRD §5.3, Master Prompt §10 | PRC-006 | US-PRC-005 | T-PRC-006 | (pending) | (pending) | AC-PRC-004 |
| PRD §5.3 (date activation) | PRC-007 | US-PRC-005 | T-PRC-006 | (pending) | (pending) | AC-PRC-004 |
| Master Prompt §6 (delivery pricing) | PRC-008 | US-PRC-006 | T-PRC-003 | (pending) | (pending) | AC-PRC-006 |
| PRD §5.2 (distance-based) | PRC-009 | US-PRC-006 | T-PRC-003 | (pending) | (pending) | AC-PRC-006 |
| PRD §4.2 (business pricing) | PRC-010 | US-PRC-007 | T-PRC-004 | (pending) | (pending) | AC-PRC-009 |
| PRD §4.2 (negotiated rates) | PRC-011 | US-PRC-007 | T-PRC-004 | (pending) | (pending) | AC-PRC-009 |

---

## Coupons / Promotions (CPN)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §5.2 (validate coupon) | CPN-001 | US-CPN-001 | T-CPN-003 | (pending) | (pending) | AC-CPN-001 |
| PRD §5.2, J1 Step 7 | CPN-002 | US-CPN-001 | T-CPN-003 | (pending) | (pending) | AC-CPN-002, AC-CPN-005 |
| Master Prompt §1 Rule 3 | CPN-003 | US-CPN-002 | T-CPN-004 | (pending) | (pending) | AC-CPN-006 |
| PRD §5.3 (usage limits) | CPN-004 | US-CPN-003 | T-CPN-005 | (pending) | (pending) | AC-CPN-003, AC-CPN-004 |
| PRD §5.3 (admin coupons) | CPN-005 | US-CPN-004 | T-CPN-006 | (pending) | (pending) | — |
| PRD §5.3 (configurable rules) | CPN-006 | US-CPN-004 | T-CPN-006 | (pending) | (pending) | — |

---

## Orders (ORD)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| J1 Step 5-8, PRD §5.2 | ORD-001 | US-ORD-001 | T-ORD-003 | (pending) | (pending) | AC-ORD-001 |
| Master Prompt §1 Rule 3 | ORD-002 | US-ORD-001 | T-ORD-003 | (pending) | (pending) | AC-ORD-001 |
| Master Prompt §1 Rule 1 | ORD-003 | US-ORD-001 | T-ORD-006 | (pending) | (pending) | AC-ORD-010, AC-ORD-011 |
| J1 Step 7 (reserve) | ORD-004 | US-ORD-001 | T-ORD-003 | (pending) | (pending) | AC-ORD-001 |
| J1 Step 8 (payment intent) | ORD-005 | US-ORD-001 | T-ORD-003 | (pending) | (pending) | AC-ORD-001 |
| RULE-016 (idempotency) | ORD-006 | US-ORD-002 | T-ORD-003 | (pending) | (pending) | AC-ORD-004 |
| PRD §5.2 (order list) | ORD-007 | US-ORD-003 | T-ORD-007 | (pending) | (pending) | AC-ORD-015 |
| Master Prompt §8 (state machine) | ORD-008 | US-ORD-005 | T-ORD-004 | (pending) | (pending) | AC-ORD-008, AC-ORD-009 |
| PRD §5.2 (tracking) | ORD-009 | US-ORD-003 | T-ORD-007 | (pending) | (pending) | AC-ORD-015 |
| PRD §5.2 (cancel) | ORD-010 | US-ORD-004 | T-ORD-005 | (pending) | (pending) | AC-ORD-005 |
| RULE-017 (cancel window) | ORD-011 | US-ORD-004 | T-ORD-005 | (pending) | (pending) | AC-ORD-006 |
| Master Prompt §1 Rule 8 | ORD-012 | US-ORD-005 | T-ORD-004 | (pending) | (pending) | AC-ORD-008 |
| Master Prompt §8 (transitions) | ORD-013 | US-ORD-005 | T-ORD-004 | (pending) | (pending) | AC-ORD-009 |
| Master Prompt §8 (side effects) | ORD-014 | US-ORD-005 | T-ORD-004 | (pending) | (pending) | AC-ORD-014 |
| J2 Step 3 (create delivery) | ORD-015 | US-ORD-006 | T-ORD-006 | (pending) | (pending) | AC-ORD-010 |
| Master Prompt §1 Rule 6 | ORD-016 | US-ORD-007 | T-ORD-003 | (pending) | (pending) | AC-ORD-002, AC-ORD-003 |
| Master Prompt §1 Rule 6 | ORD-017 | US-ORD-007 | T-ORD-003 | (pending) | (pending) | AC-ORD-003 |
| PRD §5.3 (admin orders) | ORD-018 | US-ORD-008 | T-ORD-009 | (pending) | (pending) | — |
| PRD §5.3 (admin filter) | ORD-019 | US-ORD-008 | T-ORD-009 | (pending) | (pending) | — |
| PRD §5.3 (admin cancel) | ORD-020 | US-ORD-008 | T-ORD-009 | (pending) | (pending) | AC-ORD-007 |
| PRD §5.2 (reorder) | ORD-021 | US-ORD-009 | T-ORD-008 | (pending) | (pending) | AC-ORD-012 |
| PRD §5.2 (scheduled) | ORD-022 | US-ORD-010 | T-ORD-003 | (pending) | (pending) | AC-ORD-013 |

---

## Deliveries (DEL)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| J2 Step 3-4, Master Prompt §8 | DEL-001 | US-DEL-001 | T-DEL-004 | (pending) | (pending) | AC-DEL-001 |
| Master Prompt §8 (auto-offer) | DEL-002 | US-DEL-001 | T-DEL-004 | (pending) | (pending) | AC-DEL-001 |
| Master Prompt §10 Step 16 | DEL-003 | US-DEL-001 | T-DEL-004 | (pending) | (pending) | AC-DEL-001 |
| J2 Step 4 (accept) | DEL-004 | US-DEL-002 | T-DEL-006 | (pending) | (pending) | AC-DEL-002 |
| J2 Step 4 (reject) | DEL-005 | US-DEL-002 | T-DEL-006 | (pending) | (pending) | AC-DEL-003 |
| Master Prompt §8 (timeout) | DEL-006 | US-DEL-002 | T-DEL-005 | (pending) | (pending) | AC-DEL-004, AC-DEL-005 |
| J2 Step 5 (start trip) | DEL-007 | US-DEL-003 | T-DEL-007 | (pending) | (pending) | AC-DEL-006 |
| J2 Step 6 (arrive) | DEL-008 | US-DEL-003 | T-DEL-007 | (pending) | (pending) | AC-DEL-007 |
| J2 Step 7 (OTP verify) | DEL-009 | US-DEL-003 | T-DEL-008 | (pending) | (pending) | AC-DEL-008 |
| J2 Step 7 (complete) | DEL-010 | US-DEL-003 | T-DEL-008 | (pending) | (pending) | AC-DEL-008 |
| PRD §5.2, J2 Step 7 (OTP proof) | DEL-011 | US-DEL-004 | T-DEL-008 | (pending) | (pending) | AC-DEL-008, AC-DEL-009 |
| PRD §5.2 (GPS proof) | DEL-012 | US-DEL-004 | T-DEL-008 | (pending) | (pending) | AC-DEL-008 |
| PRD §5.2 (photo proof) | DEL-013 | US-DEL-004 | T-DEL-008 | (pending) | (pending) | AC-DEL-016 |
| RULE-018 (partial delivery) | DEL-014 | US-DEL-005 | T-DEL-009 | (pending) | (pending) | AC-DEL-010 |
| RULE-018 (remainder delivery) | DEL-015 | US-DEL-005 | T-DEL-009 | (pending) | (pending) | AC-DEL-010 |
| PRD §5.2 (failed delivery) | DEL-016 | US-DEL-006 | T-DEL-010 | (pending) | (pending) | AC-DEL-011 |
| RULE-022 (driver escalation) | DEL-017 | US-DEL-006 | T-DEL-010 | (pending) | (pending) | AC-DEL-011 |
| J1 Step 9 (customer tracking) | DEL-018 | US-DEL-007 | T-DEL-012 | (pending) | (pending) | AC-DEL-015 |
| PRD §5.3 (admin deliveries) | DEL-019 | US-DEL-008 | T-DEL-011 | (pending) | (pending) | AC-DEL-012 |
| PRD §5.3 (manual assign) | DEL-020 | US-DEL-008 | T-DEL-011 | (pending) | (pending) | AC-DEL-012 |
| PRD §5.3 (reassign) | DEL-021 | US-DEL-008 | T-DEL-011 | (pending) | (pending) | AC-DEL-013 |
| Master Prompt §8 (event log) | DEL-022 | US-DEL-009 | T-DEL-003 | (pending) | (pending) | AC-DEL-014 |

---

## Driver Management (DRV)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §4.3, J2 Step 1 | DRV-001 | US-DRV-001 | T-DRV-002 | (pending) | (pending) | AC-DRV-001 |
| PRD §4.3 (availability) | DRV-002 | US-DRV-001 | T-DRV-002 | (pending) | (pending) | AC-DRV-002 |
| PRD §4.3 (delivery history) | DRV-003 | US-DRV-002 | T-DRV-003 | (pending) | (pending) | AC-DRV-003 |
| PRD §4.3 (earnings) | DRV-004 | US-DRV-003 | T-DRV-004 | (pending) | (pending) | AC-DRV-004 |
| PRD §5.3 (admin driver mgmt) | DRV-005 | US-DRV-004 | T-DRV-005 | (pending) | (pending) | AC-DRV-005 |
| PRD §5.3 (driver profile) | DRV-006 | US-DRV-004 | T-DRV-005 | (pending) | (pending) | AC-DRV-005 |
| PRD §5.3 (deactivate) | DRV-007 | US-DRV-004 | T-DRV-005 | (pending) | (pending) | AC-DRV-006 |

---

## Vehicle / Fleet Management (VEH)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| Master Prompt §6, §10 Step 15 | VEH-001 | US-VEH-001 | T-VEH-002 | (pending) | (pending) | AC-VEH-001 |
| Master Prompt §6 (capacity) | VEH-002 | US-VEH-001 | T-VEH-001 | (pending) | (pending) | AC-VEH-004 |
| PRD §5.3 (fleet mgmt) | VEH-003 | US-VEH-001 | T-VEH-002 | (pending) | (pending) | AC-VEH-002 |
| PRD §5.3 (assign driver) | VEH-004 | US-VEH-002 | T-VEH-002 | (pending) | (pending) | AC-VEH-003 |
| PRD §5.3 (reassign driver) | VEH-005 | US-VEH-002 | T-VEH-002 | (pending) | (pending) | AC-VEH-003 |

---

## Payments (PAY)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| J1 Step 8, Master Prompt §1 Rule 9 | PAY-001 | US-PAY-001 | T-PAY-003 | (pending) | (pending) | AC-PAY-001 |
| Master Prompt §3 (Razorpay) | PAY-002 | US-PAY-001 | T-PAY-003 | (pending) | (pending) | AC-PAY-005 |
| Master Prompt §1 Rule 9 (webhook) | PAY-003 | US-PAY-002 | T-PAY-004 | (pending) | (pending) | AC-PAY-002 |
| Master Prompt §1 Rule 9 (signature) | PAY-004 | US-PAY-002 | T-PAY-004 | (pending) | (pending) | AC-PAY-003 |
| RULE-009 (webhook only) | PAY-005 | US-PAY-002 | T-PAY-004 | (pending) | (pending) | AC-PAY-004 |
| PRD §5.2 (retry payment) | PAY-006 | US-PAY-003 | T-PAY-005 | (pending) | (pending) | AC-PAY-006 |
| Master Prompt §6 (raw payload) | PAY-007 | US-PAY-004 | T-PAY-004 | (pending) | (pending) | AC-PAY-008 |
| RULE-019 (audit trail) | PAY-008 | US-PAY-004 | T-PAY-004 | (pending) | (pending) | AC-PAY-008 |
| PRD §5.3 (admin payments) | PAY-009 | US-PAY-005 | T-PAY-006 | (pending) | (pending) | AC-PAY-007 |
| PRD §5.3 (payment detail) | PAY-010 | US-PAY-005 | T-PAY-006 | (pending) | (pending) | AC-PAY-007 |

---

## Refunds (RFD)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §5.2 (auto-refund) | RFD-001 | US-RFD-001 | T-RFD-002 | (pending) | (pending) | AC-RFD-001 |
| PRD §5.2 (cancel → refund) | RFD-002 | US-RFD-001 | T-RFD-002 | (pending) | (pending) | AC-RFD-002 |
| PRD §5.3 (manual refund) | RFD-003 | US-RFD-002 | T-RFD-003 | (pending) | (pending) | AC-RFD-003 |
| PRD §5.3 (mandatory reason) | RFD-004 | US-RFD-002 | T-RFD-003 | (pending) | (pending) | AC-RFD-003 |
| Master Prompt §8 (refund webhook) | RFD-005 | US-RFD-003 | T-RFD-004 | (pending) | (pending) | AC-RFD-004 |
| PRD §5.3 (refund status) | RFD-006 | US-RFD-003 | T-RFD-004 | (pending) | (pending) | AC-RFD-005 |

---

## Notifications (NTF)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §5.2 (lifecycle events) | NTF-001 | US-NTF-001 | T-NTF-002 | (pending) | (pending) | AC-NTF-001 |
| Master Prompt §9 (channel-agnostic) | NTF-002 | US-NTF-001 | T-NTF-002 | (pending) | (pending) | AC-NTF-001 |
| PRD §5.2 (customer notifications) | NTF-003 | US-NTF-001 | T-NTF-002 | (pending) | (pending) | AC-NTF-001 |
| Master Prompt §3 (Push/SMS/Email) | NTF-004 | US-NTF-002 | T-NTF-002 | (pending) | (pending) | AC-NTF-001 |
| PRD §9.1 (channel selection) | NTF-005 | US-NTF-002 | T-NTF-006 | (pending) | (pending) | AC-NTF-006 |
| RULE-021 (notification resilience) | NTF-006 | US-NTF-003 | T-NTF-003 | (pending) | (pending) | AC-NTF-002, AC-NTF-003 |
| PRD §5.2 (device registration) | NTF-007 | US-NTF-004 | T-NTF-004 | (pending) | (pending) | AC-NTF-004 |
| PRD §5.2 (notification list) | NTF-008 | US-NTF-005 | T-NTF-005 | (pending) | (pending) | AC-NTF-005 |
| NFR-COMP-001 (DLT) | NTF-009 | US-NTF-006 | T-NTF-006 | (pending) | (pending) | AC-NTF-006 |

---

## Reviews / Ratings (REV)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §5.2 (submit review) | REV-001 | US-REV-001 | T-REV-002 | (pending) | (pending) | AC-REV-001, AC-REV-002 |
| PRD §5.2 (one per order) | REV-002 | US-REV-001 | T-REV-002 | (pending) | (pending) | AC-REV-003, AC-REV-004 |
| PRD §4.3 (driver views) | REV-003 | US-REV-002 | T-REV-003 | (pending) | (pending) | — |
| PRD §5.3 (admin reviews) | REV-004 | US-REV-003 | T-REV-003 | (pending) | (pending) | — |

---

## Admin Operations (ADM)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §5.3 (dashboard) | ADM-001 | US-ADM-001 | T-ADM-001 | (pending) | (pending) | AC-ADM-001 |
| PRD §5.3 (alerts) | ADM-002 | US-ADM-001 | T-ADM-001 | (pending) | (pending) | AC-ADM-001 |
| PRD §5.1 (role management) | ADM-003 | US-ADM-002 | T-ADM-002 | (pending) | (pending) | AC-ADM-003 |
| PRD §5.3 (catalog config) | ADM-004 | US-ADM-003 | T-CAT-004 | (pending) | (pending) | AC-CAT-004 |
| PRD §5.3 (pricing config) | ADM-005 | US-ADM-003 | T-PRC-006 | (pending) | (pending) | AC-PRC-007 |

---

## Reporting (RPT)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §5.3 (sales report) | RPT-001 | US-RPT-001 | T-RPT-001 | (pending) | (pending) | AC-RPT-001 |
| PRD §5.3 (inventory report) | RPT-002 | US-RPT-002 | T-RPT-002 | (pending) | (pending) | AC-RPT-002 |
| PRD §5.3 (delivery report) | RPT-003 | US-RPT-003 | T-RPT-002 | (pending) | (pending) | AC-RPT-003 |
| PRD §5.3 (customer report) | RPT-004 | US-RPT-004 | T-RPT-001 | (pending) | (pending) | — |
| Master Prompt §9 (scheduled) | RPT-005 | US-RPT-005 | T-RPT-003 | (pending) | (pending) | AC-RPT-004 |

---

## Analytics (ANL)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §5.3 (order trends) | ANL-001 | US-ANL-001 | T-ANL-001 | (pending) | (pending) | AC-ANL-002 |
| PRD §5.3 (customer retention) | ANL-002 | US-ANL-002 | T-ANL-001 | (pending) | (pending) | — (Phase 2) |
| PRD §5.3 (delivery efficiency) | ANL-003 | US-ANL-003 | T-ANL-001 | (pending) | (pending) | — (Phase 2) |
| PRD §5.3 (inventory forecast) | ANL-004 | US-ANL-004 | T-ANL-001 | (pending) | (pending) | — (Phase 2) |
| PRD §5.3 (revenue analytics) | ANL-005 | US-ANL-005 | T-ANL-001 | (pending) | (pending) | — (Phase 2) |

---

## Businesses / B2B (BIZ)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §4.2 (business account) | BIZ-001 | US-BIZ-001 | T-BIZ-002 | (pending) | (pending) | AC-BIZ-001 |
| PRD §4.2 (registration) | BIZ-002 | US-BIZ-001 | T-BIZ-001 | (pending) | (pending) | AC-BIZ-001 |
| Sub-Phase 0B §0 Correction 2 | BIZ-003 | US-BIZ-002 | T-BIZ-002 | (pending) | (pending) | AC-BIZ-002 |
| PRD §4.2 (employee invite) | BIZ-004 | US-BIZ-002 | T-BIZ-002 | (pending) | (pending) | AC-BIZ-002 |
| PRD §4.2 (sites) | BIZ-005 | US-BIZ-003 | T-BIZ-002 | (pending) | (pending) | AC-BIZ-003 |
| PRD §4.2 (site management) | BIZ-006 | US-BIZ-003 | T-BIZ-002 | (pending) | (pending) | AC-BIZ-003 |
| PRD §4.2 (business dashboard) | BIZ-007 | US-BIZ-004 | T-BIZ-002 | (pending) | (pending) | — (Phase 2) |

---

## Bulk Orders (BULK)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §4.2 (bulk request) | BULK-001 | US-BULK-001 | T-BULK-001 | (pending) | (pending) | AC-BULK-001 |
| PRD §4.2, §5.2 (bulk form) | BULK-002 | US-BULK-001 | T-BULK-001 | (pending) | (pending) | AC-BULK-001 |
| PRD §5.3 (admin quote) | BULK-003 | US-BULK-002 | T-BULK-002 | (pending) | (pending) | AC-BULK-002 |
| PRD §5.3 (negotiated pricing) | BULK-004 | US-BULK-002 | T-BULK-002 | (pending) | (pending) | AC-BULK-002 |
| PRD §4.2 (accept quote) | BULK-005 | US-BULK-003 | T-BULK-002 | (pending) | (pending) | AC-BULK-003 |
| PRD §4.2 (auto-generate) | BULK-006 | US-BULK-004 | T-BULK-002 | (pending) | (pending) | — (Phase 2) |
| PRD §5.3 (bulk management) | BULK-007 | US-BULK-004 | T-BULK-002 | (pending) | (pending) | — (Phase 2) |

---

## Recurring Orders (REC)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §5.2 (set up recurring) | REC-001 | US-REC-001 | T-REC-002 | (pending) | (pending) | AC-REC-001 |
| PRD §5.2 (frequency/schedule) | REC-002 | US-REC-001 | T-REC-002 | (pending) | (pending) | AC-REC-001 |
| Sub-Phase 0B §0 Correction 1 (P1 recurring) | REC-003 | US-REC-001 | T-REC-002 | (pending) | (pending) | AC-REC-001 |
| Master Prompt §9 (Celery beat) | REC-004 | US-REC-002 | T-REC-003 | (pending) | (pending) | AC-REC-002 |
| PRD §5.2 (instance generation) | REC-005 | US-REC-002 | T-REC-003 | (pending) | (pending) | AC-REC-002 |
| PRD §5.2 (pause/resume) | REC-006 | US-REC-003 | T-REC-002 | (pending) | (pending) | AC-REC-003 |
| PRD §5.2 (cancel recurring) | REC-007 | US-REC-003 | T-REC-002 | (pending) | (pending) | AC-REC-004 |

---

## Invoices (INVC)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §4.2 (invoice generation) | INVC-001 | US-INVC-001 | T-INVC-002 | (pending) | (pending) | AC-INVC-001 |
| PRD §5.3 (billing period) | INVC-002 | US-INVC-001 | T-INVC-002 | (pending) | (pending) | AC-INVC-001 |
| PRD §5.3 (PDF generation) | INVC-003 | US-INVC-002 | T-INVC-002 | (pending) | (pending) | AC-INVC-002 |
| PRD §5.3 (invoice status) | INVC-004 | US-INVC-003 | T-INVC-003 | (pending) | (pending) | AC-INVC-003 |
| PRD §5.3 (overdue tracking) | INVC-005 | US-INVC-003 | T-INVC-003 | (pending) | (pending) | AC-INVC-003 |

---

## Routes (RTE)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| PRD §5.3 (route optimization) | RTE-001 | US-RTE-001 | T-RTE-001 | (pending) | (pending) | AC-RTE-001 |
| PRD §9.1 (optimization algo) | RTE-002 | US-RTE-001 | T-RTE-002 | (pending) | (pending) | AC-RTE-002 |
| PRD §4.3 (driver route view) | RTE-003 | US-RTE-002 | T-RTE-002 | (pending) | (pending) | AC-RTE-002 |
| PRD §5.3 (route management) | RTE-004 | US-RTE-002 | T-RTE-002 | (pending) | (pending) | AC-RTE-002 |

---

## Audit / Compliance (AUD)

| PRD Reference | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|---------------|--------|------------|------|----------------|------|---------------------|
| Master Prompt §1 Rule 10, RULE-019 | AUD-001 | US-AUD-001 | T-AUD-002 | (pending) | (pending) | AC-AUD-001 |
| Master Prompt §6 (audit_logs) | AUD-002 | US-AUD-001 | T-AUD-001 | (pending) | (pending) | AC-AUD-001 |
| Master Prompt §6 (before/after) | AUD-003 | US-AUD-001 | T-AUD-002 | (pending) | (pending) | AC-AUD-005 |
| PRD §5.3 (entity history) | AUD-004 | US-AUD-002 | T-AUD-003 | (pending) | (pending) | AC-AUD-003 |
| PRD §5.3 (audit trail view) | AUD-005 | US-AUD-002 | T-AUD-003 | (pending) | (pending) | AC-AUD-003 |
| RULE-019 (append-only) | AUD-006 | US-AUD-003 | T-AUD-001 | (pending) | (pending) | AC-AUD-002 |
| PRD §5.3 (audit search) | AUD-007 | US-AUD-004 | T-AUD-004 | (pending) | (pending) | AC-AUD-004 |

---

## Non-Functional Requirements (NFR)

| Category | SRS ID | User Story | Task | Implementation | Test | Acceptance Criteria |
|----------|--------|------------|------|----------------|------|---------------------|
| Performance | NFR-PERF-001 through NFR-PERF-008 | — | Infrastructure | (pending) | (pending) | Load test |
| Scalability | NFR-SCALE-001 through NFR-SCALE-005 | — | Infrastructure | (pending) | (pending) | Stress test |
| Availability | NFR-AVAIL-001 through NFR-AVAIL-005 | — | Infrastructure | (pending) | (pending) | Uptime monitoring |
| Security | NFR-SEC-001 through NFR-SEC-009 | — | All modules | (pending) | (pending) | Security review |
| Compliance | NFR-COMP-001 through NFR-COMP-003 | — | Integration | (pending) | (pending) | Compliance audit |
| Auditability | NFR-AUD-001 through NFR-AUD-004 | US-AUD-001 | T-AUD-001, T-AUD-002 | (pending) | (pending) | AC-AUD-001 through AC-AUD-005 |
| Data Integrity | NFR-DATA-001 through NFR-DATA-006 | — | All modules | (pending) | (pending) | Integration test |
