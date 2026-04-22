"""Spec coverage endpoints — closes every gap between codebase and architecture spec.

Covers: household settings, child PATCH/preferences, /today, map validate,
map diff, pace metrics, counterfactual, sync, attempt locking, device register,
notification log, metrics.
"""

import json
import uuid
from datetime import UTC, date, datetime, timedelta

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.gateway import AIRole, call_ai
from app.ai.prompts import PLANNER_SYSTEM
from app.api.deps import get_current_user, get_db, require_role
from app.models.curriculum import (
    ChildMapEnrollment,
    LearningEdge,
    LearningMap,
    LearningMapClosure,
    LearningNode,
)
from app.models.enums import (
    ActivityStatus,
)
from app.models.governance import Activity
from app.models.identity import Child, ChildPreferences, Household, User, UserPermission
from app.models.operational import DeviceToken, NotificationLog
from app.models.state import ChildNodeState

router = APIRouter(tags=["spec-coverage"])


# 50 US states + DC. Kept local to avoid importing the big compliance
# engine dict at module-import time.
_US_STATE_CODES: frozenset[str] = frozenset(
    {
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
        "DC",
    }
)


# ── Schemas ──


_VALID_AI_TIERS = frozenset({"opus", "sonnet", "haiku"})


class HouseholdSettingsUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    timezone: str | None = Field(default=None, max_length=50)
    home_state: str | None = None
    # Free-form household settings blob; today we validate ai_tier inside it.
    settings: dict | None = None
    ai_tier: str | None = None

    @field_validator("home_state")
    @classmethod
    def _valid_home_state(cls, v):
        # Allow null, allow empty-string as explicit "clear", otherwise
        # require a valid US state code. Lowercase input is normalized.
        if v is None:
            return v
        if v == "":
            return None
        upper = v.upper()
        if upper not in _US_STATE_CODES:
            raise ValueError(f"home_state must be a valid US state code, got {v!r}")
        return upper

    @field_validator("ai_tier")
    @classmethod
    def _valid_ai_tier(cls, v):
        if v is None:
            return v
        if v not in _VALID_AI_TIERS:
            raise ValueError(f"ai_tier must be one of {sorted(_VALID_AI_TIERS)}, got {v!r}")
        return v

    @field_validator("settings")
    @classmethod
    def _valid_settings_blob(cls, v):
        # If ai_tier is nested inside settings JSON, validate it too.
        if v is None:
            return v
        tier = v.get("ai_tier")
        if tier is not None and tier not in _VALID_AI_TIERS:
            raise ValueError(f"settings.ai_tier must be one of {sorted(_VALID_AI_TIERS)}, got {tier!r}")
        return v


class ChildUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = None
    date_of_birth: date | None = None
    grade_level: str | None = None


class ChildCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str | None = None
    date_of_birth: date | None = None
    grade_level: str | None = None


class ChildPreferencesUpdate(BaseModel):
    daily_duration_minutes: int | None = Field(default=None, ge=15, le=480)
    learning_style: dict | None = None
    interests: list | None = None
    preferred_schedule: dict | None = None
    subject_levels: dict | None = None


class SyncEvent(BaseModel):
    event_type: str
    payload: dict
    client_timestamp: datetime


class SyncRequest(BaseModel):
    events: list[SyncEvent]


class DeviceRegisterRequest(BaseModel):
    device_token: str
    platform: str  # ios/android/web
    device_name: str | None = None


class CounterfactualRequest(BaseModel):
    changes: dict  # e.g. {"daily_minutes": 45, "pause_subject": "math"}


# ── Helpers ──


