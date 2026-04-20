"""Tests for governance mode and node type expansion."""

import pytest
from sqlalchemy import select

from app.models.enums import GovernanceMode, NodeType
from app.models.identity import Child, Household, User


class TestGovernanceModeDefaults:
    @pytest.mark.asyncio
    async def test_new_household_defaults_to_parent_governed(self, db_session):
        h = Household(name="Default Family")
        db_session.add(h)
        await db_session.flush()

        loaded = (
            await db_session.execute(select(Household).where(Household.id == h.id))
        ).scalar_one()
        assert loaded.governance_mode == "parent_governed"

    @pytest.mark.asyncio
    async def test_new_household_defaults_to_homeschool(self, db_session):
        h = Household(name="Homeschool Default")
        db_session.add(h)
        await db_session.flush()

        loaded = (
            await db_session.execute(select(Household).where(Household.id == h.id))
        ).scalar_one()
        assert loaded.organization_type == "homeschool"
        assert loaded.learner_age_range == "k12"

    @pytest.mark.asyncio
    async def test_new_user_defaults_not_self_learner(self, db_session, household):
        u = User(
            household_id=household.id,
            email="normal@example.com",
            password_hash="hashed",
            display_name="Normal User",
            role="owner",
        )
        db_session.add(u)
        await db_session.flush()

        loaded = (
            await db_session.execute(select(User).where(User.id == u.id))
        ).scalar_one()
        assert loaded.is_self_learner is False
        assert loaded.linked_child_id is None
        assert loaded.institutional_role is None

    def test_governance_mode_enum_has_four_values(self):
        expected = {
            "parent_governed",
            "self_governed",
            "institution_governed",
            "mentor_governed",
        }
        assert {m.value for m in GovernanceMode} == expected
        assert len(list(GovernanceMode)) == 4


class TestGovernanceModeAssignment:
    @pytest.mark.asyncio
    async def test_set_self_governed(self, db_session):
        h = Household(name="Solo", governance_mode="self_governed", organization_type="self_directed")
        db_session.add(h)
        await db_session.flush()

        await db_session.refresh(h)
        loaded = (
            await db_session.execute(select(Household).where(Household.id == h.id))
        ).scalar_one()
        assert loaded.governance_mode == "self_governed"
        assert loaded.organization_type == "self_directed"

    @pytest.mark.asyncio
    async def test_set_institution_governed(self, db_session):
        h = Household(
            name="Test U",
            governance_mode="institution_governed",
            organization_type="university",
        )
        db_session.add(h)
        await db_session.flush()

        loaded = (
            await db_session.execute(select(Household).where(Household.id == h.id))
        ).scalar_one()
        assert loaded.governance_mode == "institution_governed"
        assert loaded.organization_type == "university"

    @pytest.mark.asyncio
    async def test_set_mentor_governed(self, db_session):
        h = Household(
            name="Apprentice Shop",
            governance_mode="mentor_governed",
            organization_type="trade",
        )
        db_session.add(h)
        await db_session.flush()

        loaded = (
            await db_session.execute(select(Household).where(Household.id == h.id))
        ).scalar_one()
        assert loaded.governance_mode == "mentor_governed"

    @pytest.mark.asyncio
    async def test_organization_metadata_stores_json(self, db_session):
        metadata = {"accreditation": "ABET", "credit_system": "semester"}
        h = Household(name="Meta Org", organization_metadata=metadata)
        db_session.add(h)
        await db_session.commit()

        loaded = (
            await db_session.execute(select(Household).where(Household.id == h.id))
        ).scalar_one()
        assert loaded.organization_metadata == metadata


class TestSelfLearnerLinking:
    @pytest.mark.asyncio
    async def test_self_learner_links_to_child(self, db_session, household):
        child = Child(household_id=household.id, first_name="Self")
        db_session.add(child)
        await db_session.flush()

        user = User(
            household_id=household.id,
            email="solo@example.com",
            password_hash="hashed",
            display_name="Solo",
            role="owner",
            is_self_learner=True,
            linked_child_id=child.id,
        )
        db_session.add(user)
        await db_session.flush()

        loaded = (
            await db_session.execute(select(User).where(User.id == user.id))
        ).scalar_one()
        assert loaded.is_self_learner is True
        assert loaded.linked_child_id == child.id

        # FK resolves to a real Child row
        linked_child = (
            await db_session.execute(select(Child).where(Child.id == loaded.linked_child_id))
        ).scalar_one()
        assert linked_child.first_name == "Self"
        assert linked_child.household_id == household.id

    @pytest.mark.asyncio
    async def test_non_self_learner_has_no_linked_child(self, db_session, household):
        user = User(
            household_id=household.id,
            email="parent@example.com",
            password_hash="hashed",
            display_name="Parent",
            role="owner",
        )
        db_session.add(user)
        await db_session.flush()

        loaded = (
            await db_session.execute(select(User).where(User.id == user.id))
        ).scalar_one()
        assert loaded.is_self_learner is False
        assert loaded.linked_child_id is None


class TestNodeTypeExpansion:
    def test_all_new_node_types_in_enum(self):
        new_types = {
            "lecture",
            "reading",
            "research",
            "lab",
            "thesis_component",
            "exam_prep",
            "peer_review",
            "practicum",
        }
        values = {m.value for m in NodeType}
        missing = new_types - values
        assert not missing, f"Missing higher-ed node types: {missing}"

    @pytest.mark.asyncio
    async def test_create_node_with_lecture_type(self, db_session, household, learning_map):
        from app.models.curriculum import LearningNode

        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.lecture,
            title="Intro Lecture",
        )
        db_session.add(node)
        await db_session.flush()

        loaded = (
            await db_session.execute(select(LearningNode).where(LearningNode.id == node.id))
        ).scalar_one()
        assert loaded.title == "Intro Lecture"
        # node_type comes back as the enum member
        assert loaded.node_type == NodeType.lecture

    def test_existing_node_types_still_valid(self):
        existing = {
            "root",
            "milestone",
            "concept",
            "skill",
            "safety",
            "knowledge",
            "technique",
            "project",
            "certification_prep",
        }
        values = {m.value for m in NodeType}
        missing = existing - values
        assert not missing, f"Missing legacy node types: {missing}"
