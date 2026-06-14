"""Annual Curriculum service.

Generates 36-week year-long curricula, materializes them into
Plan/PlanWeek/Activity records, tracks week completion, and
maintains the historical record of planned vs actual.
"""

import bisect
import hashlib
import json
import logging
import uuid
from datetime import UTC, date, datetime, timedelta

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.gateway import AIRole, call_ai
from app.ai.prompts import build_philosophical_constraints
from app.models.annual_curriculum import AnnualCurriculum
from app.models.curriculum import LearningEdge, LearningNode
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    GovernanceAction,
    PlanStatus,
)
from app.models.governance import Activity, Attempt, Plan, PlanWeek
from app.models.identity import Child, ChildPreferences, Household

logger = logging.getLogger("methean.annual_curriculum")
slog = structlog.get_logger()


class MaterializationError(Exception):
    """A curriculum approved for materialization produced zero output from a
    populated request.

    Raised instead of silently creating an empty Plan. This means the stored
    ``scope_sequence`` is the wrong shape (e.g. the multi-year ``year_plans``
    mock shape was saved instead of the annual ``weeks[]`` contract), not that
    the plan was intentionally empty. The message names the subject/tier and
    the likely cause so the bad provider output is diagnosable.
    """


def _subject_is_authored(subject_name: str) -> bool:
    """True if scope_sequences defines any topics for this subject (any level).

    Used by the materialization guard to tell a broken shape (an authored
    subject that should have produced weeks) apart from a genuinely empty
    shell for a subject with no authored scope yet.
    """
    try:
        from app.content.scope_sequences import SCOPE_SEQUENCES
        from app.core.learning_levels import SUBJECT_CATALOG
    except ImportError as exc:
        # The authored content modules failing to import is a build
        # defect, not an empty subject: shout, then keep the
        # conservative answer.
        slog.error("scope_sequence_import_failed", error=str(exc))
        return False

    subj_id = subject_name.lower().replace(" ", "_").replace("&", "and")
    for cat in SUBJECT_CATALOG.values():
        for s in cat:
            if s["name"].lower() == subject_name.lower() or s["id"] == subj_id:
                subj_id = s["id"]
                break
    return bool(SCOPE_SEQUENCES.get(subj_id))


def _resolve_subject_id(subject_name: str) -> str:
    """Map a subject display name to its scope_sequences subject_id."""
    from app.core.learning_levels import SUBJECT_CATALOG

    subj_id = subject_name.lower().replace(" ", "_").replace("&", "and")
    for cat in SUBJECT_CATALOG.values():
        for s in cat:
            if s["name"].lower() == subject_name.lower() or s["id"] == subj_id:
                return s["id"]
    return subj_id


def _level_is_generatable(subject_id: str, level: str) -> bool:
    """True when subject_id+level has at least one scope topic backed by a wired
    content template, so it resolves to real focus_nodes rather than an empty
    needs_content shell.

    Pure and synchronous: reads only scope_sequences and the TEMPLATES registry
    (through the node_resolver's pure helpers). It authors no content and
    touches no DB.
    """
    from app.content.scope_sequences import get_scope_sequence
    from app.services.node_resolver import resolve_ref_to_content_id, template_for_content_id

    for topic in get_scope_sequence(subject_id, level):
        ref = topic.get("ref")
        if not ref:
            continue
        content_id = resolve_ref_to_content_id(ref)
        if content_id is not None and template_for_content_id(content_id) is not None:
            return True
    return False


def _resolve_generatable_level(subject_name: str, subject_id: str, level: str) -> str:
    """Return a tier with generatable content for this subject.

    If ``level`` already resolves to wired content, it is returned unchanged. If
    not, fall back to the populated default tier (foundational) when that tier
    is itself generatable for the subject, emitting a structured fallback event
    so the substitution is transparent. If neither the requested level nor the
    default is generatable (a genuinely unauthored subject, e.g. science today),
    the requested level is returned untouched so the materialize loud-failure
    guard keeps its warn-vs-raise distinction. No content is fabricated here.
    """
    from app.core.learning_levels import DEFAULT_LEVEL

    if _level_is_generatable(subject_id, level):
        return level
    if level != DEFAULT_LEVEL and _level_is_generatable(subject_id, DEFAULT_LEVEL):
        slog.info(
            "annual_curriculum.tier_fallback",
            subject=subject_name,
            subject_id=subject_id,
            requested_level=level,
            fallback_level=DEFAULT_LEVEL,
        )
        return DEFAULT_LEVEL
    return level


