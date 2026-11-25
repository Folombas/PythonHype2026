"""Детерминированный extractive-суммаризатор: без сети, без ключей, воспроизводимый."""

from __future__ import annotations

import re
from collections import Counter

from hype.models import Article, Summary

_STOPWORDS = frozenset(
    {
        "и", "в", "на", "с", "по", "для", "это", "как", "что", "не", "а", "но", "же",
        "из", "у", "к", "о", "от", "до", "за", "при", "чтобы", "которые",
        "the", "a", "an", "of", "to", "in", "on", "for", "and", "is", "are",
    }
)


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _words(text: str) -> list[str]:
    return [
        w
        for w in re.findall(r"[а-яёa-z]+", text.lower())
        if w not in _STOPWORDS and len(w) > 2
    ]


class ExtractiveSummarizer:
    """Частотный extractive-метод: одинаковый вход -> одинаковый вывод."""

    def __init__(self, sentences: int = 2) -> None:
        self._sentences = max(1, sentences)

    def summarize(self, article: Article) -> Summary:
        base = article.summary.strip() or article.title.strip()
        sentences = _split_sentences(base) or [base]
        freq: Counter[str] = Counter(_words(base))

        scored: list[tuple[int, int, str]] = []
        for order, sentence in enumerate(sentences):
            score = sum(freq.get(w, 0) for w in _words(sentence))
            scored.append((score, -order, sentence))
        scored.sort(reverse=True)

        chosen = [s for _, _, s in scored[: self._sentences]]
        position = {s: i for i, s in enumerate(sentences)}
        chosen.sort(key=lambda s: position[s])  # выходной порядок как в тексте
        return Summary(
            article_id=article.id,
            text=" ".join(chosen) if chosen else article.title,
            method="extractive",
        )
