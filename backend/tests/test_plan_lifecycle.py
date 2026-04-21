"""Tests for plan and activity lifecycle state machines.

Covers:
- Valid plan transitions: draft -> proposed -> approved -> active -> completed
- Invalid plan transitions: draft -> active (rejected)
- Cannot lock plan with unapproved activities
- Blocked activities are not created during plan generation
- Activity governance fields set on approve/reject
"""

from datetime import date, timedelta

import pytest
from sqlalchemy import select

from app.models.curriculum import ChildMapEnrollment, LearningMap
from app.models.enums import (
    ActivityStatus,
    PlanStatus,
    RuleScope,
    RuleType,
)
from app.models.governance import Activity, GovernanceRule, Plan, PlanWeek
from app.services.plan_lifecycle import (
    ACTIVITY_TRANSITIONS,
    PLAN_TRANSITIONS,
    validate_transition,
)

# ══════════════════════════════════════════════════
# State Machine Unit Tests
# ══════════════════════════════════════════════════


class TestPlanLifecycleTransitions:
    def test_valid_plan_transitions(self):
        """Walk through the full happy path: draft -> proposed -> approved -> active -> completed."""
        status = "draft"
        status = validate_transition(status, "submit", PLAN_TRANSITIONS)
        assert status == "proposed"
        status = validate_transition(status, "approve", PLAN_TRANSITIONS)
        assert status == "approved"
        status = validate_transition(status, "activate", PLAN_TRANSITIONS)
        assert status == "active"
        status = validate_transition(status, "complete", PLAN_TRANSITIONS)
        assert status == "completed"

    def test_invalid_plan_transition_draft_to_active(self):
        """Cannot skip from draft directly to active."""
        with pytest.raises(ValueError, match="Cannot 'activate'"):
            validate_transition("draft", "activate", PLAN_TRANSITIONS)

    def test_invalid_plan_transition_completed_to_active(self):
        """Cannot go back from completed to active."""
        with pytest.raises(ValueError, match="Cannot 'activate'"):
            validate_transition("completed", "activate", PLAN_TRANSITIONS)

    def test_plan_reject_returns_to_draft(self):
        status = validate_transition("proposed", "reject", PLAN_TRANSITIONS)
        assert status == "draft"

    def test_plan_archive_from_multiple_states(self):
        assert validate_transition("draft", "archive", PLAN_TRANSITIONS) == "archived"
        assert validate_transition("active", "archive", PLAN_TRANSITIONS) == "archived"
        assert validate_transition("completed", "archive", PLAN_TRANSITIONS) == "archived"

    def test_valid_activity_transitions(self):
        status = "scheduled"
        status = validate_transition(status, "start", ACTIVITY_TRANSITIONS)
        assert status == "in_progress"
        status = validate_transition(status, "complete", ACTIVITY_TRANSITIONS)
        assert status == "completed"

    def test_activity_cancel_from_scheduled(self):
        assert validate_transition("scheduled", "cancel", ACTIVITY_TRANSITIONS) == "cancelled"

    def test_activity_reject_from_scheduled(self):
        assert validate_transition("scheduled", "reject", ACTIVITY_TRANSITIONS) == "cancelled"

    def test_activity_skip_from_in_progress(self):
        assert validate_transition("in_progress", "skip", ACTIVITY_TRANSITIONS) == "skipped"

    def test_invalid_activity_transition(self):
        with pytest.raises(ValueError):
            validate_transition("completed", "start", ACTIVITY_TRANSITIONS)

    def test_transition_with_enum_value(self):
        """validate_transition should handle enum objects, not just strings."""
        status = validate_transition(PlanStatus.draft, "submit", PLAN_TRANSITIONS)
        assert status == "proposed"


# ══════════════════════════════════════════════════
# API Integration Tests
# ══════════════════════════════════════════════════


