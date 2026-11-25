"""Фабрика FastAPI: состояние, маршруты, middleware, health/version."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from hype.ai.fallback import ExtractiveSummarizer
from hype.ai.langchain_adapter import LangChainSummarizer, make_runner
from hype.api.middleware import install_middleware
from hype.config import Settings, get_settings


def build_summarizer(settings: Settings) -> Any:
    """Fallback по умолчанию; при заданном провайдере - LangChain-адаптер."""
    if settings.langchain_provider.strip():
        return LangChainSummarizer(make_runner(settings))
    return ExtractiveSummarizer()


def create_app(db_path: str | None = None, settings: Settings | None = None) -> FastAPI:
    """Создаёт приложение; db_path - точка расширения для тестов (tmp DuckDB)."""
    cfg = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.settings = cfg
        app.state.repository = ArticleRepository(db_path or cfg.db_path)
        app.state.summarizer = build_summarizer(cfg)
        try:
            yield
        finally:
            app.state.repository.close()

    app = FastAPI(
        title="FinPulse Hype",
        description="Сбор финансовых новостей, аналитика и AI-суммаризация",
        version=cfg.version,
        lifespan=lifespan,
    )

    install_middleware(app, cfg)

    from hype.api.routes_analytics import router as analytics_router
    from hype.api.routes_articles import router as articles_router

    app.include_router(articles_router)
    app.include_router(analytics_router)

    @app.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/version", tags=["meta"])
    def version() -> dict[str, str]:
        return {"app": cfg.app_name, "version": cfg.version}

    return app
