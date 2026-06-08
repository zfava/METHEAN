"""Grant (or revoke) the native-curriculum entitlement for one household.

The native-curriculum generation/materialization path is gated behind a
per-household entitlement (``Household.native_curriculum_access``) that defaults
OFF. Turning it on for a household (e.g. the founder's account at launch) is a
DATA operation, not a code branch: no email is hardcoded in application logic.

This script takes the household identifier and flips the boolean. It is
idempotent (running it twice leaves the same state) and prints the before/after.

Identify the household either by a member user's email or by the household UUID:

    # by a member's email (most convenient for the founder account)
    python -m scripts.grant_native_curriculum_access --email founder@example.com

    # by household UUID
    python -m scripts.grant_native_curriculum_access --household-id <uuid>

    # revoke (turn it back off)
    python -m scripts.grant_native_curriculum_access --email founder@example.com --off

Run from the backend dir (``python -m scripts.grant_native_curriculum_access``)
or inside the container (``python scripts/grant_native_curriculum_access.py``).
"""

import argparse
import asyncio
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.models.identity import Household, User


async def _resolve_household(db: AsyncSession, *, email: str | None, household_id: str | None) -> Household:
    if household_id:
        hh = await db.get(Household, uuid.UUID(household_id))
        if hh is None:
            raise SystemExit(f"No household with id {household_id}")
        return hh
    assert email is not None
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise SystemExit(f"No user with email {email}")
    hh = await db.get(Household, user.household_id)
    if hh is None:
        raise SystemExit(f"User {email} has no household")
    return hh


async def _run(email: str | None, household_id: str | None, enable: bool) -> None:
    engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as db:
        hh = await _resolve_household(db, email=email, household_id=household_id)
        before = hh.native_curriculum_access
        hh.native_curriculum_access = enable
        await db.commit()
        print(f"household {hh.id} ('{hh.name}'): native_curriculum_access {before} -> {hh.native_curriculum_access}")
    await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--email", help="email of a member user of the target household")
    group.add_argument("--household-id", help="UUID of the target household")
    parser.add_argument(
        "--off",
        action="store_true",
        help="revoke the entitlement (default is to grant it)",
    )
    args = parser.parse_args()
    asyncio.run(_run(args.email, args.household_id, enable=not args.off))


if __name__ == "__main__":
    main()
