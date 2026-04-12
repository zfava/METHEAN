"""Family Intelligence — cross-child pattern detection.

Identifies systemic issues no per-child model can see. All detection
requires 2+ children with active learning data. Single-child households
produce no insights by design.
"""

import logging
import math
import uuid
from collections import defaultdict
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.calibration import EvaluatorPrediction
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import FamilyPatternType, InsightStatus, MasteryLevel
from app.models.family_insight import FamilyInsight, FamilyInsightConfig
from app.models.identity import Child
from app.models.state import ChildNodeState

logger = logging.getLogger(__name__)

# Statuses that indicate a non-duplicate existing insight
ACTIVE_STATUSES = {InsightStatus.detected, InsightStatus.notified, InsightStatus.acknowledged}

DEFAULT_CONFIG = {
    "shared_struggle": {"enabled": True, "min_children": 2, "drift_threshold": 1.5},
    "curriculum_gap": {"enabled": True, "confidence_threshold": 0.5},
    "pacing_divergence": {"enabled": True, "divergence_factor": 2.0},
    "environmental_correlation": {"enabled": True, "window_days": 7},
    "material_effectiveness": {"enabled": True, "min_attempts": 5},
}


# ── Helpers ──


async def _get_household_children(db: AsyncSession, household_id: uuid.UUID) -> list[Child]:
    result = await db.execute(select(Child).where(Child.household_id == household_id))
    return list(result.scalars().all())


async def _get_node_title(db: AsyncSession, node_id: uuid.UUID) -> str:
    result = await db.execute(select(LearningNode.title).where(LearningNode.id == node_id))
    row = result.one_or_none()
    return row[0] if row else "Unknown Node"


async def _get_node_subject(db: AsyncSession, node_id: uuid.UUID) -> str:
    result = await db.execute(
        select(Subject.name)
        .join(LearningMap, Subject.id == LearningMap.subject_id)
        .join(LearningNode, LearningMap.id == LearningNode.learning_map_id)
        .where(LearningNode.id == node_id)
    )
    row = result.one_or_none()
    return row[0] if row else "Unknown"


async def _insight_exists(
    db: AsyncSession,
    household_id: uuid.UUID,
    pattern_type: FamilyPatternType,
    affected_nodes: list[str],
) -> bool:
    """Check if a non-dismissed insight already exists for this pattern + nodes."""
    result = await db.execute(
        select(func.count())
        .select_from(FamilyInsight)
        .where(
            FamilyInsight.household_id == household_id,
            FamilyInsight.pattern_type == pattern_type,
            FamilyInsight.affected_nodes == affected_nodes,
            FamilyInsight.status.in_([s.value for s in ACTIVE_STATUSES]),
        )
    )
    return (result.scalar() or 0) > 0


def _get_setting(config: FamilyInsightConfig | None, pattern: str) -> dict:
    """Get settings for a pattern type, with defaults."""
    if config and config.pattern_settings:
        return config.pattern_settings.get(pattern, DEFAULT_CONFIG.get(pattern, {}))
    return DEFAULT_CONFIG.get(pattern, {})


def _is_enabled(config: FamilyInsightConfig | None, pattern: str) -> bool:
    if config and not config.enabled:
        return False
    settings = _get_setting(config, pattern)
    return settings.get("enabled", True)


# ── Detection Algorithm 1: Shared Struggle ──


