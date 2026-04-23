"""Comprehensive tests for the fitness system.

Covers:
- Curriculum templates: registration, progression, content schema.
- Service layer: logging, node state updates, benchmarks, progress, trends.
- Compliance integration: PE hours land under Physical Fitness subject.
- HTTP API: 201s on create, GETs on read, auth enforcement, household isolation.
"""

from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy import select

from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import NodeType
from app.models.fitness import FitnessBenchmark, FitnessLog
from app.models.identity import Child, Household
from app.models.state import ChildNodeState
from app.services.compliance_engine import get_hours_breakdown
from app.services.fitness_service import (
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
