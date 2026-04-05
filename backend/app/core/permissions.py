"""Permission constants and checker for METHEAN role-based access.

Permissions are granular strings (e.g. "rules.create") stored in the
UserPermission table. Owners bypass all checks. Other roles get
explicit permission grants, optionally scoped to a specific child
or subject.
"""

import uuid

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import UserRole
from app.models.identity import User, UserPermission

# ── Permission constants ──

# Governance
PERM_RULES_CREATE = "rules.create"
PERM_RULES_EDIT = "rules.edit"
PERM_RULES_CONSTITUTIONAL = "rules.constitutional"
PERM_APPROVE_ACTIVITIES = "approve.activities"
PERM_OVERRIDE_PREREQUISITES = "override.prerequisites"
PERM_CHANGE_PHILOSOPHY = "change.philosophy"

# Learning
PERM_GENERATE_PLANS = "plans.generate"
PERM_VIEW_PROGRESS = "view.progress"
PERM_TUTOR_INTERACT = "tutor.interact"

# Admin
PERM_MANAGE_USERS = "manage.users"
PERM_MANAGE_CHILDREN = "manage.children"
PERM_EXPORT_DATA = "export.data"
PERM_VIEW_AI_RUNS = "view.ai_runs"

# Role defaults
ALL_PERMISSIONS = [
    PERM_RULES_CREATE, PERM_RULES_EDIT, PERM_RULES_CONSTITUTIONAL,
    PERM_APPROVE_ACTIVITIES, PERM_OVERRIDE_PREREQUISITES, PERM_CHANGE_PHILOSOPHY,
    PERM_GENERATE_PLANS, PERM_VIEW_PROGRESS, PERM_TUTOR_INTERACT,
    PERM_MANAGE_USERS, PERM_MANAGE_CHILDREN, PERM_EXPORT_DATA, PERM_VIEW_AI_RUNS,
]

OWNER_PERMISSIONS = ALL_PERMISSIONS

CO_PARENT_PERMISSIONS = [
    PERM_RULES_CREATE, PERM_RULES_EDIT,
    PERM_APPROVE_ACTIVITIES, PERM_OVERRIDE_PREREQUISITES,
    PERM_GENERATE_PLANS, PERM_VIEW_PROGRESS, PERM_TUTOR_INTERACT,
    PERM_MANAGE_CHILDREN, PERM_EXPORT_DATA, PERM_VIEW_AI_RUNS,
]

OBSERVER_PERMISSIONS = [
    PERM_VIEW_PROGRESS,
]

ROLE_DEFAULTS = {
    "owner": OWNER_PERMISSIONS,
    "co_parent": CO_PARENT_PERMISSIONS,
    "observer": OBSERVER_PERMISSIONS,
}


async def grant_role_permissions(
    db: AsyncSession,
    user_id: uuid.UUID,
    household_id: uuid.UUID,
    role: str,
    granted_by: uuid.UUID,
) -> list[UserPermission]:
    """Grant all default permissions for a role."""
    perms = ROLE_DEFAULTS.get(role, OBSERVER_PERMISSIONS)
    created = []
    for perm in perms:
        p = UserPermission(
            user_id=user_id,
            household_id=household_id,
            permission=perm,
            scope_type="all",
            granted_by=granted_by,
        )
        db.add(p)
        created.append(p)
    await db.flush()
    return created


async def check_permission(
    db: AsyncSession,
    user: User,
    permission: str,
    scope_type: str | None = None,
    scope_id: uuid.UUID | None = None,
) -> bool:
    """Check if a user has a specific permission.

    Owners always have all permissions (bypass check).
    Other users need an explicit UserPermission record.
    Scoped permissions: checks both scoped (specific child/subject)
    and unscoped (scope_type="all") grants.
    """
    role_val = user.role.value if hasattr(user.role, "value") else str(user.role)
    if role_val == "owner":
        return True

    query = select(UserPermission.id).where(
        UserPermission.user_id == user.id,
        UserPermission.household_id == user.household_id,
        UserPermission.permission == permission,
    )

    if scope_type and scope_id:
        # Check both the specific scope and the "all" scope
        query = query.where(
            or_(
                UserPermission.scope_type == "all",
                (UserPermission.scope_type == scope_type) & (UserPermission.scope_id == scope_id),
            )
        )

    result = await db.execute(query.limit(1))
    return result.scalar_one_or_none() is not None