async def detect_shared_struggles(
    db: AsyncSession,
    household_id: uuid.UUID,
    children: list[Child],
    config: FamilyInsightConfig | None,
) -> list[FamilyInsight]:
    if not _is_enabled(config, "shared_struggle") or len(children) < 2:
        return []

    settings = _get_setting(config, "shared_struggle")
    min_children = settings.get("min_children", 2)
    cutoff = datetime.now(UTC) - timedelta(days=90)

    child_ids = [c.id for c in children]
    child_names = {c.id: c.first_name for c in children}

    # Get struggling states
    result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.household_id == household_id,
            ChildNodeState.child_id.in_(child_ids),
            ChildNodeState.mastery_level.in_([MasteryLevel.emerging, MasteryLevel.developing]),
            ChildNodeState.attempts_count >= 3,
        )
    )
    states = result.scalars().all()

    # Group by node_id
    node_children: dict[uuid.UUID, list[ChildNodeState]] = defaultdict(list)
    for s in states:
        if s.last_activity_at and s.last_activity_at >= cutoff:
            node_children[s.node_id].append(s)

    insights = []
    for node_id, child_states in node_children.items():
        if len(child_states) < min_children:
            continue

        node_id_str = str(node_id)
        if await _insight_exists(db, household_id, FamilyPatternType.shared_struggle, [node_id_str]):
            continue

        node_title = await _get_node_title(db, node_id)
        subject = await _get_node_subject(db, node_id)
        affected = [str(s.child_id) for s in child_states]
        names = [child_names.get(s.child_id, "?") for s in child_states]

        evidence = {
            "children": [
                {
                    "child_id": str(s.child_id),
                    "child_name": child_names.get(s.child_id, "?"),
                    "mastery_level": s.mastery_level.value
                    if hasattr(s.mastery_level, "value")
                    else str(s.mastery_level),
                    "attempts_count": s.attempts_count,
                }
                for s in child_states
            ],
            "node_title": node_title,
        }

        confidence = len(child_states) / len(children)
        names_str = " and ".join(names) if len(names) <= 2 else ", ".join(names[:-1]) + f", and {names[-1]}"

        insight = FamilyInsight(
            household_id=household_id,
            pattern_type=FamilyPatternType.shared_struggle,
            affected_children=affected,
            affected_nodes=[node_id_str],
            affected_subjects=[subject],
            evidence_json=evidence,
            confidence=round(confidence, 2),
            recommendation=(
                f"Both {names_str} have found {node_title} challenging. "
                f"This may indicate the attached materials need supplementing, "
                f"or that this concept benefits from a different teaching approach."
            ),
        )
        db.add(insight)
        insights.append(insight)

    return insights


# ── Detection Algorithm 2: Curriculum Gap ──


async def detect_curriculum_gaps(
    db: AsyncSession,
    household_id: uuid.UUID,
    children: list[Child],
    config: FamilyInsightConfig | None,
) -> list[FamilyInsight]:
    if not _is_enabled(config, "curriculum_gap") or len(children) < 2:
        return []

    settings = _get_setting(config, "curriculum_gap")
    conf_threshold = settings.get("confidence_threshold", 0.5)
    child_ids = [c.id for c in children]
    {c.id: c.first_name for c in children}

    # Get all predictions, grouped by child+node, find first per child per node
    result = await db.execute(
        select(EvaluatorPrediction)
        .where(
            EvaluatorPrediction.household_id == household_id,
            EvaluatorPrediction.child_id.in_(child_ids),
        )
        .order_by(EvaluatorPrediction.created_at)
    )
    all_preds = result.scalars().all()

    # First prediction per (child, node)
    first_pred: dict[tuple[uuid.UUID, uuid.UUID], EvaluatorPrediction] = {}
    for p in all_preds:
        key = (p.child_id, p.node_id)
        if key not in first_pred:
            first_pred[key] = p

    # Group by node: find nodes attempted by 2+ children
    node_first_attempts: dict[uuid.UUID, list[EvaluatorPrediction]] = defaultdict(list)
    for (_child_id, node_id), pred in first_pred.items():
        node_first_attempts[node_id].append(pred)

    insights = []
    for node_id, preds in node_first_attempts.items():
        if len(preds) < 2:
            continue

        # Check if ALL first attempts are below threshold
        if all(p.predicted_confidence < conf_threshold for p in preds):
            node_id_str = str(node_id)
            if await _insight_exists(db, household_id, FamilyPatternType.curriculum_gap, [node_id_str]):
                continue

            node_title = await _get_node_title(db, node_id)
            subject = await _get_node_subject(db, node_id)
            affected = list({str(p.child_id) for p in preds})

            avg_conf = sum(p.predicted_confidence for p in preds) / len(preds)
            insight = FamilyInsight(
                household_id=household_id,
                pattern_type=FamilyPatternType.curriculum_gap,
                affected_children=affected,
                affected_nodes=[node_id_str],
                affected_subjects=[subject],
                evidence_json={
                    "node_title": node_title,
                    "first_attempt_confidences": [
                        {"child_id": str(p.child_id), "confidence": p.predicted_confidence} for p in preds
                    ],
                },
                confidence=round(1.0 - avg_conf, 2),
                recommendation=(
                    f"{node_title} appears to be consistently challenging on first exposure "
                    f"for your children. Consider supplementing the materials for this topic "
                    f"or adjusting the prerequisite sequence."
                ),
            )
            db.add(insight)
            insights.append(insight)

    return insights


# ── Detection Algorithm 3: Pacing Divergence ──


