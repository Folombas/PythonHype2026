"""LangChain-адаптер за портом: lazy import, ключ передаётся env-переменной провайдера."""

from __future__ import annotations

from typing import Any

from hype.config import Settings
from hype.models import Article, Summary


def make_runner(settings: Settings) -> Any:
    """Собирает модель по строке 'provider:model'; langchain - опциональная зависимость.

    Ключ не передаётся кодом: SDK читает стандартную переменную окружения провайдера.
    """
    provider = settings.langchain_provider.strip()
    if not provider:
        raise ValueError(
            "langchain_provider пуст: задай HYPE_LANGCHAIN_PROVIDER или используй fallback"
        )
    try:
        from langchain.chat_models import init_chat_model
    except ImportError as exc:  # pragma: no cover - зависимость опциональна
        raise RuntimeError(
            "langchain не установлен: поставь экстра-группу 'ai' (uv sync --extra ai)"
        ) from exc
    return init_chat_model(f"{provider}:{settings.langchain_model}")


class LangChainSummarizer:
    """Оборачивает langchain-модель в SummarizerPort; без ключа падает с ясной ошибкой."""

    def __init__(self, runner: Any) -> None:
        self._runner = runner

    def summarize(self, article: Article) -> Summary:
        prompt = (
            "Суммаризируй финансовую новость одним сжатым предложением на русском языке.\n"
            f"Заголовок: {article.title}\n"
            f"Текст: {article.summary}\n"
            "Ответ: только предложение."
        )
        answer = self._runner.invoke(prompt)
        text = str(getattr(answer, "content", answer)).strip()
        return Summary(
            article_id=article.id,
            text=text or "Суммаризация не вернула текст",
            method="langchain",
        )
