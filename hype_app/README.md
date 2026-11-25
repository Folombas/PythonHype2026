# 🏛 FinPulse Hype (hype_app)

Мини-конвейер финансовых новостей на хайповом Python-стеке 2026: **FastAPI + Pydantic v2 + Polars + DuckDB + LangChain (опционально) + Typer/Rich + Streamlit**, сборка через **uv**.

Сестринский проект экосистемы [FinFocus](https://github.com/Folombas/FinFocus): берём финансовые заголовки, нормализуем, храним, агрегируем и суммаризируем.

> Данные: `data/seed_articles.json` - **синтетические демо-записи** (не реальные новости).

## 🚀 Быстрый старт

```bash
uv sync                    # окружение по pyproject (uv.lock появится при первом реальном запуске)
uv run hype ingest         # seed-JSON -> DuckDB (data/hype.duckdb)
uv run hype ls --limit 5   # последние статьи таблицей
uv run hype stats          # топ источников, дни, ключевые слова
uv run hype summarize a-001
uv run hype serve          # API: http://127.0.0.1:8000/docs
uv run streamlit run src/hype/dashboard.py
```

## 📡 API

| Метод | Путь | Что делает |
|---|---|---|
| GET | `/health` | живость |
| GET | `/version` | имя и версия приложения |
| GET | `/articles` | список: фильтры `source/since/until`, пагинация `limit/offset` |
| GET | `/articles/{id}` | одна статья (404 под error-envelope) |
| GET | `/analytics/top-sources?n=` | топ источников (Polars) |
| GET | `/analytics/per-day` | статьи по дням |
| GET | `/analytics/keywords?top=` | частотный топ ключевых слов |
| GET | `/summarize/{article_id}` | AI-суммаризация через порт |

Во всех ответах - заголовок `x-request-id` и единый error-envelope.

## 🖥 CLI (`hype`)

| Команда | Что делает |
|---|---|
| `hype ingest [--env-file JSON] [--rss]` | залить статьи в базу (с прогресс-баром) |
| `hype ls [--limit] [--source]` | последние статьи Rich-таблицей |
| `hype stats [--top]` | аналитика тремя таблицами |
| `hype summarize ID` | суммаризация одной статьи |
| `hype export OUT [--fmt json\|csv]` | экспорт выборки |
| `hype serve [--host] [--port]` | поднять API |

## 🤖 AI-суммаризация

- По умолчанию: **детерминированный extractive-fallback** - работает без сети и ключей, одинаковый вход даёт одинаковый вывод.
- Опционально: `uv sync --extra ai`, затем `HYPE_LANGCHAIN_PROVIDER=openai` в `.env` (см. `.env.example`). Ключ кладётся в стандартную переменную окружения провайдера: в коде и репозитории секретов нет.

## ✅ Проверки

```bash
uv run ruff check .
uv run python -m compileall -q src tests
uv run pytest -q
```

CI: `.github/workflows/hype.yml` (hype-ci) - uv sync + ruff + compileall + pytest на каждый push/PR, затрагивающий `hype_app/**`.

## 🐳 Docker

```bash
docker compose up --build
# api: http://localhost:8000/docs
# dashboard: http://localhost:8501
```

## 📐 Архитектура

Смотри [ARCHITECTURE.md](ARCHITECTURE.md): поток данных, слои и ADR (порт+адаптеры AI, Polars, DuckDB, изоляция hype_app).

---

© Alex Folombas · сестринские проекты: [FinFocus](https://github.com/Folombas/FinFocus), [web-games](https://github.com/Folombas/web-games)
