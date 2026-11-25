"""Тесты DuckDB-хранилища на временных базах."""

from datetime import UTC, datetime
from pathlib import Path

from hype.models import Article, QueryParams
from hype.storage import ArticleRepository


def _article(i: int, source: str = "S", day: int = 1) -> Article:
    return Article(
        id="t-" + format(i, "03d"),
        title="Новость " + str(i),
        source=source,
        url="https://example.com/t-" + format(i, "03d"),
        published_at=datetime(2026, 11, day, 12, tzinfo=UTC),
        summary="Текст.",
        keywords=["k"],
    )


def test_upsert_and_count(tmp_path: Path) -> None:
    repo = ArticleRepository(tmp_path / "s.duckdb")
    try:
        assert repo.count() == 0
        assert repo.upsert_many([_article(1), _article(2)]) == 2
        assert repo.count() == 2
    finally:
        repo.close()


def test_upsert_is_idempotent(tmp_path: Path) -> None:
    repo = ArticleRepository(tmp_path / "s.duckdb")
    try:
        repo.upsert_many([_article(1)])
        repo.upsert_many([_article(1)])
        assert repo.count() == 1
    finally:
        repo.close()


def test_query_filters_and_pagination(tmp_path: Path) -> None:
    repo = ArticleRepository(tmp_path / "s.duckdb")
    try:
        repo.upsert_many(
            [
                _article(1, source="A", day=5),
                _article(2, source="B", day=6),
                _article(3, source="A", day=7),
            ]
        )
        assert len(repo.query(QueryParams(source="A"))) == 2
        single = repo.query(QueryParams(limit=1, offset=0))
        assert single[0].id == "t-003"  # свежие первыми
        assert repo.query(QueryParams(limit=10, offset=1))[0].id == "t-002"
        window = repo.query(QueryParams(
            since=datetime(2026, 11, 6, tzinfo=UTC),
        ))
        assert {a.id for a in window} == {"t-002", "t-003"}
    finally:
        repo.close()


def test_get_returns_none_for_missing(tmp_path: Path) -> None:
    repo = ArticleRepository(tmp_path / "s.duckdb")
    try:
        repo.upsert_many([_article(1)])
        assert repo.get("t-001") is not None
        assert repo.get("nope") is None
    finally:
        repo.close()
