"""Comprehensive tests for the fitness system.

Covers:
- Curriculum templates: registration, progression, content schema.
- Service layer: logging, node state updates, benchmarks, progress, trends.
- Compliance integration: PE hours land under Physical Fitness subject.
- HTTP API: 201s on create, GETs on read, auth enforcement, household isolation.
"""

import uuid
from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy import select

from app.api.child_dashboard import _build_fitness_block, _fitness_trend
from app.models.achievements import Achievement, Streak
from app.models.curriculum import ChildMapEnrollment, LearningMap, LearningNode, Subject
from app.models.enums import NodeType
from app.models.evidence import Alert
from app.models.fitness import FitnessBenchmark, FitnessLog
from app.models.identity import Child, Household
from app.models.state import ChildNodeState, FSRSCard
from app.services.achievements import ACHIEVEMENT_DEFS
from app.services.alert_engine import (
    detect_fitness_overtraining,
    detect_fitness_regression,
    detect_fitness_stall,
)
from app.services.compliance_engine import get_hours_breakdown
from app.services.fitness_service import (
    _rate_fitness_session,
    get_detailed_stats,
    get_progress_summary,
    log_fitness_activity,
    record_benchmark,
)
from app.services.fitness_templates import FITNESS_TEMPLATES
from app.services.templates import TEMPLATES

# ══════════════════════════════════════════════════
# Fixtures — PE subject/map/node rooted at the household
# ══════════════════════════════════════════════════


@pytest_asyncio.fixture
async def pe_subject(db_session, household) -> Subject:
    s = Subject(household_id=household.id, name="Physical Fitness")
    db_session.add(s)
    await db_session.flush()
    return s


@pytest_asyncio.fixture
async def pe_map(db_session, household, pe_subject) -> LearningMap:
    lm = LearningMap(
        household_id=household.id,
        subject_id=pe_subject.id,
        name="Physical Fitness: Foundations",
    )
    db_session.add(lm)
    await db_session.flush()
    return lm


@pytest_asyncio.fixture
async def pe_node(db_session, household, pe_map) -> LearningNode:
    node = LearningNode(
        learning_map_id=pe_map.id,
        household_id=household.id,
        node_type=NodeType.skill,
        title="Two-Foot Jump",
        content={
            "description": "Jump forward from two feet.",
            "benchmark_criteria": "Land 8 of 10 jumps balanced.",
            "assessment_type": "counted",
            "measurement_unit": "repetitions",
            "suggested_frequency": 4,
        },
    )
    db_session.add(node)
    await db_session.flush()
    return node


@pytest_asyncio.fixture
async def second_node(db_session, household, pe_map) -> LearningNode:
    node = LearningNode(
        learning_map_id=pe_map.id,
        household_id=household.id,
        node_type=NodeType.skill,
        title="Balance",
        content={
            "description": "Single-leg balance.",
            "benchmark_criteria": "Hold 10 seconds.",
            "assessment_type": "timed",
            "measurement_unit": "seconds",
            "suggested_frequency": 3,
        },
    )
    db_session.add(node)
    await db_session.flush()
    return node


# ══════════════════════════════════════════════════
# 1. Fitness templates (pure Python — no DB)
# ══════════════════════════════════════════════════


class TestFitnessTemplates:
    EXPECTED_IDS = [
        "physical_fitness_foundations",
        "physical_fitness_development",
        "physical_fitness_intermediate",
        "physical_fitness_advanced",
        "physical_fitness_independent",
    ]

    def test_five_tiers_registered(self):
        assert len(FITNESS_TEMPLATES) == 5
        for tid in self.EXPECTED_IDS:
            assert tid in FITNESS_TEMPLATES, f"Missing tier: {tid}"
            assert tid in TEMPLATES, f"Tier {tid} not in shared TEMPLATES registry"

    def test_foundations_has_movement_nodes(self):
        tpl = FITNESS_TEMPLATES["physical_fitness_foundations"]
        titles = " ".join(n.title.lower() for n in tpl.nodes)
        # Locomotor skills (walking, running, jumping, hopping)
        assert any(word in titles for word in ("walk", "run", "jump", "hop"))
        # Object control (throwing, catching)
        assert any(word in titles for word in ("toss", "throw", "catch"))
        # Body management (balance, flexibility, climbing)
        assert any(word in titles for word in ("balance", "flex", "climb"))

    def test_development_requires_foundations(self):
        """Tier 2's description references foundational movement as a prerequisite."""
        dev = FITNESS_TEMPLATES["physical_fitness_development"]
        desc = dev.description.lower()
        assert any(phrase in desc for phrase in ("foundation", "builds on"))

    def test_nodes_have_benchmark_criteria(self):
        for tid, tpl in FITNESS_TEMPLATES.items():
            for node in tpl.nodes:
                assert node.content is not None, f"{tid}/{node.ref}: missing content"
                assert node.content.get("benchmark_criteria"), f"{tid}/{node.ref}: missing benchmark_criteria"

    def test_nodes_have_measurement_type(self):
        valid_assessments = {"timed", "counted", "pass_fail", "observed"}
        valid_units = {
            "seconds",
            "minutes",
            "repetitions",
            "distance_yards",
            "distance_miles",
            "inches",
            "pounds",
            "boolean",
        }
        for tid, tpl in FITNESS_TEMPLATES.items():
            for node in tpl.nodes:
                assert node.content["assessment_type"] in valid_assessments, f"{tid}/{node.ref}: bad assessment_type"
                assert node.content["measurement_unit"] in valid_units, f"{tid}/{node.ref}: bad measurement_unit"


# ══════════════════════════════════════════════════
# 2. Fitness logging (service layer)
# ══════════════════════════════════════════════════


