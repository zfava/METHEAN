"""Deterministic native curriculum generator.

Emits a year plan in the EXACT shape ``materialize_full_year`` consumes (see
docs/curriculum_pipeline_audit.md, finding 1 and 3): a top-level dict with a
``weeks`` list, each week carrying ``week_number`` / ``assessment_focus`` /
``suggested_activities`` / ``focus_nodes``, each activity carrying
``day`` / ``type`` / ``title`` / ``description`` / ``minutes``. It deliberately
does NOT emit per-week ``title`` / ``objectives`` (materialize does not read
them) and never emits ``year_plans`` (that is the broken mock shape).

``focus_nodes`` entries are real LearningNode UUIDs obtained through the 0.2a
namespace resolver. A ref with no authored/persistable node does not crash;
its week is flagged ``needs_content`` and that slot is omitted from
``focus_nodes``.

The generator is deterministic: same inputs produce byte-identical output. It
makes no AI/network calls and uses no randomness. The only I/O is the resolver,
which is itself idempotent, so repeated calls yield identical UUIDs.

This module is wired into the AI gateway provider chain (Claude -> OpenAI ->
NATIVE -> Mock): when the real providers are absent it produces the annual
curriculum directly. It declines (returns None) for prompts/roles it does not
handle, letting the mock fallback take over.
"""

import re
from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.node_resolver import resolve_ref_to_uuid

if TYPE_CHECKING:
    import uuid

    from app.ai.gateway import AIRole


@dataclass(frozen=True)
class Topic:
    """One scope-and-sequence topic: an ordered, prerequisite-respecting unit."""

    ref: str
    title: str
    estimated_weeks: int = 1


# Per-day instruction template. Five instruction days, deterministic types.
INSTRUCTION_DAYS: list[tuple[str, str]] = [
    ("Monday", "lesson"),
    ("Tuesday", "practice"),
    ("Wednesday", "lesson"),
    ("Thursday", "practice"),
    ("Friday", "review"),
]
ACTIVITIES_PER_WEEK = len(INSTRUCTION_DAYS)
CHECKPOINT_EVERY = 6  # every 6th week is an assessment checkpoint

# Philosophy-specific framing. Selected by household.philosophical_profile
# ["educational_philosophy"]; falls back to "traditional" when absent/unknown.
PHILOSOPHY_BLOCKS: dict[str, dict[str, str]] = {
    "classical": {"framing": "grammar-stage memorization and recitation", "verb": "Recite and master"},
    "charlotte_mason": {"framing": "living books, narration, and nature study", "verb": "Narrate and observe"},
    "montessori": {"framing": "self-directed hands-on work", "verb": "Explore hands-on"},
    "unschooling": {"framing": "interest-led exploration", "verb": "Investigate"},
    "eclectic": {"framing": "mixed methods", "verb": "Practice"},
    "traditional": {"framing": "structured textbook lessons", "verb": "Study"},
}
DEFAULT_PHILOSOPHY = "traditional"


def philosophy_key(profile: dict | None) -> str:
    """Resolve a philosophy block key from a household philosophical profile."""
    if not profile:
        return DEFAULT_PHILOSOPHY
    key = (profile.get("educational_philosophy") or "").strip().lower()
    return key if key in PHILOSOPHY_BLOCKS else DEFAULT_PHILOSOPHY


def topics_for_subject(subject_id: str, level: str) -> list[Topic]:
    """Read scope_sequences[subject_id][level] in authored (prerequisite) order.

    Order is preserved exactly; nothing is reordered or skipped.
    """
    from app.content.scope_sequences import get_scope_sequence

    raw = get_scope_sequence(subject_id, level)
    topics: list[Topic] = []
    for t in raw:
        ref = t.get("ref")
        if not ref:
            continue
        topics.append(
            Topic(
                ref=ref,
                title=t.get("title", ref),
                estimated_weeks=int(t.get("estimated_weeks", 1) or 1),
            )
        )
    return topics


