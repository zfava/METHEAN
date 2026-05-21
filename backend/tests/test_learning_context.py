"""Tests for learning context endpoint and service.

Covers:
- Learn endpoint returns structured lesson content
- Learn endpoint generates content for unenriched nodes
- Attempt stores responses and self_reflection in feedback
- Tutor messages are contextual to the activity
"""

from datetime import UTC, date, datetime

import pytest
from sqlalchemy import select

from app.models.curriculum import LearningNode
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    AttemptStatus,
    NodeType,
    PlanStatus,
)
from app.models.governance import Activity, Attempt, Plan, PlanWeek
from app.services.learning_context import get_activity_learning_context


class TestLearningContext:
    @pytest.mark.asyncio
    async def test_learn_returns_lesson_content(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """Call learning context for an activity with enriched node, verify content returned."""
        # Create an enriched node
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Double-Digit Addition",
            content={
                "learning_objectives": ["Add two-digit numbers", "Carry over tens"],
                "teaching_guidance": {
                    "introduction": "Today we learn to add bigger numbers!",
                    "practice_activities": ["Solve 23 + 45", "Solve 37 + 18"],
                    "common_misconceptions": ["Forgetting to carry the ten"],
                    "scaffolding_sequence": ["Start with no carrying", "Introduce carrying"],
                    "socratic_questions": ["What happens when digits add to more than 9?"],
                    "real_world_connections": ["Adding prices at the store"],
                },
                "assessment_criteria": {
                    "mastery_indicators": ["Correctly adds with carrying"],
                    "sample_assessment_prompts": ["What is 48 + 35?"],
                    "assessment_methods": ["written work"],
                },
                "resource_guidance": {"required": ["pencil", "paper"], "recommended": ["base-10 blocks"]},
                "time_estimates": {"first_exposure": 30, "practice_session": 20},
            },
        )
        db_session.add(node)
        await db_session.flush()

        # Create plan/week/activity linked to node
        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            node_id=node.id,
            activity_type=ActivityType.lesson,
            title="Double-Digit Addition Lesson",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        # Get learning context
        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )

        assert ctx["activity"]["title"] == "Double-Digit Addition Lesson"
        assert ctx["activity"]["activity_type"] == "lesson"
        assert ctx["tutor_available"] is True

        # Lesson content
        assert "Today we learn" in ctx["lesson"]["introduction"]
        assert len(ctx["lesson"]["objectives"]) == 2
        assert len(ctx["lesson"]["steps"]) > 0
        assert any(s["type"] == "read" for s in ctx["lesson"]["steps"])
        assert len(ctx["lesson"]["practice_prompts"]) > 0
        assert "pencil" in ctx["lesson"]["resources_needed"]
        assert "store" in ctx["lesson"]["real_world_connection"]

        # Assessment
        assert len(ctx["assessment"]["prompts"]) > 0
        assert "carrying" in ctx["assessment"]["mastery_criteria"]

    @pytest.mark.asyncio
    async def test_learn_with_unenriched_node(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """Activity with unenriched node still returns basic structure."""
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Fractions",
            content={},  # Not enriched
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            node_id=node.id,
            activity_type=ActivityType.practice,
            title="Fractions Practice",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )

        # Content comes from enrichment (mock AI) or fallback from node title
        assert ctx["activity"]["title"] == "Fractions Practice"
        assert ctx["activity"]["activity_type"] == "practice"
        assert len(ctx["lesson"]["introduction"]) > 0
        assert len(ctx["lesson"]["objectives"]) >= 2
        assert len(ctx["lesson"]["steps"]) > 0
        assert len(ctx["assessment"]["prompts"]) > 0

    @pytest.mark.asyncio
    async def test_practice_items_surfaced_in_context(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """A node with authored practice_items exposes them in context["practice"]."""
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Counting to Ten",
            content={
                "learning_objectives": ["Count to ten", "Recognize number order"],
                "teaching_guidance": {
                    "introduction": "Today we count!",
                    "scaffolding_sequence": ["Count out loud"],
                    "socratic_questions": ["What comes after five?"],
                },
                "assessment_criteria": {
                    "mastery_indicators": ["Counts to ten reliably"],
                    "sample_assessment_prompts": ["Count to ten."],
                    "assessment_methods": ["oral narration"],
                },
                "practice_items": [
                    {
                        "type": "problem",
                        "difficulty": 1,
                        "prompt": "What number comes after 9?",
                        "expected_type": "number",
                        "correct_answer": "10",
                        "hints": ["Count: 7, 8, 9, ..."],
                        "explanation": "After 9 comes 10.",
                    },
                    {
                        "type": "problem",
                        "difficulty": 2,
                        "prompt": "Count backward from 12 to 7.",
                        "expected_type": "text",
                        "hints": ["Start at 12 and go down"],
                        "explanation": "12, 11, 10, 9, 8, 7",
                    },
                ],
            },
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            node_id=node.id,
            activity_type=ActivityType.practice,
            title="Counting Practice",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )

        items = ctx["practice"]["items"]
        assert len(items) == 2
        first = items[0]
        assert first["expected_type"] == "number"
        assert first["correct_answer"] == "10"

    @pytest.mark.asyncio
    async def test_assessment_items_derived_without_hints(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """context["assessment"]["items"] is derived from practice_items.

        The "text" expected_type normalizes to "open_response", and no
        assessment item carries hints or worked explanations. The legacy
        prompts list must remain a list of strings.
        """
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Counting to Ten",
            content={
                "learning_objectives": ["Count to ten", "Recognize number order"],
                "teaching_guidance": {
                    "introduction": "Today we count!",
                    "scaffolding_sequence": ["Count out loud"],
                    "socratic_questions": ["What comes after five?"],
                },
                "assessment_criteria": {
                    "mastery_indicators": ["Counts to ten reliably"],
                    "sample_assessment_prompts": ["Count to ten.", "Count backward."],
                    "assessment_methods": ["oral narration"],
                },
                "practice_items": [
                    {
                        "type": "problem",
                        "difficulty": 1,
                        "prompt": "What number comes after 9?",
                        "expected_type": "number",
                        "correct_answer": "10",
                        "hints": ["Count: 7, 8, 9, ..."],
                        "explanation": "After 9 comes 10.",
                    },
                    {
                        "type": "problem",
                        "difficulty": 2,
                        "prompt": "Count backward from 12 to 7.",
                        "expected_type": "text",
                        "hints": ["Start at 12 and go down"],
                        "explanation": "12, 11, 10, 9, 8, 7",
                    },
                ],
            },
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            node_id=node.id,
            activity_type=ActivityType.assessment,
            title="Counting Assessment",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )

        items = ctx["assessment"]["items"]
        assert len(items) == 2
        assert items[0]["type"] == "number"
        assert items[0]["correct_answer"] == "10"
        # "text" normalizes to "open_response".
        assert items[1]["type"] == "open_response"
        # No assessment item leaks hints or worked explanations.
        for item in items:
            assert "hints" not in item
            assert "explanation" not in item

        # Regression: the legacy prompts list is untouched.
        prompts = ctx["assessment"]["prompts"]
        assert isinstance(prompts, list)
        assert all(isinstance(p, str) for p in prompts)
        assert len(prompts) == 2

    @pytest.mark.asyncio
    async def test_practice_items_empty_for_unenriched_node(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """An unenriched node yields an empty practice item list, no exception."""
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Fractions",
            content={},  # Not enriched
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            node_id=node.id,
            activity_type=ActivityType.practice,
            title="Fractions Practice",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )

        assert ctx["practice"]["items"] == []

    @pytest.mark.asyncio
    async def test_assessment_items_prefer_authored_field(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """A node with authored assessment_items uses them, with rubric and target_concept."""
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Counting to Ten",
            content={
                "learning_objectives": ["Count to ten", "Recognize number order"],
                "teaching_guidance": {
                    "introduction": "Today we count!",
                    "scaffolding_sequence": ["Count out loud"],
                    "socratic_questions": ["What comes after five?"],
                },
                "assessment_criteria": {
                    "mastery_indicators": ["Counts to ten reliably"],
                    "sample_assessment_prompts": ["Count to ten."],
                    "assessment_methods": ["oral narration"],
                },
                "practice_items": [
                    {
                        "type": "problem",
                        "difficulty": 1,
                        "prompt": "What number comes after 9?",
                        "expected_type": "number",
                        "correct_answer": "10",
                        "hints": ["Count: 7, 8, 9, ..."],
                    },
                ],
                "assessment_items": [
                    {
                        "prompt": "Count from 1 to 10 out loud.",
                        "type": "open_response",
                        "target_concept": "rote counting sequence",
                        "rubric": "Says every number 1 through 10 in order.",
                    },
                    {
                        "prompt": "Which number comes right after 7?",
                        "type": "text",
                        "target_concept": "number order",
                        "rubric": "Identifies 8.",
                    },
                ],
            },
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            node_id=node.id,
            activity_type=ActivityType.assessment,
            title="Counting Assessment",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )

        items = ctx["assessment"]["items"]
        assert len(items) == 2
        # Authored items are used, not the practice_items-derived ones.
        assert items[0]["prompt"] == "Count from 1 to 10 out loud."
        assert items[0]["rubric"] == "Says every number 1 through 10 in order."
        assert items[0]["target_concept"] == "rote counting sequence"
        # "text" normalizes to "open_response".
        assert items[1]["type"] == "open_response"
        assert items[1]["rubric"] == "Identifies 8."
        # The practice_items-derived fallback is not used here.
        assert all(i["prompt"] != "What number comes after 9?" for i in items)

    @pytest.mark.asyncio
    async def test_assessment_items_fall_back_to_practice_items(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """A node with practice_items but no assessment_items still yields assessment items.

        The practice_items-derived fallback fills assessment.items, and
        assessment.prompts plus practice.items remain intact.
        """
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Counting to Ten",
            content={
                "learning_objectives": ["Count to ten", "Recognize number order"],
                "teaching_guidance": {
                    "introduction": "Today we count!",
                    "scaffolding_sequence": ["Count out loud"],
                    "socratic_questions": ["What comes after five?"],
                },
                "assessment_criteria": {
                    "mastery_indicators": ["Counts to ten reliably"],
                    "sample_assessment_prompts": ["Count to ten.", "Count backward."],
                    "assessment_methods": ["oral narration"],
                },
                "practice_items": [
                    {
                        "type": "problem",
                        "difficulty": 1,
                        "prompt": "What number comes after 9?",
                        "expected_type": "number",
                        "correct_answer": "10",
                        "hints": ["Count: 7, 8, 9, ..."],
                    },
                ],
                # No assessment_items key.
            },
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            node_id=node.id,
            activity_type=ActivityType.assessment,
            title="Counting Assessment",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )

        items = ctx["assessment"]["items"]
        assert len(items) == 1
        assert items[0]["prompt"] == "What number comes after 9?"
        assert items[0]["type"] == "number"
        assert items[0]["correct_answer"] == "10"

        # Regression: prompts stays a list of strings; practice.items intact.
        prompts = ctx["assessment"]["prompts"]
        assert isinstance(prompts, list)
        assert all(isinstance(p, str) for p in prompts)
        assert len(prompts) == 2
        assert len(ctx["practice"]["items"]) == 1
        assert ctx["practice"]["items"][0]["prompt"] == "What number comes after 9?"

    @pytest.mark.asyncio
    async def test_media_and_passages_surfaced_in_context(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """A node with media and passages surfaces them with all fields intact."""
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Counting on a Number Line",
            content={
                "learning_objectives": ["Place numbers on a number line"],
                "teaching_guidance": {
                    "introduction": "A number line shows numbers in order.",
                    "scaffolding_sequence": ["Find zero first"],
                    "socratic_questions": ["Where does 5 sit?"],
                },
                "assessment_criteria": {
                    "mastery_indicators": ["Places numbers accurately"],
                    "sample_assessment_prompts": ["Place 7 on the line."],
                    "assessment_methods": ["demonstration"],
                },
                "media": [
                    {
                        "id": "nl1",
                        "kind": "number_line",
                        "alt": "A number line from 0 to 10",
                        "caption": "Count each step",
                        "params": {"min": 0, "max": 10, "ticks": 11, "highlight": 7},
                    },
                ],
                "passages": [
                    {
                        "id": "p1",
                        "title": "Sam and the Map",
                        "text": "Sam ran to the map. The map had a path.",
                        "level": "early-decodable",
                        "decodable_focus": ["short a", "consonant blends"],
                        "questions": ["Where did Sam run?"],
                    },
                ],
            },
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            node_id=node.id,
            activity_type=ActivityType.lesson,
            title="Number Line Lesson",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )

        media = ctx["lesson"]["media"]
        assert len(media) == 1
        assert media[0]["kind"] == "number_line"
        assert media[0]["alt"] == "A number line from 0 to 10"
        assert media[0]["params"]["highlight"] == 7

        passages = ctx["reading"]["passages"]
        assert len(passages) == 1
        assert passages[0]["text"] == "Sam ran to the map. The map had a path."
        assert passages[0]["decodable_focus"] == ["short a", "consonant blends"]
        assert passages[0]["questions"] == ["Where did Sam run?"]

    @pytest.mark.asyncio
    async def test_legacy_node_yields_empty_media_and_passages(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """A node with no media or passages yields empty lists, raises nothing."""
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Double-Digit Addition",
            content={
                "learning_objectives": ["Add two-digit numbers"],
                "teaching_guidance": {
                    "introduction": "Add bigger numbers.",
                    "scaffolding_sequence": ["Start without carrying"],
                    "socratic_questions": ["What happens past 9?"],
                },
                "assessment_criteria": {
                    "mastery_indicators": ["Adds with carrying"],
                    "sample_assessment_prompts": ["What is 48 + 35?"],
                    "assessment_methods": ["written work"],
                },
            },
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            node_id=node.id,
            activity_type=ActivityType.lesson,
            title="Addition Lesson",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )

        assert ctx["lesson"]["media"] == []
        assert ctx["reading"]["passages"] == []

    @pytest.mark.asyncio
    async def test_widgets_surfaced_in_context(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """A node with widgets surfaces them at context.lesson.widgets intact."""
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Counting Objects",
            content={
                "learning_objectives": ["Count objects to ten"],
                "teaching_guidance": {
                    "introduction": "Count the apples.",
                    "scaffolding_sequence": ["Touch each one"],
                    "socratic_questions": ["How many are left?"],
                },
                "assessment_criteria": {
                    "mastery_indicators": ["Counts accurately"],
                    "sample_assessment_prompts": ["Count these."],
                    "assessment_methods": ["demonstration"],
                },
                "widgets": [
                    {
                        "id": "w1",
                        "widget": "counting_objects",
                        "params": {"count": 7, "object": "apple"},
                        "prompt": "Tap each apple as you count.",
                        "target": 7,
                    },
                    {
                        "id": "w2",
                        "widget": "number_line",
                        "params": {"min": 0, "max": 10},
                    },
                ],
            },
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            node_id=node.id,
            activity_type=ActivityType.lesson,
            title="Counting Lesson",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )

        widgets = ctx["lesson"]["widgets"]
        assert len(widgets) == 2
        assert widgets[0]["id"] == "w1"
        assert widgets[0]["widget"] == "counting_objects"
        assert widgets[0]["params"] == {"count": 7, "object": "apple"}
        assert widgets[0]["prompt"] == "Tap each apple as you count."
        assert widgets[1]["widget"] == "number_line"

    @pytest.mark.asyncio
    async def test_legacy_node_yields_empty_widgets(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """A node with no widgets yields context.lesson.widgets == [], raises nothing."""
        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Double-Digit Addition",
            content={
                "learning_objectives": ["Add two-digit numbers"],
                "teaching_guidance": {
                    "introduction": "Add bigger numbers.",
                    "scaffolding_sequence": ["Start without carrying"],
                    "socratic_questions": ["What happens past 9?"],
                },
                "assessment_criteria": {
                    "mastery_indicators": ["Adds with carrying"],
                    "sample_assessment_prompts": ["What is 48 + 35?"],
                    "assessment_methods": ["written work"],
                },
            },
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            node_id=node.id,
            activity_type=ActivityType.lesson,
            title="Addition Lesson",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )

        assert ctx["lesson"]["widgets"] == []

    @pytest.mark.asyncio
    async def test_learn_no_tutor_for_assessment(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """Assessment activities should not have tutor available."""
        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            activity_type=ActivityType.assessment,
            title="Weekly Assessment",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )
        assert ctx["tutor_available"] is False

    @pytest.mark.asyncio
    async def test_previous_attempts_returned(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """Previous attempts for the same activity are returned."""
        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            activity_type=ActivityType.lesson,
            title="Test",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        # Add a previous attempt
        db_session.add(
            Attempt(
                activity_id=activity.id,
                household_id=household.id,
                child_id=child.id,
                status=AttemptStatus.completed,
                completed_at=datetime.now(UTC),
                duration_minutes=20,
                score=0.8,
            )
        )
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session,
            activity.id,
            household.id,
            child.id,
        )
        assert len(ctx["previous_attempts"]) == 1
        assert ctx["previous_attempts"][0]["duration_minutes"] == 20


