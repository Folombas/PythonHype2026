"""Тесты приёма (seed + RSS) и аналитики: pure, без сети."""

import json
from pathlib import Path

import polars as pl
import pytest

from hype.analytics import keyword_score, per_day, top_sources
from hype.ingest import ARTICLE_SCHEMA, load_seed, parse_rss
from hype.models import Article

SEED = [
    {
        "id": "s-001",
        "title": "Ставка без изменений",
        "source": "Demo",
        "url": "https://example.com/s-001",
        "published_at": "2026-11-03T10:00:00Z",
        "summary": "Регулятор сохранил ставку. Рынок спокоен.",
        "keywords": ["ставка", "цб"],
    },
    {
        "id": "s-002",
        "title": "Нефть отскочила",
        "source": "Energy",
        "url": "https://example.com/s-002",
        "published_at": "2026-11-04T12:00:00Z",
        "summary": "Цены восстановились.",
        "keywords": ["нефть"],
    },
]

RSS = """<?xml version="1.0"?>
<rss version="2.0"><channel><title>Feed</title>
  <item><title>Рубль укрепился</title><link>https://ex.com/1</link>
    <pubDate>Tue, 10 Nov 2026 14:40:00 +0000</pubDate>
    <description>Курс вырос.</description></item>
  <item><title>Отчётность банков</title><link>https://ex.com/2</link>
    <pubDate>Thu, 12 Nov 2026 09:00:00 +0000</pubDate></item>
  <item><link>https://ex.com/skip</link></item>
</channel></rss>
"""


def _articles() -> list[Article]:
    return [Article.model_validate(item) for item in SEED]


def test_load_seed_validates_schema(tmp_path: Path) -> None:
    seed_file = tmp_path / "seed.json"
    seed_file.write_text(json.dumps(SEED, ensure_ascii=False), encoding="utf-8")
    articles = load_seed(seed_file)
    assert [a.id for a in articles] == ["s-001", "s-002"]
    assert articles[0].keywords == ["ставка", "цб"]


def test_load_seed_strict_schema() -> None:
    """Схема строгая: keyword типа str вместо list обрывает загрузку поларс-ошибкой."""
    bad = [dict(SEED[0], keywords="ставка")]
    with pytest.raises(Exception):
        pl.DataFrame(bad, schema=ARTICLE_SCHEMA, strict=True)


def test_parse_rss_normalizes() -> None:
    articles = parse_rss(RSS)
    assert len(articles) == 2  # item без title пропущен
    assert all(a.source == "rss" for a in articles)
    assert articles[0].id.startswith("rss-")
    assert articles[0].published_at.year == 2026
    assert articles[1].summary == ""
    assert len({a.id for a in articles}) == 2  # ids уникальны


def test_parse_rss_deterministic_ids() -> None:
    assert [a.id for a in parse_rss(RSS)] == [a.id for a in parse_rss(RSS)]


def test_top_sources() -> None:
    stats = top_sources(_articles())
    assert stats[0] == {"source": "Demo", "count": 1}
    assert len(stats) == 2


def test_per_day_sorted() -> None:
    days = per_day(_articles())
    assert [str(row["day"]) for row in days] == sorted(str(row["day"]) for row in days)
    assert len(days) == 2


def test_keyword_score() -> None:
    stats = keyword_score(_articles(), top=5)
    assert {"keyword": "ставка", "score": 1} in stats