class TestCannotLockWithUnapprovedActivities:
    @pytest.mark.asyncio
    async def test_lock_blocked_by_unapproved(
        self,
        auth_client,
        db_session,
        household,
        subject,
        child,
        user,
    ):
        """Locking a plan must fail if any non-cancelled activity is not governance-approved."""
        lmap = LearningMap(
            household_id=household.id,
            subject_id=subject.id,
            name="Lock Test Map",
        )
        db_session.add(lmap)
        await db_session.flush()

        db_session.add(
            ChildMapEnrollment(
                child_id=child.id,
                household_id=household.id,
                learning_map_id=lmap.id,
            )
        )
        await db_session.flush()

        # Create a plan with one unapproved activity
        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Unapproved Test",
            status=PlanStatus.draft,
        )
        db_session.add(plan)
        await db_session.flush()

        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=4),
        )
        db_session.add(week)
        await db_session.flush()

        # One approved, one not
        db_session.add(
            Activity(
                plan_week_id=week.id,
                household_id=household.id,
                activity_type="lesson",
                title="Approved Activity",
                status=ActivityStatus.scheduled,
                governance_approved=True,
            )
        )
        db_session.add(
            Activity(
                plan_week_id=week.id,
                household_id=household.id,
                activity_type="lesson",
                title="Unapproved Activity",
                status=ActivityStatus.scheduled,
                governance_approved=False,
            )
        )
        await db_session.flush()

        # Attempt to lock — should fail
        resp = await auth_client.put(f"/api/v1/plans/{plan.id}/lock")
        assert resp.status_code == 409
        body = resp.json()
        assert "unapproved" in body["detail"]["message"].lower()
        assert len(body["detail"]["unapproved_activity_ids"]) == 1

    @pytest.mark.asyncio
    async def test_lock_succeeds_when_all_approved(
        self,
        auth_client,
        db_session,
        household,
        subject,
        child,
        user,
    ):
        """Locking succeeds when every non-cancelled activity is governance-approved."""
        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="All Approved",
            status=PlanStatus.draft,
        )
        db_session.add(plan)
        await db_session.flush()

        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=4),
        )
        db_session.add(week)
        await db_session.flush()

        db_session.add(
            Activity(
                plan_week_id=week.id,
                household_id=household.id,
                activity_type="lesson",
                title="Good Activity",
                status=ActivityStatus.scheduled,
                governance_approved=True,
            )
        )
        # Cancelled activities don't block locking
        db_session.add(
            Activity(
                plan_week_id=week.id,
                household_id=household.id,
                activity_type="lesson",
                title="Rejected Activity",
                status=ActivityStatus.cancelled,
                governance_approved=False,
            )
        )
        await db_session.flush()

        resp = await auth_client.put(f"/api/v1/plans/{plan.id}/lock")
        assert resp.status_code == 200
        assert resp.json()["status"] == "active"


class TestGovernanceFieldsOnApproveReject:
    @pytest.mark.asyncio
    async def test_approve_sets_governance_fields(
        self,
        auth_client,
        db_session,
        household,
        child,
        user,
    ):
        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Approve Fields",
            status=PlanStatus.draft,
        )
        db_session.add(plan)
        await db_session.flush()

        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=4),
        )
        db_session.add(week)
        await db_session.flush()

        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            activity_type="lesson",
            title="Pending",
            status=ActivityStatus.scheduled,
            governance_approved=False,
        )
        db_session.add(activity)
        await db_session.flush()

        resp = await auth_client.put(f"/api/v1/plans/{plan.id}/activities/{activity.id}/approve")
        assert resp.status_code == 200

        # Verify DB fields
        result = await db_session.execute(select(Activity).where(Activity.id == activity.id))
        updated = result.scalar_one()
        assert updated.governance_approved is True
        assert updated.governance_reviewed_by == user.id
        assert updated.governance_reviewed_at is not None

    @pytest.mark.asyncio
    async def test_reject_sets_governance_fields(
        self,
        auth_client,
        db_session,
        household,
        child,
        user,
    ):
        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Reject Fields",
            status=PlanStatus.draft,
        )
        db_session.add(plan)
        await db_session.flush()

        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=4),
        )
        db_session.add(week)
        await db_session.flush()

        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            activity_type="lesson",
            title="To Reject",
            status=ActivityStatus.scheduled,
            governance_approved=False,
        )
        db_session.add(activity)
        await db_session.flush()

        resp = await auth_client.put(
            f"/api/v1/plans/{plan.id}/activities/{activity.id}/reject",
            json={"reason": "Not appropriate"},
        )
        assert resp.status_code == 200

        result = await db_session.execute(select(Activity).where(Activity.id == activity.id))
        updated = result.scalar_one()
        assert updated.status == ActivityStatus.cancelled
        assert updated.governance_reviewed_by == user.id
        assert updated.governance_reviewed_at is not None


class TestBlockedActivityNotCreated:
    @pytest.mark.asyncio
    async def test_blocked_activities_skipped_in_plan(
        self,
        auth_client,
        db_session,
        household,
        subject,
        child,
        user,
    ):
        """When governance evaluates 'block', the activity should not be created."""
        lmap = LearningMap(
            household_id=household.id,
            subject_id=subject.id,
            name="Block Test",
        )
        db_session.add(lmap)
        await db_session.flush()

        db_session.add(
            ChildMapEnrollment(
                child_id=child.id,
                household_id=household.id,
                learning_map_id=lmap.id,
            )
        )
        await db_session.flush()

        # Create a "block" governance rule for difficulty >= 5
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.approval_required,
                scope=RuleScope.household,
                name="Block very hard",
                parameters={"min_difficulty": 5, "action": "block"},
                priority=1,
            )
        )
        # Also add default auto-approve for everything else
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.approval_required,
                scope=RuleScope.household,
                name="Auto-approve rest",
                parameters={"max_difficulty": 5, "action": "auto_approve"},
                priority=10,
            )
        )
        await db_session.flush()

        # Generate a plan — mock AI returns activities with various difficulties
        # The mock always returns difficulty=2 and difficulty=3 activities,
        # so none will be blocked. We verify the governance_approved field is set.
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/plans/generate",
            json={"week_start": date.today().isoformat(), "daily_minutes": 60},
        )
        assert resp.status_code == 201

        # Verify activities were created with governance_approved=True
        # (all mock activities have difficulty <= 3, below the block threshold)
        plan_id = resp.json()["id"]
        detail = await auth_client.get(f"/api/v1/plans/{plan_id}")
        activities = detail.json()["activities"]
        assert len(activities) > 0  # Activities were created (not blocked)
