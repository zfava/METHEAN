"""Tutor efficacy: the tutor's memory checks itself against outcomes.

A tutor profile entry ("baking analogies work for fractions") is a
belief. This module turns belief into evidence. For each active entry it
measures the child's real attempt outcomes in the window since the entry
became active against a baseline window before it, and surfaces an honest
signal to the parent. When the evidence says the child has outgrown a
strategy, it proposes retiring it, through the exact same autonomy policy
as everything else: standard queues the proposal, autonomous applies it
citing the standing grant, off observes but proposes nothing.

HONEST STATISTICS OR NOTHING. These are observational correlations on
small samples, never causal proof. Three structural honesties:

1. Minimum-volume gate. No label beyond insufficient_data until there are
   at least MIN_ATTEMPTS attempts in the active window AND at least
   MIN_ATTEMPTS in the baseline window. A delta on tiny N is noise.
2. Conservative words, never scores. The parent sees working_well,
   no_clear_effect, may_have_outgrown, or insufficient_data, and always
   with the sample sizes behind them. Never a number without its N.
3. Retirement is a proposal, never an automatic act. Two consecutive
   may_have_outgrown readings are required before the engine proposes,
   and even then it only proposes: the parent (standard) or the standing
   grant (autonomous) decides.

This module READS attempts and mastery outcomes and writes NOTHING
except TutorEntryObservation rows and proposals routed through
tutor_profile.route_proposal. It is the SINGLE writer of observations,
mirroring the TutorProfileEntry writer guard. It makes ZERO AI calls:
pure SQL aggregation and stdlib math.
"""

import asyncio
import uuid
from datetime import UTC, datetime, timedelta

import structlog
from sqlalchemy import case, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.learning_levels import LEARNING_LEVELS, VALID_LEVELS
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import AttemptStatus, GovernanceAction
from app.models.governance import Activity, Attempt, GovernanceEvent
from app.models.intelligence import TutorEntryObservation, TutorProfileEntry
from app.services.governance import (
    log_governance_event,
)
from app.services.tutor_profile import route_proposal

logger = structlog.get_logger()

# ── Labels ──────────────────────────────────────────────────────────
# Words, never scores. The parent never sees a delta without its N.
LABEL_WORKING_WELL = "working_well"
LABEL_NO_CLEAR_EFFECT = "no_clear_effect"
LABEL_MAY_HAVE_OUTGROWN = "may_have_outgrown"
LABEL_INSUFFICIENT_DATA = "insufficient_data"

# ── Thresholds (documented; the spec's were suggestions) ────────────
# Both windows must clear this floor before any label beyond
# insufficient_data is computed. A correlation on a handful of attempts
# is noise dressed as signal.
MIN_ATTEMPTS = 20

# The baseline window reaches back from activation but no further than
# this: the child a year ago is not the right comparison for the child
# this month.
BASELINE_CAP_DAYS = 90

# Idempotency floor for the weekly batch: an entry evaluated inside this
# window is skipped, so a re-run in the same week is a near no-op.
EVAL_COOLDOWN_DAYS = 6

# Label bands on the delta (active_success_rate - baseline_success_rate),
# applied only when both volume gates are met:
#   delta >= +0.05  -> working_well
#   -0.05 < delta < +0.05 -> no_clear_effect
#   delta <= -0.05  -> may_have_outgrown (a single reading)
# A single may_have_outgrown reading sets the displayed label but never
# retires anything; retirement needs two consecutive may_have_outgrown
# readings (see _two_consecutive_outgrown). This keeps the consequential
# action conservative while the displayed word stays honest.
WORKING_WELL_DELTA = 0.05
OUTGROWN_DELTA = -0.05

# Success metric, REUSED from the mastery system, never reinvented. An
# attempt's outcome flows score -> confidence -> FSRS rating via
# state_engine.confidence_to_rating; FSRS treats Again (1) as a lapse and
# Hard/Good/Easy (2/3/4) as successful recalls. So an attempt is a
# "success" exactly when its rating is not Again, which is score >= 0.3
# under confidence_to_rating. SUCCESS_MIN_SCORE is that boundary; a guard
# test (test_success_metric_matches_mastery_definition) fails if a future
# change to confidence_to_rating moves it, so the reuse can never drift.
SUCCESS_MIN_SCORE = 0.3

