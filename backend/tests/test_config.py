"""Production-config startup guard tests (METHEAN-6-09).

The ``Settings`` model_validator must refuse to boot when
``APP_ENV`` is ``production`` (or, for a smaller set of checks,
``staging``) and any critical setting still carries a development
default. These tests exercise each check in isolation, confirm the
dev path stays permissive, and verify that all failures are
aggregated into a single error message.
"""

import pytest
from pydantic import ValidationError

from app.core.config import Settings

# Env vars pydantic_settings reads from the OS or ``.env``. Any of
# them can sneak in and pollute test results when running in a real
# shell or container, so we strip them before building each Settings.
_RELEVANT_ENV_VARS = (
    "APP_ENV",
    "APP_DEBUG",
    "DATABASE_URL",
    "DATABASE_URL_SYNC",
    "REDIS_URL",
    "JWT_SECRET",
    "AI_API_KEY",
    "AI_FALLBACK_API_KEY",
    "AI_MOCK_ENABLED",
    "ALLOW_AI_MOCK_IN_PRODUCTION",
    "S3_ACCESS_KEY",
    "S3_SECRET_KEY",
    "STRIPE_SECRET_KEY",
    "STRIPE_WEBHOOK_SECRET",
    "RESEND_API_KEY",
    "APP_URL",
)


def _good_prod_overrides() -> dict:
    """Baseline of prod-grade values that pass every check.

    Tests mutate one field at a time off this baseline so each
    failure test verifies the check it claims to verify.
    """
    return {
        "APP_ENV": "production",
        "DATABASE_URL": "postgresql+asyncpg://methean:s3cret@db.prod.example.com:5432/methean",
        "DATABASE_URL_SYNC": "postgresql://methean:s3cret@db.prod.example.com:5432/methean",
        "REDIS_URL": "redis://cache.prod.example.com:6379/0",
        "JWT_SECRET": "prod-secret-not-default",
        "AI_API_KEY": "sk-ant-live-real-key",
        "S3_ACCESS_KEY": "real-access-key",
        "S3_SECRET_KEY": "real-secret-key",
        "STRIPE_SECRET_KEY": "sk_live_real_stripe_key",
        "STRIPE_WEBHOOK_SECRET": "whsec_real",
        "RESEND_API_KEY": "re_real",
        "APP_URL": "https://methean.app",
    }


@pytest.fixture(autouse=True)
def _clear_env(monkeypatch):
    """Strip any inherited env vars before every test in this module."""
    for key in _RELEVANT_ENV_VARS:
        monkeypatch.delenv(key, raising=False)
    # Also disable .env loading so a developer's local .env can't taint
    # the assertions. Pydantic accepts None to skip env-file loading.
    monkeypatch.setattr(
        Settings,
        "model_config",
        {"env_file": None, "env_file_encoding": "utf-8"},
    )


def _make(**overrides) -> Settings:
    base = {"APP_ENV": "development"}
    return Settings(**(base | overrides))


def _make_prod(**overrides) -> Settings:
    """Build a prod Settings off the good baseline with one mutation."""
    return Settings(**(_good_prod_overrides() | overrides))


# ══════════════════════════════════════════════════════════════════════
# Dev path stays permissive
# ══════════════════════════════════════════════════════════════════════


def test_dev_config_loads_with_defaults():
    s = _make()
    assert s.APP_ENV == "development"
    assert s.is_production is False


# ══════════════════════════════════════════════════════════════════════
# Production rejections — one bad field at a time
# ══════════════════════════════════════════════════════════════════════


def test_prod_config_rejects_dev_database_url():
    with pytest.raises(ValidationError) as exc:
        _make_prod(
            DATABASE_URL="postgresql+asyncpg://methean:methean_dev@postgres:5432/methean"
        )
    assert "DATABASE_URL must not be a development default" in str(exc.value)


def test_prod_config_rejects_localhost_redis():
    with pytest.raises(ValidationError) as exc:
        _make_prod(REDIS_URL="redis://localhost:6379/0")
    assert "REDIS_URL must not point to localhost" in str(exc.value)


def test_prod_config_rejects_minio_s3_credentials():
    with pytest.raises(ValidationError) as exc:
        _make_prod(S3_ACCESS_KEY="minioadmin", S3_SECRET_KEY="minioadmin")
    msg = str(exc.value)
    assert "S3_ACCESS_KEY must not be the minio default" in msg
    assert "S3_SECRET_KEY must not be the minio default" in msg


