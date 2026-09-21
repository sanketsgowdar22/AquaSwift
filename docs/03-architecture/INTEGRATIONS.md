# AquaSwift — External Integrations Architecture

**Version:** 1.0
**Status:** Draft
**Last Updated:** 2026-09-03

---

> All external integrations follow the **adapter pattern** — business logic depends on an abstract interface, and a concrete adapter implements the interface for a specific provider. Swapping providers requires only a new adapter class, with zero changes to call sites. See DEC-AUTH-001, DEC-PAY-001, DEC-NOTIFY-001.

---

## 1. Adapter Pattern Overview

```python
# Abstract interface (in core/)
class PaymentGatewayAdapter(ABC):
    @abstractmethod
    async def create_intent(self, amount: Decimal, currency: str, metadata: dict) -> PaymentIntent: ...
    
    @abstractmethod
    async def verify_webhook(self, payload: bytes, signature: str) -> WebhookEvent: ...
    
    @abstractmethod
    async def refund(self, gateway_payment_id: str, amount: Decimal) -> RefundResult: ...

# Concrete implementation (in integrations/)
class RazorpayAdapter(PaymentGatewayAdapter):
    def __init__(self, key_id: str, key_secret: str): ...
    async def create_intent(self, ...) -> PaymentIntent: ...
    async def verify_webhook(self, ...) -> WebhookEvent: ...
    async def refund(self, ...) -> RefundResult: ...

# Dependency injection (in core/dependencies.py)
def get_payment_gateway() -> PaymentGatewayAdapter:
    return RazorpayAdapter(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
```

```
backend/app/
├── integrations/
│   ├── __init__.py
│   ├── payment/
│   │   ├── __init__.py
│   │   ├── base.py           # PaymentGatewayAdapter ABC
│   │   └── razorpay.py       # RazorpayAdapter
│   ├── sms/
│   │   ├── __init__.py
│   │   ├── base.py           # SMSProvider ABC
│   │   └── msg91.py          # MSG91Adapter
│   ├── push/
│   │   ├── __init__.py
│   │   ├── base.py           # PushProvider ABC
│   │   └── fcm.py            # FCMAdapter
│   ├── email/
│   │   ├── __init__.py
│   │   ├── base.py           # EmailProvider ABC
│   │   └── sendgrid.py       # SendGridAdapter
│   ├── maps/
│   │   ├── __init__.py
│   │   ├── base.py           # MapsProvider ABC
│   │   └── google_maps.py    # GoogleMapsAdapter
│   └── storage/
│       ├── __init__.py
│       ├── base.py           # StorageProvider ABC
│       └── s3.py             # S3Adapter
```

---

## 2. Payment Gateway — Razorpay (V1)

### 2.1 Interface

```python
class PaymentGatewayAdapter(ABC):
    @abstractmethod
    async def create_order(
        self, amount_paise: int, currency: str, receipt: str, notes: dict
    ) -> PaymentOrder:
        """Create a payment order/intent. Amount in smallest currency unit (paise)."""

    @abstractmethod
    async def verify_webhook_signature(
        self, payload: bytes, signature: str
    ) -> bool:
        """Verify the webhook's cryptographic signature. Returns True if valid."""

    @abstractmethod
    async def parse_webhook_event(self, payload: bytes) -> WebhookEvent:
        """Parse webhook payload into a structured event."""

    @abstractmethod
    async def process_refund(
        self, payment_id: str, amount_paise: int, notes: dict
    ) -> RefundResult:
        """Initiate a refund for a captured payment."""
```

### 2.2 Razorpay Implementation Details

