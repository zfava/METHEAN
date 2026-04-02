"""Comprehensive tests for Parent Governance + AI Integration.

Tests cover:
- AI Gateway: mock fallback, AIRun logging
- Governance Rules: creation, evaluation, default rules
- Plan Generation: AI planner through governance routing
- Plan approve/reject/lock
- Tutor interaction
- AI inspection endpoints
- Governance event log
- AI fallback when providers unavailable
"""

import uuid
from datetime import date, timedelta

import pytest
from sqlalchemy import select

from app.ai.gateway import AIRole, _call_mock
from app.models.enums import (
    ActivityStatus,
    GovernanceAction,
    PlanStatus,
    RuleScope,
    RuleType,
)
from app.models.governance import Activity, GovernanceEvent, GovernanceRule, Plan, PlanWeek
from app.models.operational import AIRun
from app.services.governance import (
    GovernanceDecision,
    create_default_rules,
    evaluate_activity,
    log_governance_event,
)


# ══════════════════════════════════════════════════
# AI Gateway Unit Tests
# ══════════════════════════════════════════════════

class TestAIGateway:

    def test_mock_planner_returns_valid_json(self):
        import json
        result = _call_mock(AIRole.planner, "test")
        data = json.loads(result["content"])
        assert "activities" in data
        assert len(data["activities"]) > 0
        assert "total_minutes" in data

    def test_mock_evaluator_returns_valid_json(self):
        import json
        result = _call_mock(AIRole.evaluator, "test")
        data = json.loads(result["content"])
        assert "quality_rating" in data
        assert "confidence_score" in data
        assert 0 <= data["confidence_score"] <= 1

    def test_mock_tutor_returns_valid_json(self):
        import json
        result = _call_mock(AIRole.tutor, "test")
        data = json.loads(result["content"])
        assert "message" in data

    def test_mock_advisor_returns_valid_json(self):
        import json
        result = _call_mock(AIRole.advisor, "test")
        data = json.loads(result["content"])
        assert "summary" in data
        assert "highlights" in data

    def test_mock_cartographer_returns_valid_json(self):
        import json
        result = _call_mock(AIRole.cartographer, "test")
        data = json.loads(result["content"])
        assert "estimated_weeks" in data

    @pytest.mark.asyncio
    async def test_gateway_logs_ai_run(self, db_session, household, user):
        from app.ai.gateway import call_ai

        result = await call_ai(
            db_session,
            role=AIRole.planner,
            system_prompt="test",
            user_prompt="test",
            household_id=household.id,
            triggered_by=user.id,
        )

        assert result["is_mock"] is True
        assert result["ai_run_id"] is not None

        # Verify AIRun was logged
        run_result = await db_session.execute(
            select(AIRun).where(AIRun.id == result["ai_run_id"])
        )
        ai_run = run_result.scalar_one()
        assert ai_run.run_type == "planner"
        assert ai_run.model_used == "mock"
        assert ai_run.output_data is not None
        assert ai_run.status.value == "completed" if hasattr(ai_run.status, 'value') else ai_run.status == "completed"

    @pytest.mark.asyncio
    async def test_gateway_all_roles(self, db_session, household, user):
        from app.ai.gateway import call_ai

        for role in AIRole:
            result = await call_ai(
                db_session, role=role,
                system_prompt="test", user_prompt="test",
                household_id=household.id, triggered_by=user.id,
            )
            assert result["is_mock"] is True
            assert result["output"] is not None


# ══════════════════════════════════════════════════
# Governance Rules Engine Tests
# ══════════════════════════════════════════════════

class TestGovernanceRules:

    @pytest.mark.asyncio
    async def test_create_default_rules(self, db_session, household, user):
        rules = await create_default_rules(db_session, household.id, user.id)
        assert len(rules) == 3

        names = {r.name for r in rules}
        assert "Auto-approve easy activities" in names
        assert "Review difficult activities" in names
        assert "Daily time limit" in names

    @pytest.mark.asyncio
    async def test_auto_approve_low_difficulty(self, db_session, household, user):
        await create_default_rules(db_session, household.id, user.id)

        decision = await evaluate_activity(
            db_session, household.id, difficulty=2,
        )
        assert decision.action == "auto_approve"

    @pytest.mark.asyncio
    async def test_require_review_high_difficulty(self, db_session, household, user):
        await create_default_rules(db_session, household.id, user.id)

        decision = await evaluate_activity(
            db_session, household.id, difficulty=4,
        )
        assert decision.action == "require_review"

    @pytest.mark.asyncio
    async def test_no_rules_auto_approves(self, db_session, household):
        decision = await evaluate_activity(db_session, household.id, difficulty=5)
        assert decision.action == "auto_approve"

    @pytest.mark.asyncio
    async def test_governance_event_logged(self, db_session, household, user):
        event = await log_governance_event(
            db_session, household.id, user.id,
            GovernanceAction.approve, "test_target", uuid.uuid4(),
            reason="Test reason",
        )
        assert event.id is not None
        assert event.action == GovernanceAction.approve