class TestFitnessLogging:
    @pytest.mark.asyncio
    async def test_log_activity(self, db_session, household, child, user, pe_node):
        result = await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=30,
            measurement_type="counted",
            measurement_value=12,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        assert result["id"] is not None
        assert result["child_id"] == child.id
        assert result["node_id"] == pe_node.id
        assert result["duration_minutes"] == 30
        assert result["measurement_type"] == "counted"
        assert result["measurement_value"] == 12

    @pytest.mark.asyncio
    async def test_log_updates_time_spent(self, db_session, household, child, user, pe_node):
        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=45,
            measurement_type="counted",
            measurement_value=10,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        state_result = await db_session.execute(
            select(ChildNodeState).where(
                ChildNodeState.child_id == child.id,
                ChildNodeState.node_id == pe_node.id,
            )
        )
        state = state_result.scalar_one()
        assert state.time_spent_minutes == 45

    @pytest.mark.asyncio
    async def test_log_with_strength_data(self, db_session, household, child, user, pe_node):
        result = await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=30,
            measurement_type="weight_reps",
            sets=3,
            reps=8,
            weight_lbs=135.0,
            logged_by=user.id,
        )
        assert result["sets"] == 3
        assert result["reps"] == 8
        assert result["weight_lbs"] == 135.0

    @pytest.mark.asyncio
    async def test_log_with_distance(self, db_session, household, child, user, pe_node):
        result = await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=25,
            measurement_type="timed",
            measurement_value=8.5,
            measurement_unit="minutes",
            distance_value=1.0,
            logged_by=user.id,
        )
        assert result["distance_value"] == 1.0

    @pytest.mark.asyncio
    async def test_get_logs_by_child(self, db_session, household, child, user, pe_node, auth_client):
        for minutes in (20, 25, 30):
            await log_fitness_activity(
                db_session,
                household_id=household.id,
                child_id=child.id,
                node_id=pe_node.id,
                logged_at=datetime.now(UTC),
                duration_minutes=minutes,
                measurement_type="counted",
                measurement_value=10,
                measurement_unit="repetitions",
                logged_by=user.id,
            )
        await db_session.commit()

        resp = await auth_client.get(f"/api/v1/fitness/log/{child.id}")
        assert resp.status_code == 200
        body = resp.json()
        assert body["count"] == 3
        # Sorted descending by logged_at — we don't check timestamps here, but
        # verify all three durations are represented.
        durations = {item["duration_minutes"] for item in body["items"]}
        assert durations == {20, 25, 30}

    @pytest.mark.asyncio
    async def test_get_logs_by_node(self, db_session, household, child, user, pe_node, second_node, auth_client):
        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=20,
            measurement_type="counted",
            measurement_value=10,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=second_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=30,
            measurement_type="timed",
            measurement_value=15,
            measurement_unit="seconds",
            logged_by=user.id,
        )
        await db_session.commit()

        resp = await auth_client.get(
            f"/api/v1/fitness/log/{child.id}",
            params={"node_id": str(pe_node.id)},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["count"] == 1
        assert body["items"][0]["node_id"] == str(pe_node.id)

    @pytest.mark.asyncio
    async def test_get_logs_date_range(self, db_session, household, child, user, pe_node, auth_client):
        now = datetime.now(UTC)
        old = now - timedelta(days=10)
        recent = now - timedelta(days=1)
        for ts in (old, recent):
            await log_fitness_activity(
                db_session,
                household_id=household.id,
                child_id=child.id,
                node_id=pe_node.id,
                logged_at=ts,
                duration_minutes=20,
                measurement_type="counted",
                measurement_value=10,
                measurement_unit="repetitions",
                logged_by=user.id,
            )
        await db_session.commit()

        start = (now - timedelta(days=3)).isoformat()
        resp = await auth_client.get(
            f"/api/v1/fitness/log/{child.id}",
            params={"start_date": start},
        )
        assert resp.status_code == 200
        assert resp.json()["count"] == 1


# ══════════════════════════════════════════════════
# 3. Fitness benchmarks
# ══════════════════════════════════════════════════


class TestFitnessBenchmarks:
    @pytest.mark.asyncio
    async def test_record_benchmark(self, db_session, household, child):
        result = await record_benchmark(
            db_session,
            household_id=household.id,
            child_id=child.id,
            benchmark_name="mile_run",
            value=540.0,
            unit="seconds",
        )
        assert result["id"] is not None
        assert result["benchmark_name"] == "mile_run"
        assert result["value"] == 540.0
        assert result["unit"] == "seconds"
        assert result["personal_best"] is True
        assert result["improvement_pct"] == 0.0

    @pytest.mark.asyncio
    async def test_benchmark_history(self, db_session, household, child):
        base = datetime.now(UTC) - timedelta(days=60)
        for offset, value in [(0, 600), (30, 540), (60, 480)]:
            await record_benchmark(
                db_session,
                household_id=household.id,
                child_id=child.id,
                benchmark_name="mile_run",
                value=value,
                unit="seconds",
                measured_at=base + timedelta(days=offset),
            )
        rows_result = await db_session.execute(
            select(FitnessBenchmark)
            .where(FitnessBenchmark.child_id == child.id)
            .order_by(FitnessBenchmark.measured_at.asc())
        )
        rows = list(rows_result.scalars().all())
        assert [r.value for r in rows] == [600, 540, 480]

    @pytest.mark.asyncio
    async def test_personal_best_flagged(self, db_session, household, child):
        base = datetime.now(UTC) - timedelta(days=30)
        r1 = await record_benchmark(
            db_session,
            household_id=household.id,
            child_id=child.id,
            benchmark_name="mile_run",
            value=600.0,
            unit="seconds",
            measured_at=base,
        )
        r2 = await record_benchmark(
            db_session,
            household_id=household.id,
            child_id=child.id,
            benchmark_name="mile_run",
            value=620.0,  # slower — NOT a PB for a lower-is-better metric
            unit="seconds",
            measured_at=base + timedelta(days=10),
        )
        r3 = await record_benchmark(
            db_session,
            household_id=household.id,
            child_id=child.id,
            benchmark_name="mile_run",
            value=580.0,  # faster — IS a PB
            unit="seconds",
            measured_at=base + timedelta(days=20),
        )
        assert r1["personal_best"] is True
        assert r2["personal_best"] is False
        assert r3["personal_best"] is True

    @pytest.mark.asyncio
    async def test_improvement_pct(self, db_session, household, child):
        base = datetime.now(UTC) - timedelta(days=60)
        await record_benchmark(
            db_session,
            household_id=household.id,
            child_id=child.id,
            benchmark_name="mile_run",
            value=600.0,
            unit="seconds",
            measured_at=base,
        )
        latest = await record_benchmark(
            db_session,
            household_id=household.id,
            child_id=child.id,
            benchmark_name="mile_run",
            value=480.0,
            unit="seconds",
            measured_at=base + timedelta(days=60),
        )
        # (600 - 480) / 600 * 100 = 20%
        assert latest["improvement_pct"] == pytest.approx(20.0, abs=0.01)


# ══════════════════════════════════════════════════
# 4. Progress summary
# ══════════════════════════════════════════════════


class TestFitnessProgress:
    @pytest.mark.asyncio
    async def test_progress_empty(self, db_session, household, child):
        result = await get_progress_summary(db_session, household.id, child.id)
        assert result["fitness_hours"]["all_time"] == 0.0
        assert result["fitness_hours"]["this_month"] == 0.0
        assert result["fitness_hours"]["this_week"] == 0.0
        assert result["benchmarks"] == []
        assert result["nodes"]["mastered"] == 0
        assert result["nodes"]["total"] == 0

    @pytest.mark.asyncio
    async def test_progress_with_data(self, db_session, household, child, user, pe_node):
        now = datetime.now(UTC)
        for minutes in (30, 45, 60):
            await log_fitness_activity(
                db_session,
                household_id=household.id,
                child_id=child.id,
                node_id=pe_node.id,
                logged_at=now,
                duration_minutes=minutes,
                measurement_type="counted",
                measurement_value=10,
                measurement_unit="repetitions",
                logged_by=user.id,
            )
        result = await get_progress_summary(db_session, household.id, child.id)
        assert result["fitness_hours"]["all_time"] == pytest.approx(2.25, abs=0.05)

    @pytest.mark.asyncio
    async def test_trend_improving(self, db_session, household, child):
        """Five counted-reps benchmarks increasing over time → improving."""
        base = datetime.now(UTC) - timedelta(days=50)
        for offset, value in [(0, 10), (10, 12), (20, 14), (30, 16), (40, 18)]:
            await record_benchmark(
                db_session,
                household_id=household.id,
                child_id=child.id,
                benchmark_name="pullups",
                value=value,
                unit="repetitions",
                measured_at=base + timedelta(days=offset),
            )
        result = await get_progress_summary(db_session, household.id, child.id)
        pullups = next(b for b in result["benchmarks"] if b["benchmark_name"] == "pullups")
        assert pullups["trend"] == "improving"

    @pytest.mark.asyncio
    async def test_trend_declining(self, db_session, household, child):
        """Five counted-reps benchmarks decreasing over time → declining."""
        base = datetime.now(UTC) - timedelta(days=50)
        for offset, value in [(0, 20), (10, 18), (20, 16), (30, 14), (40, 12)]:
            await record_benchmark(
                db_session,
                household_id=household.id,
                child_id=child.id,
                benchmark_name="pullups",
                value=value,
                unit="repetitions",
                measured_at=base + timedelta(days=offset),
            )
        result = await get_progress_summary(db_session, household.id, child.id)
        pullups = next(b for b in result["benchmarks"] if b["benchmark_name"] == "pullups")
        assert pullups["trend"] == "declining"

    @pytest.mark.asyncio
    async def test_total_hours(self, db_session, household, child, user, pe_node):
        """30 + 45 + 60 minutes = 2.25 hours."""
        now = datetime.now(UTC)
        for minutes in (30, 45, 60):
            await log_fitness_activity(
                db_session,
                household_id=household.id,
                child_id=child.id,
                node_id=pe_node.id,
                logged_at=now,
                duration_minutes=minutes,
                measurement_type="counted",
                measurement_value=10,
                measurement_unit="repetitions",
                logged_by=user.id,
            )
        result = await get_progress_summary(db_session, household.id, child.id)
        assert result["fitness_hours"]["all_time"] == pytest.approx(2.25, abs=0.05)


# ══════════════════════════════════════════════════
# 5. Compliance integration
# ══════════════════════════════════════════════════


class TestFitnessCompliance:
    @pytest.mark.asyncio
    async def test_pe_hours_in_compliance(self, db_session, household, child, user, pe_node):
        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=60,
            measurement_type="counted",
            measurement_value=12,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        hours = await get_hours_breakdown(db_session, household.id, child.id)
        assert "Physical Fitness" in hours["by_subject"]
        assert hours["by_subject"]["Physical Fitness"] == pytest.approx(1.0, abs=0.05)

    @pytest.mark.asyncio
    async def test_pe_and_academic_separate(self, db_session, household, child, user, pe_node, subject, learning_map):
        math_node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Fractions",
        )
        db_session.add(math_node)
        await db_session.flush()
        db_session.add(
            ChildNodeState(
                child_id=child.id,
                household_id=household.id,
                node_id=math_node.id,
                time_spent_minutes=90,
            )
        )
        await db_session.flush()

        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=30,
            measurement_type="counted",
            measurement_value=10,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        hours = await get_hours_breakdown(db_session, household.id, child.id)
        # 90 min math + 30 min PE = 2.0 total hours
        assert hours["total_hours"] == pytest.approx(2.0, abs=0.05)
        assert hours["by_subject"]["Mathematics"] == pytest.approx(1.5, abs=0.05)
        assert hours["by_subject"]["Physical Fitness"] == pytest.approx(0.5, abs=0.05)


