"""Qualified-human runtime presence: attestation reads shared by the
learning-context gate and the parent day view.

requires_qualified_human_present_at_runtime (services/node_content.py)
identifies WHICH nodes need a qualified human physically present at
the work. This module answers WHETHER that presence has been attested
for a given child and node today, and what role the attestation should
claim. Attestation creation lives on the API endpoint (mirroring the
mastery-override precedent in api/state.py); reads live here so the
gate in services/learning_context.py and the today-view enrichment in
api/spec_coverage.py consult one implementation.

Everything fails closed: no row, an expired row, a row for another
child or node, or an unresolvable timezone all mean "not attested".
"""

import uuid
from datetime import UTC, datetime, time
from zoneinfo import ZoneInfo

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.governance import SupervisionAttestation

logger = structlog.get_logger()

# Maps the lowercase qualified-human phrases recognised by
# requires_qualified_human_present_at_runtime to the display role an
# attestation pre-fills. Ordered: more specific licensed roles first,
# the generic fallback last, matching the authoring discipline
# (hc-021 / elc-021 canonical pattern).
ROLE_PHRASE_DISPLAY: tuple[tuple[str, str], ...] = (
    ("licensed electrician", "licensed electrician"),
    ("licensed hvac technician", "licensed HVAC technician"),
    ("licensed gas fitter", "licensed gas fitter"),
    ("608-certified", "EPA 608-certified technician"),
    ("epa-608", "EPA 608-certified technician"),
    ("qualified human", "qualified adult"),
)


def required_role_from_content(content: dict | None) -> str | None:
    """Display name of the qualified role a node's supervision_basis names.

    Returns None when the content does not name one (callers should
    already have checked requires_qualified_human_present_at_runtime;
    None doubles as a fail-closed signal for malformed content).
    """
    if not isinstance(content, dict):
        return None
    safety_basis = content.get("safety_basis")
    if not isinstance(safety_basis, dict):
        return None
    basis = safety_basis.get("supervision_basis", "")
    if not isinstance(basis, str):
        return None
    basis_lower = basis.lower()
    for phrase, display in ROLE_PHRASE_DISPLAY:
        if phrase in basis_lower:
            return display
    return None


def local_end_of_day(timezone_name: str | None, now: datetime | None = None) -> datetime:
    """End of the current day in the household's timezone, as an aware UTC datetime.

    An attestation created at any point during the household's day
    expires at that day's last microsecond, local time: per child, per
    node, per day, never a standing waiver. An unresolvable timezone
    falls back to UTC (the notifications quiet-hours precedent), which
    only ever shortens or shifts the window, never extends it past a
    real day.
    """
    current = now or datetime.now(UTC)
    try:
        tz = ZoneInfo(timezone_name or "UTC")
    except (KeyError, ValueError, TypeError, OSError) as exc:
        # ZoneInfo raises ZoneInfoNotFoundError (a KeyError) for unknown
        # keys, ValueError/TypeError for malformed ones, OSError when no
        # tz database is reachable. UTC fallback only ever shortens the
        # attestation window, never extends it.
        logger.warning(
            "household_timezone_invalid",
            timezone_name=timezone_name,
            error=str(exc),
        )
        tz = ZoneInfo("UTC")
    local_now = current.astimezone(tz)
    local_end = datetime.combine(local_now.date(), time.max, tzinfo=tz)
    return local_end.astimezone(UTC)


async def get_valid_attestation(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    node_id: uuid.UUID,
    now: datetime | None = None,
) -> SupervisionAttestation | None:
    """The unexpired attestation for this child and node, or None.

    None means the runtime presence gate stays closed.
    """
    current = now or datetime.now(UTC)
    result = await db.execute(
        select(SupervisionAttestation)
        .where(
            SupervisionAttestation.household_id == household_id,
            SupervisionAttestation.child_id == child_id,
            SupervisionAttestation.node_id == node_id,
            SupervisionAttestation.expires_at > current,
        )
        .order_by(SupervisionAttestation.expires_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_attested_node_ids(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    node_ids: list[uuid.UUID],
    now: datetime | None = None,
) -> set[uuid.UUID]:
    """Node ids among ``node_ids`` with an unexpired attestation for this child.

    Batch form of get_valid_attestation for the parent day view, so the
    today endpoint stays a single extra query regardless of how many
    hazardous activities are scheduled.
    """
    if not node_ids:
        return set()
    current = now or datetime.now(UTC)
    result = await db.execute(
        select(SupervisionAttestation.node_id).where(
            SupervisionAttestation.household_id == household_id,
            SupervisionAttestation.child_id == child_id,
            SupervisionAttestation.node_id.in_(node_ids),
            SupervisionAttestation.expires_at > current,
        )
    )
    return {row[0] for row in result.all()}
