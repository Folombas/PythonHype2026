"""Настройки приложения: только из переменных окружения и .env (без секретов в коде)."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Строгие настройки: окружение -> .env -> дефолты."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="HYPE_", extra="ignore")

    app_name: str = "finpulse-hype"
    version: str = "0.1.0"

    db_path: str = "data/hype.duckdb"
    seed_path: str = "data/seed_articles.json"

    cors_origins: list[str] = ["*"]

    # AI: если провайдер задан - используем LangChain-адаптер, иначе extractive-fallback.
    # Ключ передаётся стандартной переменной окружения выбранного провайдера (читает сам SDK).
    langchain_provider: str = ""
    langchain_model: str = "gpt-4o-mini"


@lru_cache
def get_settings() -> Settings:
    """Кешированный доступ к настройкам."""
    return Settings()