# ══════════════════════════════════════════════════
# 6. API layer
# ══════════════════════════════════════════════════


class TestFitnessAPI:
    @pytest.mark.asyncio
    async def test_log_endpoint_201(self, auth_client, db_session, household, child, pe_node):
        resp = await auth_client.post(
            "/api/v1/fitness/log",
            json={
                "child_id": str(child.id),
                "node_id": str(pe_node.id),
                "duration_minutes": 30,
                "measurement_type": "counted",
                "measurement_value": 12,
                "measurement_unit": "repetitions",
            },
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["duration_minutes"] == 30
        assert body["measurement_type"] == "counted"

    @pytest.mark.asyncio
    async def test_benchmark_endpoint_201(self, auth_client, child):
        resp = await auth_client.post(
            "/api/v1/fitness/benchmark",
            json={
                "child_id": str(child.id),
                "benchmark_name": "mile_run",
                "value": 540.0,
                "unit": "seconds",
            },
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["benchmark_name"] == "mile_run"
        assert body["personal_best"] is True

    @pytest.mark.asyncio
    async def test_progress_endpoint(self, auth_client, child):
        resp = await auth_client.get(f"/api/v1/fitness/progress/{child.id}")
        assert resp.status_code == 200
        body = resp.json()
        assert "fitness_hours" in body
        assert "benchmarks" in body
        assert "nodes" in body

    @pytest.mark.asyncio
    async def test_stats_endpoint(self, auth_client, child):
        resp = await auth_client.get(f"/api/v1/fitness/stats/{child.id}")
        assert resp.status_code == 200
        body = resp.json()
        for key in ("weekly_minutes", "strength", "endurance", "flexibility"):
            assert key in body

    @pytest.mark.asyncio
    async def test_auth_required(self, client, child, pe_node):
        """All six fitness endpoints reject unauthenticated access."""
        client.cookies.clear()
        client.headers.pop("Authorization", None)

        endpoints = [
            (
                "POST",
                "/api/v1/fitness/log",
                {
                    "child_id": str(child.id),
                    "node_id": str(pe_node.id),
                    "duration_minutes": 10,
                    "measurement_type": "counted",
                },
            ),
            ("GET", f"/api/v1/fitness/log/{child.id}", None),
            (
                "POST",
                "/api/v1/fitness/benchmark",
                {"child_id": str(child.id), "benchmark_name": "x", "value": 1, "unit": "seconds"},
            ),
            ("GET", f"/api/v1/fitness/benchmarks/{child.id}", None),
            ("GET", f"/api/v1/fitness/progress/{child.id}", None),
            ("GET", f"/api/v1/fitness/stats/{child.id}", None),
        ]
        for method, path, body in endpoints:
            if method == "GET":
                resp = await client.get(path)
            else:
                resp = await client.post(path, json=body or {})
            assert resp.status_code in (401, 403), f"{method} {path} → {resp.status_code}"

    @pytest.mark.asyncio
    async def test_household_isolation(self, auth_client, db_session, household, user):
        """auth_client (household A) cannot read household B's child fitness data."""
        other_household = Household(name="Other Family", timezone="UTC")
        db_session.add(other_household)
        await db_session.flush()

        other_child = Child(
            household_id=other_household.id,
            first_name="Other",
            last_name="Kid",
        )
        db_session.add(other_child)
        await db_session.flush()

        # Put a log under the other household.
        other_subj = Subject(household_id=other_household.id, name="Physical Fitness")
        db_session.add(other_subj)
        await db_session.flush()
        other_map = LearningMap(
            household_id=other_household.id,
            subject_id=other_subj.id,
            name="Other PE Map",
        )
        db_session.add(other_map)
        await db_session.flush()
        other_node = LearningNode(
            learning_map_id=other_map.id,
            household_id=other_household.id,
            node_type=NodeType.skill,
            title="Other Jump",
        )
        db_session.add(other_node)
        await db_session.flush()
        db_session.add(
            FitnessLog(
                household_id=other_household.id,
                child_id=other_child.id,
                node_id=other_node.id,
                logged_at=datetime.now(UTC),
                duration_minutes=30,
                measurement_type="counted",
                measurement_value=10,
            )
        )
        await db_session.commit()

        # Household A asks for Household B's child logs.
        resp = await auth_client.get(f"/api/v1/fitness/log/{other_child.id}")
        # Either 404 (child not found in our household) or empty list — both
        # prove isolation. Never leak the other household's records.
        if resp.status_code == 200:
            assert resp.json()["count"] == 0
        else:
            assert resp.status_code == 404


# ══════════════════════════════════════════════════
# 7. Detailed stats — Epley 1RM, timeseries shape
# ══════════════════════════════════════════════════


class TestFitnessDetailedStats:
    @pytest.mark.asyncio
    async def test_epley_1rm_from_strength_log(self, db_session, household, child, user, pe_node):
        """weight_reps logs produce estimated_1rm = weight * (1 + reps/30)."""
        now = datetime.now(UTC)
        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=now,
            duration_minutes=30,
            measurement_type="weight_reps",
            sets=3,
            reps=10,
            weight_lbs=150.0,
            logged_by=user.id,
        )
        start = now - timedelta(days=1)
        end = now + timedelta(days=1)
        stats = await get_detailed_stats(db_session, household.id, child.id, start, end)
        assert len(stats["strength"]) == 1
        entry = stats["strength"][0]
        # 150 * (1 + 10/30) = 200.0
        assert entry["estimated_1rm"] == pytest.approx(200.0, abs=0.01)


# ══════════════════════════════════════════════════
# 8. FSRS integration (pure-Python rating logic + DB-backed card creation)
# ══════════════════════════════════════════════════


class TestFitnessFSRSRating:
    """Pure-Python tests for the _rate_fitness_session mapping."""

    def test_no_threshold_returns_good(self):
        from fsrs import Rating

        assert _rate_fitness_session(None, None, "gte", "pass_fail") == Rating.Good
        assert _rate_fitness_session(12, None, "gte", "counted") == Rating.Good

    def test_threshold_met_returns_easy(self):
        from fsrs import Rating

        # gte: 22 reps meets a 20-rep target.
        assert _rate_fitness_session(22, 20, "gte", "counted") == Rating.Easy
        # lte: 540s beats a 600s target.
        assert _rate_fitness_session(540, 600, "lte", "timed") == Rating.Easy

    def test_struggled_returns_hard(self):
        from fsrs import Rating

        # gte + <50% of target → Hard.
        assert _rate_fitness_session(8, 20, "gte", "counted") == Rating.Hard
        # lte + >200% of target (e.g. 1500s when goal was 600s) → Hard.
        assert _rate_fitness_session(1500, 600, "lte", "timed") == Rating.Hard

    def test_partial_between_50_and_100_returns_good(self):
        from fsrs import Rating

        # gte + 60% of target (not met, but not struggling) → Good.
        assert _rate_fitness_session(12, 20, "gte", "counted") == Rating.Good
        # lte + 150% of target (slow but not struggling) → Good.
        assert _rate_fitness_session(900, 600, "lte", "timed") == Rating.Good


class TestFitnessFSRSCardCreation:
    @pytest.mark.asyncio
    async def test_log_creates_fsrs_card(self, db_session, household, child, user, pe_node):
        """First fitness log on a node creates an FSRSCard row."""
        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=30,
            measurement_type="counted",
            measurement_value=12,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        card_result = await db_session.execute(
            select(FSRSCard).where(
                FSRSCard.child_id == child.id,
                FSRSCard.node_id == pe_node.id,
            )
        )
        card = card_result.scalar_one()
        assert card.last_review is not None
        assert card.reps >= 1

    @pytest.mark.asyncio
    async def test_second_log_reuses_existing_card(self, db_session, household, child, user, pe_node):
        """Subsequent fitness logs update the existing card rather than creating a new one."""
        for _ in range(2):
            await log_fitness_activity(
                db_session,
                household_id=household.id,
                child_id=child.id,
                node_id=pe_node.id,
                logged_at=datetime.now(UTC),
                duration_minutes=20,
                measurement_type="counted",
                measurement_value=12,
                measurement_unit="repetitions",
                logged_by=user.id,
            )
        cards_result = await db_session.execute(
            select(FSRSCard).where(
                FSRSCard.child_id == child.id,
                FSRSCard.node_id == pe_node.id,
            )
        )
        cards = cards_result.scalars().all()
        assert len(cards) == 1
        assert cards[0].reps >= 2

    @pytest.mark.asyncio
    async def test_log_result_includes_fsrs_rating(self, db_session, household, child, user, pe_node):
        """log_fitness_activity returns the FSRS rating used for the review."""
        result = await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=20,
            measurement_type="counted",
            measurement_value=12,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        # Node has no benchmark_threshold and assessment_type="counted" → Good (3).
        assert result["fsrs_rating"] == 3


# ══════════════════════════════════════════════════
# 9. Fitness alert detection
# ══════════════════════════════════════════════════


class TestFitnessAlerts:
    @pytest.mark.asyncio
    async def test_stall_fires_when_no_logs_for_14_days(self, db_session, household, child, pe_map):
        """Active PE enrollment with zero logs → info alert."""
        db_session.add(
            ChildMapEnrollment(
                child_id=child.id,
                household_id=household.id,
                learning_map_id=pe_map.id,
                is_active=True,
            )
        )
        await db_session.flush()

        alerts = await detect_fitness_stall(db_session, household.id)
        assert len(alerts) == 1
        assert alerts[0].severity.value == "info"
        assert alerts[0].source == "fitness_stall_detection"
        assert "two weeks" in alerts[0].message

    @pytest.mark.asyncio
    async def test_stall_does_not_fire_with_recent_log(self, db_session, household, child, user, pe_node, pe_map):
        """Any log in the last 14 days suppresses the stall alert."""
        db_session.add(
            ChildMapEnrollment(
                child_id=child.id,
                household_id=household.id,
                learning_map_id=pe_map.id,
                is_active=True,
            )
        )
        await db_session.flush()
        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC) - timedelta(days=1),
            duration_minutes=20,
            measurement_type="counted",
            measurement_value=10,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        alerts = await detect_fitness_stall(db_session, household.id)
        assert alerts == []

    @pytest.mark.asyncio
    async def test_stall_skips_children_without_pe_enrollment(self, db_session, household, child):
        """Children with no PE enrollment are not candidates for the stall check."""
        alerts = await detect_fitness_stall(db_session, household.id)
        assert alerts == []

    @pytest.mark.asyncio
    async def test_regression_fires_on_three_worsening_benchmarks(self, db_session, household, child):
        """Three consecutively worse mile_run times → warning alert."""
        base = datetime.now(UTC) - timedelta(days=30)
        for offset, value in [(0, 500), (10, 520), (20, 540)]:
            await record_benchmark(
                db_session,
                household_id=household.id,
                child_id=child.id,
                benchmark_name="mile_run",
                value=value,
                unit="seconds",
                measured_at=base + timedelta(days=offset),
            )
        # record_benchmark fires the alert inline. Query directly.
        alerts_result = await db_session.execute(
            select(Alert).where(
                Alert.household_id == household.id,
                Alert.child_id == child.id,
                Alert.source == "fitness_regression:mile_run",
            )
        )
        alert = alerts_result.scalar_one()
        assert alert.severity.value == "warning"
        assert "declined" in alert.message

    @pytest.mark.asyncio
    async def test_regression_does_not_fire_on_mixed_trend(self, db_session, household, child):
        """Improving or mixed benchmarks do not trigger regression."""
        base = datetime.now(UTC) - timedelta(days=30)
        for offset, value in [(0, 540), (10, 500), (20, 480)]:  # improving
            await record_benchmark(
                db_session,
                household_id=household.id,
                child_id=child.id,
                benchmark_name="mile_run",
                value=value,
                unit="seconds",
                measured_at=base + timedelta(days=offset),
            )
        alerts = await detect_fitness_regression(db_session, child.id, household.id, "mile_run")
        assert alerts is None

    @pytest.mark.asyncio
    async def test_overtraining_fires_for_tier_1_child(self, db_session, household, child, user, pe_node, pe_map):
        """>6 long sessions in current week for a Tier 1 child → info alert."""
        db_session.add(
            ChildMapEnrollment(
                child_id=child.id,
                household_id=household.id,
                learning_map_id=pe_map.id,
                is_active=True,
            )
        )
        await db_session.flush()
        now = datetime.now(UTC)
        for _ in range(7):
            await log_fitness_activity(
                db_session,
                household_id=household.id,
                child_id=child.id,
                node_id=pe_node.id,
                logged_at=now,
                duration_minutes=45,
                measurement_type="counted",
                measurement_value=10,
                measurement_unit="repetitions",
                logged_by=user.id,
            )
        alerts_result = await db_session.execute(
            select(Alert).where(
                Alert.household_id == household.id,
                Alert.child_id == child.id,
                Alert.source == "fitness_overtraining_detection",
            )
        )
        alert = alerts_result.scalar_one()
        assert alert.severity.value == "info"
        assert "rest day" in alert.message.lower()

    @pytest.mark.asyncio
    async def test_overtraining_skips_short_sessions(self, db_session, household, child, user, pe_node, pe_map):
        """Sessions ≤ 30 minutes are not counted toward the overtraining threshold."""
        db_session.add(
            ChildMapEnrollment(
                child_id=child.id,
                household_id=household.id,
                learning_map_id=pe_map.id,
                is_active=True,
            )
        )
        await db_session.flush()
        now = datetime.now(UTC)
        for _ in range(8):
            await log_fitness_activity(
                db_session,
                household_id=household.id,
                child_id=child.id,
                node_id=pe_node.id,
                logged_at=now,
                duration_minutes=25,  # below threshold
                measurement_type="counted",
                measurement_value=10,
                measurement_unit="repetitions",
                logged_by=user.id,
            )
        result = await detect_fitness_overtraining(db_session, child.id, household.id)
        assert result is None

    @pytest.mark.asyncio
    async def test_overtraining_skips_tier_4_and_5(self, db_session, household, child, user, pe_subject):
        """Tier 4 (Advanced) and Tier 5 (Independent) children are exempt."""
        advanced_map = LearningMap(
            household_id=household.id,
            subject_id=pe_subject.id,
            name="Physical Fitness: Advanced",
        )
        db_session.add(advanced_map)
        await db_session.flush()
        advanced_node = LearningNode(
            learning_map_id=advanced_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Pull-Up",
            content={
                "description": "Strict pull-up.",
                "benchmark_criteria": "5 strict.",
                "assessment_type": "counted",
                "measurement_unit": "repetitions",
                "suggested_frequency": 3,
            },
        )
        db_session.add(advanced_node)
        await db_session.flush()
        db_session.add(
            ChildMapEnrollment(
                child_id=child.id,
                household_id=household.id,
                learning_map_id=advanced_map.id,
                is_active=True,
            )
        )
        await db_session.flush()
        now = datetime.now(UTC)
        for _ in range(7):
            await log_fitness_activity(
                db_session,
                household_id=household.id,
                child_id=child.id,
                node_id=advanced_node.id,
                logged_at=now,
                duration_minutes=60,
                measurement_type="counted",
                measurement_value=8,
                measurement_unit="repetitions",
                logged_by=user.id,
            )
        result = await detect_fitness_overtraining(db_session, child.id, household.id)
        assert result is None


