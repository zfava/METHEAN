"""Email delivery via Resend API.

Graceful degradation: no API key = no email, app still works.
"""

import logging

import httpx

from app.core.config import settings

logger = logging.getLogger("methean.email")


async def send_email(to: str, subject: str, html: str, text: str | None = None) -> bool:
    """Send transactional email via Resend API. Never raises."""
    if not settings.RESEND_API_KEY:
        logger.info("Email not sent (no RESEND_API_KEY): to=%s subject=%s", to, subject)
        return False

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}"},
                json={
                    "from": settings.EMAIL_FROM,
                    "to": [to],
                    "subject": subject,
                    "html": html,
                    "text": text or "",
                },
            )
            if resp.status_code == 200:
                logger.info("Email sent: to=%s subject=%s", to, subject)
                return True
            logger.warning("Email failed: status=%d to=%s", resp.status_code, to)
            return False
    except Exception as e:
        logger.error("Email exception: %s to=%s", e, to)
        return False
