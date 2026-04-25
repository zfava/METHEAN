"""Tests for the AI gateway's mock-fallback policy and 503 handling.

The gateway:

* refuses to silently mock in production unless explicitly allowed
* raises ``AIProviderUnavailableError`` when real providers fail and
  mock fallback is disabled
* always tags responses with ``provider``, ``is_mock``, ``degraded``

The FastAPI app translates ``AIProviderUnavailableError`` into HTTP
503 with a structured body and ``Retry-After`` header.
"""

import logging
import uuid

import pytest
from pydantic import ValidationError

from app.ai.gateway import AIProviderUnavailableError, AIRole, call_ai
from app.core.config import Settings, settings

# ══════════════════════════════════════════════════════════════════════
# Settings validator
# ══════════════════════════════════════════════════════════════════════


class TestSettingsValidator:
    def test_settings_refuse_to_load_with_prod_mock_no_override(self, monkeypatch):
        """Settings(APP_ENV=production, AI_MOCK_ENABLED=True) without
        the explicit override env must fail validation at boot time.
        """
        for key in (
            "APP_ENV",
            "AI_MOCK_ENABLED",
            "ALLOW_AI_MOCK_IN_PRODUCTION",
            "JWT_SECRET",
        ):
            monkeypatch.delenv(key, raising=False)
        monkeypatch.setenv("APP_ENV", "production")
        monkeypatch.setenv("AI_MOCK_ENABLED", "true")
        monkeypatch.setenv("JWT_SECRET", "test-prod-secret-not-default")

        with pytest.raises(ValidationError) as exc:
            Settings()
        assert "ALLOW_AI_MOCK_IN_PRODUCTION" in str(exc.value)

    def test_settings_load_with_prod_mock_and_override(self, monkeypatch):
        for key in (
            "APP_ENV",
            "AI_MOCK_ENABLED",
            "ALLOW_AI_MOCK_IN_PRODUCTION",
            "JWT_SECRET",
        ):
            monkeypatch.delenv(key, raising=False)
        monkeypatch.setenv("APP_ENV", "production")
        monkeypatch.setenv("AI_MOCK_ENABLED", "true")
        monkeypatch.setenv("ALLOW_AI_MOCK_IN_PRODUCTION", "true")
        monkeypatch.setenv("JWT_SECRET", "test-prod-secret-not-default")

        s = Settings()
        assert s.AI_MOCK_ENABLED is True
        assert s.ALLOW_AI_MOCK_IN_PRODUCTION is True


# ══════════════════════════════════════════════════════════════════════
# Gateway behaviour
# ══════════════════════════════════════════════════════════════════════


