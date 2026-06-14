"""Tests for the local-inference provider and its place in the chain.

The local provider runs an open-weight model on the family's own
hardware via an OpenAI-compatible endpoint. It slots into the gateway
chain behind the exact same contract Claude and OpenAI use, so
governance, provenance, and cost controls apply unchanged. These tests
prove:

* the provider maps a successful OpenAI-compatible response into the
  chain's expected object;
* every failure mode (unreachable, timeout, malformed) raises the
  provider-unavailable signal, logs a structured warning with the
  failure kind only, never hangs, and lets the chain fall through;
* provenance: a local run records provider=local on the AIRun;
* cost: a local run records $0 and never counts toward the spend cap,
  so a household at its cap can still use local;
* governance parity: a local-answered call has the same run shape as a
  Claude-answered one, differing only in provenance;
* the chain ordering honors PROVIDER_CHAIN and LOCAL_AI_ENABLED, and an
  all-external-disabled config resolves to LOCAL then NATIVE;
* the health probe reports reachable/model/latency and never throws.
"""

import httpx
import pytest
from sqlalchemy import select
from structlog.testing import capture_logs

from app.ai.gateway import AIProvider, AIRole, _get_provider_chain, call_ai
from app.ai.providers import LocalProviderError, call_local, probe_local
from app.core.config import settings
from app.models.enums import AIRunStatus
from app.models.operational import AIRun

# ---------------------------------------------------------------------------
# httpx mocking helpers
# ---------------------------------------------------------------------------


def _patch_httpx(monkeypatch, handler, captured: dict | None = None):
    """Route the provider's httpx client through a MockTransport.

    ``handler`` is a callable taking an httpx.Request and returning an
    httpx.Response (or raising an httpx error to simulate transport
    failure). When ``captured`` is given, the timeout passed to the
    client is recorded under ``captured["timeout"]``.
    """
    real_client = httpx.AsyncClient

    def factory(*args, **kwargs):
        if captured is not None:
            captured["timeout"] = kwargs.get("timeout")
        kwargs["transport"] = httpx.MockTransport(handler)
        return real_client(*args, **kwargs)

    monkeypatch.setattr("app.ai.providers.local.httpx.AsyncClient", factory)


def _ok_chat_response(request: httpx.Request) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "model": "llama3.1:8b",
            "choices": [{"message": {"role": "assistant", "content": '{"message": "hello from local"}'}}],
            "usage": {"prompt_tokens": 11, "completion_tokens": 22},
        },
    )


# ---------------------------------------------------------------------------
# Provider unit tests: response mapping and failure modes
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestCallLocal:
    async def test_success_maps_response(self, monkeypatch):
        """A successful endpoint maps into the chain's expected object."""
        _patch_httpx(monkeypatch, _ok_chat_response)
        result = await call_local("sys", "user", 256)
        assert result["content"] == '{"message": "hello from local"}'
        assert result["model"] == "llama3.1:8b"
        assert result["input_tokens"] == 11
        assert result["output_tokens"] == 22

    async def test_unreachable_raises_and_logs(self, monkeypatch):
        """Connection refused raises LocalProviderError, logs failure kind."""

        def refuse(request):
            raise httpx.ConnectError("connection refused")

        _patch_httpx(monkeypatch, refuse)
        with capture_logs() as logs, pytest.raises(LocalProviderError):
            await call_local("sys", "user", 256)
        warnings = [log for log in logs if log["event"] == "local_provider_call_failed"]
        assert warnings and warnings[0]["failure_kind"] == "unreachable"
        # The prompt content must never appear in the log record.
        assert all("user" not in str(v) for log in warnings for v in log.values())

    async def test_timeout_raises_with_timeout_kind(self, monkeypatch):
        """A slow endpoint that times out aborts as a LocalProviderError."""

        def slow(request):
            raise httpx.ReadTimeout("timed out")

        _patch_httpx(monkeypatch, slow)
        with capture_logs() as logs, pytest.raises(LocalProviderError):
            await call_local("sys", "user", 256)
        assert any(log.get("failure_kind") == "timeout" for log in logs)

    async def test_configured_timeout_is_passed_to_client(self, monkeypatch):
        """The provider enforces LOCAL_AI_TIMEOUT_SECONDS on the client."""
        captured: dict = {}
        _patch_httpx(monkeypatch, _ok_chat_response, captured=captured)
        monkeypatch.setattr(settings, "LOCAL_AI_TIMEOUT_SECONDS", 7.5)
        await call_local("sys", "user", 256)
        assert captured["timeout"] == 7.5
        # An explicit override wins over the setting.
        await call_local("sys", "user", 256, timeout=3.0)
        assert captured["timeout"] == 3.0

    async def test_malformed_json_fails_gracefully(self, monkeypatch):
        """A body that is not JSON fails gracefully and signals fallthrough."""

        def bad_json(request):
            return httpx.Response(200, content=b"this is not json", headers={"content-type": "application/json"})

        _patch_httpx(monkeypatch, bad_json)
        with pytest.raises(LocalProviderError):
            await call_local("sys", "user", 256)

    async def test_missing_choices_fails_gracefully(self, monkeypatch):
        """Valid JSON in the wrong shape fails gracefully."""

        def wrong_shape(request):
            return httpx.Response(200, json={"unexpected": True})

        _patch_httpx(monkeypatch, wrong_shape)
        with capture_logs() as logs, pytest.raises(LocalProviderError):
            await call_local("sys", "user", 256)
        assert any(log.get("failure_kind") == "malformed_response" for log in logs)

    async def test_http_error_status_fails_gracefully(self, monkeypatch):
        """A 500 from the endpoint raises and falls through."""

        def server_error(request):
            return httpx.Response(500, json={"error": "boom"})

        _patch_httpx(monkeypatch, server_error)
        with pytest.raises(LocalProviderError):
            await call_local("sys", "user", 256)


