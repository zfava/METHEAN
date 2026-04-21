# Auth Token Rotation

Last verified: 2026-04-17 (dual-key rotation code verified; production rotation not yet exercised)

## JWT Secret Rotation

The backend supports dual-key JWT rotation: `JWT_SECRET` (current) and `PREVIOUS_JWT_SECRET` (previous). During rotation, tokens signed with either key are accepted.

### Procedure

```bash
# 1. Generate a new secret
NEW_SECRET=$(openssl rand -hex 32)

# 2. Copy current JWT_SECRET to PREVIOUS_JWT_SECRET
railway variables set PREVIOUS_JWT_SECRET=$CURRENT_JWT_SECRET

# 3. Set the new JWT_SECRET
railway variables set JWT_SECRET=$NEW_SECRET

# 4. Restart the backend
railway service restart backend

# 5. Wait for all existing tokens to expire (access tokens: 30 min, refresh: 7 days)
# During this window, both keys are accepted

# 6. After 7 days, clear the previous key
railway variables unset PREVIOUS_JWT_SECRET
railway service restart backend
```

### Verification

```bash
# Old tokens should still work during the overlap window
curl -H "Authorization: Bearer $OLD_TOKEN" http://localhost:8000/api/v1/auth/me
# Expected: 200 (token signed with PREVIOUS_JWT_SECRET is accepted)

# New tokens use the new key
curl -X POST http://localhost:8000/api/v1/auth/login -d '{"email":"test@test.com","password":"test"}'
# The returned token is signed with the new JWT_SECRET
```

## Password Reset (Bulk)

If credentials are compromised (database breach, leaked password hashes):

```bash
# 1. Rotate JWT secret immediately (invalidates all sessions)
# Follow the JWT rotation procedure above, but skip the overlap window:
railway variables set JWT_SECRET=$(openssl rand -hex 32)
railway variables unset PREVIOUS_JWT_SECRET
railway service restart backend
# All users are now logged out

# 2. Send password reset emails to all users
cd backend
python -c "
import asyncio
from app.services.password_reset import generate_reset_token
from app.core.database import async_session_factory
from sqlalchemy import select
from app.models.identity import User

async def bulk_reset():
    async with async_session_factory() as db:
        users = (await db.execute(select(User).where(User.is_active == True))).scalars().all()
        for user in users:
            await generate_reset_token(db, user.email)
        await db.commit()
        print(f'Sent reset emails to {len(users)} users')

asyncio.run(bulk_reset())
"

# 3. Notify users via out-of-band channel (email, in-app banner)
```

## Session Invalidation (Specific User)

To invalidate a specific user's sessions:

```bash
# Revoke all refresh tokens for the user
psql -c "UPDATE refresh_tokens SET is_revoked = true WHERE user_id = '<user_uuid>';"

# The user's access token will expire within 30 minutes
# They will not be able to refresh after that
```

## CSRF Token Rotation

CSRF tokens are per-session and rotate automatically. No manual rotation needed. If the CSRF middleware is suspected of being bypassed:

1. Check the `_CSRF_EXEMPT_PATHS` list in `app/core/middleware.py`
2. Verify the double-submit cookie pattern is functioning: the test `test_csrf_rejects_without_header` must pass
