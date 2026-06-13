"""Tutor relationship memory: milestones DERIVED, never stored.

The most human thing a long term tutor does is remember the journey:
"long division was hard for months, and then it clicked." This module
computes that continuity at context assembly time from evidence the
family already governs (mastery achievements, attempt histories, streaks,
curriculum completions). It creates no new tables and stores no new
truths. It is a computed lens over the hash chained record, cached in
Redis for speed and discarded freely.

DERIVED, NEVER STORED. This module performs ZERO database writes: it
reads existing rows and renders warm continuity lines from a small
authored template set. The selection picks facts; the templates control
tone. The dignity rule is absolute: milestones celebrate persistence and
breakthrough, and NEVER recall failure as failure. No template prints a
raw count of failures or attempts; struggle is spoken in weeks of effort
and in showing up, never in how many times something went wrong.

Source restriction: milestones derive ONLY from mastery, attempt,
curriculum, and streak records. Transcript and voice derived memory is
forbidden. Zero AI calls: pure queries plus templates.

Cache decision: milestones are cached per child under
``tutor_milestones:{child_id}`` with a 24 hour TTL. The toggle path
(enabling or disabling relationship memory) invalidates the key directly
through ``invalidate_milestones`` so a parent's choice takes effect
immediately rather than waiting out the TTL. New mastery events are NOT
wired to an explicit invalidation seam: recording a mastery change runs
through several call sites in the state engine, so a cheap single seam
does not exist, and a fresh breakthrough surfacing within 24 hours is an
acceptable bound for a warm, non authoritative continuity layer. The TTL
is the freshness guarantee for derivation; the toggle invalidation is the
governance guarantee.
"""

import uuid
from dataclasses import asdict, dataclass
from datetime import UTC, datetime

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.achievements import Streak
from app.models.curriculum import ChildMapEnrollment, LearningMap, LearningNode, Subject
from app.models.enums import MasteryLevel, StateEventType
from app.models.governance import Activity, Attempt
from app.models.state import ChildNodeState, StateEvent

logger = structlog.get_logger()

# Mastery levels that count as a reached bar, mirroring the Family
# Record's EVIDENCE_MASTERY_LEVELS so this lens can never celebrate a
# threshold the record itself would not credential.
REACHED_LEVELS = (MasteryLevel.proficient, MasteryLevel.mastered)

# The struggle then click shape: a node counts as a breakthrough when the
# attempt history that preceded reaching the bar spanned real time or real
# persistence. Either gate qualifies.
BREAKTHROUGH_MIN_DAYS = 14
BREAKTHROUGH_MIN_ATTEMPTS = 5

# A streak is "notable" at the same length the system already celebrates
# as its first streak achievement (Week Warrior, achievements.py). We
# reuse that definition rather than inventing a second one.
NOTABLE_STREAK_MIN_DAYS = 5

# Most meaningful first, capped. Breakthroughs outrank completions outrank
# streaks outrank firsts; recency breaks ties.
MAX_MILESTONES = 3
_KIND_RANK = {"breakthrough": 0, "completion": 1, "streak": 2, "first": 3}

CACHE_TTL_SECONDS = 86_400  # 24 hours
_CACHE_PREFIX = "tutor_milestones"


def _cache_key(child_id: uuid.UUID) -> str:
    return f"{_CACHE_PREFIX}:{child_id}"


# ── The authored template set (product surface) ─────────────────────────
#
# Ten templates, keyed by kind (breakthroughs carry two shapes: one for a
# struggle measured in weeks, one for persistence too short to name in
# weeks). They are spoken by the tutor to a child. They celebrate effort
# and arrival; not one of them prints a count of failures or attempts.

