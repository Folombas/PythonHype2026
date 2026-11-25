"""Маршруты аналитики и суммаризации: Polars-агрегации + AI-порт."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request

from hype.analytics import keyword_score, per_day, top_sources
from hype.models import Article, QueryParams, Summary
from hype.storage import ArticleRepository

router = APIRouter(tags=["analytics"])


def _articles(request: Request) -> list[Article]:
    """Вся таблица статей из репозитория (демо-объём датасета мал)."""
    repo: ArticleRepository = request.app.state.repository
    return repo.query(QueryParams(limit=500))


@router.get("/analytics/top-sources")
def top_sources_route(request: Request, n: int = Query(default=5, ge=1, le=50)) -> list[dict[str, Any]]:
    """Топ источников по числу статей."""
    return top_sources(_articles(request), n)


@router.get("/analytics/per-day")
def per_day_route(request: Request) -> list[dict[str, Any]]:
    """Число статей по дням."""
    return per_day(_articles(request))


@router.get("/analytics/keywords")
def keywords_route(request: Request, top: int = Query(default=10, ge=1, le=50)) -> list[dict[str, Any]]:
    """Топ ключевых слов по частоте."""
    return keyword_score(_articles(request), top)


@router.get("/summarize/{article_id}", response_model=Summary)
def summarize_route(request: Request, article_id: str) -> Summary:
    """AI-суммаризация статьи через порт (fallback или langchain по настройкам)."""
    repo: ArticleRepository = request.app.state.repository
    article = repo.get(article_id)
    if article is None:
        raise HTTPException(status_code=404, detail={"reason": "article-not-found", "id": article_id})
    summarizer = request.app.state.summarizer
    return summarizer.summarize(article)
