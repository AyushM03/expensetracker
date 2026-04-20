from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    APP_NAME: str = "ExpenseTracker API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    MONGODB_URL: str = "mongodb://mongo:27017"
    DATABASE_NAME: str = "expensetracker"

    SECRET_KEY: str = "changeme-in-production-use-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    REDIS_URL: str = "redis://redis:6379"

    ANTHROPIC_API_KEY: Optional[str] = None

    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
