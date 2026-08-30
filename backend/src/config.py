"""
Project ORCA Configuration & Environment Settings
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Project ORCA — Agentic Marine Intelligence"
    API_V1_STR: str = "/v1"
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    
    # Provenance & Safety Constraints
    MIN_EVIDENCE_CONFIDENCE_THRESHOLD: float = 0.65
    HIGH_CONFIDENCE_THRESHOLD: float = 0.80
    STRICT_PROVENANCE_REQUIRED: bool = True
    
    # Feature Flags
    FLAG_PFZ_LIVE_RECOMPUTATION: bool = True
    FLAG_CONVERSATIONAL_ADVISORY: bool = True
    FLAG_SAFE_MODE: bool = False
    
    # Default Database / Cache URLs
    DATABASE_URL: str = "postgresql://orca_user:orca_password@localhost:5432/orca_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    S3_ENDPOINT: str = "http://localhost:9000"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]

settings = Settings()
