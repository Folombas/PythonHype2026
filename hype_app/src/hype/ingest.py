"""Пайплайн приёма новостей: seed JSON / RSS -> Polars со строгой схемой -> валидированные Article."""

from __future__ import annotations

import hashlib
import json
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

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


def _rss_id(url: str, published: datetime) -> str:
    digest = hashlib.sha256(f"{url}|{published.isoformat()}".encode("utf-8")).hexdigest()[:12]
    return f"rss-{digest}"


def parse_rss(xml: str) -> list[Article]:
    """Нормализует RSS 2.0 (channel/item) в Article без внешних зависимостей."""
    root = ET.fromstring(xml)
    out: list[Article] = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_raw = (item.findtext("pubDate") or "").strip()
        desc = (item.findtext("description") or "").strip()
        if not title or not link:
            continue
        published = parsedate_to_datetime(pub_raw) if pub_raw else datetime.now(timezone.utc)
        out.append(
            Article(
                id=_rss_id(link, published),
                title=title,
                source="rss",
                url=link,
                published_at=published,
                summary=desc,
                keywords=[],
            )
        )
    return out


def load_articles(path: str | Path, *, rss: bool = False) -> list[Article]:
    """Единая точка приёма: seed-файл по умолчанию, rss=True -> файл содержит RSS-XML."""
    if rss:
        return parse_rss(Path(path).read_text(encoding="utf-8"))
    return load_seed(path)
