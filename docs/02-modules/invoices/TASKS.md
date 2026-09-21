# Invoices Module — Tasks

## T-INVC-001: Create Invoice Model & Schemas

**User Story:** All invoice stories
**Type:** Backend
**Description:** Create `invoices` model with invoice_number, business_id, billing period, subtotal, tax, total, status, due_date, pdf_url.
**Files:** `backend/app/invoices/models.py`, `backend/app/invoices/schemas.py`
**Dependencies:** T-BIZ-001, T-ORD-001
**Estimated Effort:** S

---

## T-INVC-002: Implement Invoice Generation Service

**User Story:** US-INVC-001, US-INVC-002
**Type:** Backend
**Description:** Implement invoice generation: aggregate business orders for billing period, compute totals, generate PDF, upload to S3, create invoice record.
**Files:** `backend/app/invoices/service.py`
**Dependencies:** T-INVC-001, S3 adapter
**Estimated Effort:** L

---

## T-INVC-003: Implement Invoice Admin Endpoints & Tests

**User Story:** All invoice stories
**Type:** Backend
**Description:** Admin: GET/POST/PATCH /admin/invoices. Tests for generation, PDF storage, status tracking.
**Files:** `backend/app/invoices/router.py`, `backend/app/invoices/tests/`
**Dependencies:** T-INVC-002
**Estimated Effort:** M
