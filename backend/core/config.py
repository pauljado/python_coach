"""Configuration settings for the FastAPI backend."""

from pathlib import Path


class Settings:
    """Application settings."""
    
    # API Settings
    API_V1_PREFIX = "/api"
    
    # CORS Settings
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    PROBLEMS_DIR = PROJECT_ROOT / "problems"


settings = Settings()
