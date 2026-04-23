"""Mastery Track: universal infrastructure for infinite progression past Tier 5.

The Mastery Track kicks in when a child reaches ≥80% mastery of a subject's
Tier 5 (Independent) learning map. From there, the Cartographer AI generates
five progressively harder nodes per "depth level". There is no ceiling — a
motivated child can grind through depth 1, 2, 3, …, each level tuned harder
than the last with growing cross-domain connections and, past depth 3, a
teaching requirement.

Design principle: this module is domain-agnostic. It discovers qualifying
domains from TEMPLATES at runtime by looking for the `*_independent` tier
naming convention, so adding a new domain with 5 tiers enables the Mastery
Track for it automatically with zero new code here.
"""

import uuid
from collections import defaultdict
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import MasteryLevel
from app.models.identity import Child, Household
from app.models.state import ChildNodeState
from app.services.templates import TEMPLATES

# ── Constants ──

MASTERY_TRACK_NODES_PER_LEVEL = 5
MASTERY_TRACK_ELIGIBILITY_THRESHOLD = 0.80

_TIER_SUFFIXES = ("foundations", "development", "intermediate", "advanced", "independent")

# Cross-domain connections used by the Cartographer to braid mastered
# concepts from adjacent subjects into a given domain's Mastery Track.
# Missing subjects default to an empty list via the defaultdict wrapper.
_CROSS_DOMAIN_SEED: dict[str, list[str]] = {
    "Mathematics": ["Science", "Computer Science", "Financial Literacy", "Robotics and Engineering"],
    "Science": ["Mathematics", "Gardening and Agriculture", "First Aid and Emergency Preparedness"],
    "Language Arts": ["Creative Writing", "Public Speaking and Rhetoric", "History and Social Studies"],
    "Creative Writing": ["Language Arts", "Theater and Drama", "History and Social Studies"],
    "Visual Art": ["Design and Fabrication", "Photography", "Creative Writing"],
    "Music": ["Mathematics", "Theater and Drama", "History and Social Studies"],
    "History and Social Studies": [
        "Language Arts",
        "Community Service and Civic Engagement",
        "Leadership and Ethics",
    ],
    "Computer Science": ["Mathematics", "Robotics and Engineering", "Design and Fabrication"],
    "Physical Education": [
        "First Aid and Emergency Preparedness",
        "Wilderness Skills",
        "Gardening and Agriculture",
    ],
    "Physical Fitness": [
        "First Aid and Emergency Preparedness",
        "Wilderness Skills",
        "Gardening and Agriculture",
    ],
    "Financial Literacy": ["Mathematics", "Entrepreneurship and Business", "Leadership and Ethics"],
    "Entrepreneurship and Business": [
        "Financial Literacy",
        "Leadership and Ethics",
        "Public Speaking and Rhetoric",
    ],
    "Leadership and Ethics": [
        "Community Service and Civic Engagement",
        "Public Speaking and Rhetoric",
        "History and Social Studies",
    ],
    "Public Speaking and Rhetoric": ["Language Arts", "Leadership and Ethics", "Theater and Drama"],
    "Theater and Drama": ["Creative Writing", "Music", "Public Speaking and Rhetoric"],
    "Photography": ["Visual Art", "Design and Fabrication"],
    "Design and Fabrication": ["Visual Art", "Computer Science", "Robotics and Engineering"],
    "Robotics and Engineering": ["Mathematics", "Computer Science", "Design and Fabrication"],
    "Gardening and Agriculture": ["Science", "Wilderness Skills"],
    "Wilderness Skills": [
        "First Aid and Emergency Preparedness",
        "Gardening and Agriculture",
        "Physical Fitness",
    ],
    "First Aid and Emergency Preparedness": [
        "Science",
        "Wilderness Skills",
        "Physical Fitness",
    ],
    "Community Service and Civic Engagement": [
        "History and Social Studies",
        "Leadership and Ethics",
    ],
}
CROSS_DOMAIN_CONNECTIONS: defaultdict[str, list[str]] = defaultdict(list, _CROSS_DOMAIN_SEED)

_PROFICIENT_OR_BETTER = (MasteryLevel.proficient, MasteryLevel.mastered)


# ══════════════════════════════════════════════════
# 1. Domain discovery
# ══════════════════════════════════════════════════


