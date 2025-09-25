from pydantic import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True

    # Database Configuration
    database_url: str = "sqlite:///./issues.db"
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # CORS Configuration
    cors_origins: List[str] = ["http://localhost:4200"]

    # Security Configuration
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