| Aspect | Detail |
|--------|--------|
| **SDK** | `razorpay` Python package |
| **Auth** | API Key ID + Secret (env vars: `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`) |
| **Order Creation** | `POST /v1/orders` — returns `razorpay_order_id` |
| **Client Checkout** | Gateway-hosted checkout (Razorpay.js) — no card data touches server (NFR-SEC-003) |
| **Webhook Events** | `payment.captured`, `payment.failed`, `refund.processed`, `refund.failed` |
| **Signature Verification** | HMAC-SHA256 with webhook secret (`RAZORPAY_WEBHOOK_SECRET`) |
| **Idempotency** | `receipt` field serves as idempotency key for order creation |
| **Amount Format** | Paise (integer) — multiply INR amount by 100 |

### 2.3 Webhook Handler Flow

```
1. Razorpay → POST /payments/webhook (raw JSON payload + X-Razorpay-Signature header)
2. Server extracts signature from header
3. Server verifies HMAC-SHA256(payload, webhook_secret) == signature
4. If invalid → HTTP 400, log security alert
5. If valid → parse event
6. Check idempotency: has this event_id been processed? If yes → HTTP 200 (no-op)
7. Process event:
   - payment.captured → write SUCCESS to payments, transition order PENDING_PAYMENT → CONFIRMED
   - payment.failed → write FAILED to payments, log for retry
   - refund.processed → write COMPLETED to refunds, transition order → REFUNDED
   - refund.failed → write FAILED to refunds, alert ops
8. Store raw payload in payment_transactions
9. Return HTTP 200
```

### 2.4 Error Handling & Retry

| Scenario | Handling |
|----------|---------|
| Gateway timeout on order creation | Retry up to 3 times with exponential backoff |
| Gateway 5xx on order creation | Queue for retry via Celery; show customer "payment processing" |
| Webhook delivery failure | Razorpay retries automatically; handler is idempotent |
| Duplicate webhook | Detected by event_id check; return 200 without re-processing |
| Signature verification failure | Log security alert; return 400; do not process |
| Refund failure | Record FAILED status; alert ops team; available for manual retry |

### 2.5 Environment Configuration

```bash
RAZORPAY_KEY_ID=rzp_live_xxxxxx        # API Key ID
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxx    # API Key Secret
RAZORPAY_WEBHOOK_SECRET=xxxxxxxx        # Webhook signature verification secret
```

---

## 3. SMS / OTP — MSG91 (V1)

### 3.1 Interface

```python
class SMSProvider(ABC):
    @abstractmethod
    async def send_otp(self, phone: str, otp_length: int = 6) -> OTPSendResult:
        """Send OTP via SMS. Returns send status and request ID."""

    @abstractmethod
    async def verify_otp(self, phone: str, otp: str) -> OTPVerifyResult:
        """Verify OTP code. Returns verification status."""

    @abstractmethod
    async def send_transactional_sms(
        self, phone: str, template_id: str, variables: dict
    ) -> SMSSendResult:
        """Send a transactional SMS using a DLT-registered template."""
```

### 3.2 MSG91 Implementation Details

| Aspect | Detail |
|--------|--------|
| **SDK** | HTTP REST API (no official Python SDK) |
| **Auth** | Auth Key (env var: `MSG91_AUTH_KEY`) |
| **OTP Send** | `POST https://control.msg91.com/api/v5/otp` |
| **OTP Verify** | `POST https://control.msg91.com/api/v5/otp/verify` |
| **Transactional SMS** | `POST https://control.msg91.com/api/v5/flow/` |
| **DLT Compliance** | All templates registered with telecom operators; template IDs stored in config |
| **OTP Expiry** | Configurable via `OTP_EXPIRY_SECONDS` (default: 300) |
| **OTP Length** | 6 digits |
| **Retry Logic** | MSG91 handles retries for OTP; explicit retry for transactional SMS |

### 3.3 DLT Template Registration

Templates must be registered with Indian telecom operators (DLT) before use:

