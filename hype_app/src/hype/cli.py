"""Typer-CLI FinPulse Hype: ingest, ls, stats, summarize, serve, export (Rich-вывод)."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import track
from rich.table import Table

from hype.analytics import keyword_score, per_day, top_sources
from hype.config import get_settings
from hype.ingest import load_articles
from hype.models import QueryParams
from hype.storage import ArticleRepository

app = typer.Typer(
    help="FinPulse Hype: пайплайн новостей, аналитика и суммаризация",
    no_args_is_help=True,
)
console = Console()


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
    """Заливает статьи из источника в базу (с прогресс-баром)."""
    source = env_file or Path(get_settings().seed_path)
    articles = load_articles(source, rss=rss)
    repo = _open_repo(db)
    try:
        written = 0
        for a in track(articles, description="Загрузка в DuckDB"):
            repo.upsert_many([a])
            written += 1
        console.print(f"[green]загружено статей:[/green] {written} (всего в базе: {repo.count()})")
    finally:
        repo.close()


@app.command("ls")
def ls(
    limit: int = typer.Option(10, min=1, max=500),
    source: str = typer.Option(None, help="фильтр по источнику"),
    db: Path = typer.Option(None, help="путь к DuckDB"),
) -> None:
    """Показывает последние статьи таблицей."""
    repo = _open_repo(db)
    try:
        articles = repo.query(QueryParams(limit=limit, source=source))
    finally:
        repo.close()
    table = Table(title="Последние статьи")
    table.add_column("id", style="cyan", no_wrap=True)
    table.add_column("дата", style="dim")
    table.add_column("источник", style="magenta")
    table.add_column("заголовок")
    for a in articles:
        table.add_row(a.id, f"{a.published_at:%Y-%m-%d}", a.source, a.title)
    console.print(table)


@app.command()
def stats(
    top: int = typer.Option(5, min=1, max=50, help="размер топа источников/слов"),
    db: Path = typer.Option(None, help="путь к DuckDB"),
) -> None:
    """Аналитика: топ источников, статьи по дням, ключевые слова."""
    repo = _open_repo(db)
    try:
        articles = repo.query(QueryParams(limit=500))
    finally:
        repo.close()
    if not articles:
        console.print("[yellow]база пуста: сначала выполни hype ingest[/yellow]")
        raise typer.Exit()

    t1 = Table("источник", "статей", title=f"Топ источников (top={top})")
    for row in top_sources(articles, top):
        t1.add_row(str(row["source"]), str(row["count"]))
    console.print(t1)

    t2 = Table("день", "статей", title="Публикации по дням")
    for row in per_day(articles):
        t2.add_row(str(row["day"]), str(row["count"]))
    console.print(t2)

    t3 = Table("ключевое слово", "частота", title=f"Ключевые слова (top={top})")
    for row in keyword_score(articles, top):
        t3.add_row(str(row["keyword"]), str(row["score"]))
    console.print(t3)


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
        console.print(f"[red]статья не найдена:[/red] {article_id}")
        raise typer.Exit(code=1)
    result = build_summarizer(get_settings()).summarize(found)
    console.print(f"[bold][{result.method}][/bold] {result.text}")


@app.command()
def export(
    out: Path = typer.Argument(..., help="путь до файла export"),
    fmt: str = typer.Option("json", help="формат: json или csv"),
    limit: int = typer.Option(500, min=1, max=100000),
    db: Path = typer.Option(None, help="путь к DuckDB"),
) -> None:
    """Экспорт статей в JSON или CSV."""
    fmt = fmt.strip().lower()
    if fmt not in ("json", "csv"):
        console.print("[red]формат: json или csv[/red]")
        raise typer.Exit(code=2)
    repo = _open_repo(db)
    try:
        articles = repo.query(QueryParams(limit=limit))
    finally:
        repo.close()
    rows = [
        {
            "id": a.id,
            "title": a.title,
            "source": a.source,
            "url": a.url,
            "published_at": a.published_at.isoformat(),
            "summary": a.summary,
            "keywords": ",".join(a.keywords),
        }
        for a in articles
    ]
    if fmt == "json":
        out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        with out.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["id"])
            writer.writeheader()
            writer.writerows(rows)
    console.print(f"[green]экспортировано[/green] {len(rows)} -> {out}")


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1"),
    port: int = typer.Option(8000, min=1, max=65535),
) -> None:
    """Поднимает API (uvicorn) из фабрики приложения."""
    import uvicorn

    console.print(f"FinPulse Hype API: [link]http://{host}:{port}/docs[/link]")
    uvicorn.run("hype.api.app:create_app", factory=True, host=host, port=port)


def main() -> None:
    """Точка входа для console-script hype."""
    app()


if __name__ == "__main__":
    main()
