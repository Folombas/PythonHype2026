"""Маршруты статей: список с фильтрами и пагинацией + одиночная статья."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Request

from hype.models import Article, QueryParams
from hype.storage import ArticleRepository

router = APIRouter(prefix="/articles", tags=["articles"])


def _repo(request: Request) -> ArticleRepository:
    """Достаёт репозиторий из состояния приложения."""
    repo: ArticleRepository = request.app.state.repository
    return repo


@router.get("", response_model=list[Article])
def list_articles(
    request: Request,
    source: str | None = None,
    since: datetime | None = None,
    until: datetime | None = None,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> list[Article]:
    """Список статей: фильтры по источнику и датам, пагинация."""
    params = QueryParams(source=source, since=since, until=until, limit=limit, offset=offset)
    return _repo(request).query(params)


@router.get("/{article_id}", response_model=Article)
def get_article(request: Request, article_id: str) -> Article:
    """Одиночная статья по id; 404, если нет."""
    found = _repo(request).get(article_id)
    if found is None:
        raise HTTPException(status_code=404, detail={"reason": "article-not-found", "id": article_id})
    return found
