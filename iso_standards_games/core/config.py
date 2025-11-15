"""Configuration settings for the application."""

from enum import Enum
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    OLLAMA = "ollama"
    AZURE = "azure"


class Settings(BaseSettings):
    """Application settings."""

    # App settings
    APP_NAME: str = "ISO Standards Games"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    DEFAULT_LOCALE: str = "en"
    
    # LLM settings
    LLM_PROVIDER: LLMProvider = LLMProvider.OLLAMA
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen3"
    
    # Azure OpenAI settings (optional)
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_VERSION: str = "2023-05-15"
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-35-turbo"
    
    # Database settings (for storing game progress)
    DATABASE_URL: str = "sqlite:///./iso_standards_games.db"
    
    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()