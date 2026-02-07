"""Application configuration settings."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Genomic Analysis Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "change-this-in-production"
    
    # Database
    DATABASE_URL: str = "postgresql://genomics_user:genomics_pass@localhost:5432/genomics_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # NCBI
    NCBI_EMAIL: str
    NCBI_API_KEY: str = ""
    NCBI_RATE_LIMIT: int = 3  # requests per second
    
    # File Storage
    DATA_DIR: str = "./data"
    MAX_GENOME_SIZE_MB: int = 50
    CACHE_TTL_HOURS: int = 24
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
