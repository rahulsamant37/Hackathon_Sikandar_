import os
from typing import List, Optional

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = "AI Learning Platform"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Frontend local development
        "https://your-production-frontend-domain.com",
    ]

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-development")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    # AI Model
    AI_MODEL_NAME: str = os.getenv("AI_MODEL_NAME", "google/flan-t5-base")
    AI_MODEL_TEMPERATURE: float = float(os.getenv("AI_MODEL_TEMPERATURE", "0.7"))
    AI_MAX_TOKENS: int = int(os.getenv("AI_MAX_TOKENS", "1000"))

    # Database
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

    # Testing
    TEST_SUPABASE_URL: Optional[str] = os.getenv("TEST_SUPABASE_URL")
    TEST_SUPABASE_KEY: Optional[str] = os.getenv("TEST_SUPABASE_KEY")
    TEST_USER_EMAIL: Optional[str] = os.getenv("TEST_USER_EMAIL")
    TEST_USER_PASSWORD: Optional[str] = os.getenv("TEST_USER_PASSWORD")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Email
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_PORT: Optional[int] = int(os.getenv("SMTP_PORT", "587")) if os.getenv("SMTP_PORT") else None
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    EMAIL_FROM: Optional[str] = os.getenv("EMAIL_FROM")

    # Redis
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")

    # Storage
    STORAGE_BUCKET: Optional[str] = os.getenv("STORAGE_BUCKET")

    # Frontend URL
    FRONTEND_URL: str = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:3000").replace("/api/v1", "")

    # Analytics
    ANALYTICS_ENABLED: bool = os.getenv("ANALYTICS_ENABLED", "true").lower() == "true"

    class Config:
        case_sensitive = True

settings = Settings()