MILESTONE_TEMPLATES: dict[str, list[str]] = {
    # Breakthrough, struggle measured in weeks of effort.
    "breakthrough_weeks": [
        "You worked at {title} for {weeks} weeks, and then it clicked. That kind of staying power is yours now.",
        "{title} took {weeks} weeks of real effort before it came together. You did not give up, and it paid off.",
    ],
    # Breakthrough, persistence too short to name in weeks: no number, just
    # the shape of sticking with something hard until it gave way.
    "breakthrough_persist": [
        "{title} did not come easy, and you kept at it until it did. That persistence is the whole game.",
        "You stuck with {title} through the hard part and got there. Remember that the next time something feels tough.",
    ],
    "completion": [
        "You finished every part of {title}. A whole stretch of {subject}, start to finish, behind you now.",
        "That is {title}, complete. You can look back at the full distance you have covered in {subject}.",
    ],
    "streak": [
        "You showed up to learn {days} days running. Showing up like that, day after day, is its own kind of strong.",
        "There was a stretch where you learned {days} days in a row. That rhythm is something to be proud of.",
    ],
    "first": [
        "{title} was your first real milestone in {subject}. Everything since has been built on that first step.",
        "You reached your first milestone in {subject} with {title}. That was the start of something.",
    ],
}

# The one line preface that frames the block for the tutor. It instructs
# natural, sparing use, never a list recital.
BLOCK_PREFACE = (
    "TUTOR RELATIONSHIP MEMORY (the journey so far, drawn only from this learner's own governed record; "
    "let it warm how you speak and show you remember how far they have come, used naturally and sparingly, "
    "never recited back as a list and never quoted verbatim):"
)


@dataclass
class Milestone:
    """One derived continuity memory. ``line`` is the rendered, tutor
    facing sentence; the other fields are the facts it was selected
    from, surfaced to the parent preview so nothing is hidden."""

    kind: str  # breakthrough | completion | streak | first
    subject: str | None
    title: str | None  # node or unit title; None for a streak
    when: datetime | None
    line: str


def _render(template_key: str, seed: uuid.UUID, **slots: object) -> str:
    """Render a template, choosing the variant deterministically from a
    stable seed so the same child state always yields the same line (the
    parent preview and the tutor injection must match exactly)."""
    variants = MILESTONE_TEMPLATES[template_key]
    return variants[seed.int % len(variants)].format(**slots)


def _weeks(span_days: int) -> int:
    """Span in whole weeks, never below two (this shape is only used when
    the span already cleared the 14 day breakthrough gate)."""
    return max(2, round(span_days / 7))


