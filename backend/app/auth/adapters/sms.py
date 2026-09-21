"""
AquaSwift — SMS Adapter (Stub)

Stub adapter for MSG91 SMS/OTP service. Logs OTP codes to console
instead of sending real SMS. Swap for real adapter when MSG91 API
key is available.
"""

from __future__ import annotations

import structlog

from app.core.config import settings

logger = structlog.get_logger()


class SMSAdapter:
    """SMS adapter interface. Stub implementation for development."""

    async def send_otp(self, phone: str, otp: str) -> bool:
        """
        Send OTP to phone number.

        In production, this calls MSG91 OTP API.
        In development, this logs the OTP to console.
        """
        if settings.is_production and settings.MSG91_AUTH_KEY:
            return await self._send_real_otp(phone, otp)

        # Stub — log OTP for development
        logger.info(
            "otp_sent_stub",
            phone=phone,
            otp=otp,
            message=f"OTP for {phone}: {otp} (stub — not actually sent)",
        )
        return True

    async def _send_real_otp(self, phone: str, otp: str) -> bool:
        """Send real OTP via MSG91. To be implemented with MSG91 API."""
        import httpx

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://control.msg91.com/api/v5/otp",
                    headers={"authkey": settings.MSG91_AUTH_KEY},
                    json={
                        "template_id": settings.MSG91_OTP_TEMPLATE_ID,
                        "mobile": phone.replace("+", ""),
                        "otp": otp,
                    },
                    timeout=10.0,
                )
                response.raise_for_status()
                logger.info("otp_sent_real", phone=phone, status=response.status_code)
                return True
        except Exception as e:
            logger.error("otp_send_failed", phone=phone, error=str(e))
            return False


# Singleton
sms_adapter = SMSAdapter()
