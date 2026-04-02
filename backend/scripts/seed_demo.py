"""Seed demo data for METHEAN investor demo.

Creates a living system:
- Parent account (demo@methean.com / demo123)
- 2 children (ages 8 and 11)
- Each enrolled in a map with varied mastery states
- Current week plan with approved/pending/completed activities
- Completed attempts with evaluator output
- Governance events
- FSRS cards with varied due dates
- Advisor report

Run: python -m scripts.seed_demo
"""

import asyncio
import uuid
from datetime import UTC, date, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.database import Base
from app.core.security import hash_password
from app.models.curriculum import (
    ChildMapEnrollment,
    LearningEdge,
    LearningMap,
    LearningNode,
    Subject,
)
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    AIRunStatus,
    AlertSeverity,
    AlertStatus,
    AttemptStatus,
    EdgeRelation,
    GovernanceAction,
    MasteryLevel,
    NodeType,
    PlanStatus,
    RuleScope,
    RuleType,
    StateEventType,
)
from app.models.evidence import AdvisorReport, Alert
from app.models.governance import Activity, Attempt, GovernanceEvent, GovernanceRule, Plan, PlanWeek
from app.models.identity import Child, ChildPreferences, Household, User
from app.models.operational import AIRun
from app.models.state import ChildNodeState, FSRSCard, StateEvent