def get_mastery_track_domains() -> list[str]:
    """Discover Mastery-Track-eligible domains from TEMPLATES.

    A domain qualifies only if all five tier templates exist:
    `<domain>_foundations`, `_development`, `_intermediate`, `_advanced`,
    `_independent`. Missing any tier disqualifies the domain.
    """
    candidates: dict[str, set[str]] = defaultdict(set)
    for template_id in TEMPLATES:
        for suffix in _TIER_SUFFIXES:
            marker = f"_{suffix}"
            if template_id.endswith(marker):
                prefix = template_id[: -len(marker)]
                candidates[prefix].add(suffix)
                break
    qualified = [prefix for prefix, suffixes in candidates.items() if set(_TIER_SUFFIXES).issubset(suffixes)]
    return sorted(qualified)


def _tier5_template_name_for_subject(subject_name: str) -> str:
    """Return the canonical Tier 5 LearningMap name for a subject."""
    return f"{subject_name}: Independent"


# ══════════════════════════════════════════════════
# 2. Eligibility
# ══════════════════════════════════════════════════


async def _tier5_map_ids(db: AsyncSession, household_id: uuid.UUID, subject_id: uuid.UUID) -> list[uuid.UUID]:
    """Learning maps in the subject whose name marks them as Tier 5."""
    result = await db.execute(
        select(LearningMap.id).where(
            LearningMap.household_id == household_id,
            LearningMap.subject_id == subject_id,
            LearningMap.name.ilike("%: Independent%"),
        )
    )
    return list(result.scalars().all())


async def check_mastery_track_eligibility(
    db: AsyncSession,
    child_id: uuid.UUID,
    subject_id: uuid.UUID,
) -> dict:
    """Is this child ready to start (or continue) the Mastery Track for a subject?"""
    subj_result = await db.execute(select(Subject).where(Subject.id == subject_id))
    subject = subj_result.scalar_one_or_none()
    if subject is None:
        return {"eligible": False, "pct_mastered": 0.0, "remaining_nodes": 0}

    tier5_maps = await _tier5_map_ids(db, subject.household_id, subject_id)
    if not tier5_maps:
        return {
            "eligible": False,
            "pct_mastered": 0.0,
            "remaining_nodes": 0,
            "reason": "no_tier5_map",
        }

    # Tier 5 nodes only — exclude generated Mastery-Track nodes so the
    # threshold reflects base Tier 5 mastery, not already-generated depth work.
    all_tier5_nodes_result = await db.execute(
        select(LearningNode).where(
            LearningNode.learning_map_id.in_(tier5_maps),
            LearningNode.is_active == True,  # noqa: E712
        )
    )
    tier5_nodes = [n for n in all_tier5_nodes_result.scalars().all() if not (n.content or {}).get("mastery_track")]
    total = len(tier5_nodes)
    if total == 0:
        return {
            "eligible": False,
            "pct_mastered": 0.0,
            "remaining_nodes": 0,
            "reason": "no_tier5_nodes",
        }

    node_ids = [n.id for n in tier5_nodes]
    mastered_result = await db.execute(
        select(func.count(ChildNodeState.id)).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.node_id.in_(node_ids),
            ChildNodeState.mastery_level.in_(_PROFICIENT_OR_BETTER),
        )
    )
    mastered = mastered_result.scalar_one() or 0
    pct = round(mastered / total, 4)

    if pct >= MASTERY_TRACK_ELIGIBILITY_THRESHOLD:
        depth = await get_mastery_depth(db, child_id, subject_id)
        return {
            "eligible": True,
            "mastery_depth": depth,
            "pct_mastered": pct,
            "specializations_available": CROSS_DOMAIN_CONNECTIONS[subject.name],
        }
    return {
        "eligible": False,
        "pct_mastered": pct,
        "remaining_nodes": total - mastered,
    }


# ══════════════════════════════════════════════════
# 3. Mastery depth
# ══════════════════════════════════════════════════


