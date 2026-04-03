"""Seed demo data for METHEAN investor demo.

Creates "The Builder Family" with three children spanning K-12,
each enrolled in a different curriculum template with realistic
mastery progression, FSRS cards, plans, alerts, and snapshots.

Idempotent: checks for existing demo user before creating.

Run from backend dir:  python -m scripts.seed_demo
Run from container:    python scripts/seed_demo.py
"""

import asyncio
import uuid
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import select
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
from app.models.evidence import AdvisorReport, Alert, WeeklySnapshot
from app.models.governance import (
    Activity,
    Attempt,
    GovernanceEvent,
    GovernanceRule,
    Plan,
    PlanWeek,
)
from app.models.identity import Child, Household, User
from app.models.operational import AIRun
from app.models.state import ChildNodeState, FSRSCard, ReviewLog, StateEvent

DEMO_EMAIL = "zack@methean.app"
DEMO_PASSWORD = "demo123"
NOW = datetime.now(UTC)
TODAY = date.today()
WEEK_START = TODAY - timedelta(days=TODAY.weekday())  # Monday


# ── Template definitions (mirrors app/services/templates.py) ──

K2_NODES = [
    ("Literacy", "root", None, 0),
    ("Letter Recognition", "milestone", 30, 1),
    ("Basic Phonics", "concept", 25, 2),
    ("Sight Words", "skill", 20, 3),
    ("Simple Reading", "skill", 30, 4),
    ("Numeracy", "root", None, 10),
    ("Counting to 100", "milestone", 20, 11),
    ("Addition", "concept", 25, 12),
    ("Subtraction", "concept", 25, 13),
    ("Word Problems", "skill", 30, 14),
]
K2_EDGES = [
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

ELEM_NODES = [
    ("Mathematics", "root", None, 0),
    ("Multiplication", "milestone", 30, 1),
    ("Division", "concept", 30, 2),
    ("Fractions", "concept", 35, 3),
    ("Decimals", "skill", 30, 4),
    ("Language Arts", "root", None, 10),
    ("Paragraph Writing", "milestone", 30, 11),
    ("Essay Structure", "concept", 35, 12),
    ("Grammar & Mechanics", "skill", 25, 13),
    ("Science", "root", None, 20),
    ("Scientific Method", "milestone", 30, 21),
    ("Life Science", "concept", 35, 22),
    ("Earth Science", "concept", 35, 23),
]
ELEM_EDGES = [
    ("Mathematics", "Multiplication"),
    ("Multiplication", "Division"),
    ("Division", "Fractions"),
    ("Fractions", "Decimals"),
    ("Language Arts", "Paragraph Writing"),
    ("Paragraph Writing", "Essay Structure"),
    ("Paragraph Writing", "Grammar & Mechanics"),
    ("Science", "Scientific Method"),
    ("Scientific Method", "Life Science"),
    ("Scientific Method", "Earth Science"),
]

LOGIC_NODES = [
    ("Formal Logic", "root", None, 0),
    ("Propositions", "milestone", 30, 1),
    ("Syllogisms", "concept", 35, 2),
    ("Logical Fallacies", "concept", 30, 3),
    ("Argument Construction", "skill", 40, 4),
    ("Rhetoric Foundations", "root", None, 10),
    ("Ethos", "concept", 25, 11),
    ("Pathos", "concept", 25, 12),
    ("Logos", "concept", 25, 13),
    ("Persuasive Writing", "skill", 40, 14),
]
LOGIC_EDGES = [
    ("Formal Logic", "Propositions"),
    ("Propositions", "Syllogisms"),
    ("Syllogisms", "Logical Fallacies"),
    ("Logical Fallacies", "Argument Construction"),
    ("Rhetoric Foundations", "Ethos"),
    ("Rhetoric Foundations", "Pathos"),
    ("Rhetoric Foundations", "Logos"),
    ("Ethos", "Persuasive Writing"),
    ("Pathos", "Persuasive Writing"),
    ("Logos", "Persuasive Writing"),
    ("Syllogisms", "Logos"),
]


async def _create_map(
    db: AsyncSession,
    household_id: uuid.UUID,
    name: str,
    color: str,
    node_defs: list,
    edge_defs: list,
) -> tuple[LearningMap, dict[str, LearningNode]]:
    subj = Subject(household_id=household_id, name=name, color=color)
    db.add(subj)
    await db.flush()

    lmap = LearningMap(
        household_id=household_id, subject_id=subj.id, name=name, version=3,
    )
    db.add(lmap)
    await db.flush()

    nodes: dict[str, LearningNode] = {}
    for title, ntype, minutes, order in node_defs:
        n = LearningNode(
            learning_map_id=lmap.id, household_id=household_id,
            node_type=ntype, title=title,
            estimated_minutes=minutes, sort_order=order,
        )
        db.add(n)
        await db.flush()
        nodes[title] = n

    for f, t in edge_defs:
        db.add(LearningEdge(
            learning_map_id=lmap.id, household_id=household_id,
            from_node_id=nodes[f].id, to_node_id=nodes[t].id,
            relation=EdgeRelation.prerequisite,
        ))
    await db.flush()

    return lmap, nodes


def _make_card(
    child_id, household_id, node_id,
    stability=10.0, difficulty=2.5, reps=3,
    days_since_review=5, days_until_due=5,
):
    return FSRSCard(
        child_id=child_id, household_id=household_id, node_id=node_id,
        stability=stability, difficulty=difficulty, reps=reps, state=2,
        last_review=NOW - timedelta(days=days_since_review),
        due=NOW + timedelta(days=days_until_due),
    )


def _make_review(card_id, child_id, household_id, rating, days_ago):
    return ReviewLog(
        card_id=card_id, child_id=child_id, household_id=household_id,
        rating=rating, scheduled_days=3, elapsed_days=2,
        reviewed_at=NOW - timedelta(days=days_ago),
    )


async def seed():
    engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    sf = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with sf() as db:
        # ── Idempotency check ──
        existing = await db.execute(
            select(User).where(User.email == DEMO_EMAIL)
        )
        if existing.scalar_one_or_none():
            print(f"Demo user {DEMO_EMAIL} already exists. Skipping seed.")
            await engine.dispose()
            return

        # ═══════════════════════════════════════════
        # Household + Parent
        # ═══════════════════════════════════════════
        household = Household(name="The Builder Family", timezone="America/Denver")
        db.add(household)
        await db.flush()
        hid = household.id

        parent = User(
            household_id=hid, email=DEMO_EMAIL,
            password_hash=hash_password(DEMO_PASSWORD),
            display_name="Zack", role="owner",
        )
        db.add(parent)
        await db.flush()
        pid = parent.id

        # ═══════════════════════════════════════════
        # Children
        # ═══════════════════════════════════════════
        emma = Child(
            household_id=hid, first_name="Emma", last_name="Builder",
            date_of_birth=date(2020, 4, 12), grade_level="K",
        )
        liam = Child(
            household_id=hid, first_name="Liam", last_name="Builder",
            date_of_birth=date(2017, 1, 8), grade_level="4th",
        )
        sophia = Child(
            household_id=hid, first_name="Sophia", last_name="Builder",
            date_of_birth=date(2014, 9, 3), grade_level="7th",
        )
        db.add_all([emma, liam, sophia])
        await db.flush()

        # ═══════════════════════════════════════════
        # Maps + Enrollments
        # ═══════════════════════════════════════════
        map_k2, k2 = await _create_map(db, hid, "K-2 Foundations", "#4CAF50", K2_NODES, K2_EDGES)
        map_elem, elem = await _create_map(db, hid, "Elementary Core", "#2196F3", ELEM_NODES, ELEM_EDGES)
        map_logic, logic = await _create_map(db, hid, "Classical Logic", "#9C27B0", LOGIC_NODES, LOGIC_EDGES)

        for child, lmap in [(emma, map_k2), (liam, map_elem), (sophia, map_logic)]:
            db.add(ChildMapEnrollment(
                child_id=child.id, household_id=hid,
                learning_map_id=lmap.id, enrolled_at_version=3,
            ))
        await db.flush()

        # ═══════════════════════════════════════════
        # Emma (age 6): literacy chain progression
        # 3 mastered, 2 developing, rest not started
        # ═══════════════════════════════════════════
        emma_mastery = {
            "Literacy":           (MasteryLevel.mastered, True, 4, 60),
            "Letter Recognition": (MasteryLevel.mastered, True, 3, 45),
            "Basic Phonics":      (MasteryLevel.mastered, True, 3, 40),
            "Sight Words":        (MasteryLevel.developing, True, 2, 30),
            "Simple Reading":     (MasteryLevel.developing, True, 1, 15),
            "Numeracy":           (MasteryLevel.mastered, True, 3, 40),
            "Counting to 100":    (MasteryLevel.proficient, True, 2, 25),
            "Addition":           (MasteryLevel.emerging, True, 1, 10),
            "Subtraction":        (MasteryLevel.not_started, False, 0, 0),
            "Word Problems":      (MasteryLevel.not_started, False, 0, 0),
        }
        for title, (mastery, unlocked, attempts, mins) in emma_mastery.items():
            db.add(ChildNodeState(
                child_id=emma.id, household_id=hid, node_id=k2[title].id,
                mastery_level=mastery, is_unlocked=unlocked,
                attempts_count=attempts, time_spent_minutes=mins,
                last_activity_at=NOW - timedelta(days=2) if attempts > 0 else None,
            ))

        # FSRS cards for Emma's mastered nodes
        for title in ["Literacy", "Letter Recognition", "Basic Phonics", "Numeracy"]:
            overdue = title == "Basic Phonics"
            db.add(_make_card(
                emma.id, hid, k2[title].id,
                stability=3.0 if overdue else 12.0,
                days_since_review=30 if overdue else 4,
                days_until_due=-20 if overdue else 8,
            ))
        await db.flush()

        # ═══════════════════════════════════════════
        # Liam (age 9): strong progress + 50+ review logs
        # 5 mastered, 3 proficient, 1 emerging
        # ═══════════════════════════════════════════
        liam_mastery = {
            "Mathematics":       (MasteryLevel.mastered, True, 5, 80),
            "Multiplication":    (MasteryLevel.mastered, True, 6, 90),
            "Division":          (MasteryLevel.mastered, True, 5, 75),
            "Fractions":         (MasteryLevel.proficient, True, 4, 60),
            "Decimals":          (MasteryLevel.emerging, True, 1, 15),
            "Language Arts":     (MasteryLevel.mastered, True, 4, 55),
            "Paragraph Writing": (MasteryLevel.mastered, True, 5, 70),
            "Essay Structure":   (MasteryLevel.proficient, True, 3, 50),
            "Grammar & Mechanics": (MasteryLevel.proficient, True, 3, 45),
            "Science":           (MasteryLevel.mastered, True, 3, 40),
            "Scientific Method": (MasteryLevel.proficient, True, 3, 40),
            "Life Science":      (MasteryLevel.developing, True, 2, 30),
            "Earth Science":     (MasteryLevel.not_started, False, 0, 0),
        }
        for title, (mastery, unlocked, attempts, mins) in liam_mastery.items():
            db.add(ChildNodeState(
                child_id=liam.id, household_id=hid, node_id=elem[title].id,
                mastery_level=mastery, is_unlocked=unlocked,
                attempts_count=attempts, time_spent_minutes=mins,
                last_activity_at=NOW - timedelta(days=1) if attempts > 0 else None,
            ))

        # FSRS cards + 50+ review logs for Liam
        review_count = 0
        for title in ["Mathematics", "Multiplication", "Division", "Language Arts",
                       "Paragraph Writing", "Science"]:
            card = _make_card(liam.id, hid, elem[title].id, stability=15.0, reps=6)
            db.add(card)
            await db.flush()
            # 8-10 reviews per card
            for i in range(10 if title in ("Multiplication", "Division") else 8):
                rating = 3 if i < 5 else 4  # Good then Easy
                db.add(_make_review(card.id, liam.id, hid, rating, days_ago=60 - i * 5))
                review_count += 1
        for title in ["Fractions", "Essay Structure", "Grammar & Mechanics", "Scientific Method"]:
            card = _make_card(liam.id, hid, elem[title].id, stability=8.0, reps=3,
                              days_since_review=3, days_until_due=5)
            db.add(card)
            await db.flush()
            for i in range(4):
                db.add(_make_review(card.id, liam.id, hid, 3, days_ago=20 - i * 4))
                review_count += 1
        await db.flush()

        # ═══════════════════════════════════════════
        # Sophia (age 12): slower start + one stalled node
        # 2 mastered, 4 developing, 1 stalled
        # ═══════════════════════════════════════════
        sophia_mastery = {
            "Formal Logic":           (MasteryLevel.mastered, True, 4, 60),
            "Propositions":           (MasteryLevel.mastered, True, 4, 55),
            "Syllogisms":             (MasteryLevel.developing, True, 3, 45),
            "Logical Fallacies":      (MasteryLevel.not_started, False, 0, 0),
            "Argument Construction":  (MasteryLevel.not_started, False, 0, 0),
            "Rhetoric Foundations":   (MasteryLevel.mastered, True, 3, 40),
            "Ethos":                  (MasteryLevel.developing, True, 2, 30),
            "Pathos":                 (MasteryLevel.developing, True, 2, 30),
            "Logos":                  (MasteryLevel.developing, True, 2, 25),
            "Persuasive Writing":     (MasteryLevel.not_started, False, 0, 0),
        }
        for title, (mastery, unlocked, attempts, mins) in sophia_mastery.items():
            # Stalled node: Syllogisms, last activity 20 days ago
            last_act = NOW - timedelta(days=20) if title == "Syllogisms" and attempts > 0 else (
                NOW - timedelta(days=3) if attempts > 0 else None
            )
            db.add(ChildNodeState(
                child_id=sophia.id, household_id=hid, node_id=logic[title].id,
                mastery_level=mastery, is_unlocked=unlocked,
                attempts_count=attempts, time_spent_minutes=mins,
                last_activity_at=last_act,
            ))

        for title in ["Formal Logic", "Propositions", "Rhetoric Foundations"]:
            db.add(_make_card(sophia.id, hid, logic[title].id))
        await db.flush()

        # ═══════════════════════════════════════════
        # Governance Rules (defaults)
        # ═══════════════════════════════════════════
        for name, rtype, params, prio in [
            ("Auto-approve easy activities", RuleType.approval_required,
             {"max_difficulty": 3, "action": "auto_approve"}, 10),
            ("Review difficult activities", RuleType.approval_required,
             {"min_difficulty": 3, "action": "require_review"}, 20),
            ("Daily time limit", RuleType.pace_limit,
             {"max_daily_minutes": 180}, 5),
        ]:
            db.add(GovernanceRule(
                household_id=hid, created_by=pid,
                rule_type=rtype, scope=RuleScope.household,
                name=name, parameters=params, priority=prio,
            ))
        await db.flush()

        # ═══════════════════════════════════════════
        # Plans (one per child)
        # ═══════════════════════════════════════════
        plans_created = 0
        for child, nodes, child_label in [
            (emma, k2, "Emma"),
            (liam, elem, "Liam"),
            (sophia, logic, "Sophia"),
        ]:
            plan = Plan(
                household_id=hid, child_id=child.id, created_by=pid,
                name=f"{child_label} \u2014 Week of {WEEK_START.isoformat()}",
                status=PlanStatus.active, start_date=WEEK_START,
                end_date=WEEK_START + timedelta(days=4), ai_generated=True,
            )
            db.add(plan)
            await db.flush()

            week = PlanWeek(
                plan_id=plan.id, household_id=hid,
                week_number=1, start_date=WEEK_START,
                end_date=WEEK_START + timedelta(days=4),
            )
            db.add(week)
            await db.flush()

            # Pick 3-4 nodes per child for activities
            node_titles = list(nodes.keys())[:5]
            for i, title in enumerate(node_titles):
                completed = i < 2
                a = Activity(
                    plan_week_id=week.id, household_id=hid,
                    node_id=nodes[title].id,
                    activity_type=ActivityType.review if i == 0 else ActivityType.lesson,
                    title=f"{'Review' if i == 0 else 'Study'} {title}",
                    status=ActivityStatus.completed if completed else ActivityStatus.scheduled,
                    scheduled_date=WEEK_START + timedelta(days=i),
                    estimated_minutes=25, sort_order=i,
                    instructions={"difficulty": 2 if i == 0 else 3},
                )
                db.add(a)
                await db.flush()

                # Governance events
                db.add(GovernanceEvent(
                    household_id=hid, user_id=pid,
                    action=GovernanceAction.approve,
                    target_type="activity", target_id=a.id,
                    reason="Auto-approved" if i == 0 else "Parent approved",
                ))

                # Attempts for completed activities
                if completed:
                    db.add(Attempt(
                        activity_id=a.id, household_id=hid, child_id=child.id,
                        status=AttemptStatus.completed,
                        completed_at=NOW - timedelta(hours=24 - i * 4),
                        duration_minutes=20, score=0.75,
                        feedback={"evaluator_summary": f"Good work on {title}"},
                    ))

            plans_created += 1
        await db.flush()

        # ═══════════════════════════════════════════
        # Alerts (3 types)
        # ═══════════════════════════════════════════
        db.add(Alert(
            household_id=hid, child_id=sophia.id,
            severity=AlertSeverity.warning, status=AlertStatus.unread,
            title="Stalled: Syllogisms",
            message="Sophia has not worked on 'Syllogisms' for 20 days at developing level. Consider reviewing or adjusting the approach.",
            source="stall_detection",
            metadata_={"node_id": str(logic["Syllogisms"].id), "days_stalled": 20},
        ))
        db.add(Alert(
            household_id=hid, child_id=emma.id,
            severity=AlertSeverity.warning, status=AlertStatus.unread,
            title="Regression: Basic Phonics",
            message="'Basic Phonics' dropped from mastered to proficient due to overdue review. Retention is declining.",
            source="regression_detection",
            metadata_={"node_id": str(k2["Basic Phonics"].id), "from": "mastered", "to": "proficient"},
        ))
        db.add(Alert(
            household_id=hid, child_id=liam.id,
            severity=AlertSeverity.action_required, status=AlertStatus.unread,
            title="Struggling: Decimals",
            message="Liam has had 3 consecutive low-confidence attempts on 'Decimals'. Consider reviewing prerequisite Fractions or adjusting difficulty.",
            source="pattern_detection",
            metadata_={"node_id": str(elem["Decimals"].id), "consecutive_low": 3},
        ))
        await db.flush()

        # ═══════════════════════════════════════════
        # AI Runs (inspection evidence)
        # ═══════════════════════════════════════════
        for role in ["planner", "planner", "planner", "evaluator", "evaluator", "tutor", "advisor"]:
            db.add(AIRun(
                household_id=hid, triggered_by=pid,
                run_type=role, status=AIRunStatus.completed, model_used="mock",
                input_data={"role": role, "system_prompt": "...", "user_prompt": "..."},
                output_data={"mock": True, "result": f"Mock {role} output for demo"},
                started_at=NOW - timedelta(minutes=10),
                completed_at=NOW - timedelta(minutes=9),
            ))
        await db.flush()

        # ═══════════════════════════════════════════
        # Weekly Snapshots (2 weeks of progress)
        # ═══════════════════════════════════════════
        last_week = WEEK_START - timedelta(days=7)
        for child, mastered_prev, mastered_now, progressed in [
            (emma, 2, 3, 3),
            (liam, 4, 5, 4),
            (sophia, 1, 2, 4),
        ]:
            db.add(WeeklySnapshot(
                household_id=hid, child_id=child.id,
                week_start=last_week, week_end=last_week + timedelta(days=6),
                total_minutes=120, activities_completed=4, activities_scheduled=5,
                nodes_mastered=mastered_prev, nodes_progressed=progressed - 1,
                summary={"week": "previous", "trend": "improving"},
            ))
            db.add(WeeklySnapshot(
                household_id=hid, child_id=child.id,
                week_start=WEEK_START, week_end=WEEK_START + timedelta(days=6),
                total_minutes=150, activities_completed=5, activities_scheduled=5,
                nodes_mastered=mastered_now, nodes_progressed=progressed,
                summary={"week": "current", "trend": "improving"},
            ))
        await db.flush()

        # ═══════════════════════════════════════════
        # Advisor Report (last week)
        # ═══════════════════════════════════════════
        for child, summary in [
            (emma, "Emma had a strong week mastering Basic Phonics and making progress on Sight Words and Simple Reading."),
            (liam, "Liam continues to excel in math. He mastered Division and is working through Fractions confidently."),
            (sophia, "Sophia is progressing through Formal Logic. Syllogisms has stalled and may need a different approach."),
        ]:
            db.add(AdvisorReport(
                household_id=hid, child_id=child.id,
                report_type="weekly",
                period_start=last_week, period_end=last_week + timedelta(days=6),
                content={
                    "summary": summary,
                    "highlights": ["Consistent engagement", "Mastery gains"],
                    "concerns": [] if child != sophia else ["Syllogisms stalled for 20 days"],
                    "recommended_focus": ["Continue current pace"],
                    "engagement_score": 8 if child != sophia else 6,
                },
                recommendations=["Continue current pace", "Review overdue cards"],
            ))

        # Parent override governance event
        db.add(GovernanceEvent(
            household_id=hid, user_id=pid,
            action=GovernanceAction.approve,
            target_type="child_node_state",
            target_id=k2["Addition"].id,
            reason="Emma showed addition skills during grocery shopping",
        ))

        await db.commit()

    await engine.dispose()

    # ═══════════════════════════════════════════
    # Summary
    # ═══════════════════════════════════════════
    print()
    print("=" * 52)
    print("  METHEAN Demo Data Seeded Successfully")
    print("=" * 52)
    print()
    print(f"  Login:     {DEMO_EMAIL}")
    print(f"  Password:  {DEMO_PASSWORD}")
    print(f"  Household: The Builder Family (America/Denver)")
    print()
    print("  Children:")
    print("    Emma    age 6   K      K-2 Foundations")
    print("    Liam    age 9   4th    Elementary Core")
    print("    Sophia  age 12  7th    Classical Logic")
    print()
    print("  Created:")
    print("    3 curriculum maps with prerequisite DAGs")
    print("    3 children with varied mastery progression")
    print(f"    {review_count}+ FSRS review logs (Liam)")
    print("    3 weekly plans (1 per child)")
    print("    3 alerts (stall, regression, pattern failure)")
    print("    6 weekly snapshots (2 weeks x 3 children)")
    print("    3 advisor reports")
    print("    7 AI run inspection records")
    print("    3 governance rules (defaults)")
    print("    Governance events for all activity approvals")
    print()
    print("=" * 52)


if __name__ == "__main__":
    asyncio.run(seed())
