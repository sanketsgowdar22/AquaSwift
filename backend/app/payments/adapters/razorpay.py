"""
AquaSwift — Razorpay Payment Gateway Adapter (Stub)

Stub adapter for development. Logs calls and returns mock responses.
Swap for real Razorpay SDK integration when API keys are configured.
"""
from __future__ import annotations
import uuid
import structlog
from app.core.config import settings

logger = structlog.get_logger()


class RazorpayAdapter:
    """Razorpay gateway adapter. Stub for development."""

    async def create_order(self, amount_paise: int, currency: str = "INR",
                           receipt: str | None = None) -> dict:
        """Create a Razorpay order. Returns mock order_id in dev."""
        if settings.is_production and settings.RAZORPAY_KEY_ID:
            return await self._create_real_order(amount_paise, currency, receipt)
        mock_id = f"order_mock_{uuid.uuid4().hex[:12]}"
        logger.info("razorpay_order_stub", mock_order_id=mock_id, amount=amount_paise)
        return {"id": mock_id, "amount": amount_paise, "currency": currency, "status": "created"}

    async def verify_signature(self, order_id: str, payment_id: str, signature: str) -> bool:
        """Verify Razorpay webhook signature. Returns True in dev."""
        if settings.is_production:
            return self._verify_real_signature(order_id, payment_id, signature)
        logger.info("razorpay_signature_stub", order_id=order_id, result="verified_stub")
        return True

    async def initiate_refund(self, payment_id: str, amount_paise: int, reason: str) -> dict:
        """Initiate a refund via Razorpay. Returns mock refund_id in dev."""
        mock_id = f"rfnd_mock_{uuid.uuid4().hex[:12]}"
        logger.info("razorpay_refund_stub", payment_id=payment_id, amount=amount_paise, mock_refund_id=mock_id)
        return {"id": mock_id, "amount": amount_paise, "status": "processed"}

    async def _create_real_order(self, amount_paise: int, currency: str, receipt: str | None) -> dict:
        """Real Razorpay order creation. To be implemented."""
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.razorpay.com/v1/orders",
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET),
                json={"amount": amount_paise, "currency": currency, "receipt": receipt},
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()

    def _verify_real_signature(self, order_id: str, payment_id: str, signature: str) -> bool:
        import hashlib, hmac
        message = f"{order_id}|{payment_id}"
        expected = hmac.new(settings.RAZORPAY_KEY_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)


razorpay_adapter = RazorpayAdapter()