# ══════════════════════════════════════════════════
# Plan Generation API Tests
# ══════════════════════════════════════════════════

class TestPlanGeneration:

    @pytest.mark.asyncio
    async def test_generate_plan(self, auth_client, db_session, household, subject, child, user):
        from app.models.curriculum import ChildMapEnrollment, LearningMap, LearningNode
        from app.models.enums import NodeType

        # Create map with nodes and enroll child
        lmap = LearningMap(
            household_id=household.id, subject_id=subject.id, name="Plan Test Map"
        )
        db_session.add(lmap)
        await db_session.flush()

        for title in ["Concept A", "Concept B", "Concept C"]:
            db_session.add(LearningNode(
                learning_map_id=lmap.id, household_id=household.id,
                node_type=NodeType.concept, title=title,
            ))
        await db_session.flush()

        db_session.add(ChildMapEnrollment(
            child_id=child.id, household_id=household.id,
            learning_map_id=lmap.id,
        ))
        await db_session.flush()

        # Create default governance rules
        await create_default_rules(db_session, household.id, user.id)

        # Generate plan
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/plans/generate",
            json={
                "week_start": date.today().isoformat(),
                "daily_minutes": 90,
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["ai_generated"] is True
        assert data["status"] == "draft"
        plan_id = data["id"]

        # Get plan detail
        detail_resp = await auth_client.get(f"/api/v1/plans/{plan_id}")
        assert detail_resp.status_code == 200
        detail = detail_resp.json()
        assert len(detail["activities"]) > 0

    @pytest.mark.asyncio
    async def test_list_plans(self, auth_client, db_session, household, subject, child, user):
        from app.models.curriculum import ChildMapEnrollment, LearningMap

        lmap = LearningMap(
            household_id=household.id, subject_id=subject.id, name="List Plans Map"
        )
        db_session.add(lmap)
        await db_session.flush()

        db_session.add(ChildMapEnrollment(
            child_id=child.id, household_id=household.id,
            learning_map_id=lmap.id,
        ))
        await db_session.flush()

        await create_default_rules(db_session, household.id, user.id)

        await auth_client.post(
            f"/api/v1/children/{child.id}/plans/generate",
            json={"week_start": date.today().isoformat()},
        )

        resp = await auth_client.get(f"/api/v1/children/{child.id}/plans")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1


class TestPlanManagement:

    @pytest.mark.asyncio
    async def test_approve_and_reject_activities(
        self, auth_client, db_session, household, subject, child, user,
    ):
        from app.models.curriculum import ChildMapEnrollment, LearningMap

        lmap = LearningMap(
            household_id=household.id, subject_id=subject.id, name="Approve Map"
        )
        db_session.add(lmap)
        await db_session.flush()

        db_session.add(ChildMapEnrollment(
            child_id=child.id, household_id=household.id,
            learning_map_id=lmap.id,
        ))
        await db_session.flush()

        await create_default_rules(db_session, household.id, user.id)

        gen_resp = await auth_client.post(
            f"/api/v1/children/{child.id}/plans/generate",
            json={"week_start": date.today().isoformat()},
        )
        plan_id = gen_resp.json()["id"]

        detail = await auth_client.get(f"/api/v1/plans/{plan_id}")
        activities = detail.json()["activities"]
        assert len(activities) > 0

        # Approve first activity
        act_id = activities[0]["id"]
        approve_resp = await auth_client.put(
            f"/api/v1/plans/{plan_id}/activities/{act_id}/approve",
        )
        assert approve_resp.status_code == 200
        assert approve_resp.json()["status"] == "approved"

        # Reject second activity (if exists)
        if len(activities) > 1:
            act_id2 = activities[1]["id"]
            reject_resp = await auth_client.put(
                f"/api/v1/plans/{plan_id}/activities/{act_id2}/reject",
                json={"reason": "Not appropriate for this week"},
            )
            assert reject_resp.status_code == 200
            assert reject_resp.json()["status"] == "rejected"

    @pytest.mark.asyncio
    async def test_lock_and_unlock_plan(
        self, auth_client, db_session, household, subject, child, user,
    ):
        from app.models.curriculum import ChildMapEnrollment, LearningMap

        lmap = LearningMap(
            household_id=household.id, subject_id=subject.id, name="Lock Map"
        )
        db_session.add(lmap)
        await db_session.flush()

        db_session.add(ChildMapEnrollment(
            child_id=child.id, household_id=household.id,
            learning_map_id=lmap.id,
        ))
        await db_session.flush()

        await create_default_rules(db_session, household.id, user.id)

        gen_resp = await auth_client.post(
            f"/api/v1/children/{child.id}/plans/generate",
            json={"week_start": date.today().isoformat()},
        )
        plan_id = gen_resp.json()["id"]

        # Lock
        lock_resp = await auth_client.put(f"/api/v1/plans/{plan_id}/lock")
        assert lock_resp.status_code == 200
        assert lock_resp.json()["status"] == "active"

        # Unlock
        unlock_resp = await auth_client.put(f"/api/v1/plans/{plan_id}/unlock")
        assert unlock_resp.status_code == 200
        assert unlock_resp.json()["status"] == "draft"


# ══════════════════════════════════════════════════
# Tutor Tests
# ══════════════════════════════════════════════════

class TestTutor:

    @pytest.mark.asyncio
    async def test_tutor_message(
        self, auth_client, db_session, household, subject, child, user,
    ):
        from app.models.curriculum import LearningMap, LearningNode
        from app.models.enums import ActivityType, NodeType, PlanStatus
        from datetime import date

        lmap = LearningMap(
            household_id=household.id, subject_id=subject.id, name="Tutor Map"
        )
        db_session.add(lmap)
        await db_session.flush()

        node = LearningNode(
            learning_map_id=lmap.id, household_id=household.id,
            node_type=NodeType.skill, title="Addition",
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id, child_id=child.id,
            created_by=user.id, name="Tutor Plan", status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()

        week = PlanWeek(
            plan_id=plan.id, household_id=household.id,
            week_number=1, start_date=date.today(),
            end_date=date.today() + timedelta(days=4),
        )
        db_session.add(week)
        await db_session.flush()

        activity = Activity(
            plan_week_id=week.id, household_id=household.id,
            node_id=node.id, activity_type=ActivityType.lesson,
            title="Learn Addition",
        )
        db_session.add(activity)
        await db_session.flush()

        resp = await auth_client.post(
            f"/api/v1/tutor/{activity.id}/message",
            json={"child_id": str(child.id), "message": "I think 2+2 is 5?"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "message" in data
        assert data["ai_run_id"] is not None


# ══════════════════════════════════════════════════
# Governance Rules API Tests
# ══════════════════════════════════════════════════

class TestGovernanceRulesAPI:

    @pytest.mark.asyncio
    async def test_create_and_list_rules(self, auth_client, db_session, household, user):
        resp = await auth_client.post("/api/v1/governance-rules", json={
            "rule_type": "approval_required",
            "scope": "household",
            "name": "Test Rule",
            "parameters": {"max_difficulty": 4, "action": "require_review"},
            "priority": 5,
        })
        assert resp.status_code == 201
        assert resp.json()["name"] == "Test Rule"

        list_resp = await auth_client.get("/api/v1/governance-rules")
        assert list_resp.status_code == 200
        assert any(r["name"] == "Test Rule" for r in list_resp.json())

    @pytest.mark.asyncio
    async def test_update_rule(self, auth_client, db_session, household, user):
        create_resp = await auth_client.post("/api/v1/governance-rules", json={
            "rule_type": "pace_limit",
            "name": "Old Name",
            "parameters": {},
        })
        rule_id = create_resp.json()["id"]

        update_resp = await auth_client.put(f"/api/v1/governance-rules/{rule_id}", json={
            "name": "New Name",
            "is_active": False,
        })
        assert update_resp.status_code == 200
        assert update_resp.json()["name"] == "New Name"
        assert update_resp.json()["is_active"] is False

    @pytest.mark.asyncio
    async def test_init_default_rules(self, auth_client, db_session, household, user):
        resp = await auth_client.post("/api/v1/governance-rules/defaults")
        assert resp.status_code == 201
        assert len(resp.json()) == 3


# ══════════════════════════════════════════════════
# AI Inspection Tests
# ══════════════════════════════════════════════════

class TestAIInspection:

    @pytest.mark.asyncio
    async def test_list_ai_runs(self, auth_client, db_session, household, user):
        from app.ai.gateway import call_ai

        # Create some AI runs
        await call_ai(db_session, AIRole.planner, "test", "test",
                       household.id, user.id)
        await call_ai(db_session, AIRole.evaluator, "test", "test",
                       household.id, user.id)

        resp = await auth_client.get("/api/v1/ai-runs")
        assert resp.status_code == 200
        runs = resp.json()
        assert len(runs) >= 2

    @pytest.mark.asyncio
    async def test_get_ai_run_detail(self, auth_client, db_session, household, user):
        from app.ai.gateway import call_ai

        result = await call_ai(db_session, AIRole.planner, "test", "test",
                                household.id, user.id)

        resp = await auth_client.get(f"/api/v1/ai-runs/{result['ai_run_id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["run_type"] == "planner"
        assert data["model_used"] == "mock"
        assert data["output_data"] is not None

    @pytest.mark.asyncio
    async def test_filter_ai_runs_by_role(self, auth_client, db_session, household, user):
        from app.ai.gateway import call_ai

        await call_ai(db_session, AIRole.tutor, "test", "test",
                       household.id, user.id)

        resp = await auth_client.get("/api/v1/ai-runs?role=tutor")
        assert resp.status_code == 200
        runs = resp.json()
        assert all(r["run_type"] == "tutor" for r in runs)

    @pytest.mark.asyncio
    async def test_governance_events_log(self, auth_client, db_session, household, user):
        await log_governance_event(
            db_session, household.id, user.id,
            GovernanceAction.approve, "test", uuid.uuid4(),
            reason="Test event",
        )

        resp = await auth_client.get("/api/v1/governance-events")
        assert resp.status_code == 200
        events = resp.json()
        assert len(events) >= 1

    @pytest.mark.asyncio
    async def test_decision_trace(
        self, auth_client, db_session, household, subject, child, user,
    ):
        from app.models.curriculum import ChildMapEnrollment, LearningMap

        lmap = LearningMap(
            household_id=household.id, subject_id=subject.id, name="Trace Map"
        )
        db_session.add(lmap)
        await db_session.flush()

        db_session.add(ChildMapEnrollment(
            child_id=child.id, household_id=household.id,
            learning_map_id=lmap.id,
        ))
        await db_session.flush()

        await create_default_rules(db_session, household.id, user.id)

        gen_resp = await auth_client.post(
            f"/api/v1/children/{child.id}/plans/generate",
            json={"week_start": date.today().isoformat()},
        )
        plan_id = gen_resp.json()["id"]

        trace_resp = await auth_client.get(f"/api/v1/plans/{plan_id}/decision-trace")
        assert trace_resp.status_code == 200
        data = trace_resp.json()
        assert "ai_run" in data
        assert "activity_decisions" in data
        assert len(data["activity_decisions"]) > 0
        # Each activity should have governance events
        for act_dec in data["activity_decisions"]:
            assert "governance_events" in act_dec


# ══════════════════════════════════════════════════
# Advisor Reports Tests
# ══════════════════════════════════════════════════

class TestAdvisorReports:

    @pytest.mark.asyncio
    async def test_generate_and_list_advisor_reports(
        self, auth_client, db_session, household, child, user,
    ):
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/advisor-reports/generate"
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["report_type"] == "weekly"
        assert data["content"] is not None
        report_id = data["id"]

        # List
        list_resp = await auth_client.get(
            f"/api/v1/children/{child.id}/advisor-reports"
        )
        assert list_resp.status_code == 200
        assert len(list_resp.json()) >= 1

        # Get detail
        detail_resp = await auth_client.get(f"/api/v1/advisor-reports/{report_id}")
        assert detail_resp.status_code == 200


# ══════════════════════════════════════════════════
# Cartographer Tests
# ══════════════════════════════════════════════════

class TestCartographer:

    @pytest.mark.asyncio
    async def test_cartographer_calibrate(
        self, auth_client, db_session, household, subject, child, user,
    ):
        from app.models.curriculum import LearningMap, LearningNode
        from app.models.enums import NodeType

        lmap = LearningMap(
            household_id=household.id, subject_id=subject.id, name="Carto Map"
        )
        db_session.add(lmap)
        await db_session.flush()

        for title in ["Node X", "Node Y"]:
            db_session.add(LearningNode(
                learning_map_id=lmap.id, household_id=household.id,
                node_type=NodeType.concept, title=title,
            ))
        await db_session.flush()

        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/cartographer/calibrate",
            json={
                "learning_map_id": str(lmap.id),
                "parent_goals": "Master basic math by end of year",
                "notes": "Child enjoys visual learning",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "estimated_weeks" in data
        assert data["ai_run_id"] is not None