# ══════════════════════════════════════════════════
# 10. Fitness achievements
# ══════════════════════════════════════════════════


class TestFitnessAchievementDefinitions:
    """Pure-Python checks on the six fitness ACHIEVEMENT_DEFS entries."""

    EXPECTED = {
        "first_mile",
        "iron_consistency",
        "personal_best",
        "tier_up",
        "century_fitness",
        "coaching_badge",
    }

    def test_all_six_registered(self):
        types = {d["type"] for d in ACHIEVEMENT_DEFS if d.get("category") == "fitness"}
        assert types == self.EXPECTED

    def test_icons_are_slug_strings(self):
        slug_icons = {"trophy-running", "calendar-check", "medal", "arrow-up-circle", "flame", "users"}
        for d in ACHIEVEMENT_DEFS:
            if d.get("category") == "fitness":
                assert d["icon"] in slug_icons


class TestFitnessAchievements:
    @pytest.mark.asyncio
    async def test_first_mile_fires_on_mile_run_benchmark(self, db_session, household, child):
        await record_benchmark(
            db_session,
            household_id=household.id,
            child_id=child.id,
            benchmark_name="mile_run",
            value=540.0,
            unit="seconds",
        )
        result = await db_session.execute(
            select(Achievement).where(
                Achievement.child_id == child.id,
                Achievement.achievement_type == "first_mile",
            )
        )
        assert result.scalar_one_or_none() is not None

    @pytest.mark.asyncio
    async def test_first_mile_skips_other_benchmarks(self, db_session, household, child):
        await record_benchmark(
            db_session,
            household_id=household.id,
            child_id=child.id,
            benchmark_name="vertical_jump",
            value=18.0,
            unit="inches",
        )
        result = await db_session.execute(
            select(Achievement).where(
                Achievement.child_id == child.id,
                Achievement.achievement_type == "first_mile",
            )
        )
        assert result.scalar_one_or_none() is None

    @pytest.mark.asyncio
    async def test_personal_best_fires_on_new_record(self, db_session, household, child):
        """First benchmark does NOT grant PB; subsequent improvement does."""
        base = datetime.now(UTC) - timedelta(days=30)
        await record_benchmark(
            db_session,
            household_id=household.id,
            child_id=child.id,
            benchmark_name="mile_run",
            value=600.0,
            unit="seconds",
            measured_at=base,
        )
        first_pb = await db_session.execute(
            select(Achievement).where(
                Achievement.child_id == child.id,
                Achievement.achievement_type == "personal_best",
            )
        )
        assert first_pb.scalar_one_or_none() is None

        await record_benchmark(
            db_session,
            household_id=household.id,
            child_id=child.id,
            benchmark_name="mile_run",
            value=540.0,
            unit="seconds",
            measured_at=base + timedelta(days=10),
        )
        after = await db_session.execute(
            select(Achievement).where(
                Achievement.child_id == child.id,
                Achievement.achievement_type == "personal_best",
            )
        )
        assert after.scalar_one_or_none() is not None

    @pytest.mark.asyncio
    async def test_century_fitness_fires_at_100_logs(self, db_session, household, child, user, pe_node):
        now = datetime.now(UTC)
        for i in range(99):
            db_session.add(
                FitnessLog(
                    household_id=household.id,
                    child_id=child.id,
                    node_id=pe_node.id,
                    logged_at=now - timedelta(minutes=i),
                    duration_minutes=15,
                    measurement_type="counted",
                    measurement_value=10,
                    measurement_unit="repetitions",
                    logged_by=user.id,
                )
            )
        await db_session.flush()

        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=now,
            duration_minutes=15,
            measurement_type="counted",
            measurement_value=12,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        result = await db_session.execute(
            select(Achievement).where(
                Achievement.child_id == child.id,
                Achievement.achievement_type == "century_fitness",
            )
        )
        assert result.scalar_one_or_none() is not None

    @pytest.mark.asyncio
    async def test_century_fitness_does_not_fire_at_low_count(self, db_session, household, child, user, pe_node):
        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=10,
            measurement_type="counted",
            measurement_value=5,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        result = await db_session.execute(
            select(Achievement).where(
                Achievement.child_id == child.id,
                Achievement.achievement_type == "century_fitness",
            )
        )
        assert result.scalar_one_or_none() is None

    @pytest.mark.asyncio
    async def test_iron_consistency_fires_on_4_weeks_of_5_days(self, db_session, household, child, user, pe_node):
        now = datetime.now(UTC)
        current_week_start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        window_start = current_week_start - timedelta(weeks=4)

        for w in range(4):
            for d in range(5):
                db_session.add(
                    FitnessLog(
                        household_id=household.id,
                        child_id=child.id,
                        node_id=pe_node.id,
                        logged_at=window_start + timedelta(weeks=w, days=d, hours=9),
                        duration_minutes=20,
                        measurement_type="counted",
                        measurement_value=10,
                        measurement_unit="repetitions",
                        logged_by=user.id,
                    )
                )
        await db_session.flush()

        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=now,
            duration_minutes=20,
            measurement_type="counted",
            measurement_value=10,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        result = await db_session.execute(
            select(Achievement).where(
                Achievement.child_id == child.id,
                Achievement.achievement_type == "iron_consistency",
            )
        )
        assert result.scalar_one_or_none() is not None

    @pytest.mark.asyncio
    async def test_iron_consistency_misses_sparse_week(self, db_session, household, child, user, pe_node):
        now = datetime.now(UTC)
        current_week_start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        window_start = current_week_start - timedelta(weeks=4)

        for w in range(4):
            days = 5 if w != 1 else 2
            for d in range(days):
                db_session.add(
                    FitnessLog(
                        household_id=household.id,
                        child_id=child.id,
                        node_id=pe_node.id,
                        logged_at=window_start + timedelta(weeks=w, days=d, hours=9),
                        duration_minutes=20,
                        measurement_type="counted",
                        measurement_value=10,
                        measurement_unit="repetitions",
                        logged_by=user.id,
                    )
                )
        await db_session.flush()

        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=now,
            duration_minutes=20,
            measurement_type="counted",
            measurement_value=10,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        result = await db_session.execute(
            select(Achievement).where(
                Achievement.child_id == child.id,
                Achievement.achievement_type == "iron_consistency",
            )
        )
        assert result.scalar_one_or_none() is None

    @pytest.mark.asyncio
    async def test_coaching_badge_fires_on_coaching_node_mastery(self, db_session, household, child, user, pe_subject):
        independent = LearningMap(
            household_id=household.id,
            subject_id=pe_subject.id,
            name="Physical Fitness: Independent",
        )
        db_session.add(independent)
        await db_session.flush()
        coaching = LearningNode(
            learning_map_id=independent.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Coaching Fundamentals",
            content={
                "description": "Teach a fitness skill.",
                "benchmark_criteria": "Deliver a 20-minute lesson.",
                "assessment_type": "pass_fail",
                "measurement_unit": "boolean",
                "suggested_frequency": 1,
            },
        )
        db_session.add(coaching)
        await db_session.flush()

        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=coaching.id,
            logged_at=datetime.now(UTC),
            duration_minutes=20,
            measurement_type="pass_fail",
            measurement_value=1,
            measurement_unit="boolean",
            logged_by=user.id,
        )
        result = await db_session.execute(
            select(Achievement).where(
                Achievement.child_id == child.id,
                Achievement.achievement_type == "coaching_badge",
            )
        )
        assert result.scalar_one_or_none() is not None