async def derive_milestones(db: AsyncSession, child_id: uuid.UUID) -> list[Milestone]:
    """Compute milestone memories for a child from existing rows only.

    Pure derivation: no writes, no AI, no caching (the caller decides
    whether to cache). Returns at most ``MAX_MILESTONES`` milestones,
    most meaningful first. An empty list is the normal answer for a
    learner with no qualifying history.
    """
    # 1. Reached nodes (proficient or above), with their title and subject,
    #    mirroring the Family Record's evidence query.
    states_result = await db.execute(
        select(ChildNodeState, LearningNode.title, Subject.name)
        .join(LearningNode, LearningNode.id == ChildNodeState.node_id)
        .join(LearningMap, LearningNode.learning_map_id == LearningMap.id)
        .join(Subject, LearningMap.subject_id == Subject.id, isouter=True)
        .where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.mastery_level.in_(REACHED_LEVELS),
        )
    )
    rows = states_result.all()
    node_meta: dict[uuid.UUID, tuple[str, str | None, ChildNodeState]] = {}
    for state, title, subject_name in rows:
        node_meta[state.node_id] = (title, subject_name, state)
    node_ids = list(node_meta.keys())

    # 2. Attempt history per reached node: count and the span of dates.
    #    Joined through Activity, since Attempt has no node_id of its own.
    attempt_count: dict[uuid.UUID, int] = {}
    attempt_first: dict[uuid.UUID, datetime] = {}
    attempt_last: dict[uuid.UUID, datetime] = {}
    if node_ids:
        attempts_result = await db.execute(
            select(Activity.node_id, Attempt.started_at, Attempt.completed_at)
            .join(Activity, Attempt.activity_id == Activity.id)
            .where(Attempt.child_id == child_id, Activity.node_id.in_(node_ids))
        )
        for node_id, started_at, completed_at in attempts_result.all():
            attempt_count[node_id] = attempt_count.get(node_id, 0) + 1
            start = started_at
            end = completed_at or started_at
            if start is not None:
                cur = attempt_first.get(node_id)
                if cur is None or start < cur:
                    attempt_first[node_id] = start
            if end is not None:
                cur = attempt_last.get(node_id)
                if cur is None or end > cur:
                    attempt_last[node_id] = end

    # 3. achieved_at: the latest mastery_change whose to_state matches the
    #    node's current level (the Family Record's achieved_at rule).
    achieved_at: dict[uuid.UUID, datetime] = {}
    if node_ids:
        events_result = await db.execute(
            select(StateEvent)
            .where(
                StateEvent.child_id == child_id,
                StateEvent.node_id.in_(node_ids),
                StateEvent.event_type == StateEventType.mastery_change,
            )
            .order_by(StateEvent.created_at.asc())
        )
        current_level = {nid: meta[2].mastery_level.value for nid, meta in node_meta.items()}
        for event in events_result.scalars().all():
            if event.to_state == current_level.get(event.node_id):
                achieved_at[event.node_id] = event.created_at

    def node_when(node_id: uuid.UUID) -> datetime | None:
        return achieved_at.get(node_id) or attempt_last.get(node_id) or node_meta[node_id][2].last_activity_at

    milestones: list[Milestone] = []
    breakthrough_nodes: set[uuid.UUID] = set()

    # ── Breakthrough arcs ────────────────────────────────────────────────
    for node_id, (title, subject_name, _state) in node_meta.items():
        n_attempts = attempt_count.get(node_id, 0)
        span_days = 0
        first, last = attempt_first.get(node_id), attempt_last.get(node_id)
        if first is not None and last is not None:
            span_days = (last - first).days
        long_struggle = span_days >= BREAKTHROUGH_MIN_DAYS
        many_attempts = n_attempts >= BREAKTHROUGH_MIN_ATTEMPTS
        if not (long_struggle or many_attempts):
            continue
        if long_struggle:
            line = _render("breakthrough_weeks", node_id, title=title, weeks=_weeks(span_days))
        else:
            line = _render("breakthrough_persist", node_id, title=title)
        milestones.append(
            Milestone(kind="breakthrough", subject=subject_name, title=title, when=node_when(node_id), line=line)
        )
        breakthrough_nodes.add(node_id)

    # ── Curriculum completions: a unit (learning map) all of whose active
    #    nodes the child has reached. Reuses the all nodes proficient+
    #    shape the fitness tier_up achievement already uses. ──────────────
    enroll_result = await db.execute(
        select(LearningMap.id, LearningMap.name, Subject.name)
        .join(ChildMapEnrollment, ChildMapEnrollment.learning_map_id == LearningMap.id)
        .join(Subject, LearningMap.subject_id == Subject.id, isouter=True)
        .where(
            ChildMapEnrollment.child_id == child_id,
            ChildMapEnrollment.is_active == True,  # noqa: E712
        )
    )
    enrolled_maps = enroll_result.all()
    map_ids = [m[0] for m in enrolled_maps]
    map_nodes: dict[uuid.UUID, list[uuid.UUID]] = {}
    if map_ids:
        nodes_result = await db.execute(
            select(LearningNode.id, LearningNode.learning_map_id).where(
                LearningNode.learning_map_id.in_(map_ids),
                LearningNode.is_active == True,  # noqa: E712
            )
        )
        for nid, map_id in nodes_result.all():
            map_nodes.setdefault(map_id, []).append(nid)
    reached_node_ids = set(node_ids)
    for map_id, map_name, subject_name in enrolled_maps:
        unit_nodes = map_nodes.get(map_id, [])
        if not unit_nodes or not all(nid in reached_node_ids for nid in unit_nodes):
            continue
        unit_whens = [w for w in (node_when(nid) for nid in unit_nodes) if w is not None]
        when = max(unit_whens) if unit_whens else None
        line = _render("completion", map_id, title=map_name, subject=subject_name or "this subject")
        milestones.append(Milestone(kind="completion", subject=subject_name, title=map_name, when=when, line=line))

    # ── Notable streak: read the canonical Streak row directly (the
    #    dashboard's definition) WITHOUT the get_streak create side effect,
    #    so derivation stays a pure read. ─────────────────────────────────
    streak_result = await db.execute(select(Streak).where(Streak.child_id == child_id))
    streak = streak_result.scalar_one_or_none()
    if streak is not None and streak.longest_streak >= NOTABLE_STREAK_MIN_DAYS:
        when = (
            datetime(
                streak.last_activity_date.year,
                streak.last_activity_date.month,
                streak.last_activity_date.day,
                tzinfo=UTC,
            )
            if streak.last_activity_date is not None
            else None
        )
        line = _render("streak", child_id, days=streak.longest_streak)
        milestones.append(Milestone(kind="streak", subject=None, title=None, when=when, line=line))

    # ── Firsts: the earliest reached node in each subject, skipping any
    #    node already spoken for as a breakthrough so the same arrival is
    #    never narrated twice. ─────────────────────────────────────────────
    by_subject: dict[str, tuple[uuid.UUID, str, datetime | None]] = {}
    for node_id, (title, subject_name, _state) in node_meta.items():
        if node_id in breakthrough_nodes or subject_name is None:
            continue
        when = node_when(node_id)
        existing = by_subject.get(subject_name)
        if existing is None or (when is not None and (existing[2] is None or when < existing[2])):
            by_subject[subject_name] = (node_id, title, when)
    for subject_name, (node_id, title, when) in by_subject.items():
        line = _render("first", node_id, title=title, subject=subject_name)
        milestones.append(Milestone(kind="first", subject=subject_name, title=title, when=when, line=line))

    # ── Rank: kind priority, then recency. Cap at three. ─────────────────
    def sort_key(m: Milestone) -> tuple[int, float]:
        ts = m.when.timestamp() if m.when is not None else 0.0
        return (_KIND_RANK[m.kind], -ts)

    milestones.sort(key=sort_key)
    return milestones[:MAX_MILESTONES]