# An entry gets at most this many retirement proposals over its whole
# life: one, and one more only if the parent rejected the first and the
# signal later recurs.
MAX_RETIREMENT_PROPOSALS = 2

# A strategy stamped this many content tiers (or more) below the child's
# current tier is treated as tied to an outgrown developmental stage.
TIER_LAG_THRESHOLD = 2

# Governance event types for the retirement lifecycle. target_id is the
# entry id on all three, so the lifecycle is queryable per entry.
EVT_RETIREMENT_PROPOSED = "tutor_profile_retirement_proposed"
EVT_ENTRY_RETIRED = "tutor_profile_entry_retired"
EVT_RETIREMENT_REJECTED = "tutor_profile_retirement_rejected"

# ── Subject scoping ─────────────────────────────────────────────────
# Conservative content-to-subject mapping. An explanation_style entry
# about fractions should be judged on math attempts, not reading. We
# detect a subject family from keywords in the entry content; if zero
# families match, or more than one does (ambiguous), we fall back to ALL
# attempts and record subject_scope="all" on the observation. When in
# doubt, measure on everything and say so. Matching is whole-word,
# case-insensitive, and deliberately small: a wrong narrow scope is worse
# than an honest wide one.
SUBJECT_SCOPE_ALL = "all"
SUBJECT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "math": (
        "math",
        "maths",
        "mathematics",
        "arithmetic",
        "fraction",
        "fractions",
        "decimal",
        "decimals",
        "multiplication",
        "division",
        "addition",
        "subtraction",
        "geometry",
        "algebra",
        "number",
        "numbers",
        "counting",
        "equation",
        "equations",
    ),
    "reading": (
        "reading",
        "phonics",
        "vocabulary",
        "comprehension",
        "spelling",
        "sight word",
        "sight words",
        "decoding",
    ),
    "writing": (
        "writing",
        "handwriting",
        "essay",
        "essays",
        "grammar",
        "punctuation",
        "composition",
        "paragraph",
    ),
    "science": (
        "science",
        "biology",
        "chemistry",
        "physics",
        "experiment",
        "experiments",
        "ecosystem",
        "molecule",
        "molecules",
    ),
}


def _derive_subject_scope(content: str) -> str:
    """Return the single matched subject family, or "all" when none or
    more than one family is implied (ambiguous, so measure on everything).
    Whole-word, case-insensitive matching."""
    import re

    text = content.lower()
    matched: set[str] = set()
    for family, keywords in SUBJECT_KEYWORDS.items():
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text):
                matched.add(family)
                break
    if len(matched) == 1:
        return matched.pop()
    return SUBJECT_SCOPE_ALL


def _success_rate_query(
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    start: datetime,
    end: datetime,
    subject_scope: str,
):
    """Pure-SQL aggregation: (attempt count, success count) for completed,
    scored attempts whose completed_at falls in [start, end). Success uses
    the reused mastery definition (rating not Again == score >= 0.3). When
    subject_scope is a family, the sample is narrowed to attempts whose
    subject name matches that family's keywords via the
    attempt -> activity -> node -> map -> subject join."""
    success_expr = func.sum(case((Attempt.score >= SUCCESS_MIN_SCORE, 1), else_=0))
    stmt = select(func.count().label("n"), success_expr.label("successes")).where(
        Attempt.child_id == child_id,
        Attempt.household_id == household_id,
        Attempt.status == AttemptStatus.completed,
        Attempt.score.isnot(None),
        Attempt.completed_at >= start,
        Attempt.completed_at < end,
    )
    if subject_scope != SUBJECT_SCOPE_ALL:
        keywords = SUBJECT_KEYWORDS.get(subject_scope, ())
        if keywords:
            # Narrow to attempts whose subject name matches the family,
            # via attempt -> activity -> node -> map -> subject. ILIKE
            # keeps the match case-insensitive and dialect-safe.
            ilike_clauses = [Subject.name.ilike(f"%{kw}%") for kw in keywords]
            stmt = (
                stmt.join(Activity, Activity.id == Attempt.activity_id)
                .join(LearningNode, LearningNode.id == Activity.node_id)
                .join(LearningMap, LearningMap.id == LearningNode.learning_map_id)
                .join(Subject, Subject.id == LearningMap.subject_id)
                .where(or_(*ilike_clauses))
            )
    return stmt


