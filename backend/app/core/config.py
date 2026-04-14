"""Application configuration with startup guards."""

from pydantic import field_validator
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
    AI_PRIMARY_MODEL: str = "claude-sonnet-4-20250514"
    AI_FALLBACK_MODEL: str = "gpt-4o-mini"
    AI_MOCK_ENABLED: bool = True  # Allow mock fallback when providers unavailable
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

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


settings = Settings()
