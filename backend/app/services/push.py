"""Push notification delivery via FCM HTTP v1 API.

Non-blocking: a failed push never blocks business logic.
Handles stale tokens by deactivating them on 404/410.
"""

import json
import logging
import uuid
from datetime import UTC, datetime

import httpx
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.operational import DeviceToken

logger = logging.getLogger(__name__)

# ── FCM Access Token Cache ──

_fcm_token: str | None = None
_fcm_token_expires: float = 0


async def _get_fcm_access_token() -> str | None:
    """Get a short-lived OAuth2 token for FCM v1 API."""
    global _fcm_token, _fcm_token_expires
    import time

    if _fcm_token and time.time() < _fcm_token_expires:
        return _fcm_token

    sa_json = settings.FCM_SERVICE_ACCOUNT_JSON
    if not sa_json:
        return None

    try:
        # Parse service account credentials
        if sa_json.startswith("{"):
            creds = json.loads(sa_json)
        else:
            with open(sa_json) as f:
                creds = json.load(f)

        # Build JWT for token exchange
        import jwt as pyjwt

        now = int(time.time())
        payload = {
            "iss": creds["client_email"],
            "scope": "https://www.googleapis.com/auth/firebase.messaging",
            "aud": "https://oauth2.googleapis.com/token",
            "iat": now,
            "exp": now + 3600,
        }
        signed = pyjwt.encode(payload, creds["private_key"], algorithm="RS256")

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                    "assertion": signed,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            _fcm_token = data["access_token"]
            _fcm_token_expires = now + data.get("expires_in", 3500) - 60
            return _fcm_token
    except Exception:
        logger.exception("Failed to get FCM access token")
        return None


async def send_push(
    token: str,
    platform: str,
    title: str,
    body: str,
    data: dict | None = None,
) -> bool:
    """Send a push notification via FCM HTTP v1 API.

    Returns True on success, False on failure. Logs errors but never raises.
    """
    project_id = settings.FCM_PROJECT_ID
    if not project_id:
        logger.debug("FCM_PROJECT_ID not configured, skipping push")
        return False

    access_token = await _get_fcm_access_token()
    if not access_token:
        return False

    message: dict = {
        "message": {
            "token": token,
            "notification": {"title": title, "body": body},
        }
    }
    if data:
        message["message"]["data"] = {k: str(v) for k, v in data.items()}

    # Platform-specific config
    if platform == "ios":
        message["message"]["apns"] = {
            "payload": {"aps": {"sound": "default", "badge": 1}},
        }
    elif platform == "android":
        message["message"]["android"] = {
            "priority": "high",
            "notification": {"sound": "default", "channel_id": "methean_default"},
        }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                },
                content=json.dumps(message),
                timeout=10.0,
            )
            if resp.status_code in (404, 410):
                # Token is stale — will be deactivated by caller
                return False
            resp.raise_for_status()
            return True
    except Exception:
        logger.debug("Push send failed for token %s", token[:20])
        return False


async def send_push_to_user(
    db: AsyncSession,
    user_id: uuid.UUID,
    household_id: uuid.UUID,
    title: str,
    body: str,
    data: dict | None = None,
) -> int:
    """Send push to all active devices for a user. Returns count of successful sends."""
    result = await db.execute(
        select(DeviceToken).where(
            DeviceToken.user_id == user_id,
            DeviceToken.household_id == household_id,
            DeviceToken.is_active == True,  # noqa: E712
        )
    )
    tokens = result.scalars().all()
    if not tokens:
        return 0

    sent = 0
    stale_ids = []

    for dt in tokens:
        success = await send_push(dt.token, dt.device_type, title, body, data)
        if success:
            dt.last_used_at = datetime.now(UTC)
            sent += 1
        else:
            stale_ids.append(dt.id)

    # Deactivate stale tokens
    if stale_ids:
        await db.execute(
            update(DeviceToken)
            .where(DeviceToken.id.in_(stale_ids))
            .values(is_active=False)
        )

    await db.flush()
    return sent
