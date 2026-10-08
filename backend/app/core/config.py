import json
from pathlib import Path
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Detect environment file locations
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent

env_paths = []
if (ROOT_DIR / ".env").is_file():
    env_paths.append(ROOT_DIR / ".env")
if (BACKEND_DIR / ".env").is_file():
    env_paths.append(BACKEND_DIR / ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=tuple(env_paths) if env_paths else ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Subsfolio"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/subsfolio"
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    DEV_USER_ID: Union[str, None] = None

    # Authentication & Security
    JWT_SECRET_KEY: str = "subsfolio-dev-secret-key-phase-3-jwt-signing-2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    CLERK_SECRET_KEY: Union[str, None] = None
    CLERK_PUBLISHABLE_KEY: Union[str, None] = None

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            v_str = v.strip()
            if v_str.startswith("[") and v_str.endswith("]"):
                try:
                    return json.loads(v_str)
                except Exception:
                    pass
            return [i.strip() for i in v_str.split(",") if i.strip()]
        elif isinstance(v, list):
            return [str(item) for item in v]
        return ["*"]


settings = Settings()
