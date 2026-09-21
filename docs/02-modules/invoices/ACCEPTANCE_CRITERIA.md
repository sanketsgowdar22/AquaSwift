# Invoices Module — Acceptance Criteria

## AC-INVC-001: Invoice Generated for Business

**User Story:** US-INVC-001
**Given** a business with delivered orders in September, **When** admin POST /admin/invoices for that billing period, **Then** an invoice is created with correct subtotal, tax, total, and invoice_number.

---

## AC-INVC-002: Invoice PDF Stored in S3

**User Story:** US-INVC-002
**Given** an invoice is generated, **When** the PDF is created, **Then** it is uploaded to S3 and the pdf_url is stored on the invoice record.

---

## AC-INVC-003: Overdue Invoice Detection

**User Story:** US-INVC-003
**Given** a PENDING invoice past its due_date, **When** the status is checked, **Then** it transitions to OVERDUE.