# ---------------------------------------------------------------------------
# Health probe
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestProbeLocal:
    async def test_probe_success(self, monkeypatch):
        """On success the probe reports reachable, model, and latency."""
        _patch_httpx(monkeypatch, _ok_chat_response)
        result = await probe_local()
        assert result["reachable"] is True
        assert result["model"] == "llama3.1:8b"
        assert isinstance(result["latency_ms"], float)
        assert result["latency_ms"] >= 0

    async def test_probe_failure_never_throws(self, monkeypatch):
        """On failure the probe returns reachable False, never raises."""

        def refuse(request):
            raise httpx.ConnectError("connection refused")

        _patch_httpx(monkeypatch, refuse)
        result = await probe_local()
        assert result == {"reachable": False, "model": None, "latency_ms": None}


# ---------------------------------------------------------------------------
# Chain ordering
# ---------------------------------------------------------------------------


class TestProviderChain:
    def test_local_absent_when_disabled(self, monkeypatch):
        """LOCAL_AI_ENABLED false keeps LOCAL out of the chain entirely."""
        monkeypatch.setattr(settings, "LOCAL_AI_ENABLED", False)
        monkeypatch.setattr(settings, "PROVIDER_CHAIN", "")
        monkeypatch.setattr(settings, "AI_API_KEY", "sk-test")
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", True)
        chain = _get_provider_chain()
        assert AIProvider.local not in chain
        # Historical ordering is unchanged.
        assert chain == [AIProvider.claude, AIProvider.native, AIProvider.mock]

    def test_local_first_by_default_when_enabled(self, monkeypatch):
        """With LOCAL enabled and no explicit chain, LOCAL leads."""
        monkeypatch.setattr(settings, "LOCAL_AI_ENABLED", True)
        monkeypatch.setattr(settings, "PROVIDER_CHAIN", "")
        monkeypatch.setattr(settings, "AI_API_KEY", "sk-test")
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "sk-fallback")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", True)
        chain = _get_provider_chain()
        assert chain == [
            AIProvider.local,
            AIProvider.claude,
            AIProvider.openai,
            AIProvider.native,
            AIProvider.mock,
        ]

    def test_explicit_provider_chain_parses_and_orders(self, monkeypatch):
        """PROVIDER_CHAIN parses to the requested order, skipping the absent."""
        monkeypatch.setattr(settings, "LOCAL_AI_ENABLED", True)
        monkeypatch.setattr(settings, "PROVIDER_CHAIN", "local, claude , native")
        monkeypatch.setattr(settings, "AI_API_KEY", "sk-test")
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)
        chain = _get_provider_chain()
        assert chain == [AIProvider.local, AIProvider.claude, AIProvider.native]

    def test_all_external_disabled_resolves_local_then_native(self, monkeypatch):
        """No external keys, LOCAL on: the chain is LOCAL then NATIVE."""
        monkeypatch.setattr(settings, "LOCAL_AI_ENABLED", True)
        monkeypatch.setattr(settings, "PROVIDER_CHAIN", "")
        monkeypatch.setattr(settings, "AI_API_KEY", "")
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)
        chain = _get_provider_chain()
        assert chain == [AIProvider.local, AIProvider.native]

    def test_native_floor_guaranteed_even_if_omitted(self, monkeypatch):
        """An explicit chain that omits native still gets the native floor."""
        monkeypatch.setattr(settings, "LOCAL_AI_ENABLED", True)
        monkeypatch.setattr(settings, "PROVIDER_CHAIN", "local")
        monkeypatch.setattr(settings, "AI_API_KEY", "")
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)
        chain = _get_provider_chain()
        assert chain == [AIProvider.local, AIProvider.native]


