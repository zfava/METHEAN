"""Tests for assessment and portfolio system.

Covers:
- Parent assessment overrides mastery
- Assessment triggers FSRS review with confidence override
- Transcript maps mastery to grades
- Portfolio export organized by subject
- Governance event logged on mastery override
"""

import pytest
from sqlalchemy import select

from app.models.curriculum import LearningNode
from app.models.enums import MasteryLevel, NodeType
from app.models.governance import GovernanceEvent
from app.models.state import ChildNodeState


class TestParentAssessment:
    @pytest.mark.asyncio
    async def test_assessment_overrides_mastery(
        self,
        auth_client,
        db_session,
        household,
        child,
        subject,
        learning_map,
        user,
    ):
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Assessed Node",
        )
        db_session.add(node)
        await db_session.flush()

        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/assessments",
            json={
                "node_id": str(node.id),
                "assessment_type": "narration",
                "title": "Chapter 5 Narration",
                "qualitative_notes": "Excellent narration with all key events",
                "mastery_judgment": "mastered",
            },
        )
        assert resp.status_code == 201

        # Verify mastery was updated
        state = await db_session.execute(
            select(ChildNodeState).where(
                ChildNodeState.child_id == child.id,
                ChildNodeState.node_id == node.id,
            )
        )
        ns = state.scalar_one()
        assert ns.mastery_level == MasteryLevel.mastered

    @pytest.mark.asyncio
    async def test_governance_event_on_override(
        self,
        auth_client,
        db_session,
        household,
        child,
        subject,
        learning_map,
        user,
    ):
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.concept,
            title="Gov Event Node",
        )
        db_session.add(node)
        await db_session.flush()

        # Set initial state
        db_session.add(
            ChildNodeState(
                child_id=child.id,
                household_id=household.id,
                node_id=node.id,
                mastery_level=MasteryLevel.developing,
            )
        )
        await db_session.flush()

        await auth_client.post(
            f"/api/v1/children/{child.id}/assessments",
            json={
                "node_id": str(node.id),
                "assessment_type": "demonstration",
                "title": "Skill Demo",
                "mastery_judgment": "proficient",
            },
        )

        result = await db_session.execute(
            select(GovernanceEvent).where(
                GovernanceEvent.target_type == "mastery_override",
                GovernanceEvent.target_id == node.id,
            )
        )
        event = result.scalar_one()
        assert "developing" in event.reason
        assert "proficient" in event.reason

    @pytest.mark.asyncio
    async def test_confidence_override_triggers_fsrs(
        self,
        auth_client,
        db_session,
        household,
        child,
        subject,
        learning_map,
        user,
    ):
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="FSRS Override Node",
        )
        db_session.add(node)
        await db_session.flush()

        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/assessments",
            json={
                "node_id": str(node.id),
                "assessment_type": "written",
                "title": "Chapter Quiz",
                "confidence_override": 0.85,
            },
        )
        assert resp.status_code == 201

        # FSRS card should exist now
        from app.models.state import FSRSCard

        card = await db_session.execute(
            select(FSRSCard).where(
                FSRSCard.child_id == child.id,
                FSRSCard.node_id == node.id,
            )
        )
        assert card.scalar_one_or_none() is not None


class TestTranscript:
    @pytest.mark.asyncio
    async def test_transcript_maps_mastery_to_grades(
        self,
        auth_client,
        db_session,
        household,
        child,
        subject,
        learning_map,
        user,
    ):
        for title, mastery in [("A Node", MasteryLevel.mastered), ("B Node", MasteryLevel.proficient)]:
            node = LearningNode(
                learning_map_id=learning_map.id,
                household_id=household.id,
                node_type=NodeType.skill,
                title=title,
            )
            db_session.add(node)
            await db_session.flush()
            db_session.add(
                ChildNodeState(
                    child_id=child.id,
                    household_id=household.id,
                    node_id=node.id,
                    mastery_level=mastery,
                    time_spent_minutes=60,
                )
            )
        await db_session.flush()

        resp = await auth_client.get(f"/api/v1/children/{child.id}/transcript")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["subjects"]) >= 1
        # At least one subject should have grade A (mastered node)
        grades = [s["grade"] for s in data["subjects"]]
        assert "A" in grades or "B" in grades


class TestPortfolio:
    @pytest.mark.asyncio
    async def test_portfolio_crud(self, auth_client, db_session, household, child, user):
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/portfolio",
            json={
                "entry_type": "work_sample",
                "title": "Essay on Ancient Rome",
                "subject": "History",
                "date_completed": "2026-03-15",
                "parent_notes": "Excellent use of primary sources",
                "tags": ["history", "writing"],
            },
        )
        assert resp.status_code == 201

        list_resp = await auth_client.get(f"/api/v1/children/{child.id}/portfolio")
        assert list_resp.status_code == 200
        assert list_resp.json()["total"] >= 1

    @pytest.mark.asyncio
    async def test_portfolio_export(self, auth_client, db_session, household, child, user):
        from datetime import date

        from app.models.assessment import PortfolioEntry

        db_session.add(
            PortfolioEntry(
                household_id=household.id,
                child_id=child.id,
                entry_type="narrative",
                title="Weekly Summary",
                subject="General",
                date_completed=date.today(),
            )
        )
        await db_session.flush()

        resp = await auth_client.get(
            f"/api/v1/children/{child.id}/portfolio/export",
            params={"from": "2026-01-01", "to": "2026-12-31"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_entries"] >= 1
        assert "General" in data["subjects"]


# ══════════════════════════════════════════════════
# Higher-education assessment types
# ══════════════════════════════════════════════════


class TestHigherEdAssessmentTypes:
    async def _post_assessment(self, auth_client, child_id, atype: str):
        return await auth_client.post(
            f"/api/v1/children/{child_id}/assessments",
            json={
                "assessment_type": atype,
                "title": f"{atype} test",
                "qualitative_notes": "",
            },
        )

    @pytest.mark.asyncio
    async def test_create_timed_exam_assessment(self, auth_client, child):
        resp = await self._post_assessment(auth_client, child.id, "timed_exam")
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data["assessment_type"] == "timed_exam"
        assert data["title"] == "timed_exam test"

    @pytest.mark.asyncio
    async def test_create_research_paper_assessment(self, auth_client, child):
        resp = await self._post_assessment(auth_client, child.id, "research_paper")
        assert resp.status_code == 201, resp.text
        assert resp.json()["assessment_type"] == "research_paper"

    @pytest.mark.asyncio
    async def test_create_clinical_evaluation(self, auth_client, child):
        resp = await self._post_assessment(auth_client, child.id, "clinical_evaluation")
        assert resp.status_code == 201, resp.text
        assert resp.json()["assessment_type"] == "clinical_evaluation"

    @pytest.mark.asyncio
    async def test_existing_observation_still_works(self, auth_client, child):
        resp = await self._post_assessment(auth_client, child.id, "observation")
        assert resp.status_code == 201, resp.text
        assert resp.json()["assessment_type"] == "observation"

    @pytest.mark.asyncio
    async def test_invalid_assessment_type_rejected(self, auth_client, child):
        resp = await self._post_assessment(auth_client, child.id, "invalid_type")
        assert resp.status_code == 422, resp.text
