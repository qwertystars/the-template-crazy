"""
Application configuration management.
Uses pydantic-settings for environment variable validation.
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "FlexiBase"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://flexibase_user:flexibase_password@localhost:5432/flexibase_db"
    )
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # Security
    SECRET_KEY: str = Field(default="change-me-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_origins(cls, v: str) -> List[str]:
        """Parse comma-separated CORS origins."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # Email
    EMAIL_ENABLED: bool = False
    SENDGRID_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@flexibase.com"
    FROM_NAME: str = "FlexiBase"

    # Payment
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "./uploads"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Global settings instance
settings = Settings()