async def detect_pacing_divergence(
    db: AsyncSession,
    household_id: uuid.UUID,
    children: list[Child],
    config: FamilyInsightConfig | None,
) -> list[FamilyInsight]:
    if not _is_enabled(config, "pacing_divergence") or len(children) < 2:
        return []

    settings = _get_setting(config, "pacing_divergence")
    divergence_factor = settings.get("divergence_factor", 2.0)

    [c.id for c in children]
    child_names = {c.id: c.first_name for c in children}
    cutoff = datetime.now(UTC) - timedelta(weeks=4)

    # Compute mastered-per-week for each child over last 4 weeks
    child_rates: dict[uuid.UUID, float] = {}
    for child in children:
        result = await db.execute(
            select(func.count())
            .select_from(ChildNodeState)
            .where(
                ChildNodeState.child_id == child.id,
                ChildNodeState.household_id == household_id,
                ChildNodeState.mastery_level == MasteryLevel.mastered,
                ChildNodeState.last_activity_at >= cutoff,
            )
        )
        mastered_count = result.scalar() or 0
        child_rates[child.id] = mastered_count / 4.0  # per week

    # Find pairs with divergence >= factor
    rates = list(child_rates.items())
    if not rates:
        return []

    max_rate = max(r for _, r in rates)
    min_rate = min(r for _, r in rates)

    if min_rate == 0 and max_rate == 0:
        return []

    # Check divergence
    if min_rate > 0 and max_rate / min_rate < divergence_factor:
        return []
    if min_rate == 0 and max_rate >= 1.0:
        pass  # Infinite divergence — always flag
    elif min_rate == 0:
        return []

    # Already have an active insight?
    if await _insight_exists(db, household_id, FamilyPatternType.pacing_divergence, []):
        return []

    fast_child = max(rates, key=lambda x: x[1])
    slow_child = min(rates, key=lambda x: x[1])

    insight = FamilyInsight(
        household_id=household_id,
        pattern_type=FamilyPatternType.pacing_divergence,
        affected_children=[str(cid) for cid, _ in rates],
        affected_nodes=[],
        affected_subjects=[],
        evidence_json={
            "child_rates": {str(cid): round(rate, 2) for cid, rate in rates},
            "window_weeks": 4,
        },
        confidence=round(min(1.0, (max_rate / max(min_rate, 0.01)) / 10), 2),
        recommendation=(
            f"{child_names.get(fast_child[0], '?')} is progressing at roughly "
            f"{fast_child[1]:.1f} nodes per week while "
            f"{child_names.get(slow_child[0], '?')} is at {slow_child[1]:.1f}. "
            f"This divergence may indicate that your family schedule works better "
            f"for one child than the other, or that their maps need difficulty adjustment."
        ),
    )
    db.add(insight)
    return [insight]


# ── Detection Algorithm 4: Environmental Correlation ──