async def get_mastery_depth(
    db: AsyncSession,
    child_id: uuid.UUID,
    subject_id: uuid.UUID,
) -> int:
    """How many complete Mastery-Track levels beyond Tier 5 has this child finished?

    A level is "complete" when every node at that depth is mastered.
    Returns the highest contiguous completed level — 0 means still in Tier 5.
    """
    subj_result = await db.execute(select(Subject).where(Subject.id == subject_id))
    subject = subj_result.scalar_one_or_none()
    if subject is None:
        return 0

    maps_result = await db.execute(
        select(LearningMap.id).where(
            LearningMap.household_id == subject.household_id,
            LearningMap.subject_id == subject_id,
        )
    )
    map_ids = list(maps_result.scalars().all())
    if not map_ids:
        return 0

    nodes_result = await db.execute(
        select(LearningNode).where(
            LearningNode.learning_map_id.in_(map_ids),
            LearningNode.is_active == True,  # noqa: E712
        )
    )
    by_depth: dict[int, list[uuid.UUID]] = defaultdict(list)
    for node in nodes_result.scalars().all():
        content = node.content or {}
        if not content.get("mastery_track"):
            continue
        level = content.get("depth_level")
        if isinstance(level, int) and level >= 1:
            by_depth[level].append(node.id)

    if not by_depth:
        return 0

    # Node-level mastery lookup for all track nodes, in one query.
    all_track_ids = [nid for nids in by_depth.values() for nid in nids]
    mastered_result = await db.execute(
        select(ChildNodeState.node_id).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.node_id.in_(all_track_ids),
            ChildNodeState.mastery_level.in_(_PROFICIENT_OR_BETTER),
        )
    )
    mastered_ids = set(mastered_result.scalars().all())

    completed = 0
    for depth in sorted(by_depth.keys()):
        nids = by_depth[depth]
        if nids and all(nid in mastered_ids for nid in nids):
            completed = depth
        else:
            break  # must be contiguous to count
    return completed


# ══════════════════════════════════════════════════
# 4. Generation prompt + node creation
# ══════════════════════════════════════════════════


async def _cross_domain_mastery_snapshot(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    related_subjects: list[str],
) -> list[dict]:
    """For each related subject, note the highest tier the child has cleared."""
    if not related_subjects:
        return []

    subj_result = await db.execute(
        select(Subject).where(
            Subject.household_id == household_id,
            Subject.name.in_(related_subjects),
        )
    )
    snapshot: list[dict] = []
    for subj in subj_result.scalars().all():
        # Find the highest tier map for this subject where the child has proficient+ mastery on
        # at least half the nodes. Cheap heuristic: count mastered nodes per map.
        maps_result = await db.execute(
            select(LearningMap).where(
                LearningMap.household_id == household_id,
                LearningMap.subject_id == subj.id,
            )
        )
        best_tier = None
        best_pct = 0.0
        for lmap in maps_result.scalars().all():
            nodes_r = await db.execute(
                select(func.count(LearningNode.id)).where(
                    LearningNode.learning_map_id == lmap.id,
                    LearningNode.is_active == True,  # noqa: E712
                )
            )
            total = nodes_r.scalar_one() or 0
            if total == 0:
                continue
            mastered_r = await db.execute(
                select(func.count(ChildNodeState.id))
                .select_from(ChildNodeState)
                .join(LearningNode, LearningNode.id == ChildNodeState.node_id)
                .where(
                    ChildNodeState.child_id == child_id,
                    LearningNode.learning_map_id == lmap.id,
                    ChildNodeState.mastery_level.in_(_PROFICIENT_OR_BETTER),
                )
            )
            mastered = mastered_r.scalar_one() or 0
            pct = mastered / total
            if pct > best_pct:
                best_pct = pct
                best_tier = lmap.name
        if best_tier is not None:
            snapshot.append(
                {"subject": subj.name, "highest_cleared_map": best_tier, "pct_mastered": round(best_pct, 2)}
            )
    return snapshot


async def _mastery_history_for_subject(
    db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID, subject_id: uuid.UUID
) -> list[dict]:
    """Every node the child has mastered in this subject, across all tiers."""
    result = await db.execute(
        select(LearningNode, LearningMap.name, ChildNodeState.mastery_level)
        .join(LearningMap, LearningMap.id == LearningNode.learning_map_id)
        .join(ChildNodeState, ChildNodeState.node_id == LearningNode.id)
        .where(
            LearningMap.household_id == household_id,
            LearningMap.subject_id == subject_id,
            ChildNodeState.child_id == child_id,
            ChildNodeState.mastery_level.in_(_PROFICIENT_OR_BETTER),
        )
    )
    return [
        {
            "node_id": str(node.id),
            "title": node.title,
            "map_name": map_name,
            "mastery_level": level.value if hasattr(level, "value") else str(level),
        }
        for node, map_name, level in result.all()
    ]