| Template | Purpose | Example |
|----------|---------|---------|
| `OTP_LOGIN` | Authentication OTP | "Your AquaSwift OTP is {otp}. Valid for 5 minutes." |
| `ORDER_CONFIRMED` | Order confirmation | "Your order {order_number} is confirmed. Delivery by {time}." |
| `DELIVERY_OTP` | Proof of delivery | "Your delivery OTP is {otp}. Share with the driver upon arrival." |
| `DELIVERY_ARRIVED` | Driver arrived | "Your AquaSwift driver has arrived at your location." |
| `REFUND_INITIATED` | Refund notification | "Refund of ₹{amount} initiated for order {order_number}." |

### 3.4 Error Handling

| Scenario | Handling |
|----------|---------|
| SMS delivery failure | Retry up to 2 times; if still failing, attempt email OTP fallback (AUTH-010) |
| MSG91 API timeout | Retry with exponential backoff (3 attempts) |
| Invalid phone number | Return validation error to client |
| DLT rejection | Log error; alert ops; SMS will not be delivered until template is re-registered |
| Rate limit by MSG91 | Backoff; respect rate limits; alert if sustained |

### 3.5 Environment Configuration

```bash
MSG91_AUTH_KEY=xxxxxxxxxxxxxx           # MSG91 auth key
MSG91_SENDER_ID=AQUASW                  # 6-char sender ID
MSG91_OTP_TEMPLATE_ID=xxxxxxxx         # DLT-registered OTP template
MSG91_DLT_TE_ID=xxxxxxxxxxx            # DLT Template Entity ID
```

---

## 4. Push Notifications — Firebase Cloud Messaging (FCM)

### 4.1 Interface

```python
class PushProvider(ABC):
    @abstractmethod
    async def send_push(
        self, device_token: str, title: str, body: str, data: dict | None = None
    ) -> PushSendResult:
        """Send a push notification to a specific device."""

    @abstractmethod
    async def send_push_batch(
        self, tokens: list[str], title: str, body: str, data: dict | None = None
    ) -> list[PushSendResult]:
        """Send push notification to multiple devices."""
```

### 4.2 FCM Implementation Details

| Aspect | Detail |
|--------|--------|
| **SDK** | `firebase-admin` Python SDK |
| **Auth** | Service account key JSON (env var: `GOOGLE_APPLICATION_CREDENTIALS`) |
| **Protocol** | FCM HTTP v1 API |
| **Token Registration** | Client registers FCM token via `POST /notifications/register-device` |
| **Token Storage** | Stored in `user_devices` table (user_id, fcm_token, platform, last_seen) |
| **Platform Support** | Android + iOS via Flutter's `firebase_messaging` package |

### 4.3 Notification Events

| Event | Title | Body Example | Data Payload |
|-------|-------|-------------|-------------|
| `order_confirmed` | Order Confirmed | "Your order AQ-001 is confirmed!" | `{ "order_id": "uuid", "screen": "order_detail" }` |
| `delivery_assigned` | Driver Assigned | "A driver has been assigned to your delivery." | `{ "delivery_id": "uuid" }` |
| `driver_en_route` | Driver En Route | "Your driver is on the way!" | `{ "delivery_id": "uuid" }` |
| `driver_arrived` | Driver Arrived | "Your AquaSwift driver has arrived." | `{ "delivery_id": "uuid" }` |
| `delivery_completed` | Delivery Complete | "5,000L of RO+UV water delivered!" | `{ "order_id": "uuid" }` |
| `delivery_otp` | Delivery OTP | "Your delivery OTP is 482910." | `{ "delivery_id": "uuid" }` |
| `partial_delivery` | Partial Delivery | "3,000L delivered. 2,000L will follow." | `{ "delivery_id": "uuid" }` |
| `order_cancelled` | Order Cancelled | "Your order AQ-001 has been cancelled." | `{ "order_id": "uuid" }` |
| `refund_initiated` | Refund Started | "Refund of ₹2,250 initiated." | `{ "order_id": "uuid" }` |
| `delivery_offer` | New Delivery (Driver) | "New delivery: 5,000L to Gachibowli" | `{ "delivery_id": "uuid" }` |