async def seed():
    db_url = settings.DATABASE_URL
    engine = create_async_engine(db_url, poolclass=NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as db:
        # ── Household ──
        household = Household(name="The Demo Family", timezone="America/New_York")
        db.add(household)
        await db.flush()

        # ── Parent ──
        parent = User(
            household_id=household.id,
            email="demo@methean.com",
            password_hash=hash_password("demo123"),
            display_name="Alex Demo",
            role="owner",
        )
        db.add(parent)
        await db.flush()

        # ── Children ──
        child1 = Child(
            household_id=household.id,
            first_name="Emma",
            last_name="Demo",
            date_of_birth=date(2018, 3, 15),
            grade_level="2nd",
        )
        child2 = Child(
            household_id=household.id,
            first_name="Liam",
            last_name="Demo",
            date_of_birth=date(2015, 7, 22),
            grade_level="5th",
        )
        db.add_all([child1, child2])
        await db.flush()

        # ── Subject + Map for Emma (K-2 Foundations) ──
        subj1 = Subject(household_id=household.id, name="K-2 Foundations", color="#4CAF50")
        db.add(subj1)
        await db.flush()

        map1 = LearningMap(
            household_id=household.id, subject_id=subj1.id,
            name="K-2 Foundations", version=3,
        )
        db.add(map1)
        await db.flush()

        # Nodes
        nodes1 = {}
        for title, ntype, minutes in [
            ("Literacy", "root", None),
            ("Letter Recognition", "milestone", 30),
            ("Basic Phonics", "concept", 25),
            ("Sight Words", "skill", 20),
            ("Simple Reading", "skill", 30),
            ("Numeracy", "root", None),
            ("Counting to 100", "milestone", 20),
            ("Addition", "concept", 25),
            ("Subtraction", "concept", 25),
            ("Word Problems", "skill", 30),
        ]:
            n = LearningNode(
                learning_map_id=map1.id, household_id=household.id,
                node_type=ntype, title=title, estimated_minutes=minutes,
            )
            db.add(n)
            await db.flush()
            nodes1[title] = n

        # Edges
        edges1 = [
            ("Literacy", "Letter Recognition"),
            ("Letter Recognition", "Basic Phonics"),
            ("Basic Phonics", "Sight Words"),
            ("Sight Words", "Simple Reading"),
            ("Numeracy", "Counting to 100"),
            ("Counting to 100", "Addition"),
            ("Counting to 100", "Subtraction"),
            ("Addition", "Word Problems"),
            ("Subtraction", "Word Problems"),
        ]
        for f, t in edges1:
            db.add(LearningEdge(
                learning_map_id=map1.id, household_id=household.id,
                from_node_id=nodes1[f].id, to_node_id=nodes1[t].id,
                relation=EdgeRelation.prerequisite,
            ))
        await db.flush()

        # Enroll Emma
        db.add(ChildMapEnrollment(
            child_id=child1.id, household_id=household.id,
            learning_map_id=map1.id, enrolled_at_version=3,
        ))

        # Emma's mastery states
        now = datetime.now(UTC)
        mastery_data = {
            "Literacy": (MasteryLevel.mastered, True),
            "Letter Recognition": (MasteryLevel.mastered, True),
            "Basic Phonics": (MasteryLevel.mastered, True),
            "Sight Words": (MasteryLevel.proficient, True),
            "Simple Reading": (MasteryLevel.not_started, False),
            "Numeracy": (MasteryLevel.mastered, True),
            "Counting to 100": (MasteryLevel.mastered, True),
            "Addition": (MasteryLevel.developing, True),
            "Subtraction": (MasteryLevel.emerging, False),
            "Word Problems": (MasteryLevel.not_started, False),
        }
        for title, (mastery, unlocked) in mastery_data.items():
            db.add(ChildNodeState(
                child_id=child1.id, household_id=household.id,
                node_id=nodes1[title].id,
                mastery_level=mastery, is_unlocked=unlocked,
                attempts_count=3 if mastery == MasteryLevel.mastered else (1 if mastery != MasteryLevel.not_started else 0),
                time_spent_minutes=45 if mastery == MasteryLevel.mastered else 15,
            ))
        await db.flush()

        # FSRS cards for mastered nodes (some overdue for decay demo)
        for title in ["Literacy", "Letter Recognition", "Basic Phonics", "Numeracy", "Counting to 100"]:
            stability = 10.0 if title != "Basic Phonics" else 3.0
            last_rev = now - timedelta(days=5) if title != "Basic Phonics" else now - timedelta(days=30)
            due = now + timedelta(days=5) if title != "Basic Phonics" else now - timedelta(days=20)
            db.add(FSRSCard(
                child_id=child1.id, household_id=household.id,
                node_id=nodes1[title].id,
                stability=stability, difficulty=2.5,
                reps=3, state=2,  # Review state
                last_review=last_rev, due=due,
            ))
        await db.flush()

        # ── Governance Rules ──
        for rule_data in [
            ("Auto-approve easy", RuleType.approval_required, {"max_difficulty": 3, "action": "auto_approve"}, 10),
            ("Review difficult", RuleType.approval_required, {"min_difficulty": 3, "action": "require_review"}, 20),
            ("Daily limit", RuleType.pace_limit, {"max_daily_minutes": 180}, 5),
        ]:
            db.add(GovernanceRule(
                household_id=household.id, created_by=parent.id,
                rule_type=rule_data[1], scope=RuleScope.household,
                name=rule_data[0], parameters=rule_data[2], priority=rule_data[3],
            ))
        await db.flush()

        # ── Plan + Activities for Emma ──
        today = date.today()
        week_start = today - timedelta(days=today.weekday())

        plan = Plan(
            household_id=household.id, child_id=child1.id,
            created_by=parent.id, name=f"Week of {week_start.isoformat()}",
            status=PlanStatus.active, start_date=week_start,
            end_date=week_start + timedelta(days=4), ai_generated=True,
        )
        db.add(plan)
        await db.flush()

        week = PlanWeek(
            plan_id=plan.id, household_id=household.id,
            week_number=1, start_date=week_start,
            end_date=week_start + timedelta(days=4),
        )
        db.add(week)
        await db.flush()

        activities_data = [
            ("Review Phonics", ActivityType.review, ActivityStatus.completed, week_start, nodes1["Basic Phonics"].id),
            ("Practice Sight Words", ActivityType.practice, ActivityStatus.completed, week_start + timedelta(days=1), nodes1["Sight Words"].id),
            ("Addition Lesson", ActivityType.lesson, ActivityStatus.scheduled, week_start + timedelta(days=2), nodes1["Addition"].id),
            ("Subtraction Intro", ActivityType.lesson, ActivityStatus.scheduled, week_start + timedelta(days=3), nodes1["Subtraction"].id),
            ("Counting Review", ActivityType.review, ActivityStatus.scheduled, week_start + timedelta(days=4), nodes1["Counting to 100"].id),
        ]
        created_activities = []
        for title, atype, status, sdate, nid in activities_data:
            a = Activity(
                plan_week_id=week.id, household_id=household.id,
                node_id=nid, activity_type=atype, title=title,
                status=status, scheduled_date=sdate, estimated_minutes=25,
                instructions={"difficulty": 2 if "Review" in title else 3},
            )
            db.add(a)
            await db.flush()
            created_activities.append(a)

        # Completed attempts
        for a in created_activities[:2]:
            attempt = Attempt(
                activity_id=a.id, household_id=household.id,
                child_id=child1.id, status=AttemptStatus.completed,
                completed_at=now - timedelta(hours=2),
                duration_minutes=20, score=0.75,
                feedback={"evaluator_summary": "Good progress on foundational skills"},
            )
            db.add(attempt)
        await db.flush()

        # ── Governance Events ──
        for a in created_activities:
            db.add(GovernanceEvent(
                household_id=household.id, user_id=parent.id,
                action=GovernanceAction.approve,
                target_type="activity", target_id=a.id,
                reason="Auto-approved: difficulty < 3" if "Review" in a.title else "Parent approved",
            ))

        # Override event
        db.add(GovernanceEvent(
            household_id=household.id, user_id=parent.id,
            action=GovernanceAction.approve,
            target_type="child_node_state",
            target_id=nodes1["Subtraction"].id,
            reason="Emma demonstrated understanding in daily life",
        ))
        await db.flush()

        # ── AI Runs ──
        for role, status in [("planner", "completed"), ("evaluator", "completed"), ("tutor", "completed")]:
            db.add(AIRun(
                household_id=household.id, triggered_by=parent.id,
                run_type=role, status=status, model_used="mock",
                input_data={"role": role, "system_prompt": "...", "user_prompt": "..."},
                output_data={"mock": True, "result": f"Mock {role} output"},
                started_at=now - timedelta(minutes=5),
                completed_at=now - timedelta(minutes=4),
            ))
        await db.flush()

        # ── Advisor Report ──
        db.add(AdvisorReport(
            household_id=household.id, child_id=child1.id,
            report_type="weekly",
            period_start=week_start - timedelta(days=7),
            period_end=week_start - timedelta(days=1),
            content={
                "summary": "Emma had a productive week. She mastered Basic Phonics and made strong progress on Sight Words.",
                "highlights": ["Mastered Basic Phonics", "Consistent daily engagement", "3 activities completed"],
                "concerns": ["Basic Phonics card is overdue for review — schedule a review session"],
                "recommended_focus": ["Review Basic Phonics to maintain retention", "Continue Sight Words practice"],
                "engagement_score": 8,
            },
            recommendations=["Review Basic Phonics", "Continue Sight Words", "Begin Addition concepts"],
        ))

        # ── Alert ──
        db.add(Alert(
            household_id=household.id, child_id=child1.id,
            severity=AlertSeverity.warning,
            status=AlertStatus.unread,
            title="Review Overdue",
            message="Basic Phonics has not been reviewed in 30 days. Retention is declining.",
            source="retention_engine",
        ))

        await db.commit()

    await engine.dispose()
    print("Demo data seeded successfully!")
    print("Login: demo@methean.com / demo123")


if __name__ == "__main__":
    asyncio.run(seed())