ANNUAL_CURRICULUM_SYSTEM = """You are METHEAN's Annual Curriculum Architect.

You design COMPLETE year-long scope-and-sequence plans for individual subjects.
Each plan covers exactly {total_weeks} weeks of instruction.

RULES:
- Produce exactly {total_weeks} weeks of content
- For each week: title, learning objectives, 3-5 daily activities (Mon-Fri), assessment focus
- Activities must have: title, type (lesson/practice/assessment/review/project), minutes, day
- Respect the DAG order: prerequisite nodes MUST come before dependent nodes
- Every 6th week is a REVIEW week (lighter, consolidation + formal assessment checkpoint)
- Be realistic: 3-5 nodes per week maximum for elementary, 2-4 for secondary
- Include varied activity types: hands-on, reading, discussion, practice, creative
- Total weekly minutes should approximate the hours_per_week budget
- Assessment checkpoints every 6 weeks with specific criteria

{philosophical_constraints}

OUTPUT FORMAT (JSON):
{{
  "overview": "Year-long narrative of curriculum coverage",
  "philosophy_alignment": "How this curriculum reflects family values",
  "materials": ["resource types needed"],
  "weeks": [
    {{
      "week_number": 1,
      "title": "Week title",
      "focus_nodes": ["node-id-1"],
      "objectives": ["objective 1", "objective 2"],
      "suggested_activities": [
        {{"title": "Activity name", "type": "lesson", "minutes": 25, "day": "Monday", "description": "Brief description"}},
        ...
      ],
      "assessment_focus": "What to evaluate this week",
      "parent_notes_placeholder": ""
    }},
    ...
  ]
}}
"""


