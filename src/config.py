"""Configuration module for Parent Phone SOS."""

import os
from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # API Configuration
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    PREFERRED_PROVIDER: Literal["openai", "anthropic"] = "openai"
    OPENAI_MODEL: str = "gpt-4o"
    ANTHROPIC_MODEL: str = "claude-opus-4-6"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 3600

    # Image Configuration
    MAX_IMAGE_SIZE_MB: int = 20
    ALLOWED_IMAGE_FORMATS: list = ["jpeg", "jpg", "png", "webp"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
