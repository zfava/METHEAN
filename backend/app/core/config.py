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
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # AI
    AI_API_KEY: str = ""
    AI_FALLBACK_API_KEY: str = ""

    # S3
    S3_ENDPOINT_URL: str = "http://minio:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET_NAME: str = "methean-artifacts"

    # Celery
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    @field_validator("JWT_SECRET")
    @classmethod
    def jwt_secret_must_not_be_default_in_prod(cls, v: str, info) -> str:
        env = info.data.get("APP_ENV", "development")
        if env == "production" and v == "CHANGE_ME_IN_PRODUCTION":
            raise ValueError(
                "JWT_SECRET must be changed from default in production. "
                "Refusing to boot."
            )
        return v

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


settings = Settings()
