import json
import os
from pydantic_settings import BaseSettings
from pydantic import field_validator


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

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


settings = Settings()