def _partition(topics: list[Topic], total_weeks: int) -> list[list[Topic]]:
    """Split topics into ``total_weeks`` contiguous, order-preserving groups.

    Even split: week k gets topics[floor(k*n/W) : floor((k+1)*n/W)]. When there
    are fewer topics than weeks some groups are empty (consolidation weeks);
    when there are more, groups hold several topics. Fully deterministic.
    """
    n = len(topics)
    groups: list[list[Topic]] = []
    for k in range(total_weeks):
        start = (k * n) // total_weeks
        end = ((k + 1) * n) // total_weeks
        groups.append(topics[start:end])
    return groups


def _activity_minutes(hours_per_week: float) -> int:
    """Per-activity minutes derived from the weekly time budget."""
    return max(5, round(hours_per_week * 60 / ACTIVITIES_PER_WEEK))


def _build_activities(
    topics: list[Topic],
    block: dict[str, str],
    minutes: int,
    is_checkpoint: bool,
) -> list[dict]:
    """Build the per-day activity list for one week (deterministic)."""
    activities: list[dict] = []
    for i, (day, base_type) in enumerate(INSTRUCTION_DAYS):
        atype = base_type
        if is_checkpoint and day == "Friday":
            atype = "assessment"
        if topics:
            topic = topics[i % len(topics)]
            title = f"{atype.capitalize()}: {topic.title}"
            description = f"{block['verb']} {topic.title} through {block['framing']}."
        else:
            title = f"{atype.capitalize()}: consolidation"
            description = f"Consolidate and revisit prior skills through {block['framing']}."
        activities.append(
            {
                "day": day,
                "type": atype,
                "title": title,
                "description": description,
                "minutes": minutes,
            }
        )
    return activities


def _assessment_focus(topics: list[Topic], is_checkpoint: bool) -> str:
    if is_checkpoint:
        return "Checkpoint: assess mastery of recently covered topics."
    if topics:
        return "Assess understanding of: " + ", ".join(t.title for t in topics)
    return "Consolidation and review of prior weeks."


async def generate_native_curriculum(
    db: AsyncSession,
    household_id: "uuid.UUID",
    *,
    topics: list[Topic],
    hours_per_week: float,
    total_weeks: int,
    start_date: date,
    child_age: float = 8.0,
    philosophy: str = DEFAULT_PHILOSOPHY,
) -> dict:
    """Build the year plan from an ordered topic list.

    Returns a scope_sequence dict shaped exactly for materialize_full_year.
    Each topic's ref is resolved to a persisted UUID via the namespace
    resolver; unresolved topics flag their week ``needs_content`` and are
    omitted from ``focus_nodes`` (no crash, partial libraries still generate).
    """
    block = PHILOSOPHY_BLOCKS.get(philosophy, PHILOSOPHY_BLOCKS[DEFAULT_PHILOSOPHY])
    total_weeks = max(1, total_weeks)
    minutes = _activity_minutes(hours_per_week)
    groups = _partition(topics, total_weeks)

    weeks: list[dict] = []
    for k, group in enumerate(groups):
        week_number = k + 1
        is_checkpoint = week_number % CHECKPOINT_EVERY == 0

        focus_nodes: list[str] = []
        needs_content = False
        for topic in group:
            resolution = await resolve_ref_to_uuid(db, topic.ref, household_id)
            if resolution.node_uuid is not None:
                focus_nodes.append(str(resolution.node_uuid))
            else:
                needs_content = True

        week: dict = {
            "week_number": week_number,
            "assessment_focus": _assessment_focus(group, is_checkpoint),
            "suggested_activities": _build_activities(group, block, minutes, is_checkpoint),
            "focus_nodes": focus_nodes,
        }
        if needs_content:
            week["needs_content"] = True
        weeks.append(week)

    return {
        "overview": (
            f"Deterministic native {total_weeks}-week plan ({block['framing']}), "
            f"starting {start_date.isoformat()}, ~{hours_per_week:g}h/week, "
            f"for a {child_age:.0f}-year-old."
        ),
        "philosophy_alignment": f"Aligned to the {philosophy} approach: {block['framing']}.",
        "materials": ["scope_sequence content modules"],
        "generator": "native",
        "weeks": weeks,
    }