# ---------------------------------------------------------------------------
# Gateway integration: provenance, fallthrough, cost, parity
# ---------------------------------------------------------------------------


def _local_only(monkeypatch):
    """Configure settings so the chain is LOCAL then NATIVE."""
    monkeypatch.setattr(settings, "LOCAL_AI_ENABLED", True)
    monkeypatch.setattr(settings, "PROVIDER_CHAIN", "")
    monkeypatch.setattr(settings, "AI_API_KEY", "")
    monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
    monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)


async def _fetch_run(db_session, ai_run_id) -> AIRun:
    return (await db_session.execute(select(AIRun).where(AIRun.id == ai_run_id))).scalar_one()


@pytest.mark.asyncio
class TestGatewayLocalIntegration:
    async def test_local_success_records_provenance(self, db_session, household, user, monkeypatch):
        """A successful local run answers and records provider=local."""
        _local_only(monkeypatch)

        async def fake_local(system_prompt, user_prompt, max_tokens):
            return {
                "content": '{"message": "hi"}',
                "model": "llama3.1:8b",
                "input_tokens": 12,
                "output_tokens": 34,
            }

        monkeypatch.setattr("app.ai.gateway._call_local", fake_local)

        result = await call_ai(
            db_session,
            AIRole.tutor,
            "system",
            "user",
            household_id=household.id,
        )
        assert result["provider"] == "local"
        assert result["is_mock"] is False

        run = await _fetch_run(db_session, result["ai_run_id"])
        assert run.provider == "local"
        assert run.model_used == "llama3.1:8b"
        assert run.status == AIRunStatus.completed

    async def test_unreachable_falls_through_and_logs_warning(self, db_session, household, user, monkeypatch):
        """An unreachable endpoint does not hang, logs a warning, and the
        chain falls through to the next provider rather than crashing."""
        monkeypatch.setattr(settings, "LOCAL_AI_ENABLED", True)
        monkeypatch.setattr(settings, "PROVIDER_CHAIN", "")
        monkeypatch.setattr(settings, "AI_API_KEY", "")
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", True)  # mock is the floor here

        def refuse(request):
            raise httpx.ConnectError("connection refused")

        _patch_httpx(monkeypatch, refuse)

        with capture_logs() as logs:
            result = await call_ai(
                db_session,
                AIRole.tutor,
                "system",
                "user",
                household_id=household.id,
            )
        # Request completed via a later provider, never local.
        assert result["provider"] != "local"
        assert result["provider"] in {"native", "mock"}
        # The provider layer logged a structured warning with the kind only.
        assert any(log.get("event") == "local_provider_call_failed" for log in logs)

    async def test_falls_to_native_when_local_unreachable(self, db_session, household, user, monkeypatch):
        """Independence proof: external disabled, LOCAL unreachable, NATIVE
        answers and the request still completes (no external AI, no crash)."""
        _local_only(monkeypatch)

        async def boom(system_prompt, user_prompt, max_tokens):
            raise LocalProviderError("local provider unreachable")

        async def fake_native(db, household_id, role, user_prompt, philosophical_profile):
            return {"message": "served by the native floor"}

        monkeypatch.setattr("app.ai.gateway._call_local", boom)
        monkeypatch.setattr(
            "app.services.native_curriculum_generator.build_native_response",
            fake_native,
        )

        result = await call_ai(
            db_session,
            AIRole.tutor,
            "system",
            "user",
            household_id=household.id,
        )
        assert result["provider"] == "native"
        run = await _fetch_run(db_session, result["ai_run_id"])
        assert run.provider == "native"

    async def test_local_run_costs_zero_and_does_not_decrement_budget(self, db_session, household, user, monkeypatch):
        """A local run records $0 and does not count toward the spend cap."""
        from app.ai.cost_controls import get_daily_usage

        _local_only(monkeypatch)

        async def fake_local(system_prompt, user_prompt, max_tokens):
            return {
                "content": '{"message": "hi"}',
                "model": "llama3.1:8b",
                "input_tokens": 5000,
                "output_tokens": 9000,
            }

        monkeypatch.setattr("app.ai.gateway._call_local", fake_local)

        result = await call_ai(
            db_session,
            AIRole.tutor,
            "system",
            "user",
            household_id=household.id,
        )
        run = await _fetch_run(db_session, result["ai_run_id"])
        assert run.cost_usd == 0.0
        # Local tokens are excluded from the daily spend accounting.
        usage = await get_daily_usage(db_session, household.id)
        assert usage["total_tokens"] == 0
        assert usage["total_cost_cents"] == 0

    async def test_household_at_cap_can_still_use_local(self, db_session, household, user, monkeypatch):
        """A household whose budget gate would block can still use local."""
        _local_only(monkeypatch)

        async def fake_local(system_prompt, user_prompt, max_tokens):
            return {"content": '{"message": "hi"}', "model": "llama3.1:8b", "input_tokens": 1, "output_tokens": 1}

        async def blocked_budget(*args, **kwargs):
            # Simulate a household over its hard spend cap (block mode).
            return {"allowed": False, "should_degrade": False, "should_alert": True, "usage": {}, "budget": {}}

        monkeypatch.setattr("app.ai.gateway._call_local", fake_local)
        monkeypatch.setattr("app.ai.cost_controls.check_budget", blocked_budget)

        # Even though the budget reports not-allowed, local leads the chain
        # (free primary) so the gate is skipped and the request completes.
        result = await call_ai(
            db_session,
            AIRole.tutor,
            "system",
            "user",
            household_id=household.id,
        )
        assert result["provider"] == "local"

    async def test_over_cap_local_down_never_falls_through_to_paid(self, db_session, household, user, monkeypatch):
        """Over-cap household, LOCAL first but down, paid keys configured:
        the chain must not call a paid provider; the free floor serves."""
        monkeypatch.setattr(settings, "LOCAL_AI_ENABLED", True)
        monkeypatch.setattr(settings, "PROVIDER_CHAIN", "")
        monkeypatch.setattr(settings, "AI_API_KEY", "sk-test")  # paid configured
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", True)  # mock is the free floor

        async def local_down(system_prompt, user_prompt, max_tokens):
            raise LocalProviderError("local down")

        claude_calls = {"n": 0}

        async def spy_claude(system_prompt, user_prompt, max_tokens, model=None):
            claude_calls["n"] += 1
            return {"content": '{"m": "x"}', "model": "claude-x", "input_tokens": 1, "output_tokens": 1}

        async def blocked_budget(*args, **kwargs):
            return {"allowed": False, "should_degrade": False, "should_alert": True, "usage": {}, "budget": {}}

        monkeypatch.setattr("app.ai.gateway._call_local", local_down)
        monkeypatch.setattr("app.ai.gateway._call_claude", spy_claude)
        monkeypatch.setattr("app.ai.cost_controls.check_budget", blocked_budget)

        result = await call_ai(db_session, AIRole.tutor, "system", "user", household_id=household.id)
        # The paid provider was never called while over the cap.
        assert claude_calls["n"] == 0
        assert result["provider"] not in {"anthropic", "openai"}
        # The free floor (mock here) served instead.
        assert result["provider"] == "mock"

    async def test_over_cap_local_down_no_free_answer_raises_limit(self, db_session, household, user, monkeypatch):
        """Over-cap, LOCAL down, paid configured, no free floor for the role:
        raise the usage-limit error rather than billing a paid run."""
        monkeypatch.setattr(settings, "LOCAL_AI_ENABLED", True)
        monkeypatch.setattr(settings, "PROVIDER_CHAIN", "")
        monkeypatch.setattr(settings, "AI_API_KEY", "sk-test")  # paid configured
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)  # no mock floor

        from app.services.usage import UsageLimitExceededError

        async def local_down(system_prompt, user_prompt, max_tokens):
            raise LocalProviderError("local down")

        claude_calls = {"n": 0}

        async def spy_claude(system_prompt, user_prompt, max_tokens, model=None):
            claude_calls["n"] += 1
            return {"content": '{"m": "x"}', "model": "claude-x", "input_tokens": 1, "output_tokens": 1}

        async def blocked_budget(*args, **kwargs):
            return {"allowed": False, "should_degrade": False, "should_alert": True, "usage": {}, "budget": {}}

        monkeypatch.setattr("app.ai.gateway._call_local", local_down)
        monkeypatch.setattr("app.ai.gateway._call_claude", spy_claude)
        monkeypatch.setattr("app.ai.cost_controls.check_budget", blocked_budget)

        # Native returns None for the tutor role and mock is off, so no free
        # provider can answer; the cap must surface, paid must not be called.
        with pytest.raises(UsageLimitExceededError):
            await call_ai(db_session, AIRole.tutor, "system", "user", household_id=household.id)
        assert claude_calls["n"] == 0

    async def test_budget_gate_still_blocks_when_paid_provider_leads(self, db_session, household, user, monkeypatch):
        """Control: with a paid provider leading, the cap is still enforced."""
        from app.services.usage import UsageLimitExceededError

        monkeypatch.setattr(settings, "LOCAL_AI_ENABLED", False)
        monkeypatch.setattr(settings, "PROVIDER_CHAIN", "")
        monkeypatch.setattr(settings, "AI_API_KEY", "sk-test")
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", True)

        async def blocked_budget(*args, **kwargs):
            return {"allowed": False, "should_degrade": False, "should_alert": True, "usage": {}, "budget": {}}

        monkeypatch.setattr("app.ai.cost_controls.check_budget", blocked_budget)

        with pytest.raises(UsageLimitExceededError):
            await call_ai(
                db_session,
                AIRole.tutor,
                "system",
                "user",
                household_id=household.id,
            )

    async def test_governance_parity_local_vs_claude(self, db_session, household, user, monkeypatch):
        """A local-answered run has the same shape as a Claude-answered one,
        differing only in provenance (provider and model)."""

        async def fake_claude(system_prompt, user_prompt, max_tokens, model=None):
            return {"content": '{"message": "hi"}', "model": "claude-x", "input_tokens": 5, "output_tokens": 7}

        async def fake_local(system_prompt, user_prompt, max_tokens):
            return {"content": '{"message": "hi"}', "model": "llama3.1:8b", "input_tokens": 5, "output_tokens": 7}

        # Run A: Claude answers.
        monkeypatch.setattr(settings, "LOCAL_AI_ENABLED", False)
        monkeypatch.setattr(settings, "PROVIDER_CHAIN", "")
        monkeypatch.setattr(settings, "AI_API_KEY", "sk-test")
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)
        monkeypatch.setattr("app.ai.gateway._call_claude", fake_claude)
        result_claude = await call_ai(db_session, AIRole.tutor, "system", "user", household_id=household.id)
        run_claude = await _fetch_run(db_session, result_claude["ai_run_id"])

        # Run B: local answers.
        _local_only(monkeypatch)
        monkeypatch.setattr("app.ai.gateway._call_local", fake_local)
        result_local = await call_ai(db_session, AIRole.tutor, "system", "user", household_id=household.id)
        run_local = await _fetch_run(db_session, result_local["ai_run_id"])

        # Same response envelope keys.
        assert set(result_claude.keys()) == set(result_local.keys())
        # Same run-record shape and status; same input/output structure.
        assert run_claude.run_type == run_local.run_type
        assert run_claude.status == run_local.status
        assert set(run_claude.input_data.keys()) == set(run_local.input_data.keys())
        assert isinstance(run_claude.output_data, dict) and isinstance(run_local.output_data, dict)
        # The only provenance difference.
        assert run_claude.provider == "anthropic"
        assert run_local.provider == "local"
        assert result_claude["provider"] != result_local["provider"]
