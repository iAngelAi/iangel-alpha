"""
Configuration centralisée iAngel.

Utilise Pydantic Settings pour validation stricte des variables d'environnement.
JAMAIS de valeurs hardcodées pour secrets.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration de l'application iAngel."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # === Core ===
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    app_version: str = "0.1.0-alpha"
    secret_key: str = "change-me-in-production"

    # === API ===
    api_v1_prefix: str = "/api/v1"
    allowed_hosts: str = "*"

    # === Database (Phase S2) ===
    database_url: str = Field(
        default="sqlite+aiosqlite:///./test.db",
        validation_alias="DATABASE_URL"
    )

    @field_validator("database_url", mode="before")
    @classmethod
    def make_async_database_url(cls, v: str) -> str:
        """Force l'usage du driver asynchrone (asyncpg) pour Postgres."""
        if v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    # === Anthropic (Phase S0-03) ===
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"
    anthropic_max_tokens: int = 1024
    anthropic_timeout_seconds: int = 30

    # === Railway ===
    port: int = 8000

    # === Sandbox P4 ===
    sandbox_mode: bool = False # ACTIVATION CERVEAU RÉEL (S1)
    mocks_dir: Path = Path("mocks")
    default_mock_id: str = "M01"

    @property
    def is_production(self) -> bool:
        """Vérifie si environnement de production."""
        return self.environment == "production"

    @property
    def is_debug(self) -> bool:
        """Vérifie si mode debug actif."""
        return self.debug and not self.is_production


@lru_cache
def get_settings() -> Settings:
    """
    Retourne instance singleton des settings.

    Utilise lru_cache pour éviter rechargement à chaque appel.
    """
    return Settings()