def _to_cacheable(milestones: list[Milestone]) -> list[dict]:
    out: list[dict] = []
    for m in milestones:
        d = asdict(m)
        d["when"] = m.when.isoformat() if m.when is not None else None
        out.append(d)
    return out


def _from_cacheable(payload: list[dict]) -> list[Milestone]:
    out: list[Milestone] = []
    for d in payload:
        when = datetime.fromisoformat(d["when"]) if d.get("when") else None
        out.append(Milestone(kind=d["kind"], subject=d.get("subject"), title=d.get("title"), when=when, line=d["line"]))
    return out


async def get_milestones(db: AsyncSession, child_id: uuid.UUID) -> list[Milestone]:
    """Cached read of a child's milestones.

    The single entry point used by BOTH the tutor context injection and
    the parent preview, so the two are provably the same data. Cache is
    advisory: a Redis miss or error simply derives fresh. Never writes to
    the database.
    """
    from app.core.cache import cache_get, cache_set

    key = _cache_key(child_id)
    cached = await cache_get(key)
    if cached is not None:
        try:
            return _from_cacheable(cached)
        except Exception as exc:
            # A malformed cache entry must never block the read; derive.
            logger.warning("tutor_milestones_cache_decode_failed", child_id=str(child_id), error=str(exc))

    milestones = await derive_milestones(db, child_id)
    await cache_set(key, _to_cacheable(milestones), ttl_seconds=CACHE_TTL_SECONDS)
    return milestones


async def invalidate_milestones(child_id: uuid.UUID) -> None:
    """Drop a child's cached milestones. Called when relationship memory
    is toggled so the parent's choice takes effect immediately."""
    from app.core.cache import cache_delete

    await cache_delete(_cache_key(child_id))


def render_milestone_block(milestones: list[Milestone]) -> str:
    """The delimited, prefaced block injected into the tutor context, or
    an empty string when there is nothing to remember."""
    if not milestones:
        return ""
    body = "\n".join(f"- {m.line}" for m in milestones)
    return f"{BLOCK_PREFACE}\n{body}"
