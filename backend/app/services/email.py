"""Email delivery via Resend API.

Graceful degradation: no API key = no email, app still works.
"""

import httpx

from app.core.config import settings


async def send_email(to: str, subject: str, html: str) -> bool:
    """Send transactional email via Resend API."""
    if not settings.RESEND_API_KEY:
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
                },
            )
            return resp.status_code == 200
    except Exception:
        return False