async def generate_annual_curriculum(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    user_id: uuid.UUID,
    subject_name: str,
    academic_year: str,
    learning_map_id: uuid.UUID | None = None,
    hours_per_week: float = 4.0,
    total_weeks: int = 36,
    start_date: date | None = None,
    scope_notes: str | None = None,
    content_tier: str | None = None,
) -> AnnualCurriculum:
    """Generate a complete year-long curriculum for one subject."""

    # Fetch child profile
    child_result = await db.execute(select(Child).where(Child.id == child_id))
    child = child_result.scalar_one()

    prefs_result = await db.execute(select(ChildPreferences).where(ChildPreferences.child_id == child_id))
    prefs = prefs_result.scalar_one_or_none()

    # Fetch household philosophical profile
    h_result = await db.execute(select(Household).where(Household.id == household_id))
    household = h_result.scalar_one()
    phil = household.philosophical_profile or {}

    # Read academic calendar
    from app.services.academic_calendar import calculate_end_date, get_academic_calendar, get_instruction_days

    calendar = await get_academic_calendar(db, household_id)
    if total_weeks == 36:
        total_weeks = calendar.get("total_instructional_weeks", 36)
    instruction_days = get_instruction_days(calendar)
    days_per_week = len(instruction_days)

    # Calculate dates
    if not start_date:
        cal_start = calendar.get("start_date")
        if cal_start:
            start_date = date.fromisoformat(cal_start) if isinstance(cal_start, str) else cal_start
        else:
            today = date.today()
            year = today.year if today.month < 7 else today.year + 1
            start_date = date(year, 9, 1)
    end_date = calculate_end_date(start_date, total_weeks, calendar)

    child_age = (date.today() - child.date_of_birth).days / 365.25 if child.date_of_birth else 6

    # Learning level for AI prompt. If the caller explicitly chose a
    # content tier in the picker, honor it; otherwise fall back to the
    # child's saved per-subject level (which itself defaults to the
    # populated foundational tier). Unknown values are coerced to the safe
    # DEFAULT_LEVEL rather than raising, so a stale client sending a value we
    # no longer recognize still generates something.
    from app.core.learning_levels import DEFAULT_LEVEL, LEARNING_LEVELS, VALID_LEVELS, get_level_for_subject

    if content_tier and content_tier in VALID_LEVELS:
        requested_level = content_tier
    else:
        requested_level = get_level_for_subject(prefs, subject_name)

    # Resolve the scope_sequences subject_id once (reused below) and apply the
    # fallback-safety guard: a requested tier with no wired content for this
    # subject falls back to the populated foundational tier so the parent never
    # silently lands on an empty plan. The fallback is logged transparently.
    subj_id = _resolve_subject_id(subject_name)
    level = _resolve_generatable_level(subject_name=subject_name, subject_id=subj_id, level=requested_level)
    level_info = LEARNING_LEVELS.get(level, LEARNING_LEVELS[DEFAULT_LEVEL])

    # Fetch learning map nodes in topological order if provided
    nodes_description = ""
    if learning_map_id:
        nodes_result = await db.execute(
            select(LearningNode)
            .where(LearningNode.learning_map_id == learning_map_id, LearningNode.is_active.is_(True))
            .order_by(LearningNode.sort_order)
        )
        nodes = nodes_result.scalars().all()
        edges_result = await db.execute(select(LearningEdge).where(LearningEdge.learning_map_id == learning_map_id))
        edges = edges_result.scalars().all()

        # Build topological description
        node_list = []
        for n in nodes:
            prereqs = [e.from_node_id for e in edges if str(e.to_node_id) == str(n.id)]
            prereq_titles = [next((nn.title for nn in nodes if str(nn.id) == str(p)), "?") for p in prereqs]
            node_list.append(
                f"- {n.id}: {n.title} (type={n.node_type.value}, "
                f"est_minutes={n.estimated_minutes or 30}, "
                f"prereqs=[{', '.join(prereq_titles)}])"
            )
        nodes_description = f"""
LEARNING MAP NODES (teach in this order, respecting prerequisites):
{chr(10).join(node_list)}

Use these node IDs in the focus_nodes field for each week."""

    # Build philosophical constraints
    phil_constraints = build_philosophical_constraints(phil)

    # Inject scope sequence context for pedagogically grounded curriculum.
    # subj_id and level were resolved (with fallback) above.
    scope_sequence_context = ""
    try:
        from app.content.scope_sequences import get_scope_sequence

        topics = get_scope_sequence(subj_id, level)
        if topics:
            topic_lines = []
            for t in topics:
                prereqs = ", ".join(t.get("prerequisites", [])) or "none"
                concepts = ", ".join(t.get("key_concepts", [])[:5])
                topic_lines.append(
                    f"  {t['ref']}: {t['title']} (prereqs: [{prereqs}], ~{t.get('estimated_weeks', 1)}wk, concepts: {concepts})"
                )
            scope_sequence_context = f"""
SCOPE AND SEQUENCE ({len(topics)} topics in pedagogical order for {level} level):
Follow this topic order. Respect prerequisites. Do NOT skip or reorder topics.
{chr(10).join(topic_lines)}
"""
    except Exception as exc:
        slog.warning(
            "scope_sequence_context_failed",
            subject=subject_name,
            level=level,
            error=str(exc),
        )

    # Detect vocational subject and use appropriate prompt
    from app.core.learning_levels import SUBJECT_CATALOG

    vocational_names = {s["name"].lower() for s in SUBJECT_CATALOG.get("vocational", [])}
    vocational_ids = {s["id"] for s in SUBJECT_CATALOG.get("vocational", [])}
    is_vocational = subject_name.lower() in vocational_names or subject_name.lower().replace(" ", "_") in vocational_ids

    if is_vocational:
        from app.ai.prompts import VOCATIONAL_CURRICULUM_SYSTEM

        system_prompt = VOCATIONAL_CURRICULUM_SYSTEM
    else:
        system_prompt = ANNUAL_CURRICULUM_SYSTEM.format(
            total_weeks=total_weeks,
            philosophical_constraints=phil_constraints,
        )

    user_prompt = f"""Design a complete {total_weeks}-week curriculum for:

SUBJECT: {subject_name}
ACADEMIC YEAR: {academic_year}

CHILD PROFILE:
- Name: {child.first_name}
- Age: {child_age:.1f} years
- Learning level for {subject_name}: {level_info["label"]} — {level_info["ai_instruction"]}
- Age: {child_age:.0f} (developmental context only)
- Learning style: {json.dumps(prefs.learning_style if prefs else {}, default=str)}
- Interests: {json.dumps(prefs.interests if prefs else [], default=str)}
- Accommodations: {json.dumps(prefs.accommodations if prefs else {}, default=str)}

TIME BUDGET: {hours_per_week} hours per week ({hours_per_week * 60:.0f} minutes)
TOTAL WEEKS: {total_weeks}
INSTRUCTION DAYS: {days_per_week} days per week ({", ".join(d.capitalize() for d in instruction_days)})
START DATE: {start_date}
{nodes_description}
{scope_sequence_context}
{f"ADDITIONAL GUIDANCE FROM PARENT: {scope_notes}" if scope_notes else ""}

Generate the complete {total_weeks}-week scope and sequence."""

    ai_result = await call_ai(
        db,
        role=AIRole.education_architect,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        household_id=household_id,
        triggered_by=user_id,
        philosophical_profile=phil,
        max_tokens=8000,
    )

    output = ai_result["output"] if isinstance(ai_result["output"], dict) else {}

    curriculum = AnnualCurriculum(
        household_id=household_id,
        child_id=child_id,
        learning_map_id=learning_map_id,
        created_by=user_id,
        subject_name=subject_name,
        academic_year=academic_year,
        grade_level=child.grade_level,
        total_weeks=total_weeks,
        hours_per_week=hours_per_week,
        start_date=start_date,
        end_date=end_date,
        scope_sequence=output,
        status="draft",
        ai_run_id=ai_result.get("ai_run_id"),
        actual_record={"weeks": {}},
    )
    db.add(curriculum)
    await db.flush()

    from app.services.governance import log_governance_event

    await log_governance_event(
        db,
        household_id,
        user_id,
        GovernanceAction.modify,
        "annual_curriculum",
        curriculum.id,
        reason=f"Annual curriculum generated: {subject_name} {academic_year}",
    )

    return curriculum


async def approve_annual_curriculum(
    db: AsyncSession,
    curriculum_id: uuid.UUID,
    user_id: uuid.UUID,
    household_id: uuid.UUID,
) -> AnnualCurriculum:
    """Parent approves the curriculum. Materializes ALL weeks immediately."""
    result = await db.execute(
        select(AnnualCurriculum).where(
            AnnualCurriculum.id == curriculum_id,
            AnnualCurriculum.household_id == household_id,
        )
    )
    curriculum = result.scalar_one_or_none()
    if not curriculum:
        raise ValueError("Curriculum not found")
    if curriculum.status != "draft":
        raise ValueError(f"Cannot approve curriculum in '{curriculum.status}' status")

    curriculum.status = "active"
    curriculum.approved_at = datetime.now(UTC)
    curriculum.approved_by = user_id

    from app.services.governance import log_governance_event

    await log_governance_event(
        db,
        household_id,
        user_id,
        GovernanceAction.approve,
        "annual_curriculum",
        curriculum.id,
        reason=f"Annual curriculum approved: {curriculum.subject_name} {curriculum.academic_year}",
    )

    # Materialize full year
    await materialize_full_year(db, curriculum)

    # Queue background enrichment for associated learning map
    try:
        if curriculum.learning_map_id:
            from app.tasks.worker import enrich_map_task

            enrich_map_task.delay(str(curriculum.learning_map_id), str(household_id))
    except Exception as exc:
        slog.warning(
            "enrichment_queue_failed",
            learning_map_id=str(curriculum.learning_map_id),
            household_id=str(household_id),
            error=str(exc),
        )

    return curriculum