def _build_depth_directives(depth_level: int) -> list[str]:
    """Baseline depth-scaled directives shipped with every Mastery Track prompt."""
    directives = [
        "Every node must be harder than anything in Tier 5 for this domain.",
        f"Scale difficulty with depth: this is depth {depth_level}. Depth 3 is harder than "
        "depth 1; depth 5 harder still. Raise cognitive load with each level, not just volume.",
        "Incorporate cross-domain connections: pull in concepts and techniques from subjects the "
        "child has already mastered (see `cross_domain_mastery`).",
        "Require increasingly original thinking, research, or teaching as depth increases.",
        "Every node must carry specific, measurable benchmark_criteria that the parent can "
        "evaluate without specialist knowledge.",
        "Respect the household's philosophical profile and content boundaries.",
        'Every node content JSONB must include {"mastery_track": true, "depth_level": <N>, '
        '"generated_at": <iso-timestamp>}.',
    ]
    if depth_level >= 3:
        directives.append(
            "At depth 3+, at least one node must require the child to teach a concept from this "
            "subject to another learner (sibling, peer, parent, or community member) and reflect "
            "on what made it click (or not)."
        )
    if depth_level >= 5:
        directives.append(
            "At depth 5+, at least one node must require the child to create an original artifact "
            "(essay, project, demonstration, tool, performance) that synthesizes multiple "
            "threads from this subject and its cross-domain connections."
        )
    return directives


async def generate_mastery_track_nodes(
    db: AsyncSession,
    child_id: uuid.UUID,
    subject_id: uuid.UUID,
    household_id: uuid.UUID,
) -> dict:
    """Assemble the Cartographer prompt for the next Mastery Track level.

    Returns a dict the API layer or a Celery task can hand to the Cartographer
    AI. Node creation is left to the caller after the AI call returns, so this
    function is safe to invoke without any LLM configured.
    """
    eligibility = await check_mastery_track_eligibility(db, child_id, subject_id)
    if not eligibility.get("eligible"):
        return {"eligible": False, "eligibility": eligibility, "prompt": None}

    subj_result = await db.execute(select(Subject).where(Subject.id == subject_id))
    subject = subj_result.scalar_one()

    hh_result = await db.execute(select(Household).where(Household.id == household_id))
    household = hh_result.scalar_one_or_none()
    philosophical_profile = (household.philosophical_profile if household else None) or {}

    child_result = await db.execute(select(Child).where(Child.id == child_id))
    child = child_result.scalar_one_or_none()

    current_depth = await get_mastery_depth(db, child_id, subject_id)
    next_depth = current_depth + 1

    mastery_history = await _mastery_history_for_subject(db, child_id, household_id, subject_id)
    related_subjects = CROSS_DOMAIN_CONNECTIONS[subject.name]
    cross_domain = await _cross_domain_mastery_snapshot(db, child_id, household_id, related_subjects)

    # Previous depth nodes (used for wiring prerequisites after generation).
    maps_r = await db.execute(
        select(LearningMap).where(
            LearningMap.household_id == household_id,
            LearningMap.subject_id == subject_id,
        )
    )
    subject_maps = list(maps_r.scalars().all())
    prev_level_nodes: list[uuid.UUID] = []
    tier5_anchor_nodes: list[uuid.UUID] = []
    target_map_id: uuid.UUID | None = None
    for lmap in subject_maps:
        if lmap.name.lower().endswith(": independent"):
            target_map_id = lmap.id
        nodes_r = await db.execute(
            select(LearningNode).where(
                LearningNode.learning_map_id == lmap.id,
                LearningNode.is_active == True,  # noqa: E712
            )
        )
        for node in nodes_r.scalars().all():
            content = node.content or {}
            if current_depth == 0 and not content.get("mastery_track"):
                # Depth 1 anchors to Tier 5 nodes.
                tier5_anchor_nodes.append(node.id)
            elif content.get("mastery_track") and content.get("depth_level") == current_depth:
                prev_level_nodes.append(node.id)

    prerequisite_anchor_ids = prev_level_nodes if current_depth >= 1 else tier5_anchor_nodes

    prompt = {
        "role": "cartographer",
        "task": "generate_mastery_track_nodes",
        "subject": subject.name,
        "subject_id": str(subject.id),
        "depth_level": next_depth,
        "nodes_to_generate": MASTERY_TRACK_NODES_PER_LEVEL,
        "child": {
            "id": str(child_id),
            "first_name": child.first_name if child else None,
            "grade_level": child.grade_level if child else None,
        },
        "mastery_history": mastery_history,
        "cross_domain_mastery": cross_domain,
        "philosophical_profile": philosophical_profile,
        "directives": _build_depth_directives(next_depth),
        "output_schema": {
            "nodes": [
                {
                    "title": "string",
                    "description": "string",
                    "node_type": "milestone|concept|skill|project",
                    "estimated_minutes": "int",
                    "content": {
                        "benchmark_criteria": "string — measurable, parent-evaluable",
                        "assessment_type": "timed|counted|pass_fail|observed|portfolio",
                        "mastery_track": True,
                        "depth_level": next_depth,
                        "generated_at": "iso-timestamp",
                        "cross_domain_tags": ["list", "of", "connected", "subjects"],
                    },
                }
            ]
        },
    }

    return {
        "eligible": True,
        "eligibility": eligibility,
        "current_depth": current_depth,
        "next_depth": next_depth,
        "target_map_id": str(target_map_id) if target_map_id else None,
        "prerequisite_anchor_node_ids": [str(n) for n in prerequisite_anchor_ids],
        "prompt": prompt,
        "generated_at": datetime.now(UTC).isoformat(),
    }


