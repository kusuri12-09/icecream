from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///./icecream.db"
    jwt_secret_key: str = "dev-only-change-this-secret"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    admin_emails: str = ""
    kspo_api_key: str | None = None
    kspo_center_url: str | None = None
    kspo_activity_url: str | None = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def admin_email_set(self) -> set[str]:
        return {item.strip().lower() for item in self.admin_emails.split(",") if item.strip()}


@lru_cache
def get_settings() -> Settings:
    return Settings()


BASE_DIR = Path(__file__).resolve().parents[2]
CRITERIA_PATH = BASE_DIR / "data" / "fitness_grade_criteria.json"
