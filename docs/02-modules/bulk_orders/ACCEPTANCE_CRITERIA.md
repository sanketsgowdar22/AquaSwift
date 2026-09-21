# Bulk Orders Module — Acceptance Criteria

## AC-BULK-001: Bulk Request Created

**User Story:** US-BULK-001
**Given** a business exists, **When** a bulk request is submitted with quantity, purpose, and schedule, **Then** the request is created in PENDING status.

---

## AC-BULK-002: Quote Created for Request

**User Story:** US-BULK-002
**Given** a PENDING bulk request, **When** admin creates a quote with negotiated pricing, **Then** the quote is created with valid_until date and request status → QUOTED.

---

## AC-BULK-003: Expired Quote Handled

**User Story:** US-BULK-003
**Given** a quote past its valid_until date, **When** the business attempts to accept, **Then** the system returns 400 with code `QUOTE_EXPIRED`.