async def _window_stats(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    start: datetime,
    end: datetime,
    subject_scope: str,
) -> tuple[int, float | None]:
    """Return (attempt_count, success_rate or None) for a window."""
    if start >= end:
        return 0, None
    row = (await db.execute(_success_rate_query(child_id, household_id, start, end, subject_scope))).one()
    n = int(row.n or 0)
    if n == 0:
        return 0, None
    successes = int(row.successes or 0)
    return n, successes / n


def _label_for(delta: float | None, gates_met: bool) -> str:
    """One reading's label from its delta. Volume gate dominates: without
    enough attempts there is no honest signal at all."""
    if not gates_met or delta is None:
        return LABEL_INSUFFICIENT_DATA
    if delta >= WORKING_WELL_DELTA:
        return LABEL_WORKING_WELL
    if delta <= OUTGROWN_DELTA:
        return LABEL_MAY_HAVE_OUTGROWN
    return LABEL_NO_CLEAR_EFFECT


def _activation_time(entry: TutorProfileEntry) -> datetime:
    """When the entry began influencing the tutor. decided_at is set both
    when a parent approves (standard) and when the standing grant applies
    (autonomous); proposed_at is the fail-safe fallback."""
    activated = entry.decided_at or entry.proposed_at
    if activated.tzinfo is None:
        activated = activated.replace(tzinfo=UTC)
    return activated


async def evaluate_entry(
    db: AsyncSession,
    entry: TutorProfileEntry,
    now: datetime | None = None,
) -> TutorEntryObservation:
    """Measure one entry and persist exactly one observation row.

    Active window: activation -> now (rolling). Baseline window: the
    period before activation, reaching back at most BASELINE_CAP_DAYS.
    Computes both success rates and their delta, writes the observation,
    and updates the entry's efficacy_label, observations_count, and
    last_evaluated_at. Writes NOTHING else. Returns the observation.
    """
    now = now or datetime.now(UTC)
    activation = _activation_time(entry)
    baseline_start = activation - timedelta(days=BASELINE_CAP_DAYS)

    subject_scope = _derive_subject_scope(entry.content)

    active_n, active_rate = await _window_stats(db, entry.child_id, entry.household_id, activation, now, subject_scope)
    baseline_n, baseline_rate = await _window_stats(
        db, entry.child_id, entry.household_id, baseline_start, activation, subject_scope
    )

    gates_met = active_n >= MIN_ATTEMPTS and baseline_n >= MIN_ATTEMPTS
    delta = (active_rate - baseline_rate) if (active_rate is not None and baseline_rate is not None) else None
    label = _label_for(delta, gates_met)

    observation = TutorEntryObservation(
        household_id=entry.household_id,
        child_id=entry.child_id,
        entry_id=entry.id,
        window_start=activation,
        window_end=now,
        active_attempts=active_n,
        active_success_rate=active_rate,
        baseline_attempts=baseline_n,
        baseline_success_rate=baseline_rate,
        delta=delta,
        subject_scope=subject_scope,
    )
    db.add(observation)

    entry.efficacy_label = label
    entry.observations_count = (entry.observations_count or 0) + 1
    entry.last_evaluated_at = now
    await db.flush()

    logger.info(
        "tutor_entry_evaluated",
        entry_id=str(entry.id),
        household_id=str(entry.household_id),
        child_id=str(entry.child_id),
        label=label,
        active_attempts=active_n,
        baseline_attempts=baseline_n,
        delta=delta,
        subject_scope=subject_scope,
    )
    return observation


# ── Retirement lifecycle (queryable from governance events) ─────────