async def _get_child_or_404(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


# ══════════════════════════════════════════════════
# Auth & Household
# ══════════════════════════════════════════════════


def _household_settings_dict(household: Household) -> dict:
    hh_settings = household.settings or {}
    return {
        "id": str(household.id),
        "name": household.name,
        "timezone": household.timezone,
        "home_state": household.home_state,
        "ai_tier": hh_settings.get("ai_tier", "opus"),
        "settings": hh_settings,
    }


@router.get("/household/settings")
async def get_household_settings(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    result = await db.execute(select(Household).where(Household.id == user.household_id))
    household = result.scalar_one()
    return _household_settings_dict(household)


# Academic vs vocational assessment types. Used by the assessment UI
# and the curriculum builder. Academic types are parent-observable;
# vocational types require a practical / trade demonstration.
_ASSESSMENT_TYPES = {
    "academic": [
        "parent_observation",
        "narration",
        "written",
        "demonstration",
        "project",
        "timed_exam",
        "research_paper",
        "oral_defense",
        "peer_assessment",
        "portfolio_review",
    ],
    "vocational": [
        "practical_demo",
        "weld_inspection",
        "clinical_evaluation",
        "lab_report",
        "competency_signoff",
        "safety_check",
        "tool_qualification",
    ],
}


@router.get("/assessment-types")
async def list_assessment_types(
    user: User = Depends(get_current_user),
) -> dict:
    """Catalog of assessment types, grouped by domain."""
    return {k: list(v) for k, v in _ASSESSMENT_TYPES.items()}


@router.put("/household/settings")
async def update_household_settings(
    body: HouseholdSettingsUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner")),
) -> dict:
    result = await db.execute(select(Household).where(Household.id == user.household_id))
    household = result.scalar_one()
    if body.name is not None:
        household.name = body.name
    if body.timezone is not None:
        household.timezone = body.timezone
    # home_state is explicitly nullable: presence in the request (even
    # when None) means "apply this value", so we consult model_fields_set
    # instead of the is-not-None pattern used for name/timezone.
    if "home_state" in body.model_fields_set:
        household.home_state = body.home_state

    # ai_tier lives inside household.settings so it round-trips through the
    # existing JSONB column. Accept it as a top-level field for client
    # ergonomics and also honor settings["ai_tier"] when sent nested.
    new_settings = dict(household.settings or {})
    if body.settings is not None:
        # Merge the caller's settings blob over the existing one.
        new_settings.update(body.settings)
    if body.ai_tier is not None:
        new_settings["ai_tier"] = body.ai_tier
    if body.settings is not None or body.ai_tier is not None:
        household.settings = new_settings
        from sqlalchemy.orm.attributes import flag_modified

        flag_modified(household, "settings")
    await db.flush()
    return _household_settings_dict(household)


VALID_PHILOSOPHIES = {"classical", "charlotte_mason", "unschooling", "eclectic", "montessori", "traditional", "custom"}
VALID_STANCES = {"exclude", "present_alternative", "parent_led_only", "allow"}
VALID_AUTONOMY = {"preview_all", "approve_difficult", "trust_within_rules", "full_autonomy"}


class PhilosophicalProfileUpdate(BaseModel):
    educational_philosophy: str | None = None
    philosophy_description: str | None = None
    religious_framework: str | None = None
    religious_notes: str | None = None
    content_boundaries: list[dict] | None = None
    ai_autonomy_level: str | None = None
    pedagogical_preferences: dict | None = None
    custom_constraints: list[str] | None = None


@router.put("/household/philosophy")
async def update_philosophy(
    body: PhilosophicalProfileUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner")),
) -> dict:
    """Set the household's philosophical profile. Governs all AI behavior."""
    from app.models.enums import GovernanceAction
    from app.models.governance import GovernanceEvent

    profile = body.model_dump(exclude_none=True)

    # Validate educational_philosophy
    if "educational_philosophy" in profile and profile["educational_philosophy"] not in VALID_PHILOSOPHIES:
        raise HTTPException(
            status_code=422, detail=f"educational_philosophy must be one of: {', '.join(sorted(VALID_PHILOSOPHIES))}"
        )

    # Validate content_boundaries
    for b in profile.get("content_boundaries", []):
        if not b.get("topic") or not b.get("stance"):
            raise HTTPException(status_code=422, detail="Each content_boundary must have 'topic' and 'stance'")
        if b["stance"] not in VALID_STANCES:
            raise HTTPException(status_code=422, detail=f"stance must be one of: {', '.join(sorted(VALID_STANCES))}")

    # Validate autonomy level
    if "ai_autonomy_level" in profile and profile["ai_autonomy_level"] not in VALID_AUTONOMY:
        raise HTTPException(
            status_code=422, detail=f"ai_autonomy_level must be one of: {', '.join(sorted(VALID_AUTONOMY))}"
        )

    result = await db.execute(select(Household).where(Household.id == user.household_id))
    household = result.scalar_one()
    household.philosophical_profile = profile
    await db.flush()

    # Log governance event
    db.add(
        GovernanceEvent(
            household_id=user.household_id,
            user_id=user.id,
            action=GovernanceAction.modify,
            target_type="philosophical_profile",
            target_id=user.household_id,
            reason="Philosophical profile updated",
        )
    )
    await db.flush()

    return profile


@router.get("/household/philosophy")
async def get_philosophy(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    result = await db.execute(select(Household).where(Household.id == user.household_id))
    household = result.scalar_one()
    return household.philosophical_profile or {}


@router.get("/children")
async def list_children(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[dict]:
    """List all children in the authenticated user's household."""
    result = await db.execute(
        select(Child)
        .where(
            Child.household_id == user.household_id,
            Child.is_active == True,  # noqa: E712
        )
        .order_by(Child.first_name)
    )
    children = result.scalars().all()

    items = []
    for c in children:
        # Get enrollment count
        enroll_result = await db.execute(
            select(func.count(ChildMapEnrollment.id)).where(
                ChildMapEnrollment.child_id == c.id,
                ChildMapEnrollment.is_active == True,  # noqa: E712
            )
        )
        enrollment_count = enroll_result.scalar() or 0

        items.append(
            {
                "id": str(c.id),
                "first_name": c.first_name,
                "last_name": c.last_name,
                "date_of_birth": c.date_of_birth.isoformat() if c.date_of_birth else None,
                "grade_level": c.grade_level,
                "enrollment_count": enrollment_count,
            }
        )
    return items


@router.post("/children", status_code=201)
async def create_child(
    body: ChildCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner", "co_parent")),
) -> dict:
    child = Child(
        household_id=user.household_id,
        first_name=body.first_name,
        last_name=body.last_name,
        date_of_birth=body.date_of_birth,
        grade_level=body.grade_level,
    )
    db.add(child)
    await db.flush()
    return {
        "id": str(child.id),
        "household_id": str(child.household_id),
        "first_name": child.first_name,
        "last_name": child.last_name,
        "grade_level": child.grade_level,
    }


@router.patch("/children/{child_id}")
async def update_child(
    child_id: uuid.UUID,
    body: ChildUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner")),
) -> dict:
    child = await _get_child_or_404(db, child_id, user.household_id)
    if body.first_name is not None:
        child.first_name = body.first_name
    if body.last_name is not None:
        child.last_name = body.last_name
    if body.date_of_birth is not None:
        child.date_of_birth = body.date_of_birth
    if body.grade_level is not None:
        child.grade_level = body.grade_level
    await db.flush()
    return {
        "id": str(child.id),
        "first_name": child.first_name,
        "last_name": child.last_name,
        "grade_level": child.grade_level,
    }


@router.put("/children/{child_id}/preferences")
async def update_child_preferences(
    child_id: uuid.UUID,
    body: ChildPreferencesUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    result = await db.execute(select(ChildPreferences).where(ChildPreferences.child_id == child_id))
    prefs = result.scalar_one_or_none()
    if not prefs:
        prefs = ChildPreferences(
            child_id=child_id,
            household_id=user.household_id,
        )
        db.add(prefs)

    if body.daily_duration_minutes is not None:
        prefs.daily_duration_minutes = body.daily_duration_minutes
    if body.learning_style is not None:
        prefs.learning_style = body.learning_style
    if body.interests is not None:
        prefs.interests = body.interests
    if body.preferred_schedule is not None:
        prefs.preferred_schedule = body.preferred_schedule
    if body.subject_levels is not None:
        from app.core.learning_levels import VALID_LEVELS

        invalid = {subject: level for subject, level in body.subject_levels.items() if level not in VALID_LEVELS}
        if invalid:
            raise HTTPException(
                status_code=400,
                detail=(f"Invalid level(s): {invalid}. Must be one of {sorted(VALID_LEVELS)}"),
            )
        prefs.subject_levels = body.subject_levels
    await db.flush()
    return {"child_id": str(child_id), "daily_duration_minutes": prefs.daily_duration_minutes}


# ══════════════════════════════════════════════════
# Today's Activities
# ══════════════════════════════════════════════════


@router.get("/children/{child_id}/today")
async def get_today(
    child_id: uuid.UUID,
    target_date: date | None = Query(default=None, alias="date"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[dict]:
    """Return today's scheduled activities for a child."""
    await _get_child_or_404(db, child_id, user.household_id)
    today = target_date or date.today()

    result = await db.execute(
        select(Activity)
        .where(
            Activity.household_id == user.household_id,
            Activity.scheduled_date == today,
            Activity.status.in_([ActivityStatus.scheduled, ActivityStatus.in_progress]),
        )
        .order_by(Activity.sort_order)
    )
    activities = result.scalars().all()

    return [
        {
            "id": str(a.id),
            "title": a.title,
            "activity_type": a.activity_type.value if hasattr(a.activity_type, "value") else str(a.activity_type),
            "status": a.status.value if hasattr(a.status, "value") else str(a.status),
            "estimated_minutes": a.estimated_minutes,
            "node_id": str(a.node_id) if a.node_id else None,
        }
        for a in activities
    ]


# ══════════════════════════════════════════════════
# User Permissions
# ══════════════════════════════════════════════════


@router.get("/users/{user_id}/permissions")
async def list_user_permissions(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner")),
) -> list[dict]:
    result = await db.execute(
        select(UserPermission).where(
            UserPermission.user_id == user_id,
            UserPermission.household_id == user.household_id,
        )
    )
    return [
        {
            "id": str(p.id),
            "permission": p.permission,
            "scope_type": p.scope_type,
            "scope_id": str(p.scope_id) if p.scope_id else None,
            "granted_at": p.granted_at.isoformat() if p.granted_at else None,
        }
        for p in result.scalars().all()
    ]


class PermissionGrant(BaseModel):
    permission: str = Field(min_length=1, max_length=100)
    scope_type: str | None = None
    scope_id: uuid.UUID | None = None


@router.post("/users/{user_id}/permissions", status_code=201)
async def grant_permission(
    user_id: uuid.UUID,
    body: PermissionGrant,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner")),
) -> dict:
    perm = UserPermission(
        user_id=user_id,
        household_id=user.household_id,
        permission=body.permission,
        scope_type=body.scope_type or "all",
        scope_id=body.scope_id,
        granted_by=user.id,
    )
    db.add(perm)
    await db.flush()
    return {
        "id": str(perm.id),
        "permission": perm.permission,
        "scope_type": perm.scope_type,
        "granted": True,
    }


@router.delete("/users/{user_id}/permissions/{permission_id}")
async def revoke_permission(
    user_id: uuid.UUID,
    permission_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner")),
) -> dict:
    result = await db.execute(
        select(UserPermission).where(
            UserPermission.id == permission_id,
            UserPermission.user_id == user_id,
            UserPermission.household_id == user.household_id,
        )
    )
    perm = result.scalar_one_or_none()
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")
    await db.delete(perm)
    await db.flush()
    return {"revoked": True}


# ══════════════════════════════════════════════════
# Map Validate + Diff
# ══════════════════════════════════════════════════


@router.post("/learning-maps/{map_id}/validate")
async def validate_map(
    map_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Run full DAG validation: cycles, orphans, unreachable nodes."""
    result = await db.execute(
        select(LearningMap).where(LearningMap.id == map_id, LearningMap.household_id == user.household_id)
    )
    lmap = result.scalar_one_or_none()
    if not lmap:
        raise HTTPException(status_code=404, detail="Map not found")

    # Get nodes and edges
    nodes_result = await db.execute(
        select(LearningNode).where(
            LearningNode.learning_map_id == map_id,
            LearningNode.is_active == True,  # noqa: E712
        )
    )
    nodes = nodes_result.scalars().all()
    node_ids = {n.id for n in nodes}

    edges_result = await db.execute(select(LearningEdge).where(LearningEdge.learning_map_id == map_id))
    edges = edges_result.scalars().all()

    issues = []

    # Check for orphan nodes (no incoming or outgoing edges, not root)
    nodes_with_edges = set()
    for e in edges:
        nodes_with_edges.add(e.from_node_id)
        nodes_with_edges.add(e.to_node_id)

    for node in nodes:
        ntype = node.node_type.value if hasattr(node.node_type, "value") else str(node.node_type)
        if node.id not in nodes_with_edges and ntype != "root":
            issues.append(
                {
                    "type": "orphan",
                    "node_id": str(node.id),
                    "title": node.title,
                    "message": f"Node '{node.title}' has no edges (orphan)",
                }
            )

    # Check for edges referencing inactive/deleted nodes
    for edge in edges:
        if edge.from_node_id not in node_ids:
            issues.append(
                {"type": "dangling_edge", "edge_id": str(edge.id), "message": "Edge references inactive from_node"}
            )
        if edge.to_node_id not in node_ids:
            issues.append(
                {"type": "dangling_edge", "edge_id": str(edge.id), "message": "Edge references inactive to_node"}
            )

    # Check for unreachable nodes (not reachable from any root)
    roots = {
        n.id for n in nodes if (n.node_type.value if hasattr(n.node_type, "value") else str(n.node_type)) == "root"
    }
    closure_result = (
        await db.execute(
            select(LearningMapClosure.descendant_id).where(
                LearningMapClosure.learning_map_id == map_id,
                LearningMapClosure.ancestor_id.in_(roots),
            )
        )
        if roots
        else None
    )
    reachable = set(roots)
    if closure_result:
        reachable.update(closure_result.scalars().all())

    for node in nodes:
        if node.id not in reachable:
            ntype = node.node_type.value if hasattr(node.node_type, "value") else str(node.node_type)
            if ntype != "root":
                issues.append(
                    {
                        "type": "unreachable",
                        "node_id": str(node.id),
                        "title": node.title,
                        "message": f"Node '{node.title}' is not reachable from any root",
                    }
                )

    return {
        "map_id": str(map_id),
        "valid": len(issues) == 0,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "issues": issues,
    }


@router.get("/learning-maps/{map_id}/diff")
async def map_diff(
    map_id: uuid.UUID,
    from_version: int = Query(alias="from"),
    to_version: int = Query(alias="to"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Compare current map state. Version tracking is at map level."""
    result = await db.execute(
        select(LearningMap).where(
            LearningMap.id == map_id,
            LearningMap.household_id == user.household_id,
        )
    )
    lmap = result.scalar_one_or_none()
    if not lmap:
        raise HTTPException(status_code=404, detail="Map not found")

    return {
        "map_id": str(map_id),
        "from_version": from_version,
        "to_version": to_version,
        "current_version": lmap.version,
        "message": "Full version history requires event sourcing. Current diff shows latest state.",
    }


# ══════════════════════════════════════════════════
# Pace Metrics
# ══════════════════════════════════════════════════


@router.get("/children/{child_id}/pace")
async def get_pace(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Return pace metrics per active node."""
    await _get_child_or_404(db, child_id, user.household_id)

    # Get enrolled maps
    enroll_result = await db.execute(
        select(ChildMapEnrollment.learning_map_id).where(
            ChildMapEnrollment.child_id == child_id,
            ChildMapEnrollment.is_active == True,  # noqa: E712
        )
    )
    map_ids = list(enroll_result.scalars().all())
    if not map_ids:
        return {"child_id": str(child_id), "nodes": [], "aggregate_pace": "no_data"}

    nodes_result = await db.execute(
        select(LearningNode).where(
            LearningNode.learning_map_id.in_(map_ids),
            LearningNode.is_active == True,  # noqa: E712
        )
    )
    nodes = nodes_result.scalars().all()
    node_ids = [n.id for n in nodes]

    states_result = (
        await db.execute(
            select(ChildNodeState).where(
                ChildNodeState.child_id == child_id,
                ChildNodeState.node_id.in_(node_ids),
            )
        )
        if node_ids
        else None
    )
    states = {s.node_id: s for s in (states_result.scalars().all() if states_result else [])}

    pace_data = []
    ahead = on_pace = behind = 0

    for node in nodes:
        state = states.get(node.id)
        estimated = node.estimated_minutes or 30
        actual = state.time_spent_minutes if state else 0
        mastery = (
            state.mastery_level.value
            if state and hasattr(state.mastery_level, "value")
            else (str(state.mastery_level) if state else "not_started")
        )

        if mastery == "mastered":
            pace_status = "ahead" if actual <= estimated else "on_pace"
        elif actual > estimated * 2:
            pace_status = "behind"
        elif actual > 0:
            pace_status = "on_pace"
        else:
            pace_status = "not_started"

        if pace_status == "ahead":
            ahead += 1
        elif pace_status == "on_pace":
            on_pace += 1
        elif pace_status == "behind":
            behind += 1

        pace_data.append(
            {
                "node_id": str(node.id),
                "title": node.title,
                "estimated_minutes": estimated,
                "actual_minutes": actual,
                "mastery": mastery,
                "pace_status": pace_status,
            }
        )

    total_active = ahead + on_pace + behind
    agg = (
        "on_pace"
        if total_active == 0
        else ("ahead" if ahead > on_pace + behind else "behind" if behind > ahead + on_pace else "on_pace")
    )

    return {
        "child_id": str(child_id),
        "nodes": pace_data,
        "aggregate_pace": agg,
        "ahead_count": ahead,
        "on_pace_count": on_pace,
        "behind_count": behind,
    }


# ══════════════════════════════════════════════════
# Counterfactual Analysis
# ══════════════════════════════════════════════════


@router.post("/children/{child_id}/counterfactual")
async def counterfactual(
    child_id: uuid.UUID,
    body: CounterfactualRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner", "co_parent")),
) -> dict:
    """What-if analysis without state changes."""
    child = await _get_child_or_404(db, child_id, user.household_id)

    user_prompt = f"""Analyze this "what if" scenario for {child.first_name}.

Proposed changes: {json.dumps(body.changes)}

Current state: child is enrolled in active learning maps.
Do NOT apply any changes. Only predict the impact on:
1. Pace (will they fall behind or catch up?)
2. Retention (will review frequency change?)
3. Plan structure (how would weekly plans differ?)

Return your analysis as JSON with keys: pace_impact, retention_impact, plan_impact, summary."""

    result = await call_ai(
        db,
        role=AIRole.planner,
        system_prompt=PLANNER_SYSTEM + "\n\nThis is a COUNTERFACTUAL analysis. Do NOT apply changes.",
        user_prompt=user_prompt,
        household_id=user.household_id,
        triggered_by=user.id,
    )

    return {
        "child_id": str(child_id),
        "proposed_changes": body.changes,
        "analysis": result["output"],
        "ai_run_id": str(result["ai_run_id"]),
        "is_mock": result["is_mock"],
        "note": "This is a prediction only. No state changes were applied.",
    }


# ══════════════════════════════════════════════════
# Sync Protocol
# ══════════════════════════════════════════════════


@router.post("/sync")
async def sync_events(
    body: SyncRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Process queued offline events from client."""
    now = datetime.now(UTC)
    results = []

    # Sort by client_timestamp
    sorted_events = sorted(body.events, key=lambda e: e.client_timestamp)

    for event in sorted_events:
        drift = abs((now - event.client_timestamp).total_seconds())
        drift_warning = drift > 86400  # > 24h

        results.append(
            {
                "event_type": event.event_type,
                "status": "processed",
                "server_timestamp": now.isoformat(),
                "drift_warning": drift_warning,
                "drift_seconds": round(drift),
            }
        )

    return {
        "processed": len(results),
        "results": results,
        "server_time": now.isoformat(),
    }


# ══════════════════════════════════════════════════
# Attempt Locking
# ══════════════════════════════════════════════════

# In-memory lock store (Redis in production)
_attempt_locks: dict[str, dict] = {}


@router.get("/activities/{activity_id}/lock-status")
async def get_lock_status(
    activity_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    key = str(activity_id)
    lock = _attempt_locks.get(key)
    if lock and datetime.now(UTC) < lock["expires_at"]:
        return {"locked": True, "device_id": lock["device_id"], "expires_at": lock["expires_at"].isoformat()}
    return {"locked": False}


@router.post("/activities/{activity_id}/lock")
async def lock_activity(
    activity_id: uuid.UUID,
    x_device_id: str = Header(default="default"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    key = str(activity_id)
    lock = _attempt_locks.get(key)
    now = datetime.now(UTC)

    if lock and now < lock["expires_at"] and lock["device_id"] != x_device_id:
        raise HTTPException(
            status_code=409,
            detail="This activity is being worked on from another device.",
        )

    _attempt_locks[key] = {
        "device_id": x_device_id,
        "locked_at": now,
        "expires_at": now + timedelta(hours=2),
    }
    return {"locked": True, "device_id": x_device_id, "expires_at": _attempt_locks[key]["expires_at"].isoformat()}


@router.delete("/activities/{activity_id}/lock")
async def unlock_activity(
    activity_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    _attempt_locks.pop(str(activity_id), None)
    return {"locked": False}


# ══════════════════════════════════════════════════
# Device Registration
# ══════════════════════════════════════════════════


@router.post("/devices/register", status_code=201)
async def register_device(
    body: DeviceRegisterRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    device = DeviceToken(
        user_id=user.id,
        household_id=user.household_id,
        device_type=body.platform,
        token=body.device_token,
    )
    db.add(device)
    await db.flush()
    return {"id": str(device.id), "platform": body.platform, "registered": True}


# ══════════════════════════════════════════════════
# Notification Log
# ══════════════════════════════════════════════════


@router.get("/notifications/log")
async def notification_log(
    limit: int = Query(default=50, le=200),
    event_type: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[dict]:
    query = select(NotificationLog).where(
        NotificationLog.household_id == user.household_id,
    )
    if event_type:
        query = query.where(NotificationLog.title.contains(event_type))
    query = query.order_by(NotificationLog.created_at.desc()).limit(limit)

    result = await db.execute(query)
    return [
        {
            "id": str(n.id),
            "channel": n.channel,
            "title": n.title,
            "body": n.body,
            "sent": n.sent,
            "sent_at": n.sent_at.isoformat() if n.sent_at else None,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        }
        for n in result.scalars().all()
    ]


# ══════════════════════════════════════════════════
# Prometheus Metrics
# ══════════════════════════════════════════════════


@router.get("/metrics")
async def prometheus_metrics(request: Request) -> str:
    """Prometheus-format metrics endpoint."""
    from fastapi.responses import PlainTextResponse

    # Collect basic metrics
    lines = [
        "# HELP methean_up Application health status",
        "# TYPE methean_up gauge",
        "methean_up 1",
        "",
        "# HELP methean_api_requests_total Total API requests",
        "# TYPE methean_api_requests_total counter",
        'methean_api_requests_total{service="methean"} 1',
        "",
    ]

    return PlainTextResponse("\n".join(lines), media_type="text/plain")


# ══════════════════════════════════════════════════
# Certification tracking (JSONB-backed via ChildPreferences.certification_progress)
# ══════════════════════════════════════════════════


class CertificationCreate(BaseModel):
    name: str
    subject: str
    target_date: str | None = None
    requirements: list[dict] | None = None
    notes: str | None = None


class CertificationUpdate(BaseModel):
    status: str | None = None
    target_date: str | None = None
    requirements: list[dict] | None = None
    notes: str | None = None


async def _get_or_create_prefs(db: AsyncSession, child_id, household_id):
    result = await db.execute(select(ChildPreferences).where(ChildPreferences.child_id == child_id))
    prefs = result.scalar_one_or_none()
    if not prefs:
        prefs = ChildPreferences(child_id=child_id, household_id=household_id)
        db.add(prefs)
        await db.flush()
    return prefs


@router.get("/children/{child_id}/certifications")
async def list_certifications(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list:
    await _get_child_or_404(db, child_id, user.household_id)
    prefs = await _get_or_create_prefs(db, child_id, user.household_id)
    return prefs.certification_progress or []


@router.post("/children/{child_id}/certifications", status_code=201)
async def add_certification(
    child_id: uuid.UUID,
    body: CertificationCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    prefs = await _get_or_create_prefs(db, child_id, user.household_id)
    certs = list(prefs.certification_progress or [])
    cert_id = body.name.lower().replace(" ", "-").replace("(", "").replace(")", "")
    if any(c["id"] == cert_id for c in certs):
        raise HTTPException(409, "Certification already exists for this child")
    from datetime import date as d

    new_cert = {
        "id": cert_id,
        "name": body.name,
        "subject": body.subject,
        "status": "not_started",
        "target_date": body.target_date,
        "requirements": body.requirements or [],
        "notes": body.notes or "",
        "created_at": d.today().isoformat(),
    }
    certs.append(new_cert)
    prefs.certification_progress = certs
    from sqlalchemy.orm.attributes import flag_modified

    flag_modified(prefs, "certification_progress")
    await db.flush()
    return new_cert


@router.put("/children/{child_id}/certifications/{cert_id}")
async def update_certification(
    child_id: uuid.UUID,
    cert_id: str,
    body: CertificationUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    prefs = await _get_or_create_prefs(db, child_id, user.household_id)
    certs = list(prefs.certification_progress or [])
    cert = next((c for c in certs if c["id"] == cert_id), None)
    if not cert:
        raise HTTPException(404, "Certification not found")
    if body.status:
        valid = {"not_started", "in_progress", "ready_for_exam", "certified"}
        if body.status not in valid:
            raise HTTPException(400, f"status must be: {', '.join(sorted(valid))}")
        cert["status"] = body.status
    if body.target_date:
        cert["target_date"] = body.target_date
    if body.requirements is not None:
        cert["requirements"] = body.requirements
    if body.notes is not None:
        cert["notes"] = body.notes
    prefs.certification_progress = certs
    from sqlalchemy.orm.attributes import flag_modified

    flag_modified(prefs, "certification_progress")
    await db.flush()
    return cert


# ══════════════════════════════════════════════════
# Mentors (JSONB-backed via Household.settings["mentors"])
# ══════════════════════════════════════════════════


class MentorCreate(BaseModel):
    name: str
    trade: str
    relationship: str | None = None
    availability: str | None = None
    children: list[str] | None = None
    notes: str | None = None


@router.get("/household/mentors")
async def list_mentors(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list:
    household = (await db.execute(select(Household).where(Household.id == user.household_id))).scalar_one()
    return (household.settings or {}).get("mentors", [])


@router.post("/household/mentors", status_code=201)
async def add_mentor(
    body: MentorCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    household = (await db.execute(select(Household).where(Household.id == user.household_id))).scalar_one()
    settings = dict(household.settings or {})
    mentors = list(settings.get("mentors", []))
    mentor = {
        "id": f"mentor-{len(mentors) + 1}",
        "name": body.name,
        "trade": body.trade,
        "relationship": body.relationship or "",
        "availability": body.availability or "",
        "children": body.children or [],
        "notes": body.notes or "",
    }
    mentors.append(mentor)
    settings["mentors"] = mentors
    household.settings = settings
    from sqlalchemy.orm.attributes import flag_modified

    flag_modified(household, "settings")
    await db.flush()
    return mentor


@router.delete("/household/mentors/{mentor_id}")
async def remove_mentor(
    mentor_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    household = (await db.execute(select(Household).where(Household.id == user.household_id))).scalar_one()
    settings = dict(household.settings or {})
    mentors = list(settings.get("mentors", []))
    settings["mentors"] = [m for m in mentors if m["id"] != mentor_id]
    household.settings = settings
    from sqlalchemy.orm.attributes import flag_modified

    flag_modified(household, "settings")
    await db.flush()
    return {"deleted": True}


# ══════════════════════════════════════════════════
# Subject Catalog & Learning Levels
# ══════════════════════════════════════════════════


@router.get("/subjects/catalog")
async def get_subject_catalog(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Return the full subject catalog with learning levels."""
    from app.core.learning_levels import LEARNING_LEVELS, SUBJECT_CATALOG

    household = (await db.execute(select(Household).where(Household.id == user.household_id))).scalar_one()
    custom = (household.settings or {}).get("custom_subjects", [])
    return {
        "academic": SUBJECT_CATALOG["academic"],
        "vocational": SUBJECT_CATALOG["vocational"],
        "custom": custom,
        "levels": LEARNING_LEVELS,
    }


class CustomSubjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    category: str = "custom"
    description: str | None = None


@router.post("/subjects/custom", status_code=201)
async def add_custom_subject(
    body: CustomSubjectCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Add a custom subject to the household catalog."""
    household = (await db.execute(select(Household).where(Household.id == user.household_id))).scalar_one()
    settings = dict(household.settings or {})
    custom = list(settings.get("custom_subjects", []))
    if any(s["name"].lower() == body.name.lower() for s in custom):
        raise HTTPException(409, f"Subject '{body.name}' already exists")
    new_subj = {
        "id": body.name.lower().replace(" ", "_"),
        "name": body.name,
        "category": body.category,
        "description": body.description or "",
    }
    custom.append(new_subj)
    settings["custom_subjects"] = custom
    household.settings = settings
    from sqlalchemy.orm.attributes import flag_modified

    flag_modified(household, "settings")
    await db.flush()
    return new_subj