class TestAttemptFeedback:
    @pytest.mark.asyncio
    async def test_attempt_stores_responses_in_feedback(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
    ):
        """Submit attempt with responses and self_reflection, verify stored in feedback."""
        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            activity_type=ActivityType.lesson,
            title="Test",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        attempt = Attempt(
            activity_id=activity.id,
            household_id=household.id,
            child_id=child.id,
            status=AttemptStatus.started,
            feedback={
                "responses": [
                    {"prompt": "What is 3+4?", "response": "7"},
                    {"prompt": "Spell 'cat'", "response": "c-a-t"},
                ],
                "self_reflection": "I thought the math was easy but spelling was harder.",
            },
        )
        db_session.add(attempt)
        await db_session.flush()

        # Verify feedback stored
        result = await db_session.execute(select(Attempt).where(Attempt.id == attempt.id))
        saved = result.scalar_one()
        assert len(saved.feedback["responses"]) == 2
        assert saved.feedback["responses"][0]["prompt"] == "What is 3+4?"
        assert saved.feedback["responses"][0]["response"] == "7"
        assert "spelling was harder" in saved.feedback["self_reflection"]


class TestLearningContextAPI:
    @pytest.mark.asyncio
    async def test_learn_endpoint(self, auth_client, db_session, household, child, user, subject, learning_map):
        """Test the /activities/{id}/learn API endpoint."""
        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            activity_type=ActivityType.lesson,
            title="API Test Lesson",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        resp = await auth_client.get(f"/api/v1/activities/{activity.id}/learn")
        assert resp.status_code == 200
        data = resp.json()
        assert data["activity"]["title"] == "API Test Lesson"
        assert data["activity"]["activity_type"] == "lesson"
        assert "lesson" in data
        assert "assessment" in data
        assert data["tutor_available"] is True


class TestTutorConversationHistory:
    @pytest.mark.asyncio
    async def test_tutor_with_history(self, auth_client, db_session, household, child, user, subject, learning_map):
        """Send a tutor message with conversation history, verify it's accepted."""
        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            activity_type=ActivityType.lesson,
            title="Addition",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        # Send with conversation history
        resp = await auth_client.post(
            f"/api/v1/tutor/{activity.id}/message",
            json={
                "message": "Why?",
                "conversation_history": [
                    {"role": "child", "text": "What is 3 + 4?"},
                    {"role": "tutor", "text": "What do you think happens when you add 3 and 4?"},
                ],
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "message" in data

    @pytest.mark.asyncio
    async def test_tutor_without_history(self, auth_client, db_session, household, child, user, subject, learning_map):
        """Send a tutor message without history (backward compatible)."""
        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Math",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            activity_type=ActivityType.lesson,
            title="Addition",
            status=ActivityStatus.scheduled,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        # Send without history (no conversation_history field)
        resp = await auth_client.post(
            f"/api/v1/tutor/{activity.id}/message",
            json={"message": "What is 3 + 4?"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "message" in data