async def _retirement_lifecycle_events(db: AsyncSession, entry_id: uuid.UUID) -> list[GovernanceEvent]:
    """All retirement lifecycle events for one entry, oldest first."""
    result = await db.execute(
        select(GovernanceEvent)
        .where(
            GovernanceEvent.target_id == entry_id,
            GovernanceEvent.target_type.in_([EVT_RETIREMENT_PROPOSED, EVT_ENTRY_RETIRED, EVT_RETIREMENT_REJECTED]),
        )
        .order_by(GovernanceEvent.created_at.asc(), GovernanceEvent.id.asc())
    )
    return list(result.scalars().all())


async def retirement_pending(db: AsyncSession, entry_id: uuid.UUID) -> bool:
    """True when a retirement proposal is awaiting a decision: the most
    recent lifecycle event is a proposal."""
    events = await _retirement_lifecycle_events(db, entry_id)
    return bool(events) and events[-1].target_type == EVT_RETIREMENT_PROPOSED


async def _can_propose_retirement(db: AsyncSession, entry: TutorProfileEntry) -> bool:
    """Lifetime cap: at most MAX_RETIREMENT_PROPOSALS proposals per entry,
    the second only after a rejection. Never while one is pending, never
    once retired."""
    if entry.status == "retired":
        return False
    events = await _retirement_lifecycle_events(db, entry.id)
    if events and events[-1].target_type == EVT_RETIREMENT_PROPOSED:
        return False  # pending: do not duplicate
    proposals = [e for e in events if e.target_type == EVT_RETIREMENT_PROPOSED]
    if len(proposals) >= MAX_RETIREMENT_PROPOSALS:
        return False
    if len(proposals) == 1:
        # A second proposal is allowed only if the first was rejected (and
        # the signal recurred, which is why we are here).
        return any(e.target_type == EVT_RETIREMENT_REJECTED for e in events)
    return True


async def _last_two_observations(db: AsyncSession, entry_id: uuid.UUID) -> list[TutorEntryObservation]:
    result = await db.execute(
        select(TutorEntryObservation)
        .where(TutorEntryObservation.entry_id == entry_id)
        .order_by(TutorEntryObservation.created_at.desc(), TutorEntryObservation.id.desc())
        .limit(2)
    )
    return list(result.scalars().all())


def _is_outgrown_reading(obs: TutorEntryObservation) -> bool:
    gates_met = obs.active_attempts >= MIN_ATTEMPTS and obs.baseline_attempts >= MIN_ATTEMPTS
    return gates_met and obs.delta is not None and obs.delta <= OUTGROWN_DELTA


async def _two_consecutive_outgrown(db: AsyncSession, entry_id: uuid.UUID) -> list[TutorEntryObservation]:
    """The two most recent observations when both are may_have_outgrown
    readings, else an empty list."""
    last_two = await _last_two_observations(db, entry_id)
    if len(last_two) == 2 and all(_is_outgrown_reading(o) for o in last_two):
        return last_two
    return []


def _retirement_reason(entry: TutorProfileEntry, recent: list[TutorEntryObservation]) -> str:
    """Plain-language, parent-first. Renders readably as a queue item and
    carries the two deltas and sample sizes the proposal is built on."""
    parts = []
    for obs in recent:
        a = obs.active_success_rate if obs.active_success_rate is not None else 0.0
        b = obs.baseline_success_rate if obs.baseline_success_rate is not None else 0.0
        parts.append(
            f"{a * 100:.0f}% on {obs.active_attempts} recent attempts vs "
            f"{b * 100:.0f}% on {obs.baseline_attempts} before (delta {obs.delta * 100:+.0f} points)"
        )
    evidence = "; ".join(parts)
    return (
        f"The tutor thinks this strategy may no longer help: {entry.content} "
        f"Two recent checks both came back lower: {evidence}. This is a signal, not proof."
    )


