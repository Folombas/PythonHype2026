"""DuckDB-репозиторий статей: файл-БД, параметризованный SQL, строгая типизация."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import duckdb

from hype.models import Article, QueryParams

_COLS = "id, title, source, url, published_at, summary, keywords"


def _naive(value: datetime) -> datetime:
    """DuckDB TIMESTAMP наивный: aware-даты переводим в UTC и снимаем tzinfo."""
    return value.astimezone(UTC).replace(tzinfo=None)


class ArticleRepository:
    """Владелец соединения и схемы таблицы статей."""

    def __init__(self, db_path: str | Path = "data/hype.duckdb") -> None:
        self._db_path = Path(db_path)
        if str(self._db_path.parent) not in ("", "."):
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._con: duckdb.DuckDBPyConnection = duckdb.connect(str(self._db_path))
        self._con.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id VARCHAR PRIMARY KEY,
                title VARCHAR NOT NULL,
                source VARCHAR NOT NULL,
                url VARCHAR NOT NULL,
                published_at TIMESTAMP NOT NULL,
                summary VARCHAR NOT NULL,
                keywords VARCHAR NOT NULL
            );
            """
        )

    def close(self) -> None:
        self._con.close()

    def upsert_many(self, articles: list[Article]) -> int:
        """Сохраняет статьи (INSERT OR REPLACE), возвращает число записей."""
        written = 0
        for a in articles:
            self._con.execute(
                "INSERT OR REPLACE INTO articles "
                "(id, title, source, url, published_at, summary, keywords) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    a.id,
                    a.title,
                    a.source,
                    a.url,
                    _naive(a.published_at),
                    a.summary,
                    json.dumps(a.keywords, ensure_ascii=False),
                ],
            )
            written += 1
        return written

    def _select(self, sql: str, args: list[object]) -> list[Article]:
        rows = self._con.execute(sql, args).fetchall()
        return [
            Article(
                id=r[0],
                title=r[1],
                source=r[2],
                url=r[3],
                published_at=r[4],
                summary=r[5],
                keywords=json.loads(r[6]) if r[6] else [],
            )
            for r in rows
        ]

    def get(self, article_id: str) -> Article | None:
        found = self._select("SELECT " + _COLS + " FROM articles WHERE id = ?", [article_id])
        return found[0] if found else None

    def query(self, params: QueryParams) -> list[Article]:
        """Выборка с фильтрами и пагинацией (параметризованный SQL)."""
        sql = "SELECT " + _COLS + " FROM articles WHERE 1=1"
        args: list[object] = []
        if params.source:
            sql += " AND source = ?"
            args.append(params.source)
        if params.since:
            sql += " AND published_at >= ?"
            args.append(_naive(params.since))
        if params.until:
            sql += " AND published_at <= ?"
            args.append(_naive(params.until))
        sql += " ORDER BY published_at DESC LIMIT ? OFFSET ?"
        args.extend([params.limit, params.offset])
        return self._select(sql, args)

    def count(self) -> int:
        row = self._con.execute("SELECT COUNT(*) FROM articles").fetchone()
        return int(row[0]) if row else 0
