"""Family Intelligence API — cross-child insights, config, governance."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db, require_active_subscription
from app.core.rate_limit import rate_limit_user
from app.models.curriculum import LearningNode
from app.models.enums import (
    AuditAction,
    GovernanceAction,
    InsightStatus,
)
from app.models.family_insight import FamilyInsight, FamilyInsightConfig
from app.models.governance import GovernanceEvent
from app.models.identity import Child, User
from app.models.operational import AuditLog

router = APIRouter(tags=["family-intelligence"], dependencies=[Depends(require_active_subscription)])

DEFAULT_SETTINGS = {
    "shared_struggle": {"enabled": True, "min_children": 2, "drift_threshold": 1.5},
    "curriculum_gap": {"enabled": True, "confidence_threshold": 0.5},
    "pacing_divergence": {"enabled": True, "divergence_factor": 2.0},
    "environmental_correlation": {"enabled": True, "window_days": 7},
    "material_effectiveness": {"enabled": True, "min_attempts": 5},
}


# ── Helpers ──


async def _resolve_children(db: AsyncSession, child_id_strs: list[str]) -> list[dict]:
    """Resolve child UUID strings to {id, name} dicts."""
    if not child_id_strs:
        return []
    try:
        ids = [uuid.UUID(cid) for cid in child_id_strs]
    except ValueError:
        return [{"id": cid, "name": "?"} for cid in child_id_strs]
    result = await db.execute(select(Child.id, Child.first_name).where(Child.id.in_(ids)))
    name_map = {row[0]: row[1] for row in result.all()}
    return [{"id": cid, "name": name_map.get(uuid.UUID(cid), "?")} for cid in child_id_strs]


async def _resolve_nodes(db: AsyncSession, node_id_strs: list[str]) -> list[dict]:
    """Resolve node UUID strings to {id, title} dicts."""
    if not node_id_strs:
        return []
    try:
        ids = [uuid.UUID(nid) for nid in node_id_strs]
    except ValueError:
        return [{"id": nid, "title": "?"} for nid in node_id_strs]
    result = await db.execute(select(LearningNode.id, LearningNode.title).where(LearningNode.id.in_(ids)))
    title_map = {row[0]: row[1] for row in result.all()}
    return [{"id": nid, "title": title_map.get(uuid.UUID(nid), "?")} for nid in node_id_strs]


async def _serialize_insight(db: AsyncSession, insight: FamilyInsight) -> dict:
    """Serialize a FamilyInsight with resolved names."""
    children = await _resolve_children(db, insight.affected_children or [])
    nodes = await _resolve_nodes(db, insight.affected_nodes or [])

    predictive_child = None
    if insight.predictive_child_id:
        r = await db.execute(select(Child.first_name).where(Child.id == insight.predictive_child_id))
        row = r.one_or_none()
        predictive_child = {"id": str(insight.predictive_child_id), "name": row[0] if row else "?"}

    return {
        "id": str(insight.id),
        "pattern_type": insight.pattern_type.value
        if hasattr(insight.pattern_type, "value")
        else str(insight.pattern_type),
        "affected_children": children,
        "affected_nodes": nodes,
        "affected_subjects": insight.affected_subjects or [],
        "confidence": insight.confidence,
        "recommendation": insight.recommendation,
        "status": insight.status.value if hasattr(insight.status, "value") else str(insight.status),
        "is_predictive": insight.predictive_child_id is not None,
        "predictive_child": predictive_child,
        "parent_response": insight.parent_response,
        "false_positive": insight.false_positive,
        "created_at": insight.created_at.isoformat() if insight.created_at else None,
    }


# ── GET /household/family-insights ──


@router.get("/household/family-insights")
async def list_family_insights(
    status: str | None = Query(None),
    pattern_type: str | None = Query(None),
    child_id: uuid.UUID | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Paginated list of FamilyInsights for the household."""
    query = select(FamilyInsight).where(
        FamilyInsight.household_id == user.household_id,
    )

    if status:
        query = query.where(FamilyInsight.status == status)
    if pattern_type:
        query = query.where(FamilyInsight.pattern_type == pattern_type)
    if child_id:
        # Filter insights where child_id appears in affected_children JSONB array
        child_str = str(child_id)
        query = query.where(FamilyInsight.affected_children.op("@>")(f'["{child_str}"]'))

    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Fetch page
    offset = (page - 1) * per_page
    query = query.order_by(FamilyInsight.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    insights = result.scalars().all()

    items = []
    for insight in insights:
        items.append(await _serialize_insight(db, insight))

    return {"items": items, "total": total, "page": page, "per_page": per_page}


# ── GET /household/family-insights/{insight_id} ──


@router.get("/household/family-insights/{insight_id}")
async def get_family_insight(
    insight_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Returns a single FamilyInsight with full evidence."""
    result = await db.execute(
        select(FamilyInsight).where(
            FamilyInsight.id == insight_id,
            FamilyInsight.household_id == user.household_id,
        )
    )
    insight = result.scalar_one_or_none()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")

    data = await _serialize_insight(db, insight)
    data["evidence_json"] = insight.evidence_json
    return data


# ── PATCH /household/family-insights/{insight_id}/status ──


class StatusUpdateRequest(BaseModel):
    status: str
    parent_response: str | None = None


@router.patch("/household/family-insights/{insight_id}/status")
async def update_insight_status(
    insight_id: uuid.UUID,
    body: StatusUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Update insight status (acknowledge, act on, or dismiss)."""
    valid_statuses = {"acknowledged", "acted_on", "dismissed"}
    if body.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {', '.join(valid_statuses)}")

    result = await db.execute(
        select(FamilyInsight).where(
            FamilyInsight.id == insight_id,
            FamilyInsight.household_id == user.household_id,
        )
    )
    insight = result.scalar_one_or_none()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")

    previous_status = insight.status.value if hasattr(insight.status, "value") else str(insight.status)
    insight.status = body.status
    if body.parent_response:
        insight.parent_response = body.parent_response
    if body.status == "dismissed":
        insight.false_positive = True

    action_map = {
        "acknowledged": "family_insight_acknowledged",
        "acted_on": "family_insight_acted_on",
        "dismissed": "family_insight_dismissed",
    }

    db.add(
        GovernanceEvent(
            household_id=user.household_id,
            user_id=user.id,
            action=GovernanceAction.modify,
            target_type="family_insight",
            target_id=insight.id,
            reason=f"{action_map[body.status]}: {insight.pattern_type.value if hasattr(insight.pattern_type, 'value') else insight.pattern_type}",
            metadata_={
                "action": action_map[body.status],
                "insight_id": str(insight.id),
                "pattern_type": insight.pattern_type.value
                if hasattr(insight.pattern_type, "value")
                else str(insight.pattern_type),
                "previous_status": previous_status,
                "new_status": body.status,
                "parent_response": body.parent_response,
            },
        )
    )

    db.add(
        AuditLog(
            household_id=user.household_id,
            user_id=user.id,
            action=AuditAction.update,
            resource_type="family_insight",
            resource_id=insight.id,
            details={"action": action_map[body.status], "previous_status": previous_status},
        )
    )

    await db.flush()
    await db.commit()
    return {"status": body.status, "insight_id": str(insight.id)}


# ── GET /household/family-insights/config ──


@router.get("/household/family-insights/config")
async def get_insight_config(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Returns the FamilyInsightConfig for this household."""
    result = await db.execute(
        select(FamilyInsightConfig).where(
            FamilyInsightConfig.household_id == user.household_id,
        )
    )
    config = result.scalar_one_or_none()

    if config is None:
        return {
            "enabled": True,
            "pattern_settings": DEFAULT_SETTINGS,
            "is_default": True,
        }

    return {
        "enabled": config.enabled,
        "pattern_settings": config.pattern_settings,
        "is_default": False,
    }


# ── PATCH /household/family-insights/config ──


class ConfigUpdateRequest(BaseModel):
    enabled: bool | None = None
    pattern_settings: dict | None = None


@router.patch("/household/family-insights/config")
async def update_insight_config(
    body: ConfigUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Update FamilyInsightConfig. Merges pattern_settings."""
    result = await db.execute(
        select(FamilyInsightConfig).where(
            FamilyInsightConfig.household_id == user.household_id,
        )
    )
    config = result.scalar_one_or_none()

    if config is None:
        config = FamilyInsightConfig(
            household_id=user.household_id,
            pattern_settings=dict(DEFAULT_SETTINGS),
        )
        db.add(config)
        await db.flush()

    changes = {}

    if body.enabled is not None:
        config.enabled = body.enabled
        changes["enabled"] = body.enabled

    if body.pattern_settings:
        current = dict(config.pattern_settings or DEFAULT_SETTINGS)
        for pattern_key, updates in body.pattern_settings.items():
            if pattern_key not in DEFAULT_SETTINGS:
                raise HTTPException(status_code=400, detail=f"Unknown pattern type: {pattern_key}")
            if not isinstance(updates, dict):
                raise HTTPException(status_code=400, detail=f"Settings for '{pattern_key}' must be an object")
            existing = current.get(pattern_key, {})
            existing.update(updates)
            current[pattern_key] = existing
        config.pattern_settings = current
        changes["pattern_settings"] = body.pattern_settings

    db.add(
        GovernanceEvent(
            household_id=user.household_id,
            user_id=user.id,
            action=GovernanceAction.modify,
            target_type="family_insight_config",
            target_id=config.id,
            reason=f"Family insight config updated: {list(changes.keys())}",
            metadata_={"changes": changes},
        )
    )

    db.add(
        AuditLog(
            household_id=user.household_id,
            user_id=user.id,
            action=AuditAction.update,
            resource_type="family_insight_config",
            resource_id=config.id,
            details=changes,
        )
    )

    await db.flush()
    await db.commit()
    return {"status": "updated", "changes": changes}


# ── GET /household/family-insights/summary ──


@router.get(
    "/household/family-insights/summary",
    dependencies=[Depends(rate_limit_user("ai_generation"))],
)
async def get_insight_summary(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Aggregate summary for the dashboard."""
    active_statuses = [InsightStatus.detected.value, InsightStatus.notified.value, InsightStatus.acknowledged.value]

    # Total active
    total_result = await db.execute(
        select(func.count())
        .select_from(FamilyInsight)
        .where(
            FamilyInsight.household_id == user.household_id,
            FamilyInsight.status.in_(active_statuses),
        )
    )
    total_active = total_result.scalar() or 0

    # By pattern type
    pattern_result = await db.execute(
        select(FamilyInsight.pattern_type, func.count())
        .where(
            FamilyInsight.household_id == user.household_id,
            FamilyInsight.status.in_(active_statuses),
        )
        .group_by(FamilyInsight.pattern_type)
    )
    by_pattern = {row[0].value if hasattr(row[0], "value") else str(row[0]): row[1] for row in pattern_result.all()}

    # By status
    status_result = await db.execute(
        select(FamilyInsight.status, func.count())
        .where(
            FamilyInsight.household_id == user.household_id,
            FamilyInsight.status.in_(active_statuses),
        )
        .group_by(FamilyInsight.status)
    )
    by_status = {row[0].value if hasattr(row[0], "value") else str(row[0]): row[1] for row in status_result.all()}

    # Predictive count
    predictive_result = await db.execute(
        select(func.count())
        .select_from(FamilyInsight)
        .where(
            FamilyInsight.household_id == user.household_id,
            FamilyInsight.status.in_(active_statuses),
            FamilyInsight.predictive_child_id.isnot(None),
        )
    )
    predictive_count = predictive_result.scalar() or 0

    return {
        "total_active": total_active,
        "by_pattern_type": by_pattern,
        "by_status": by_status,
        "predictive_count": predictive_count,
    }