async def generate_for_subject(
    db: AsyncSession,
    household_id: "uuid.UUID",
    subject_id: str,
    level: str,
    *,
    hours_per_week: float = 4.0,
    total_weeks: int = 36,
    start_date: date,
    child_age: float = 8.0,
    philosophy: str = DEFAULT_PHILOSOPHY,
) -> dict:
    """Convenience entry: read scope_sequences[subject_id][level] then build."""
    topics = topics_for_subject(subject_id, level)
    return await generate_native_curriculum(
        db,
        household_id,
        topics=topics,
        hours_per_week=hours_per_week,
        total_weeks=total_weeks,
        start_date=start_date,
        child_age=child_age,
        philosophy=philosophy,
    )


# ── Gateway adapter ──────────────────────────────────────────────────────
#
# The provider-chain entry. The gateway hands us only the rendered prompt, so
# we extract the ordered scope refs and the run parameters from it. The prompt
# is built deterministically by generate_annual_curriculum, so this parse is
# stable. We decline (return None) for any role/prompt we do not handle, which
# lets the mock fallback take over (e.g. the multi-year education plan, whose
# prompt carries no scope-and-sequence block).

_WEEKS_RE = re.compile(r"^TOTAL WEEKS:\s*(\d+)", re.M)
_HOURS_RE = re.compile(r"^TIME BUDGET:\s*([\d.]+)\s*hours", re.M)
_START_RE = re.compile(r"^START DATE:\s*(\d{4}-\d{2}-\d{2})", re.M)
_AGE_RE = re.compile(r"-\s*Age:\s*([\d.]+)\s*years", re.M)
# Scope block line: "  math_f_01: Counting to 20 (prereqs: [..], ~2wk, concepts: ..)"
_SCOPE_LINE_RE = re.compile(r"^\s{2}(\S+):\s+(.*?)\s+\(prereqs:.*?~(\d+)\s*wk", re.M)


def parse_prompt(user_prompt: str) -> dict | None:
    """Extract topics + parameters from an annual-curriculum prompt.

    Returns None when the prompt carries no scope-and-sequence block (nothing
    to generate from).
    """
    topics = [
        Topic(ref=m.group(1), title=m.group(2).strip(), estimated_weeks=int(m.group(3)))
        for m in _SCOPE_LINE_RE.finditer(user_prompt)
    ]
    if not topics:
        return None

    weeks_m = _WEEKS_RE.search(user_prompt)
    hours_m = _HOURS_RE.search(user_prompt)
    start_m = _START_RE.search(user_prompt)
    age_m = _AGE_RE.search(user_prompt)

    return {
        "topics": topics,
        "total_weeks": int(weeks_m.group(1)) if weeks_m else 36,
        "hours_per_week": float(hours_m.group(1)) if hours_m else 4.0,
        "start_date": date.fromisoformat(start_m.group(1)) if start_m else date(2026, 9, 1),
        "child_age": float(age_m.group(1)) if age_m else 8.0,
    }


async def build_native_response(
    db: AsyncSession,
    household_id: "uuid.UUID",
    role: "AIRole",
    user_prompt: str,
    philosophical_profile: dict | None,
) -> dict | None:
    """Provider-chain entry point. Returns the year-plan dict, or None to defer.

    Only the annual curriculum (education_architect role + a scope-and-sequence
    block in the prompt) is handled here.
    """
    if getattr(role, "value", role) != "education_architect":
        return None
    parsed = parse_prompt(user_prompt)
    if parsed is None:
        return None
    return await generate_native_curriculum(
        db,
        household_id,
        topics=parsed["topics"],
        hours_per_week=parsed["hours_per_week"],
        total_weeks=parsed["total_weeks"],
        start_date=parsed["start_date"],
        child_age=parsed["child_age"],
        philosophy=philosophy_key(philosophical_profile),
    )