def test_prod_config_rejects_localhost_app_url():
    with pytest.raises(ValidationError) as exc:
        _make_prod(APP_URL="http://localhost:3000")
    assert "APP_URL must use https://" in str(exc.value)


def test_prod_config_rejects_test_stripe_key():
    with pytest.raises(ValidationError) as exc:
        _make_prod(STRIPE_SECRET_KEY="sk_test_dev_key")
    assert "STRIPE_SECRET_KEY must be a live key" in str(exc.value)


def test_prod_config_rejects_empty_stripe_webhook_secret():
    with pytest.raises(ValidationError) as exc:
        _make_prod(STRIPE_WEBHOOK_SECRET="")
    assert "STRIPE_WEBHOOK_SECRET must be set" in str(exc.value)


def test_prod_config_rejects_empty_ai_api_key():
    with pytest.raises(ValidationError) as exc:
        _make_prod(AI_API_KEY="")
    assert "AI_API_KEY must be set" in str(exc.value)


# ══════════════════════════════════════════════════════════════════════
# Aggregation
# ══════════════════════════════════════════════════════════════════════


def test_prod_config_aggregates_all_failures():
    """A single ValidationError must list every check that failed
    so operators don't have to fix them one at a time.
    """
    bad = _good_prod_overrides() | {
        "DATABASE_URL": "postgresql+asyncpg://methean:methean_dev@postgres:5432/methean",
        "REDIS_URL": "redis://localhost:6379/0",
        "S3_ACCESS_KEY": "minioadmin",
        "STRIPE_SECRET_KEY": "sk_test_dev_key",
        "AI_API_KEY": "",
    }
    with pytest.raises(ValidationError) as exc:
        Settings(**bad)

    msg = str(exc.value)
    expected = [
        "DATABASE_URL must not be a development default",
        "REDIS_URL must not point to localhost",
        "S3_ACCESS_KEY must not be the minio default",
        "STRIPE_SECRET_KEY must be a live key",
        "AI_API_KEY must be set",
    ]
    for fragment in expected:
        assert fragment in msg, f"expected {fragment!r} in aggregated error message"


# ══════════════════════════════════════════════════════════════════════
# Staging is stricter than dev but laxer than prod for S3 + Stripe
# ══════════════════════════════════════════════════════════════════════


def test_staging_allows_minio_but_blocks_database_default():
    """Staging keeps minio S3 (used for fixtures) but refuses dev DB
    defaults — the same as production.
    """
    overrides = _good_prod_overrides() | {
        "APP_ENV": "staging",
        "S3_ACCESS_KEY": "minioadmin",
        "S3_SECRET_KEY": "minioadmin",
        "STRIPE_SECRET_KEY": "sk_test_staging",
        "STRIPE_WEBHOOK_SECRET": "",
        "RESEND_API_KEY": "",
        "DATABASE_URL": "postgresql+asyncpg://methean:methean_dev@postgres:5432/methean",
    }
    with pytest.raises(ValidationError) as exc:
        Settings(**overrides)
    msg = str(exc.value)
    assert "DATABASE_URL must not be a development default" in msg
    # Staging-exempt checks must NOT appear.
    for fragment in (
        "S3_ACCESS_KEY",
        "S3_SECRET_KEY",
        "STRIPE_SECRET_KEY",
        "STRIPE_WEBHOOK_SECRET",
        "RESEND_API_KEY",
    ):
        assert fragment not in msg, f"{fragment} should be exempt in staging"


def test_staging_allows_test_stripe_keys():
    """Staging boots cleanly with minio + sk_test_ Stripe + no Resend."""
    overrides = _good_prod_overrides() | {
        "APP_ENV": "staging",
        "S3_ACCESS_KEY": "minioadmin",
        "S3_SECRET_KEY": "minioadmin",
        "STRIPE_SECRET_KEY": "sk_test_staging",
        "STRIPE_WEBHOOK_SECRET": "",
        "RESEND_API_KEY": "",
    }
    s = Settings(**overrides)
    assert s.APP_ENV == "staging"
    assert s.STRIPE_SECRET_KEY.startswith("sk_test_")
    assert s.S3_ACCESS_KEY == "minioadmin"
