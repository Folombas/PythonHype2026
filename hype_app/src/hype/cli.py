"""Typer-CLI FinPulse Hype: ingest, ls, summarize, serve."""

from __future__ import annotations

from pathlib import Path

import typer

from hype.config import get_settings
from hype.ingest import load_articles
from hype.models import QueryParams
from hype.storage import ArticleRepository

app = typer.Typer(
    help="FinPulse Hype: пайплайн новостей, аналитика и суммаризация",
    no_args_is_help=True,
)


def _open_repo(db: Path | None) -> ArticleRepository:
    """Открывает репозиторий: явный путь или из настроек."""
    path = str(db) if db else get_settings().db_path
    return ArticleRepository(path)


@app.command()
def ingest(
    env_file: Path = typer.Option(None, help="путь к seed JSON или RSS-файлу"),
    rss: bool = typer.Option(False, help="файл содержит RSS-XML"),
    db: Path = typer.Option(None, help="путь к DuckDB (иначе из настроек)"),
) -> None:
    """Заливает статьи из источника в базу."""
    source = env_file or Path(get_settings().seed_path)
    articles = load_articles(source, rss=rss)
    repo = _open_repo(db)
    try:
        written = repo.upsert_many(articles)
        typer.echo(f"загружено статей: {written} (всего в базе: {repo.count()})")
    finally:
        repo.close()


@app.command("ls")
def ls(
    limit: int = typer.Option(10, min=1, max=500),
    source: str = typer.Option(None, help="фильтр по источнику"),
    db: Path = typer.Option(None, help="путь к DuckDB"),
) -> None:
    """Показывает последние статьи."""
    repo = _open_repo(db)
    try:
        articles = repo.query(QueryParams(limit=limit, source=source))
    finally:
        repo.close()
    for a in articles:
        typer.echo(f"{a.id}  {a.published_at:%Y-%m-%d}  [{a.source}]  {a.title}")


@app.command()
def summarize(
    article_id: str = typer.Argument(...),
    db: Path = typer.Option(None, help="путь к DuckDB"),
) -> None:
    """AI-суммаризация статьи (fallback или langchain по настройкам)."""
    from hype.api.app import build_summarizer

    repo = _open_repo(db)
    try:
        found = repo.get(article_id)
    finally:
        repo.close()
    if found is None:
        typer.echo(f"статья не найдена: {article_id}")
        raise typer.Exit(code=1)
    result = build_summarizer(get_settings()).summarize(found)
    typer.echo(f"[{result.method}] {result.text}")


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1"),
    port: int = typer.Option(8000, min=1, max=65535),
) -> None:
    """Поднимает API (uvicorn) из фабрики приложения."""
    import uvicorn

    typer.echo(f"FinPulse Hype API: http://{host}:{port}/docs")
    uvicorn.run("hype.api.app:create_app", factory=True, host=host, port=port)


def main() -> None:
    """Точка входа для console-script hype."""
    app()


if __name__ == "__main__":
    main()
