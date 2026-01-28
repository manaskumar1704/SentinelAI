"""
SentinelAI Backend Configuration

Loads environment variables and provides typed configuration.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    # Clerk Authentication
    clerk_publishable_key: str = ""
    clerk_secret_key: str = ""
    
    # Groq AI
    groq_api_key: str = ""
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # University API
    university_api_url: str = "http://universities.hipolabs.com"
    
    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

