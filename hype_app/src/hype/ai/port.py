"""Порт суммаризации: контракт, за которым скрывается любой адаптер."""

from __future__ import annotations

from typing import Protocol

from hype.models import Article, Summary


class SummarizerPort(Protocol):
    """Любой суммаризатор умеет превращать Article в Summary."""

    def summarize(self, article: Article) -> Summary:
        """Вернуть Summary для статьи (детерминированность - забота адаптера)."""
        ...


def get_default_summarizer() -> SummarizerPort:
    """Фабрика по умолчанию: детерминированный extractive-fallback (без сети и ключей)."""
    from hype.fallback import ExtractiveSummarizer  # локальный импорт: фабрика

    return ExtractiveSummarizer()