### 4.4 Error Handling

| Scenario | Handling |
|----------|---------|
| Invalid FCM token | Remove token from `user_devices`; do not retry |
| FCM service unavailable | Retry up to 3 times with backoff via Celery |
| Token expired | Remove token; user must re-register on next app open |
| Critical event push fails | Fall back to SMS via NotificationService (RULE-021) |

### 4.5 Environment Configuration

```bash
GOOGLE_APPLICATION_CREDENTIALS=/path/to/firebase-service-account.json
FCM_PROJECT_ID=aquaswift-prod
```

---

## 5. Maps — Google Maps Platform

### 5.1 Interface

```python
class MapsProvider(ABC):
    @abstractmethod
    async def geocode(self, address: str) -> GeocodingResult:
        """Convert address text to lat/lng coordinates."""

    @abstractmethod
    async def reverse_geocode(self, lat: float, lng: float) -> ReverseGeocodingResult:
        """Convert lat/lng to formatted address."""

    @abstractmethod
    async def calculate_distance(
        self, origin: tuple[float, float], destination: tuple[float, float]
    ) -> DistanceResult:
        """Calculate driving distance and duration between two points."""
```

### 5.2 Google Maps Implementation Details

| Aspect | Detail |
|--------|--------|
| **SDK** | `googlemaps` Python client |
| **Auth** | API Key (env var: `GOOGLE_MAPS_API_KEY`) |
| **APIs Used** | Geocoding API, Distance Matrix API |
| **Rate Limits** | 50 QPS (Geocoding), 100 elements/second (Distance Matrix) |
| **Billing** | Pay-per-use; budget alerts via Google Cloud Console |

### 5.3 Usage Contexts

| Context | API | Trigger |
|---------|-----|---------|
| Customer adds address | Geocoding | Address creation/update |
| Customer places pin on map | Reverse Geocoding | Map pin drop in mobile app |
| Delivery charge calculation | Distance Matrix | Order quote / creation |
| Driver assignment proximity | Distance Matrix | Delivery offer selection |
| Navigation deep link | — | Client-side Google Maps URL scheme |

### 5.4 Error Handling

| Scenario | Handling |
|----------|---------|
| API rate limit | Exponential backoff; queue geocoding requests |
| API unavailable | Allow order with existing geocoded addresses; queue new geocoding |
| Invalid address | Return validation error with suggestions |
| Over budget | Alert ops; degrade to address-only (no distance-based pricing) |

### 5.5 Environment Configuration

```bash
GOOGLE_MAPS_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_MAPS_RATE_LIMIT=50                    # requests per second
```

---

## 6. Email — SendGrid / AWS SES

### 6.1 Interface

```python
class EmailProvider(ABC):
    @abstractmethod
    async def send_email(
        self, to: str, subject: str, html_body: str, text_body: str | None = None
    ) -> EmailSendResult:
        """Send a transactional email."""

    @abstractmethod
    async def send_template_email(
        self, to: str, template_id: str, template_data: dict
    ) -> EmailSendResult:
        """Send an email using a pre-defined template."""
```

### 6.2 Implementation Details

| Aspect | Detail |
|--------|--------|
| **V1 Provider** | SendGrid (or AWS SES if already in AWS ecosystem) |
| **SDK** | `sendgrid` Python SDK (or `boto3` for SES) |
| **Auth** | API Key (env var: `SENDGRID_API_KEY`) |
| **Templates** | Stored in SendGrid Dynamic Templates |
| **From Address** | `noreply@aquaswift.in` |

### 6.3 Email Templates

| Template | Purpose |
|----------|---------|
| `welcome` | Welcome email after first registration |
| `order_confirmation` | Order confirmation with details |
| `delivery_summary` | Delivery completion summary |
| `refund_confirmation` | Refund processed confirmation |
| `invoice` | B2B invoice email with PDF attachment |
| `otp_fallback` | OTP via email when SMS fails |