# ══════════════════════════════════════════════════
# 11. Dashboard + streak integration
# ══════════════════════════════════════════════════


class TestFitnessTrendHelper:
    """Pure-Python trend classifier used by the dashboard builder."""

    def test_improving_higher_is_better(self):
        assert _fitness_trend([10, 12, 14, 16, 18], lower_is_better=False) == "improving"

    def test_improving_lower_is_better(self):
        assert _fitness_trend([600, 560, 540, 520, 500], lower_is_better=True) == "improving"

    def test_declining_higher_is_better(self):
        assert _fitness_trend([20, 18, 16, 14, 12], lower_is_better=False) == "declining"

    def test_plateau_mixed(self):
        assert _fitness_trend([10, 12, 10, 12, 10], lower_is_better=False) == "plateau"

    def test_short_series_is_plateau(self):
        assert _fitness_trend([15], lower_is_better=False) == "plateau"


class TestFitnessDashboardBlock:
    @pytest.mark.asyncio
    async def test_returns_none_without_enrollment(self, db_session, household, child):
        from datetime import date

        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        block = await _build_fitness_block(db_session, child.id, household.id, today, week_start)
        assert block is None

    @pytest.mark.asyncio
    async def test_returns_block_with_tier_and_streak(self, db_session, household, child, user, pe_map, pe_node):
        """Enrollment + two consecutive days of logs yields a populated fitness block."""
        from datetime import date

        db_session.add(
            ChildMapEnrollment(
                household_id=household.id,
                child_id=child.id,
                learning_map_id=pe_map.id,
                is_active=True,
            )
        )
        await db_session.flush()

        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        for offset in (1, 0):  # yesterday + today
            await log_fitness_activity(
                db_session,
                household_id=household.id,
                child_id=child.id,
                node_id=pe_node.id,
                logged_at=datetime.combine(today - timedelta(days=offset), datetime.min.time(), tzinfo=UTC)
                + timedelta(hours=10),
                duration_minutes=30,
                measurement_type="counted",
                measurement_value=12,
                measurement_unit="repetitions",
                logged_by=user.id,
            )

        block = await _build_fitness_block(db_session, child.id, household.id, today, week_start)
        assert block is not None
        assert block["current_tier"] == "Foundations"
        assert block["streak_days"] == 2
        assert block["this_week_minutes"] >= 30  # at least today's 30 counted

    @pytest.mark.asyncio
    async def test_recent_benchmark_includes_trend(self, db_session, household, child, pe_map):
        """Latest benchmark surfaces with a trend classification."""
        from datetime import date

        db_session.add(
            ChildMapEnrollment(
                household_id=household.id,
                child_id=child.id,
                learning_map_id=pe_map.id,
                is_active=True,
            )
        )
        await db_session.flush()

        base = datetime.now(UTC) - timedelta(days=30)
        for offset, value in [(0, 600), (10, 580), (20, 560)]:
            await record_benchmark(
                db_session,
                household_id=household.id,
                child_id=child.id,
                benchmark_name="mile_run",
                value=value,
                unit="seconds",
                measured_at=base + timedelta(days=offset),
            )

        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        block = await _build_fitness_block(db_session, child.id, household.id, today, week_start)
        assert block is not None
        bench = block["recent_benchmark"]
        assert bench is not None
        assert bench["name"] == "mile_run"
        assert bench["value"] == 560
        assert bench["unit"] == "seconds"
        assert bench["trend"] == "improving"