class TestGatewayMockFallback:
    @pytest.mark.asyncio
    async def test_ai_gateway_in_dev_falls_back_to_mock_with_warning_log(
        self, db_session, household, user, monkeypatch, caplog
    ):
        """In dev with no real provider keys, the gateway must hit the
        mock branch AND emit a WARNING log so degraded responses are
        visible.
        """
        monkeypatch.setattr(settings, "AI_API_KEY", "")
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", True)

        with caplog.at_level(logging.WARNING, logger="methean.ai.gateway"):
            result = await call_ai(
                db_session,
                role=AIRole.planner,
                system_prompt="test",
                user_prompt="test",
                household_id=household.id,
                triggered_by=user.id,
            )

        assert result["is_mock"] is True
        assert result["degraded"] is True
        assert result["provider"] == "mock"

        warnings = [
            r
            for r in caplog.records
            if r.levelno >= logging.WARNING and "mock_fallback_used" in r.message
        ]
        assert warnings, "expected at least one mock_fallback_used WARNING record"

    @pytest.mark.asyncio
    async def test_ai_gateway_in_prod_raises_provider_unavailable(
        self, db_session, household, user, monkeypatch
    ):
        """When mock is disabled and no real providers are configured,
        the gateway raises AIProviderUnavailableError instead of
        silently returning canned content.
        """
        monkeypatch.setattr(settings, "AI_API_KEY", "")
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)

        with pytest.raises(AIProviderUnavailableError) as exc:
            await call_ai(
                db_session,
                role=AIRole.planner,
                system_prompt="test",
                user_prompt="test",
                household_id=household.id,
                triggered_by=user.id,
            )
        assert exc.value.retry_after_seconds == 60

    @pytest.mark.asyncio
    async def test_ai_gateway_in_prod_with_explicit_override_falls_back_to_mock(
        self, db_session, household, user, monkeypatch
    ):
        """ALLOW_AI_MOCK_IN_PRODUCTION + AI_MOCK_ENABLED=True keeps
        the mock branch reachable.
        """
        monkeypatch.setattr(settings, "AI_API_KEY", "")
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", True)
        monkeypatch.setattr(settings, "ALLOW_AI_MOCK_IN_PRODUCTION", True)
        monkeypatch.setattr(settings, "APP_ENV", "production")

        result = await call_ai(
            db_session,
            role=AIRole.planner,
            system_prompt="test",
            user_prompt="test",
            household_id=household.id,
            triggered_by=user.id,
        )
        assert result["is_mock"] is True
        assert result["provider"] == "mock"

    @pytest.mark.asyncio
    async def test_ai_response_includes_provider_field(
        self, db_session, household, user, monkeypatch
    ):
        """Every gateway response — mock or real — exposes
        ``provider``, ``is_mock``, ``degraded``.
        """
        monkeypatch.setattr(settings, "AI_API_KEY", "")
        monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
        monkeypatch.setattr(settings, "AI_MOCK_ENABLED", True)

        result = await call_ai(
            db_session,
            role=AIRole.planner,
            system_prompt="test",
            user_prompt="test",
            household_id=household.id,
            triggered_by=user.id,
        )
        for key in ("provider", "is_mock", "degraded"):
            assert key in result, f"gateway response missing {key}"
        assert result["provider"] in {"anthropic", "openai", "mock"}
        assert isinstance(result["is_mock"], bool)
        assert isinstance(result["degraded"], bool)
        assert result["degraded"] == result["is_mock"]


# ══════════════════════════════════════════════════════════════════════
# 503 handler integration
# ══════════════════════════════════════════════════════════════════════


class TestAIUnavailableHandler:
    @pytest.mark.asyncio
    async def test_api_returns_503_with_structured_body_on_ai_unavailable(
        self, auth_client, db_session, household, child, monkeypatch
    ):
        """When call_ai raises AIProviderUnavailableError, the
        registered FastAPI handler returns 503 with a structured body
        and a Retry-After header.
        """
        from app.api import spec_coverage

        async def _explode(*_args, **_kwargs):
            raise AIProviderUnavailableError(retry_after_seconds=42)

        monkeypatch.setattr(spec_coverage, "call_ai", _explode)

        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/counterfactual",
            json={"changes": {"daily_minutes": 45}},
        )
        assert resp.status_code == 503
        assert resp.json() == {
            "error": "ai_unavailable",
            "message": "AI services are temporarily unavailable. Your request was not processed.",
            "retry_after_seconds": 42,
        }
        assert resp.headers.get("Retry-After") == "42"

    def test_unavailable_error_default_retry_after(self):
        """The default retry_after_seconds is 60 when not specified."""
        exc = AIProviderUnavailableError()
        assert exc.retry_after_seconds == 60
        assert "All AI providers unavailable" in str(exc)


# ══════════════════════════════════════════════════════════════════════
# Default config sanity
# ══════════════════════════════════════════════════════════════════════


class TestDefaultConfig:
    def test_default_app_env_dev_has_ai_mock_disabled(self, monkeypatch):
        """A vanilla Settings() defaults AI_MOCK_ENABLED to False."""
        for key in (
            "APP_ENV",
            "AI_MOCK_ENABLED",
            "ALLOW_AI_MOCK_IN_PRODUCTION",
            "JWT_SECRET",
        ):
            monkeypatch.delenv(key, raising=False)

        s = Settings()
        assert s.APP_ENV == "development"
        assert s.AI_MOCK_ENABLED is False
        assert s.ALLOW_AI_MOCK_IN_PRODUCTION is False


_ = uuid  # static-analysis silence — uuid stays imported for future use
