"""Строгие Pydantic v2 схемы домена."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Article(BaseModel):
    """Нормализованная новость."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source: str = Field(min_length=1)
    url: str
    published_at: datetime
    summary: str = ""
    keywords: list[str] = Field(default_factory=list)


class QueryParams(BaseModel):
    """Фильтры и пагинация для выборок."""

    model_config = ConfigDict(extra="forbid")

    source: str | None = None
    since: datetime | None = None
    until: datetime | None = None
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)


class Summary(BaseModel):
    """Результат суммаризации."""

    model_config = ConfigDict(extra="forbid")

    article_id: str
    text: str = Field(min_length=1)
    method: str = Field(pattern="^(extractive|langchain)$")