# ══════════════════════════════════════════════════
# 5. Dashboard summary across all the child's subjects
# ══════════════════════════════════════════════════


async def get_mastery_track_summary(db: AsyncSession, child_id: uuid.UUID) -> list[dict]:
    """One row per subject the child is enrolled in, with their current track standing."""
    child_result = await db.execute(select(Child).where(Child.id == child_id))
    child = child_result.scalar_one_or_none()
    if child is None:
        return []
    household_id = child.household_id

    # Subjects this child has at least one state row in — i.e. they've touched work in the subject.
    subjects_result = await db.execute(
        select(Subject)
        .join(LearningMap, LearningMap.subject_id == Subject.id)
        .join(LearningNode, LearningNode.learning_map_id == LearningMap.id)
        .join(ChildNodeState, ChildNodeState.node_id == LearningNode.id)
        .where(
            ChildNodeState.child_id == child_id,
            LearningMap.household_id == household_id,
        )
        .distinct()
    )
    rows: list[dict] = []
    for subject in subjects_result.scalars().all():
        eligibility = await check_mastery_track_eligibility(db, child_id, subject.id)
        depth = await get_mastery_depth(db, child_id, subject.id)
        if eligibility.get("eligible") or depth > 0:
            current_tier = "Tier 5"
        else:
            current_tier = await _infer_highest_tier(db, child_id, household_id, subject.id)

        # Count of fully completed Mastery-Track nodes (proficient+) in this subject.
        completed_track_result = await db.execute(
            select(func.count(ChildNodeState.id))
            .select_from(ChildNodeState)
            .join(LearningNode, LearningNode.id == ChildNodeState.node_id)
            .join(LearningMap, LearningMap.id == LearningNode.learning_map_id)
            .where(
                LearningMap.household_id == household_id,
                LearningMap.subject_id == subject.id,
                ChildNodeState.child_id == child_id,
                ChildNodeState.mastery_level.in_(_PROFICIENT_OR_BETTER),
                LearningNode.content["mastery_track"].astext == "true",
            )
        )
        completed_track = completed_track_result.scalar_one() or 0

        rows.append(
            {
                "subject": subject.name,
                "subject_id": str(subject.id),
                "current_tier": current_tier,
                "mastery_depth": depth,
                "eligible_for_next": bool(eligibility.get("eligible")),
                "pct_mastered_tier5": eligibility.get("pct_mastered", 0.0),
                "total_mastery_track_nodes_completed": completed_track,
            }
        )
    return rows


async def _infer_highest_tier(
    db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID, subject_id: uuid.UUID
) -> str:
    """Label the child's highest active tier from their map enrollments."""
    maps_result = await db.execute(
        select(LearningMap.name).where(
            LearningMap.household_id == household_id,
            LearningMap.subject_id == subject_id,
        )
    )
    names = [n for (n,) in maps_result.all()]
    # Prefer the most-advanced tier by position in the canonical ordering.
    ordered = ["Foundations", "Development", "Intermediate", "Advanced", "Independent"]
    best_idx = -1
    best_name = None
    for name in names:
        for idx, label in enumerate(ordered):
            if name.endswith(f": {label}") and idx > best_idx:
                best_idx = idx
                best_name = f"Tier {idx + 1}"
    return best_name or "unranked"
