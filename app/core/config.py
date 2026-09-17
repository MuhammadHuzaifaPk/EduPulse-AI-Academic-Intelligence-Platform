from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application Config
    APP_NAME: str = "EduPulse AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # API Keys & Authentication
    GEMINI_API_KEY: str
    HF_TOKEN: str = ""

    # AI Model Configuration
    GEMINI_MODEL_NAME: str = "gemini-2.5-flash"
    HF_SUMMARIZATION_MODEL: str = "facebook/bart-large-cnn"
    HF_CLASSIFICATION_MODEL: str = "distilbert-base-uncased-finetuned-sst-2-english"

    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]

    # Pydantic Settings Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignores unknown .env variables instead of throwing ValidationError
        case_sensitive=True
    )

settings = Settings()