# ── Calendar-aware date layout ────────────────────────────────────

# Canonical weekday offsets from the start of an instructional week. The
# materializer treats a curriculum's ``start_date`` (and each week's anchor)
# as offset 0, so a default Monday-Friday calendar reproduces the prior
# ``start_date + day_offset`` placement exactly, while a custom
# ``instruction_days`` cadence shifts placement onto the configured days.
_DAY_TO_OFFSET: dict[str, int] = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def _calendar_version(calendar: dict) -> str:
    """Stable SHA-256 hash of a resolved calendar, for drift detection and
    governance-event traceability. Independent of key order."""
    canonical = json.dumps(calendar, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()


def _instruction_offsets(calendar: dict) -> list[int]:
    """Sorted weekday offsets (Mon=0..Sun=6) for the configured instruction
    days. Falls back to Monday-Friday when nothing usable is configured so a
    week never has zero teaching days."""
    from app.services.academic_calendar import get_instruction_days

    offsets = sorted({_DAY_TO_OFFSET[d.lower()] for d in get_instruction_days(calendar) if d.lower() in _DAY_TO_OFFSET})
    return offsets or [0, 1, 2, 3, 4]


def _place_offset(live_offsets: dict[int, date], canonical_offset: int) -> date:
    """Map a canonical weekday offset (the activity's authored day) onto a real
    instruction date for the week.

    If the offset is itself an available instruction day, the activity lands on
    that exact day. Otherwise it is clamped to the nearest available instruction
    day by position, so a Friday activity on a Mon-Thu cadence lands on
    Thursday and a Monday activity on a Tue-Sat cadence lands on Tuesday.
    Activities therefore never land on a non-instruction or break day.
    """
    if canonical_offset in live_offsets:
        return live_offsets[canonical_offset]
    avail = sorted(live_offsets)
    pos = bisect.bisect_right(avail, canonical_offset)
    idx = min(pos, len(avail) - 1)
    return live_offsets[avail[idx]]


def _lay_weeks(
    first_week_start: date,
    calendar: dict,
    week_numbers: list[int],
) -> dict[int, tuple[date, date, dict[int, date]]]:
    """Lay instructional weeks forward onto real dates, mirroring the weekly
    planner's calendar handling (is_break_date + instruction_days).

    Walks consecutive 7-day windows from ``first_week_start`` (treated as offset
    0). For each curriculum week it materializes the configured instruction
    days, dropping any that fall inside a break. A calendar week whose every
    instruction day is a break is skipped entirely (it does not consume a
    curriculum week), so a break shifts dates and extends the calendar end
    without ever deleting a curriculum week.

    Returns ``{week_number: (week_start, week_end, {offset: date})}`` where the
    offset map holds the live (non-break) instruction dates for that week.
    """
    from app.services.academic_calendar import is_break_date

    offsets = _instruction_offsets(calendar)
    schedule: dict[int, tuple[date, date, dict[int, date]]] = {}
    week_start = first_week_start

    for wn in week_numbers:
        candidate: dict[int, date] = {}
        live: dict[int, date] = {}
        # Skip fully-break calendar weeks (guard bounds the walk).
        for _ in range(200):
            candidate = {o: week_start + timedelta(days=o) for o in offsets}
            live = {o: d for o, d in candidate.items() if not is_break_date(calendar, d)}
            if live:
                break
            week_start += timedelta(days=7)
        else:
            # Pathological all-break stretch: keep the curriculum week rather
            # than dropping it, so the instructional week count is preserved.
            live = candidate
        dates = list(live.values())
        schedule[wn] = (min(dates), max(dates), live)
        week_start += timedelta(days=7)

    return schedule


def _activity_reflowable(activity: Activity, today: date) -> bool:
    """True only for strictly-future, untouched scheduled activities.

    Locked (returns False) when work has begun or finished
    (in_progress/completed), the activity is a terminal parent decision
    (skipped/cancelled), or it is scheduled for today or earlier. Governance
    approval is deliberately NOT a lock signal: it is set automatically by the
    near-window auto-approval at materialization and does not represent a
    deliberate parent lock, so using it would pin the parent's own calendar
    edits in the common editing case.
    """
    if activity.status != ActivityStatus.scheduled:
        return False
    return activity.scheduled_date is not None and activity.scheduled_date > today


def _canonical_offset_for_activity(activity: Activity, week: PlanWeek, week_data: dict | None) -> int:
    """Recover the canonical weekday offset (Mon=0) an activity was authored
    for, so a re-flow places it on the same logical day under the new calendar.

    Primary source is the immutable scope_sequence (the authored ``day`` matched
    by sort_order), which is stable across re-flows. Parent-added activities are
    not in the scope_sequence, so fall back to the activity's current offset
    within its (pre-re-flow) week.
    """
    suggested = week_data.get("suggested_activities", []) if week_data else []
    if 0 <= activity.sort_order < len(suggested):
        name = str(suggested[activity.sort_order].get("day", "Monday")).lower()
        if name in _DAY_TO_OFFSET:
            return _DAY_TO_OFFSET[name]
    if activity.scheduled_date is not None:
        delta = (activity.scheduled_date - week.start_date).days
        if 0 <= delta <= 6:
            return delta
    return 0


async def reflow_curriculum_plan(
    db: AsyncSession,
    curriculum: AnnualCurriculum,
    calendar: dict,
    user_id: uuid.UUID | None,
    today: date | None = None,
) -> dict | None:
    """Re-flow the future, uncompleted portion of a materialized plan onto a
    (possibly edited) household academic calendar.

    Completed/in-progress/terminal and past/same-day activities are immutable
    and preserved byte-for-byte. Only weeks whose every non-cancelled activity
    is strictly-future-and-scheduled are re-dated, walking the calendar forward
    from the end of the last preserved week so a locked week never collides with
    a re-dated one and dates stay monotonic. The resolved calendar snapshot and
    version are refreshed when (and only when) a re-flow actually happens.

    Returns a summary dict, or None when the curriculum has no materialized plan.
    """
    from sqlalchemy.orm import selectinload

    today = today or date.today()

    plan_result = await db.execute(
        select(Plan)
        .where(Plan.annual_curriculum_id == curriculum.id)
        .options(selectinload(Plan.weeks).selectinload(PlanWeek.activities))
    )
    plan = plan_result.scalars().first()
    if plan is None:
        return None

    weeks = sorted(plan.weeks, key=lambda w: w.week_number)

    # Classify each week and find the frontier of the immutable (preserved)
    # past. A week is re-flowable only if it has activities and every
    # non-cancelled one is strictly-future-and-scheduled.
    reflowable_wn: dict[int, bool] = {}
    last_preserved_wn = 0
    for w in weeks:
        non_cancelled = [a for a in w.activities if a.status != ActivityStatus.cancelled]
        is_reflowable = bool(non_cancelled) and all(_activity_reflowable(a, today) for a in non_cancelled)
        reflowable_wn[w.week_number] = is_reflowable
        if not is_reflowable:
            last_preserved_wn = max(last_preserved_wn, w.week_number)

    # Only weeks strictly after the last preserved week are re-flowed.
    target_weeks = [w for w in weeks if w.week_number > last_preserved_wn and reflowable_wn[w.week_number]]
    preserved_count = len(weeks) - len(target_weeks)

    if not target_weeks:
        return {
            "plan_id": str(plan.id),
            "weeks_reflowed": 0,
            "weeks_preserved_locked": preserved_count,
            "calendar_version": _calendar_version(calendar),
        }

    # Anchor: the calendar week after the last preserved week, else the
    # calendar's start (a new start_date wins for a fully-future plan).
    if last_preserved_wn:
        anchor_week = next(w for w in weeks if w.week_number == last_preserved_wn)
        first_week_start = anchor_week.start_date + timedelta(days=7)
    else:
        cal_start = calendar.get("start_date")
        if cal_start:
            first_week_start = date.fromisoformat(cal_start) if isinstance(cal_start, str) else cal_start
        else:
            first_week_start = curriculum.start_date

    scope_by_wn = {w.get("week_number"): w for w in (curriculum.scope_sequence or {}).get("weeks", [])}
    schedule = _lay_weeks(first_week_start, calendar, [w.week_number for w in target_weeks])

    for w in target_weeks:
        ws, we, live = schedule[w.week_number]
        week_data = scope_by_wn.get(w.week_number)
        # Resolve canonical offsets BEFORE overwriting the week's old dates,
        # since the parent-added fallback measures against the old week start.
        placements = [
            (a, _canonical_offset_for_activity(a, w, week_data)) for a in w.activities if _activity_reflowable(a, today)
        ]
        w.start_date = ws
        w.end_date = we
        for a, canonical in placements:
            a.scheduled_date = _place_offset(live, canonical)

    await db.flush()

    return {
        "plan_id": str(plan.id),
        "weeks_reflowed": len(target_weeks),
        "weeks_preserved_locked": preserved_count,
        "calendar_version": _calendar_version(calendar),
        "new_end_date": max(w.end_date for w in target_weeks).isoformat(),
    }


async def reflow_household_active_curricula(
    db: AsyncSession,
    household_id: uuid.UUID,
    user_id: uuid.UUID | None,
    calendar: dict,
    today: date | None = None,
) -> list[dict]:
    """Apply a household calendar edit to every active curriculum's plan.

    Re-flows only the future/uncompleted portion of each plan (see
    reflow_curriculum_plan), refreshes the curriculum's calendar snapshot, and
    emits one ``modify`` governance event per plan that actually moved, carrying
    the calendar version and the re-flowed/preserved counts.
    """
    from app.services.governance import log_governance_event

    version = _calendar_version(calendar)
    result = await db.execute(
        select(AnnualCurriculum).where(
            AnnualCurriculum.household_id == household_id,
            AnnualCurriculum.status == "active",
        )
    )
    curricula = result.scalars().all()

    summaries: list[dict] = []
    for curriculum in curricula:
        summary = await reflow_curriculum_plan(db, curriculum, calendar, user_id, today=today)
        if summary is None:
            continue
        summaries.append({"curriculum_id": str(curriculum.id), **summary})
        if summary["weeks_reflowed"] == 0:
            continue

        # The snapshot now matches the dates on the plan's future portion.
        curriculum.calendar_snapshot = calendar
        curriculum.calendar_version = version

        slog.info(
            "annual_curriculum.calendar_reflow",
            household_id=str(household_id),
            curriculum_id=str(curriculum.id),
            plan_id=summary["plan_id"],
            calendar_version=version,
            weeks_reflowed=summary["weeks_reflowed"],
            weeks_preserved_locked=summary["weeks_preserved_locked"],
        )
        await log_governance_event(
            db,
            household_id,
            user_id,
            GovernanceAction.modify,
            "annual_curriculum",
            curriculum.id,
            reason=(
                f"Calendar edit re-flowed {summary['weeks_reflowed']} future week(s) of "
                f"'{curriculum.subject_name}' ({summary['weeks_preserved_locked']} preserved as locked)"
            ),
            metadata={
                "event_type": "calendar_reflow",
                "calendar_version": version,
                "weeks_reflowed": summary["weeks_reflowed"],
                "weeks_preserved_locked": summary["weeks_preserved_locked"],
            },
        )

    return summaries


async def materialize_full_year(
    db: AsyncSession,
    curriculum: AnnualCurriculum,
) -> dict:
    """Create Plan/PlanWeek/Activity records for ALL weeks."""

    scope = curriculum.scope_sequence or {}
    weeks_data = scope.get("weeks", [])

    if not weeks_data:
        # Zero weeks from an approved curriculum. Distinguish a broken shape
        # (raise) from a genuinely-unauthored empty shell (warn). The
        # silent-zero return this replaces hid the year_plans-vs-weeks shape
        # mismatch (see curriculum_pipeline_audit.md, cross-cutting issue 2).
        top_keys = sorted(scope.keys())
        has_year_plans = "year_plans" in scope
        authored = _subject_is_authored(curriculum.subject_name)
        if scope or has_year_plans or authored:
            detail = (
                "Detected 'year_plans' — the multi-year education-plan / mock shape "
                "was stored instead of the annual weeks[] contract. "
                if has_year_plans
                else ""
            )
            raise MaterializationError(
                f"Annual curriculum '{curriculum.subject_name}' "
                f"(grade={curriculum.grade_level}, {curriculum.academic_year}) materialized "
                f"0 weeks: scope_sequence has no usable 'weeks' list "
                f"(top-level keys present: {top_keys}). {detail}"
                f"Expected scope_sequence['weeks'] = [{{week_number, suggested_activities, "
                f"focus_nodes, assessment_focus}}, ...]. Likely cause: the AI provider "
                f"returned the wrong shape (ai_run_id={curriculum.ai_run_id})."
            )
        # Empty scope_sequence ({}) for a subject with no authored scope: nothing
        # to materialize yet. Warn loudly, do not raise.
        logger.warning(
            "annual_curriculum.materialize.empty_unauthored",
            extra={"curriculum_id": str(curriculum.id), "subject": curriculum.subject_name},
        )
        return {"weeks_created": 0, "activities_created": 0}

    # Partial-library signal: weeks authored but some have no resolved content
    # node yet. This is acceptable (the activities still materialize); warn so
    # the gap is visible, do not raise.
    needs_content_weeks = sum(1 for w in weeks_data if w.get("needs_content"))
    if needs_content_weeks:
        logger.warning(
            "annual_curriculum.materialize.needs_content",
            extra={
                "curriculum_id": str(curriculum.id),
                "subject": curriculum.subject_name,
                "needs_content_weeks": needs_content_weeks,
                "total_weeks": len(weeks_data),
            },
        )

    # Zero-activities guard, checked before any rows are written so a broken
    # shape never leaves a half-built empty Plan behind. needs_content weeks
    # still carry (consolidation) activities, so this does not fire for them.
    planned_activities = sum(len(w.get("suggested_activities", [])) for w in weeks_data)
    if planned_activities == 0:
        raise MaterializationError(
            f"Annual curriculum '{curriculum.subject_name}' ({curriculum.academic_year}) has "
            f"{len(weeks_data)} weeks but 0 activities: every week's 'suggested_activities' was "
            f"empty or missing — a broken scope_sequence shape. Expected each week to carry "
            f"suggested_activities=[{{day, type, title, description, minutes}}, ...] "
            f"(ai_run_id={curriculum.ai_run_id})."
        )

    # Load the household academic calendar and snapshot it onto the curriculum
    # so a later calendar edit can detect drift and re-flow deterministically.
    # Weeks/days are laid onto real instruction dates, skipping breaks and
    # honoring the configured cadence, mirroring the weekly planner.
    from app.services.academic_calendar import get_academic_calendar

    calendar = await get_academic_calendar(db, curriculum.household_id)
    curriculum.calendar_snapshot = calendar
    curriculum.calendar_version = _calendar_version(calendar)
    week_numbers = sorted({w.get("week_number", i + 1) for i, w in enumerate(weeks_data)})
    schedule = _lay_weeks(curriculum.start_date, calendar, list(week_numbers))

    # Determine which weeks are "near" (auto-approve governance)
    today = date.today()
    near_threshold = today + timedelta(weeks=4)

    # Create one Plan for the entire curriculum year
    plan = Plan(
        household_id=curriculum.household_id,
        child_id=curriculum.child_id,
        created_by=curriculum.created_by,
        name=f"{curriculum.subject_name} — {curriculum.academic_year}",
        description=curriculum.scope_sequence.get("overview", ""),
        status=PlanStatus.active,
        start_date=curriculum.start_date,
        end_date=curriculum.end_date,
        ai_generated=True,
        ai_run_id=curriculum.ai_run_id,
        annual_curriculum_id=curriculum.id,
    )
    db.add(plan)
    await db.flush()

    activity_type_map = {
        "lesson": ActivityType.lesson,
        "practice": ActivityType.practice,
        "assessment": ActivityType.assessment,
        "review": ActivityType.review,
        "project": ActivityType.project,
        "field_trip": ActivityType.field_trip,
    }

    total_activities = 0

    for i, week_data in enumerate(weeks_data):
        week_num = week_data.get("week_number", i + 1)
        week_start, week_end, live_offsets = schedule[week_num]

        pw = PlanWeek(
            plan_id=plan.id,
            household_id=curriculum.household_id,
            week_number=week_num,
            start_date=week_start,
            end_date=week_end,
            notes=week_data.get("assessment_focus", ""),
        )
        db.add(pw)
        await db.flush()

        is_near = week_start <= near_threshold
        activities = week_data.get("suggested_activities", [])

        for idx, act_data in enumerate(activities):
            day_name = str(act_data.get("day", "Monday")).lower()
            canonical_offset = _DAY_TO_OFFSET.get(day_name, 0)
            scheduled = _place_offset(live_offsets, canonical_offset)

            act_type_str = act_data.get("type", "lesson")
            act_type = activity_type_map.get(act_type_str, ActivityType.lesson)

            activity = Activity(
                plan_week_id=pw.id,
                household_id=curriculum.household_id,
                activity_type=act_type,
                title=act_data.get("title", f"Activity {idx + 1}"),
                description=act_data.get("description", ""),
                estimated_minutes=act_data.get("minutes", 30),
                status=ActivityStatus.scheduled,
                scheduled_date=scheduled,
                sort_order=idx,
                governance_approved=is_near,  # Near weeks auto-approved
            )

            # Link to node if specified
            focus_nodes = week_data.get("focus_nodes", [])
            if focus_nodes:
                try:
                    activity.node_id = uuid.UUID(focus_nodes[min(idx, len(focus_nodes) - 1)])
                except (ValueError, IndexError):
                    pass

            db.add(activity)
            total_activities += 1

    await db.flush()

    return {
        "weeks_created": len(weeks_data),
        "activities_created": total_activities,
        "plan_id": str(plan.id),
    }


async def evaluate_approaching_weeks(
    db: AsyncSession,
    curriculum_id: uuid.UUID,
    weeks_ahead: int = 4,
) -> list:
    """Run governance evaluation on activities in the next N weeks.

    Activities created with governance_approved=False get evaluated
    as their scheduled week approaches. This ensures rule changes
    mid-year are respected for future activities.
    """
    result = await db.execute(select(AnnualCurriculum).where(AnnualCurriculum.id == curriculum_id))
    curriculum = result.scalar_one_or_none()
    if not curriculum or curriculum.status != "active":
        return []

    today = date.today()
    threshold = today + timedelta(weeks=weeks_ahead)

    # Find unapproved activities in the approaching window
    plans_result = await db.execute(select(Plan).where(Plan.annual_curriculum_id == curriculum_id))
    plans = plans_result.scalars().all()
    evaluated = []

    for plan in plans:
        weeks_result = await db.execute(
            select(PlanWeek).where(
                PlanWeek.plan_id == plan.id,
                PlanWeek.start_date <= threshold,
                PlanWeek.start_date >= today,
            )
        )
        weeks = weeks_result.scalars().all()

        for week in weeks:
            acts_result = await db.execute(
                select(Activity).where(
                    Activity.plan_week_id == week.id,
                    Activity.governance_approved.is_(False),
                    Activity.status == ActivityStatus.scheduled,
                )
            )
            activities = acts_result.scalars().all()

            for act in activities:
                # Auto-approve approaching activities
                # In production, this would check governance rules
                act.governance_approved = True
                evaluated.append({"activity_id": str(act.id), "week": week.week_number})

    await db.flush()
    return evaluated


async def record_week_completion(
    db: AsyncSession,
    curriculum_id: uuid.UUID,
    week_number: int,
    parent_notes: str | None = None,
) -> dict:
    """Record what actually happened during a completed week."""
    result = await db.execute(select(AnnualCurriculum).where(AnnualCurriculum.id == curriculum_id))
    curriculum = result.scalar_one_or_none()
    if not curriculum:
        raise ValueError("Curriculum not found")

    # Find the plan and week
    plan_result = await db.execute(select(Plan).where(Plan.annual_curriculum_id == curriculum_id))
    plan = plan_result.scalar_one_or_none()
    if not plan:
        raise ValueError("No plan found for this curriculum")

    week_result = await db.execute(
        select(PlanWeek).where(
            PlanWeek.plan_id == plan.id,
            PlanWeek.week_number == week_number,
        )
    )
    week = week_result.scalar_one_or_none()
    if not week:
        raise ValueError(f"Week {week_number} not found")

    # Fetch all activities and their attempts
    acts_result = await db.execute(select(Activity).where(Activity.plan_week_id == week.id))
    activities = acts_result.scalars().all()

    completed = [a for a in activities if a.status == ActivityStatus.completed]
    skipped = [a for a in activities if a.status in (ActivityStatus.skipped, ActivityStatus.cancelled)]

    total_minutes = 0
    for act in activities:
        attempts_result = await db.execute(select(Attempt).where(Attempt.activity_id == act.id))
        attempts = attempts_result.scalars().all()
        total_minutes += sum(a.duration_minutes or 0 for a in attempts)

    # Build week record
    week_record = {
        "planned_activities": len(activities),
        "completed_activities": len(completed),
        "skipped_activities": len(skipped),
        "total_minutes": total_minutes,
        "parent_notes": parent_notes or "",
    }

    # Update actual_record
    actual = dict(curriculum.actual_record or {})
    weeks = dict(actual.get("weeks", {}))
    weeks[str(week_number)] = week_record
    actual["weeks"] = weeks
    curriculum.actual_record = actual

    # Force SQLAlchemy to detect JSONB change
    from sqlalchemy.orm.attributes import flag_modified

    flag_modified(curriculum, "actual_record")

    await db.flush()
    return week_record


async def get_curriculum_history(
    db: AsyncSession,
    curriculum_id: uuid.UUID,
    week_number: int | None = None,
) -> dict:
    """Get planned vs actual for a curriculum, optionally for one week."""
    result = await db.execute(select(AnnualCurriculum).where(AnnualCurriculum.id == curriculum_id))
    curriculum = result.scalar_one_or_none()
    if not curriculum:
        raise ValueError("Curriculum not found")

    scope = curriculum.scope_sequence
    actual = curriculum.actual_record or {}

    if week_number is not None:
        # Single week detail
        planned_weeks = scope.get("weeks", [])
        planned = next((w for w in planned_weeks if w.get("week_number") == week_number), None)
        actual_week = actual.get("weeks", {}).get(str(week_number), {})

        # Fetch real activities
        plan_result = await db.execute(select(Plan).where(Plan.annual_curriculum_id == curriculum_id))
        plan = plan_result.scalar_one_or_none()
        activities_data = []
        if plan:
            week_result = await db.execute(
                select(PlanWeek).where(
                    PlanWeek.plan_id == plan.id,
                    PlanWeek.week_number == week_number,
                )
            )
            week = week_result.scalar_one_or_none()
            if week:
                acts_result = await db.execute(
                    select(Activity).where(Activity.plan_week_id == week.id).order_by(Activity.sort_order)
                )
                for act in acts_result.scalars().all():
                    activities_data.append(
                        {
                            "id": str(act.id),
                            "title": act.title,
                            "type": act.activity_type.value,
                            "status": act.status.value,
                            "scheduled_date": str(act.scheduled_date) if act.scheduled_date else None,
                            "estimated_minutes": act.estimated_minutes,
                            "governance_approved": act.governance_approved,
                        }
                    )

        return {
            "week_number": week_number,
            "planned": planned,
            "actual": actual_week,
            "activities": activities_data,
        }

    # Full curriculum summary
    planned_weeks = scope.get("weeks", [])
    actual_weeks = actual.get("weeks", {})

    week_summaries = []
    for pw in planned_weeks:
        wn = pw.get("week_number", 0)
        aw = actual_weeks.get(str(wn), {})
        week_summaries.append(
            {
                "week_number": wn,
                "title": pw.get("title", ""),
                "objectives": pw.get("objectives", []),
                "has_actual": bool(aw),
                "completed_activities": aw.get("completed_activities", 0) if aw else None,
                "planned_activities": len(pw.get("suggested_activities", [])),
                "parent_notes": aw.get("parent_notes", "") if aw else None,
            }
        )

    return {
        "curriculum_id": str(curriculum.id),
        "subject_name": curriculum.subject_name,
        "academic_year": curriculum.academic_year,
        "grade_level": curriculum.grade_level,
        "status": curriculum.status,
        "overview": scope.get("overview", ""),
        "total_weeks": curriculum.total_weeks,
        "weeks": week_summaries,
    }
