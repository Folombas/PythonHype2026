"""CLI smoke-тесты: Typer CliRunner, временная DuckDB."""

from datetime import UTC, datetime
from pathlib import Path

from typer.testing import CliRunner

from hype.cli import app
from hype.models import Article
from hype.storage import ArticleRepository

runner = CliRunner()


def _seed(db: Path) -> None:
    ArticleRepository(str(db)).upsert_many(
        [
            Article(
                id="c-001",
                title="Ставка без изменений",
                source="Demo",
                url="https://example.com/c-001",
                published_at=datetime(2026, 11, 3, tzinfo=UTC),
                summary="Регулятор сохранил ставку. Рынок спокоен.",
                keywords=["ставка"],
            )
        ]
    )


def test_ls_lists_articles(tmp_path: Path) -> None:
    db = tmp_path / "cli.duckdb"
    _seed(db)
    result = runner.invoke(app, ["ls", "--db", str(db)])
    assert result.exit_code == 0
    assert "c-001" in result.output


def test_stats_shows_tables(tmp_path: Path) -> None:
    db = tmp_path / "cli.duckdb"
    _seed(db)
    result = runner.invoke(app, ["stats", "--db", str(db)])
    assert result.exit_code == 0
    assert "Топ источников" in result.output


def test_stats_on_empty_db(tmp_path: Path) -> None:
    db = tmp_path / "empty.duckdb"
    result = runner.invoke(app, ["stats", "--db", str(db)])
    assert result.exit_code != 0  # подсказка сначала залить данные


def test_summarize_missing_article(tmp_path: Path) -> None:
    db = tmp_path / "cli.duckdb"
    _seed(db)
    result = runner.invoke(app, ["summarize", "ghost", "--db", str(db)])
    assert result.exit_code == 1


def test_summarize_fallback(tmp_path: Path) -> None:
    db = tmp_path / "cli.duckdb"
    _seed(db)
    result = runner.invoke(app, ["summarize", "c-001", "--db", str(db)])
    assert result.exit_code == 0
    assert "extractive" in result.output


def test_export_csv(tmp_path: Path) -> None:
    db = tmp_path / "cli.duckdb"
    _seed(db)
    out = tmp_path / "export.csv"
    result = runner.invoke(app, ["export", str(out), "--fmt", "csv", "--db", str(db)])
    assert result.exit_code == 0
    text_content = out.read_text(encoding="utf-8")
    assert text_content.splitlines()[0].startswith("id")
    assert "c-001" in text_content
