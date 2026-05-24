import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "PhishGuard AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    MODEL_PATH: str = os.path.join("ml", "pipeline.pkl")
    DATA_DIR: str = os.path.join("data")
    DATABASE_URL: str = "sqlite:///./phishguard.db"
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "https://*.vercel.app",
    ]
    MAX_EMAIL_LENGTH: int = 50000

    model_config = {"env_file": ".env"}


settings = Settings()
