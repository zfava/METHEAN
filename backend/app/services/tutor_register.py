"""Developmental voice register for the tutor.

A tutor that talks to a thirteen year old the way it talked to her at
seven has not grown with her. The register is per-tier voice guidance,
injected into every tutor context, that tells the model how to speak to
this learner right now: sentence length, abstraction, tone, and how much
independence to grant.

The register NEVER infers age. It derives from the child's CONTENT TIER,
the same per-subject curriculum stage the system already tracks
(app.core.learning_levels.LEARNING_LEVELS, the canonical ordered source:
foundational < developing < intermediate < advanced < mastery). This is a
different axis from per-node MasteryLevel; the two once collided on the
label "developing" and the resolution was to keep them separate, so this
module reads ONLY the content tier. When subjects differ, the caller
passes the subject being tutored and we use that subject's tier. If the
tier cannot be resolved, we fall back to the most protective register,
the youngest, and fail closed. A per-child parent override, when set, is
absolute: the derived tier is ignored entirely.

The five guidance blocks below are product surface. They are read by the
tutor model on every turn and could be read aloud to a parent without
embarrassment: they are pedagogy, not filler.
"""

import uuid
from typing import cast

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.learning_levels import LEARNING_LEVELS, VALID_LEVELS

logger = structlog.get_logger()

# Canonical tier order, lowest (youngest) first. Mirrors the sort_order in
# LEARNING_LEVELS; kept here only as the protective-fallback anchor.
FALLBACK_TIER = "foundational"


# ── The five register blocks (authored, product surface) ────────────────

REGISTER_GUIDANCE: dict[str, str] = {
    "foundational": (
        "Speak to a brand new learner. Keep sentences short and say one idea at a time. "
        "Name concrete things they can picture or hold, and prefer examples over rules. "
        "Introduce a single step, wait, then offer the next; never stack two questions at once. "
        "Be warm and a little playful, and notice effort out loud often, because a learner this "
        "new grows on encouragement. Do not assume a word has been met before: offer it plainly, "
        "then use it."
    ),
    "developing": (
        "This learner has a foothold and is ready to connect ideas. Use cause and effect plainly "
        "(because, so, which means) and a little light abstraction, kept anchored to examples. "
        "Humor is welcome and helps. Praise the strategy and the effort, not just the answer "
        "(the way you checked your work paid off). Invite a short attempt before you explain, and "
        "build each new idea onto one they already hold."
    ),
    "intermediate": (
        "Treat this learner as a growing independent thinker. Pose multi step reasoning and let "
        "them carry more than one idea at once. Frame problems in the real world and in other "
        "subjects they know. Respect their autonomy: ask for their plan before you offer yours, "
        "and invite them to explain their thinking in their own words, then build on it. "
        "Encouragement stays, but make it specific and earned."
    ),
    "advanced": (
        "Engage a capable, abstract thinker with genuine intellectual respect. You can work in "
        "generality, use precise terms, and expect claims to be justified. Favor socratic moves: a "
        "sharp question over a handed answer, a counterexample over a correction. Assume competence "
        "and let them sit with difficulty rather than rushing to rescue. Keep praise sparing and "
        "aimed at the quality of the reasoning."
    ),
    "mastery": (
        "Speak to a near peer. Be terse when terseness serves, precise always, and drop the "
        "scaffolding they no longer need. Expect rigor and offer it back: defend your claims, name "
        "the move you are making, and welcome being challenged. The learner leads and you advise; "
        "your job is the incisive question, the case they overlooked, the higher standard. The "
        "warmth here is in the respect of taking them seriously."
    ),
}


# ── Tier resolution ─────────────────────────────────────────────────────


# Canonical tier order, lowest first, derived from the single source of
# truth (LEARNING_LEVELS sort_order) so it can never drift from it.
_CANON_ORDER: tuple[str, ...] = tuple(sorted(VALID_LEVELS, key=lambda t: cast("int", LEARNING_LEVELS[t]["sort_order"])))


def tier_rank(tier: str) -> int:
    """Canonical rank of a tier, higher meaning further along. Callers
    guard with VALID_LEVELS first; an unknown tier raises ValueError."""
    return _CANON_ORDER.index(tier)


