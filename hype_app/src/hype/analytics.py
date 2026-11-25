"""Аналитические агрегации на Polars (чистые функции без IO)."""

from __future__ import annotations

import polars as pl

from hype.models import Article

_BASE_SCHEMA: dict[str, pl.DataType] = {
    "id": pl.Utf8,
    "title": pl.Utf8,
    "source": pl.Utf8,
    "published_at": pl.Datetime("us"),
    "keywords": pl.List(pl.Utf8),
}


def to_frame(articles: list[Article]) -> pl.DataFrame:
    """Список статей -> строгий Polars DataFrame (naive UTC)."""
    if not articles:
        empty = pl.DataFrame(schema=_BASE_SCHEMA)
        return empty.with_columns(pl.lit("").alias("url"), pl.lit("").alias("summary")).drop("url", "summary")
    rows = [
        {
            "id": a.id,
            "title": a.title,
            "source": a.source,
            "published_at": a.published_at.replace(tzinfo=None),
            "keywords": a.keywords,
        }
        for a in articles
    ]
    return pl.DataFrame(rows, schema=_BASE_SCHEMA, strict=True)


def top_sources(articles: list[Article], n: int = 5) -> list[dict[str, object]]:
    """Топ источников по числу статей."""
    frame = (
        to_frame(articles)
        .group_by("source")
        .agg(pl.len().alias("count"))
        .sort(["count", "source"], descending=[True, False])
        .head(n)
    )
    return frame.to_dicts()


def per_day(articles: list[Article]) -> list[dict[str, object]]:
    """Число статей по дням публикации."""
    frame = (
        to_frame(articles)
        .with_columns(pl.col("published_at").dt.date().cast(pl.Utf8).alias("day"))
        .group_by("day")
        .agg(pl.len().alias("count"))
        .sort("day")
    )
    return frame.to_dicts()


def keyword_score(articles: list[Article], top: int = 10) -> list[dict[str, object]]:
    """Топ ключевых слов по частоте встречаемости."""
    base = to_frame(articles)
    if base.height == 0:
        return []
    frame = (
        base.filter(pl.col("keywords").list.len() > 0)
        .explode("keywords")
        .rename({"keywords": "keyword"})
        .group_by("keyword")
        .agg(pl.len().alias("score"))
        .sort(["score", "keyword"], descending=[True, False])
        .head(top)
    )
    return frame.to_dicts()