### 6.4 Environment Configuration

```bash
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxx
EMAIL_FROM=noreply@aquaswift.in
EMAIL_FROM_NAME=AquaSwift
```

---

## 7. Object Storage — AWS S3

### 7.1 Interface

```python
class StorageProvider(ABC):
    @abstractmethod
    async def upload_file(
        self, file: bytes, key: str, content_type: str
    ) -> UploadResult:
        """Upload a file and return the storage URL."""

    @abstractmethod
    async def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """Generate a pre-signed URL for temporary access."""

    @abstractmethod
    async def delete_file(self, key: str) -> bool:
        """Delete a file from storage."""
```

### 7.2 S3 Implementation Details

| Aspect | Detail |
|--------|--------|
| **SDK** | `boto3` |
| **Auth** | IAM role (ECS task role) or access keys (local dev) |
| **Bucket** | `aquaswift-media-{env}` |
| **Key Structure** | `{type}/{year}/{month}/{uuid}.{ext}` |

### 7.3 Storage Categories

| Category | Key Pattern | Content Type | Max Size |
|----------|-----------|-------------|----------|
| Delivery proof photos | `delivery-proofs/2026/09/{uuid}.jpg` | image/jpeg | 10 MB |
| Quality certificates | `quality-certs/2026/09/{uuid}.pdf` | application/pdf | 5 MB |
| Catalog icons | `catalog-icons/{uuid}.png` | image/png | 1 MB |
| Invoice PDFs | `invoices/2026/09/{uuid}.pdf` | application/pdf | 2 MB |

### 7.4 Environment Configuration

```bash
AWS_S3_BUCKET=aquaswift-media-prod
AWS_S3_REGION=ap-south-1
AWS_ACCESS_KEY_ID=xxx                # local dev only; production uses IAM roles
AWS_SECRET_ACCESS_KEY=xxx            # local dev only
```

---

## 8. Integration Summary

| Integration | V1 Provider | Interface | Adapter | Used By |
|------------|------------|-----------|---------|---------|
| Payment | Razorpay | `PaymentGatewayAdapter` | `RazorpayAdapter` | PAY, ORD |
| SMS/OTP | MSG91 | `SMSProvider` | `MSG91Adapter` | AUTH, NTF |
| Push | FCM | `PushProvider` | `FCMAdapter` | NTF |
| Email | SendGrid | `EmailProvider` | `SendGridAdapter` | NTF |
| Maps | Google Maps | `MapsProvider` | `GoogleMapsAdapter` | ADDR, DEL, PRC |
| Storage | AWS S3 | `StorageProvider` | `S3Adapter` | DEL, QUAL, CAT, INVC |

---

## 9. Circuit Breaker Strategy

For all external integrations, a circuit breaker pattern prevents cascading failures:

| State | Behavior |
|-------|----------|
| **CLOSED** (normal) | All requests pass through to external service |
| **OPEN** (failure threshold reached) | All requests short-circuit with a cached/fallback response or error |
| **HALF-OPEN** (after cooldown) | A single test request is allowed; if it succeeds, move to CLOSED |

**Configuration per integration:**

| Integration | Failure Threshold | Cooldown | Fallback |
|-------------|------------------|----------|----------|
| Razorpay | 5 failures in 60s | 30s | Queue for retry; show "payment processing" |
| MSG91 | 3 failures in 60s | 60s | Email OTP fallback |
| FCM | 5 failures in 60s | 30s | SMS fallback for critical events |
| Google Maps | 3 failures in 60s | 60s | Allow with existing geocoded addresses |
| SendGrid | 3 failures in 60s | 60s | Queue for retry |
| S3 | 5 failures in 60s | 30s | Return error; files are non-critical for order flow |

Implementation: Python `circuitbreaker` library or custom decorator.