async def maybe_propose_retirement(
    db: AsyncSession,
    entry: TutorProfileEntry,
) -> TutorProfileEntry | None:
    """If the entry has two consecutive may_have_outgrown readings and the
    lifetime cap allows it, build a retire_entry proposal and route it
    through the autonomy policy. Routing (queue / apply / drop) is
    route_proposal's job; off proposes nothing. Returns the routed entry
    or None."""
    recent = await _two_consecutive_outgrown(db, entry.id)
    if not recent:
        return None
    if not await _can_propose_retirement(db, entry):
        return None
    proposal = {
        "action": "retire_entry",
        "entry_id": str(entry.id),
        "reason": _retirement_reason(entry, recent),
        "deltas": [o.delta for o in recent],
        "sample_sizes": [[o.active_attempts, o.baseline_attempts] for o in recent],
    }
    return await route_proposal(db, entry.household_id, entry.child_id, proposal)


async def maybe_propose_tier_lag_retirement(
    db: AsyncSession,
    entry: TutorProfileEntry,
    now: datetime | None = None,
) -> TutorProfileEntry | None:
    """Propose retiring an active entry whose stamped tier_band sits
    TIER_LAG_THRESHOLD or more tiers below the child's current content
    tier: a strategy tied to a developmental stage the child has left.

    Routes through the same retire_entry path and honors the same lifetime
    rules (one pending at a time, at most two ever, second only after a
    rejection). The reason names both stages. Independent of efficacy
    readings: a strategy can still be working and yet belong to an outgrown
    stage. Fail closed: an unresolvable current tier proposes nothing.
    """
    from app.services.tutor_register import current_tier_for_child, tier_lag

    stamped = entry.tier_band
    if entry.status != "active" or stamped is None or stamped not in VALID_LEVELS:
        return None
    if not await _can_propose_retirement(db, entry):
        return None
    current = await current_tier_for_child(db, entry.child_id)
    if current is None or current not in VALID_LEVELS:
        return None
    lag = tier_lag(current, stamped)
    if lag is None or lag < TIER_LAG_THRESHOLD:
        return None
    reason = (
        f"Outgrown stage: this strategy was learned at the {LEARNING_LEVELS[stamped]['label']} "
        f"stage and the learner is now at the {LEARNING_LEVELS[current]['label']} stage."
    )
    proposal = {
        "action": "retire_entry",
        "entry_id": str(entry.id),
        "reason": reason,
        "deltas": None,
        "sample_sizes": None,
    }
    return await route_proposal(db, entry.household_id, entry.child_id, proposal)


async def decide_retirement(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    entry_id: uuid.UUID,
    action: str,
    user_id: uuid.UUID,
) -> TutorProfileEntry:
    """Parent decision on a queued (standard) retirement proposal.

    approve: the entry is retired (never injected again, never deleted),
    logged as tutor_profile_entry_retired. reject: the entry stays active,
    logged as tutor_profile_retirement_rejected, and the signal may
    propose once more if it recurs. Lives here, not in tutor_profile.py,
    because that module is the entry CREATION writer; this is the
    efficacy subsystem owning the retirement it proposed. It mutates
    status but never constructs an entry, so the construction writer guard
    still holds.
    """
    from app.services.tutor_profile import TutorProfileStateError, TutorProfileValidationError

    if action not in ("approve", "reject"):
        raise TutorProfileValidationError("action must be approve or reject")

    entry = (
        await db.execute(
            select(TutorProfileEntry).where(
                TutorProfileEntry.id == entry_id,
                TutorProfileEntry.household_id == household_id,
                TutorProfileEntry.child_id == child_id,
            )
        )
    ).scalar_one_or_none()
    if entry is None:
        raise LookupError("Entry not found")
    if not await retirement_pending(db, entry_id):
        raise TutorProfileStateError("No retirement proposal is pending for this entry")

    if action == "approve":
        entry.status = "retired"
        entry.decided_at = datetime.now(UTC)
        entry.decided_by = user_id
        await db.flush()
        await log_governance_event(
            db,
            household_id,
            user_id,
            GovernanceAction.approve,
            EVT_ENTRY_RETIRED,
            entry.id,
            reason=f"Parent retired tutor memory entry the child outgrew: {entry.content[:120]}",
            metadata={"child_id": str(child_id), "category": entry.category, "via": "standard_approval"},
        )
        logger.info(
            "tutor_profile_entry_retired",
            entry_id=str(entry.id),
            household_id=str(household_id),
            child_id=str(child_id),
            user_id=str(user_id),
            via="standard_approval",
        )
        return entry

    await log_governance_event(
        db,
        household_id,
        user_id,
        GovernanceAction.reject,
        EVT_RETIREMENT_REJECTED,
        entry.id,
        reason=f"Parent kept tutor memory entry despite efficacy signal: {entry.content[:120]}",
        metadata={"child_id": str(child_id), "category": entry.category},
    )
    logger.info(
        "tutor_profile_retirement_rejected",
        entry_id=str(entry.id),
        household_id=str(household_id),
        child_id=str(child_id),
        user_id=str(user_id),
    )
    return entry


