from functools import lru_cache
from pathlib import Path
from urllib.parse import quote_plus

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str | None = None
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = Field(default="icecream", validation_alias=AliasChoices("POSTGRES_DB", "DB_NAME"))
    db_user: str | None = Field(default=None, validation_alias=AliasChoices("POSTGRES_USER", "DB_USER"))
    db_password: str | None = Field(default=None, validation_alias=AliasChoices("POSTGRES_PASSWORD", "DB_PASSWORD"))
    jwt_secret_key: str = "dev-only-change-this-secret"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    admin_emails: str = ""
    kspo_api_key: str | None = None
    kspo_center_url: str | None = None
    kspo_activity_url: str | None = None
    cron_secret: str | None = None
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def admin_email_set(self) -> set[str]:
        return {item.strip().lower() for item in self.admin_emails.split(",") if item.strip()}

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip().rstrip("/") for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url.replace("postgresql+psycopg2://", "postgresql+psycopg://", 1).replace(
                "postgresql://", "postgresql+psycopg://", 1
            )
        if self.db_user and self.db_password:
            user = quote_plus(self.db_user)
            password = quote_plus(self.db_password)
            return f"postgresql+psycopg://{user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}"
        return "postgresql+psycopg://icecream:icecream@localhost:5432/icecream"


@lru_cache
def get_settings() -> Settings:
    return Settings()


BASE_DIR = Path(__file__).resolve().parents[2]
CRITERIA_PATH = BASE_DIR / "data" / "fitness_grade_criteria.json"
