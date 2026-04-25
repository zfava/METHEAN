"""Application configuration with startup guards."""

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    # Application
    APP_ENV: str = "development"
    APP_DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://methean:methean_dev@postgres:5432/methean"
    DATABASE_URL_SYNC: str = "postgresql://methean:methean_dev@postgres:5432/methean"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # Auth
    JWT_SECRET: str = "CHANGE_ME_IN_PRODUCTION"
    PREVIOUS_JWT_SECRET: str = ""  # For zero-downtime key rotation
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # AI
    AI_API_KEY: str = ""
    AI_FALLBACK_API_KEY: str = ""
    AI_PRIMARY_MODEL: str = "claude-opus-4-6"
    AI_STANDARD_MODEL: str = "claude-sonnet-4-6"
    AI_LIGHT_MODEL: str = "claude-haiku-4-5-20251001"
    AI_FALLBACK_MODEL: str = "gpt-4o-mini"
    # Mock fallback is OFF by default. In production it also requires
    # ALLOW_AI_MOCK_IN_PRODUCTION=true so it can never be flipped on
    # accidentally — see the validator below. ``ALLOW_AI_MOCK_IN_PRODUCTION``
    # must be declared above ``AI_MOCK_ENABLED`` so it's already in
    # ``info.data`` when the validator runs.
    ALLOW_AI_MOCK_IN_PRODUCTION: bool = False
    AI_MOCK_ENABLED: bool = False  # Allow mock fallback when providers unavailable
    AI_MAX_TOKENS: int = 4096
    AI_TEMPERATURE: float = 0.7

    # S3
    S3_ENDPOINT_URL: str = "http://minio:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET_NAME: str = "methean-artifacts"

    # Celery
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    # Email (Resend)
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "METHEAN <notifications@methean.app>"

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_ID: str = ""
    STRIPE_TRIAL_DAYS: int = 14
    APP_URL: str = "http://localhost:3000"

    # Monitoring
    SENTRY_DSN: str = ""  # Empty = disabled

    # Push Notifications (FCM)
    FCM_PROJECT_ID: str = ""
    FCM_SERVICE_ACCOUNT_JSON: str = ""  # Path or inline JSON for service account

    # FSRS / Retention
    FSRS_WEIGHTS: list[float] = []  # Empty = use py-fsrs defaults
    MASTERY_THRESHOLD: float = 0.8  # Confidence threshold to reach mastered
    DECAY_RETRIEVABILITY_THRESHOLD: float = 0.5  # Below this, mastered decays

    # Decay job
    DECAY_CRON_HOUR: int = 2  # 2:00 AM
    DECAY_CRON_MINUTE: int = 0
    DECAY_BATCH_SIZE: int = 500

    @field_validator("JWT_SECRET")
    @classmethod
    def jwt_secret_must_not_be_default_in_prod(cls, v: str, info) -> str:
        env = info.data.get("APP_ENV", "development")
        if env == "production" and v == "CHANGE_ME_IN_PRODUCTION":
            raise ValueError("JWT_SECRET must be changed from default in production. Refusing to boot.")
        return v

    @field_validator("AI_MOCK_ENABLED")
    @classmethod
    def mock_must_be_off_in_production(cls, v: bool, info) -> bool:
        env = info.data.get("APP_ENV", "development")
        allow = info.data.get("ALLOW_AI_MOCK_IN_PRODUCTION", False)
        if env == "production" and v and not allow:
            raise ValueError(
                "AI_MOCK_ENABLED=True in production requires ALLOW_AI_MOCK_IN_PRODUCTION=true. "
                "Refusing to boot."
            )
        return v

    @model_validator(mode="after")
    def _validate_production_defaults(self) -> "Settings":
        """Cross-field guard: refuse to boot prod/staging on dev defaults.

        Staging is treated like production for everything except S3
        credentials (may keep minio for fixtures) and Stripe keys
        (test keys allowed). Failures are aggregated so operators see
        the full punch list at once instead of fixing them one at a
        time.
        """
        if self.APP_ENV not in ("production", "staging"):
            return self

        failures: list[str] = []
        is_prod = self.APP_ENV == "production"

        # Both prod and staging
        if "methean_dev" in self.DATABASE_URL or "localhost" in self.DATABASE_URL:
            failures.append("DATABASE_URL must not be a development default")
        if "methean_dev" in self.DATABASE_URL_SYNC or "localhost" in self.DATABASE_URL_SYNC:
            failures.append("DATABASE_URL_SYNC must not be a development default")
        if "localhost" in self.REDIS_URL:
            failures.append("REDIS_URL must not point to localhost")
        if self.APP_URL.startswith("http://"):
            failures.append("APP_URL must use https://")
        if not self.AI_API_KEY:
            failures.append("AI_API_KEY must be set")

        # Prod only
        if is_prod:
            if self.S3_ACCESS_KEY == "minioadmin":
                failures.append("S3_ACCESS_KEY must not be the minio default")
            if self.S3_SECRET_KEY == "minioadmin":
                failures.append("S3_SECRET_KEY must not be the minio default")
            if not self.STRIPE_SECRET_KEY or self.STRIPE_SECRET_KEY.startswith("sk_test_"):
                failures.append("STRIPE_SECRET_KEY must be a live key")
            if not self.STRIPE_WEBHOOK_SECRET:
                failures.append("STRIPE_WEBHOOK_SECRET must be set")
            if not self.RESEND_API_KEY:
                failures.append("RESEND_API_KEY must be set")

        if failures:
            bullets = "\n  - ".join(failures)
            raise ValueError(f"Production startup blocked. Failed checks:\n  - {bullets}")

        return self

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


settings = Settings()