# ── Weekly batch ────────────────────────────────────────────────────


async def evaluate_tutor_entries(db: AsyncSession, now: datetime | None = None) -> dict:
    """Evaluate every active tutor profile entry across all households.

    Idempotent and bounded: entries evaluated within EVAL_COOLDOWN_DAYS
    are skipped, so a re-run in the same week barely touches the database.
    One structlog summary line per household. Sets the RLS tenant per
    household before touching its rows. Returns an aggregate summary.
    """
    now = now or datetime.now(UTC)
    cutoff = now - timedelta(days=EVAL_COOLDOWN_DAYS)
    from app.core.database import set_tenant

    household_rows = await db.execute(
        select(TutorProfileEntry.household_id)
        .where(
            TutorProfileEntry.status == "active",
            (TutorProfileEntry.last_evaluated_at.is_(None)) | (TutorProfileEntry.last_evaluated_at < cutoff),
        )
        .distinct()
    )
    household_ids = [row[0] for row in household_rows.all()]

    totals = {"households": 0, "entries_evaluated": 0, "proposals": 0, "skipped": 0}
    for household_id in household_ids:
        await set_tenant(db, household_id)
        entries_result = await db.execute(
            select(TutorProfileEntry).where(
                TutorProfileEntry.household_id == household_id,
                TutorProfileEntry.status == "active",
            )
        )
        entries = list(entries_result.scalars().all())

        evaluated = 0
        proposals = 0
        skipped = 0
        labels: dict[str, int] = {}
        for entry in entries:
            last = entry.last_evaluated_at
            if last is not None:
                if last.tzinfo is None:
                    last = last.replace(tzinfo=UTC)
                if last >= cutoff:
                    skipped += 1
                    continue
            observation = await evaluate_entry(db, entry, now=now)
            evaluated += 1
            label = entry.efficacy_label or LABEL_INSUFFICIENT_DATA
            labels[label] = labels.get(label, 0) + 1
            if observation.delta is not None and _is_outgrown_reading(observation):
                routed = await maybe_propose_retirement(db, entry)
                if routed is not None:
                    proposals += 1
            # Tier-lag retirement (independent of efficacy): a strategy two
            # or more tiers below the child's current stage. Honors the same
            # lifetime cap, so it will not double-propose alongside the
            # efficacy retirement above (that one leaves a pending proposal).
            tier_routed = await maybe_propose_tier_lag_retirement(db, entry, now=now)
            if tier_routed is not None:
                proposals += 1

        await db.commit()
        totals["households"] += 1
        totals["entries_evaluated"] += evaluated
        totals["proposals"] += proposals
        totals["skipped"] += skipped
        logger.info(
            "tutor_efficacy_household_evaluated",
            household_id=str(household_id),
            entries_evaluated=evaluated,
            retirement_proposals=proposals,
            skipped=skipped,
            labels=labels,
        )

    logger.info("tutor_efficacy_batch_complete", **totals)
    return totals


def run_tutor_efficacy_sync() -> dict:
    """Synchronous entry point for the Celery task."""
    return asyncio.run(_run_batch())


async def _run_batch() -> dict:
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

    from app.core.config import settings

    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    try:
        async with SessionLocal() as db:
            return await evaluate_tutor_entries(db)
    finally:
        await engine.dispose()