async def detect_environmental_correlation(
    db: AsyncSession,
    household_id: uuid.UUID,
    children: list[Child],
    config: FamilyInsightConfig | None,
) -> list[FamilyInsight]:
    if not _is_enabled(config, "environmental_correlation") or len(children) < 2:
        return []

    child_ids = [c.id for c in children]
    cutoff = datetime.now(UTC) - timedelta(days=30)

    # Get daily confidence averages per child
    result = await db.execute(
        select(EvaluatorPrediction)
        .where(
            EvaluatorPrediction.household_id == household_id,
            EvaluatorPrediction.child_id.in_(child_ids),
            EvaluatorPrediction.created_at >= cutoff,
        )
        .order_by(EvaluatorPrediction.created_at)
    )
    preds = result.scalars().all()

    if not preds:
        return []

    # Group by child → day → confidences
    child_daily: dict[uuid.UUID, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for p in preds:
        if p.created_at:
            day = p.created_at.date().isoformat()
            child_daily[p.child_id][day].append(p.predicted_confidence)

    # Need data for all children
    if len(child_daily) < 2:
        return []

    # Compute per-child mean and std_dev
    child_stats: dict[uuid.UUID, tuple[float, float]] = {}
    for child_id, daily in child_daily.items():
        all_confs = [c for confs in daily.values() for c in confs]
        if len(all_confs) < 5:
            continue
        mean = sum(all_confs) / len(all_confs)
        variance = sum((c - mean) ** 2 for c in all_confs) / len(all_confs)
        std = math.sqrt(variance) if variance > 0 else 0.1
        child_stats[child_id] = (mean, std)

    if len(child_stats) < 2:
        return []

    # Find days where ALL children dip below their mean - 1 std
    all_days = set()
    for daily in child_daily.values():
        all_days.update(daily.keys())

    dip_days = []
    for day in sorted(all_days):
        dipped_count = 0
        total_with_data = 0
        for child_id, (mean, std) in child_stats.items():
            day_confs = child_daily[child_id].get(day, [])
            if not day_confs:
                continue
            total_with_data += 1
            day_avg = sum(day_confs) / len(day_confs)
            if day_avg < mean - std:
                dipped_count += 1
        if total_with_data >= 2 and dipped_count == total_with_data:
            dip_days.append(day)

    if not dip_days:
        return []

    # Already have an active insight?
    if await _insight_exists(db, household_id, FamilyPatternType.environmental_correlation, []):
        return []

    {c.id: c.first_name for c in children}
    date_range = f"{dip_days[0]} to {dip_days[-1]}" if len(dip_days) > 1 else dip_days[0]

    insight = FamilyInsight(
        household_id=household_id,
        pattern_type=FamilyPatternType.environmental_correlation,
        affected_children=[str(cid) for cid in child_stats.keys()],
        affected_nodes=[],
        affected_subjects=[],
        evidence_json={"dip_days": dip_days, "window_days": 30},
        confidence=round(len(dip_days) / 30, 2),
        recommendation=(
            f"All of your children showed a performance dip around {date_range}. "
            f"Broad changes across all children sometimes reflect factors outside "
            f"the curriculum, such as schedule disruptions, illness, or family "
            f"transitions. You know your family best."
        ),
    )
    db.add(insight)
    return [insight]


# ── Detection Algorithm 5: Material Effectiveness ──


async def detect_material_effectiveness(
    db: AsyncSession,
    household_id: uuid.UUID,
    children: list[Child],
    config: FamilyInsightConfig | None,
) -> list[FamilyInsight]:
    if not _is_enabled(config, "material_effectiveness") or len(children) < 2:
        return []

    settings = _get_setting(config, "material_effectiveness")
    min_attempts = settings.get("min_attempts", 5)
    child_ids = [c.id for c in children]
    child_names = {c.id: c.first_name for c in children}

    # Get all predictions grouped by (child, node)
    result = await db.execute(
        select(EvaluatorPrediction).where(
            EvaluatorPrediction.household_id == household_id,
            EvaluatorPrediction.child_id.in_(child_ids),
        )
    )
    preds = result.scalars().all()

    # Group by (node_id, child_id)
    node_child_confs: dict[uuid.UUID, dict[uuid.UUID, list[float]]] = defaultdict(lambda: defaultdict(list))
    for p in preds:
        node_child_confs[p.node_id][p.child_id].append(p.predicted_confidence)

    insights = []
    for node_id, child_confs in node_child_confs.items():
        # Need 2+ children each with min_attempts
        qualified = {cid: confs for cid, confs in child_confs.items() if len(confs) >= min_attempts}
        if len(qualified) < 2:
            continue

        # Compute average confidence per child
        child_avgs = {cid: sum(confs) / len(confs) for cid, confs in qualified.items()}
        avgs = list(child_avgs.values())
        max_avg = max(avgs)
        min_avg = min(avgs)

        if max_avg - min_avg < 0.3:
            continue

        node_id_str = str(node_id)
        if await _insight_exists(db, household_id, FamilyPatternType.material_effectiveness, [node_id_str]):
            continue

        node_title = await _get_node_title(db, node_id)
        subject = await _get_node_subject(db, node_id)

        best_child = max(child_avgs, key=child_avgs.get)
        worst_child = min(child_avgs, key=child_avgs.get)

        insight = FamilyInsight(
            household_id=household_id,
            pattern_type=FamilyPatternType.material_effectiveness,
            affected_children=[str(cid) for cid in qualified.keys()],
            affected_nodes=[node_id_str],
            affected_subjects=[subject],
            evidence_json={
                "node_title": node_title,
                "child_averages": {str(cid): round(avg, 3) for cid, avg in child_avgs.items()},
            },
            confidence=round((max_avg - min_avg), 2),
            recommendation=(
                f"The materials for {node_title} seem to work well for "
                f"{child_names.get(best_child, '?')} but less so for "
                f"{child_names.get(worst_child, '?')}. This is normal. "
                f"Different children learn differently. Consider supplementing "
                f"with alternative materials for {child_names.get(worst_child, '?')}."
            ),
        )
        db.add(insight)
        insights.append(insight)

    return insights


# ── Main Entry Point ──


async def run_family_intelligence(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> dict:
    """Run all five detection algorithms for one household.

    Returns summary dict with counts per pattern type.
    """
    children = await _get_household_children(db, household_id)
    if len(children) < 2:
        return {"skipped": True, "reason": "fewer_than_2_children", "insights_created": 0}

    # Fetch or create config
    config_result = await db.execute(
        select(FamilyInsightConfig).where(FamilyInsightConfig.household_id == household_id)
    )
    config = config_result.scalar_one_or_none()

    if config and not config.enabled:
        return {"skipped": True, "reason": "disabled", "insights_created": 0}

    counts: dict[str, int] = {}
    total = 0

    detectors = [
        ("shared_struggle", detect_shared_struggles),
        ("curriculum_gap", detect_curriculum_gaps),
        ("pacing_divergence", detect_pacing_divergence),
        ("environmental_correlation", detect_environmental_correlation),
        ("material_effectiveness", detect_material_effectiveness),
    ]

    for name, detector in detectors:
        try:
            results = await detector(db, household_id, children, config)
            counts[name] = len(results)
            total += len(results)

            # AuditLog per new insight
            for insight in results:
                try:
                    from app.models.enums import AuditAction
                    from app.models.operational import AuditLog

                    db.add(
                        AuditLog(
                            household_id=household_id,
                            action=AuditAction.create,
                            resource_type="family_insight",
                            resource_id=insight.id,
                            details={
                                "pattern_type": name,
                                "confidence": insight.confidence,
                            },
                        )
                    )
                except Exception:
                    pass
        except Exception:
            logger.exception("Family intelligence detector '%s' failed for household %s", name, household_id)
            counts[name] = 0

    await db.flush()

    return {
        "skipped": False,
        "insights_created": total,
        "counts": counts,
    }


# ── Predictive Scaffolding ──


async def generate_predictive_scaffolding(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> list[FamilyInsight]:
    """For nodes where older siblings struggled, create predictive insights
    for younger siblings approaching those nodes.

    Uses the transitive closure table to check if a child is within 2
    prerequisite hops of a difficult node.
    """
    from app.models.curriculum import LearningMapClosure

    children = await _get_household_children(db, household_id)
    if len(children) < 2:
        return []

    child_ids = [c.id for c in children]
    child_names = {c.id: c.first_name for c in children}

    # Get active shared_struggle and curriculum_gap insights
    result = await db.execute(
        select(FamilyInsight).where(
            FamilyInsight.household_id == household_id,
            FamilyInsight.pattern_type.in_(
                [
                    FamilyPatternType.shared_struggle,
                    FamilyPatternType.curriculum_gap,
                ]
            ),
            FamilyInsight.status.in_([s.value for s in ACTIVE_STATUSES]),
        )
    )
    source_insights = result.scalars().all()

    if not source_insights:
        return []

    # Get all node states per child (nodes they've attempted)
    state_result = await db.execute(
        select(ChildNodeState.child_id, ChildNodeState.node_id).where(
            ChildNodeState.household_id == household_id,
            ChildNodeState.child_id.in_(child_ids),
        )
    )
    child_attempted: dict[uuid.UUID, set[uuid.UUID]] = defaultdict(set)
    for row in state_result.all():
        child_attempted[row[0]].add(row[1])

    insights = []

    for source in source_insights:
        affected_node_strs = source.affected_nodes or []
        affected_child_strs = set(source.affected_children or [])

        for node_id_str in affected_node_strs:
            try:
                target_node_id = uuid.UUID(node_id_str)
            except ValueError:
                continue

            # Find children who have NOT attempted this node
            for child in children:
                if str(child.id) in affected_child_strs:
                    continue  # Already affected
                if target_node_id in child_attempted.get(child.id, set()):
                    continue  # Already attempted

                # Check if this child is within 2 hops via closure table
                closure_result = await db.execute(
                    select(LearningMapClosure).where(
                        LearningMapClosure.descendant_id == target_node_id,
                        LearningMapClosure.depth <= 2,
                        LearningMapClosure.depth >= 1,
                    )
                )
                ancestors = closure_result.scalars().all()
                ancestor_ids = {a.ancestor_id for a in ancestors}

                # Check if child has mastered any ancestor (meaning they're approaching)
                if not ancestor_ids:
                    continue

                mastered_ancestors = child_attempted.get(child.id, set()) & ancestor_ids
                if not mastered_ancestors:
                    continue

                # Check for existing predictive insight
                existing = await db.execute(
                    select(func.count())
                    .select_from(FamilyInsight)
                    .where(
                        FamilyInsight.household_id == household_id,
                        FamilyInsight.predictive_child_id == child.id,
                        FamilyInsight.predictive_node_id == target_node_id,
                        FamilyInsight.status.in_([s.value for s in ACTIVE_STATUSES]),
                    )
                )
                if (existing.scalar() or 0) > 0:
                    continue

                node_title = await _get_node_title(db, target_node_id)
                affected_names = [child_names.get(uuid.UUID(cid), "?") for cid in affected_child_strs]
                names_str = " and ".join(affected_names[:2])

                insight = FamilyInsight(
                    household_id=household_id,
                    pattern_type=source.pattern_type,
                    affected_children=list(affected_child_strs) + [str(child.id)],
                    affected_nodes=[node_id_str],
                    affected_subjects=source.affected_subjects,
                    evidence_json={
                        "source_insight_id": str(source.id),
                        "predictive": True,
                        "approaching_child": str(child.id),
                    },
                    confidence=round(source.confidence * 0.8, 2),
                    recommendation=(
                        f"{child.first_name} will encounter {node_title} soon. "
                        f"{names_str} both found this challenging. Consider allocating "
                        f"extra time or supplementary materials when {child.first_name} "
                        f"reaches this point."
                    ),
                    predictive_child_id=child.id,
                    predictive_node_id=target_node_id,
                )
                db.add(insight)
                insights.append(insight)

    if insights:
        await db.flush()

    return insights


# ── Context Builders for AI Prompt Injection ──


PATTERN_LABELS = {
    FamilyPatternType.shared_struggle: "SHARED STRUGGLE",
    FamilyPatternType.curriculum_gap: "CURRICULUM GAP",
    FamilyPatternType.pacing_divergence: "PACING DIVERGENCE",
    FamilyPatternType.environmental_correlation: "ENVIRONMENTAL",
    FamilyPatternType.material_effectiveness: "MATERIAL EFFECTIVENESS",
}


async def build_family_context(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> str:
    """Build plain-text family intelligence context for Advisor prompt injection.

    Returns empty string if no active insights exist.
    """
    result = await db.execute(
        select(FamilyInsight)
        .where(
            FamilyInsight.household_id == household_id,
            FamilyInsight.status.in_([s.value for s in ACTIVE_STATUSES]),
        )
        .order_by(FamilyInsight.confidence.desc())
        .limit(5)
    )
    insights = result.scalars().all()

    if not insights:
        return ""

    lines = ["FAMILY PATTERNS (across your children):"]
    for insight in insights:
        label = PATTERN_LABELS.get(insight.pattern_type, insight.pattern_type.value.upper())
        conf = f" (confidence: {insight.confidence:.2f})" if insight.confidence else ""
        lines.append(f"- {label}: {insight.recommendation}{conf}")

    lines.append("")
    lines.append(
        "Include a 'Family Patterns' section in your weekly report. "
        "Reference any active family insights. Explain what the pattern "
        "means and suggest concrete actions the parent can consider."
    )

    return "\n".join(lines)


async def build_planner_scaffolding_context(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> str:
    """Build plain-text predictive scaffolding context for Planner prompt.

    Returns warnings about upcoming nodes where siblings struggled.
    """
    result = await db.execute(
        select(FamilyInsight)
        .where(
            FamilyInsight.household_id == household_id,
            FamilyInsight.predictive_child_id == child_id,
            FamilyInsight.status.in_([s.value for s in ACTIVE_STATUSES]),
        )
        .order_by(FamilyInsight.confidence.desc())
        .limit(5)
    )
    insights = result.scalars().all()

    if not insights:
        return ""

    lines = ["SIBLING INTELLIGENCE:"]
    for insight in insights:
        node_title = "unknown"
        if insight.affected_nodes:
            node_title = insight.evidence_json.get("node_title", "")
            if not node_title:
                try:
                    node_title = await _get_node_title(db, uuid.UUID(insight.affected_nodes[0]))
                except Exception:
                    node_title = "unknown"
        lines.append(
            f'- WARNING: "{node_title}" was challenging for siblings. '
            f"Allocate extra time and consider supplementary materials "
            f"when scheduling this node."
        )

    return "\n".join(lines)
