"""Пайплайн приёма новостей: seed JSON -> Polars со строгой схемой -> валидированные Article."""

from __future__ import annotations

import json
from pathlib import Path

import polars as pl

from hype.models import Article

ARTICLE_SCHEMA: dict[str, pl.DataType] = {
    "id": pl.Utf8,
    "title": pl.Utf8,
    "source": pl.Utf8,
    "url": pl.Utf8,
    "published_at": pl.Utf8,
    "summary": pl.Utf8,
    "keywords": pl.List(pl.Utf8),
}


def load_seed(path: str | Path) -> list[Article]:
    """Читает seed-JSON через Polars со строгой схемой и возвращает валидированный список статей."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    frame = pl.DataFrame(raw, schema=ARTICLE_SCHEMA, strict=True)
    return [Article.model_validate(row) for row in frame.to_dicts()]