class TestFitnessStreakIntegration:
    @pytest.mark.asyncio
    async def test_fitness_log_updates_streak(self, db_session, household, child, user, pe_node):
        """Logging a fitness session bumps the shared Streak for the child."""
        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=20,
            measurement_type="counted",
            measurement_value=10,
            measurement_unit="repetitions",
            logged_by=user.id,
        )
        streak_result = await db_session.execute(select(Streak).where(Streak.child_id == child.id))
        streak = streak_result.scalar_one()
        assert streak.current_streak >= 1
        assert streak.last_activity_date is not None


class TestFitnessActivityGovernance:
    """PE activities with activity_type=practice or assessment flow through governance unchanged."""

    @pytest.mark.asyncio
    async def test_activity_context_accepts_practice_type(self):
        """ActivityContext string activity_type field lets fitness activities ride the existing queue."""
        from app.services.governance import ActivityContext

        ctx = ActivityContext(
            household_id=uuid.uuid4(),
            child_id=uuid.uuid4(),
            activity_type="practice",
            node_id=uuid.uuid4(),
            estimated_minutes=30,
        )
        assert ctx.activity_type == "practice"

        assessment_ctx = ActivityContext(
            household_id=uuid.uuid4(),
            child_id=uuid.uuid4(),
            activity_type="assessment",
            node_id=uuid.uuid4(),
            estimated_minutes=20,
        )
        assert assessment_ctx.activity_type == "assessment"