def _tier_order(tier: str | None) -> int | None:
    """Canonical rank of a tier, or None when it is not a resolvable tier."""
    if tier is not None and tier in _CANON_ORDER:
        return _CANON_ORDER.index(tier)
    return None


def tier_lag(current: str | None, stamped: str | None) -> int | None:
    """How many tiers `current` sits above `stamped` (canonical distance),
    or None when either is not a resolvable tier. Negative if current is
    below stamped."""
    a, b = _tier_order(current), _tier_order(stamped)
    if a is None or b is None:
        return None
    return a - b


def _explicit_subject_tier(prefs, subject_name: str) -> str | None:
    """The child's explicitly recorded tier for a subject, or None.

    Unlike learning_levels.get_level_for_subject, this never invents a
    'developing' default: the register must fail closed to the youngest
    when there is no real signal, so a missing subject reads as None here
    and the caller falls back to foundational.
    """
    levels = getattr(prefs, "subject_levels", None) if prefs is not None else None
    if not isinstance(levels, dict) or not levels:
        return None
    key = subject_name.lower().replace(" ", "_").replace("&", "and")
    val = levels.get(key)
    if val is None:
        for k, v in levels.items():
            if k.lower() in subject_name.lower() or subject_name.lower() in k.lower():
                val = v
                break
    return val if val in VALID_LEVELS else None


async def current_tier_for_child(
    db: AsyncSession,
    child_id: uuid.UUID,
    subject_name: str | None = None,
) -> str | None:
    """The child's current content tier, for stamping entries and judging
    tier lag (NOT for the register, which fails closed to foundational).

    With a subject, returns that subject's explicit tier or None. Without
    a subject (the entry-stamping and tier-lag case, where a strategy is
    cross subject), returns the child's furthest reach: the highest tier
    across their subjects, or None when there is no tier data at all. Fail
    open to None so a missing signal never fabricates a stage.
    """
    from app.models.identity import ChildPreferences

    try:
        prefs = (
            await db.execute(select(ChildPreferences).where(ChildPreferences.child_id == child_id))
        ).scalar_one_or_none()
    except Exception as exc:
        logger.warning("tutor_register_prefs_unreadable", child_id=str(child_id), error=str(exc))
        return None

    if subject_name:
        return _explicit_subject_tier(prefs, subject_name)

    levels = getattr(prefs, "subject_levels", None) if prefs is not None else None
    if not isinstance(levels, dict) or not levels:
        return None
    reached = [v for v in levels.values() if v in VALID_LEVELS]
    if not reached:
        return None
    return max(reached, key=tier_rank)


async def resolve_register(
    db: AsyncSession,
    child_id: uuid.UUID,
    subject_context: str | None,
) -> tuple[str, str, str]:
    """Resolve the effective register for a child in a subject context.

    Returns (tier, guidance, source) where source is "override" when a
    per-child parent override is in force (absolute: the derived tier is
    ignored entirely) or "derived" otherwise. subject_context is the name
    of the subject being tutored; when it cannot be resolved we fall back
    to the most protective register, foundational. Fail closed: any error
    yields the foundational register, never a silent richer one.
    """
    try:
        from app.models.intelligence import ChildTutorPreferences

        ctp = (
            await db.execute(select(ChildTutorPreferences).where(ChildTutorPreferences.child_id == child_id))
        ).scalar_one_or_none()
        override = ctp.register_override if ctp is not None else None
        if override is not None and override in VALID_LEVELS:
            return override, REGISTER_GUIDANCE[override], "override"

        derived: str | None = None
        if subject_context:
            derived = await current_tier_for_child(db, child_id, subject_context)
        tier = derived if (derived is not None and derived in VALID_LEVELS) else FALLBACK_TIER
        return tier, REGISTER_GUIDANCE[tier], "derived"
    except Exception as exc:
        logger.warning("tutor_register_resolve_failed", child_id=str(child_id), error=str(exc))
        return FALLBACK_TIER, REGISTER_GUIDANCE[FALLBACK_TIER], "derived"
