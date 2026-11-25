"""Детерминизм extractive-fallback: без сети и ключей."""

from datetime import UTC, datetime

from hype.ai.fallback import ExtractiveSummarizer
from hype.models import Article


def _article(summary: str) -> Article:
    return Article(
        id="ai-001",
        title="Ставка без изменений",
        source="Demo",
        url="https://example.com/ai-001",
        published_at=datetime(2026, 11, 3, tzinfo=UTC),
        summary=summary,
        keywords=[],
    )


def test_deterministic_output() -> None:
    article = _article("Регулятор сохранил ставку. Рынок отреагировал спокойно. Аналитики ждут конца года.")
    first = ExtractiveSummarizer().summarize(article).text
    second = ExtractiveSummarizer().summarize(article).text
    assert first == second
    assert first


def test_sentences_from_source() -> None:
    summary = "Регулятор сохранил ставку. Рынок отреагировал спокойно. Вводные будущих месяцев важны."
    text = ExtractiveSummarizer(sentences=1).summarize(_article(summary)).text
    assert text in (
        "Регулятор сохранил ставку.",
        "Рынок отреагировал спокойно.",
        "Вводные будущих месяцев важны.",
    )
    assert text in summary


def test_falls_back_to_title() -> None:
    result = ExtractiveSummarizer().summarize(_article(""))
    assert result.text
    assert result.method == "extractive"
