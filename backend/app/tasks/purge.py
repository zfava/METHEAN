"""Household purge: total erasure once the 7-day soft-delete window ends.

For every household whose deletion_requested_at is older than the
window, the daily task erases every database row that references the
household, every S3 object under the household's key prefix, and any
still-active Stripe subscription. Parent sovereignty includes the
right to leave with everything gone.

The table list is derived from SQLAlchemy metadata at runtime (every
table with a household_id column, deleted in reverse dependency
order), so a future table can never be silently missed by a
hand-maintained list.
"""

import asyncio
import uuid
from datetime import UTC, datetime, timedelta

import structlog
from sqlalchemy import delete as sa_delete
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base, async_session_factory
from app.models.identity import Household

logger = structlog.get_logger()

DELETION_WINDOW_DAYS = 7

# The two append-only tables protected by migration 052's BEFORE
# UPDATE OR DELETE triggers.
_APPEND_ONLY_TABLES = ("governance_events", "state_events")


def _delete_household_objects(household_id: uuid.UUID) -> int:
    """Delete every S3 object under the household's key prefix.

    Upload keys are namespaced {household_id}/..., so the prefix sweep
    removes everything regardless of which table tracked the upload.
    Raises on S3 errors: the caller skips the household and retries on
    the next beat run rather than leaving a partial erasure.
    """
    from app.services.storage import delete_artifact, list_artifact_keys

    keys = list_artifact_keys(f"{household_id}/")
    for key in keys:
        delete_artifact(key)
    return len(keys)


async def purge_household(db: AsyncSession, household_id: uuid.UUID) -> dict[str, int]:
    """Erase every database row belonging to one household.

    Runs inside the caller's transaction so the erasure is all or
    nothing. Tables are discovered from metadata: every table with a
    household_id column, deleted children-first (reversed
    sorted_tables), then the household row itself.

    Sanctioned append-only bypass: migration 052's triggers forbid
    DELETE on governance_events and state_events. Immutability exists
    to prevent silent revision of the audit trail, not to override a
    family's legal right to be forgotten, so this purge (and only this
    purge) disables exactly those two triggers inside the transaction
    and re-enables them after the deletes. If anything fails, the
    rollback also rolls back the DISABLE TRIGGER, so the protection
    can never be left off.
    """
    is_postgres = db.bind is not None and db.bind.dialect.name == "postgresql"
    if is_postgres:
        # Scope RLS to the household being erased; transaction-local.
        await db.execute(
            text("SELECT set_config('app.current_household_id', :hid, true)"),
            {"hid": str(household_id)},
        )
        for table_name in _APPEND_ONLY_TABLES:
            await db.execute(text(f"ALTER TABLE {table_name} DISABLE TRIGGER {table_name}_forbid_mutation"))

    counts: dict[str, int] = {}
    for table in reversed(Base.metadata.sorted_tables):
        if "household_id" not in table.c:
            continue
        result = await db.execute(table.delete().where(table.c.household_id == household_id))
        if result.rowcount:
            counts[table.name] = result.rowcount

    result = await db.execute(sa_delete(Household).where(Household.id == household_id))
    counts["households"] = result.rowcount

    if is_postgres:
        # Reached only when every delete succeeded; on any error the
        # transaction rollback restores the triggers automatically.
        for table_name in _APPEND_ONLY_TABLES:
            await db.execute(text(f"ALTER TABLE {table_name} ENABLE TRIGGER {table_name}_forbid_mutation"))

    return counts


async def purge_eligible_households(session_factory=None) -> dict:
    """Find and purge every household past its deletion window.

    Each household is purged in its own transaction: one failure is
    logged and retried on the next daily run without blocking the
    rest of the batch.
    """
    factory = session_factory or async_session_factory
    cutoff = datetime.now(UTC) - timedelta(days=DELETION_WINDOW_DAYS)

    async with factory() as db:
        result = await db.execute(
            select(Household.id).where(
                Household.deletion_requested_at.is_not(None),
                Household.deletion_requested_at < cutoff,
            )
        )
        eligible = [row[0] for row in result.all()]

    purged: dict[str, dict[str, int]] = {}
    failed = 0
    for household_id in eligible:
        async with factory() as db:
            try:
                # Re-try subscription cancellation in case the request
                # time cancel failed; tolerates missing Stripe config.
                from app.services.billing import cancel_subscription

                try:
                    await cancel_subscription(db, household_id, at_period_end=False)
                except Exception as exc:
                    logger.warning(
                        "purge_stripe_cancel_failed",
                        household_id=str(household_id),
                        error=str(exc),
                    )

                objects_deleted = _delete_household_objects(household_id)
                counts = await purge_household(db, household_id)
                await db.commit()
                purged[str(household_id)] = counts
                logger.info(
                    "household_purged",
                    household_id=str(household_id),
                    s3_objects_deleted=objects_deleted,
                    rows_purged=counts,
                )
            except Exception as exc:
                await db.rollback()
                failed += 1
                logger.error(
                    "household_purge_failed",
                    household_id=str(household_id),
                    error=str(exc),
                )

    return {"eligible": len(eligible), "purged": len(purged), "failed": failed, "households": purged}


def run_purge_sync() -> dict:
    return asyncio.get_event_loop().run_until_complete(purge_eligible_households())
