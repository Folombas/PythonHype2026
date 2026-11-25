"""Юнит-тесты строгих моделей (pure)."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from hype.models import Article, QueryParams, Summary


def _article(**overrides: object) -> dict:
    data: dict = {
        "id": "a-001",
        "title": "Ставка без изменений",
        "source": "Demo",
        "url": "https://example.com/a-001",
        "published_at": datetime(2026, 11, 3, 10, tzinfo=UTC),
        "summary": "Текст новости.",
        "keywords": ["ставка"],
    }
    data.update(overrides)
    return data


def test_article_valid() -> None:
    a = Article.model_validate(_article())
    assert a.id == "a-001"
    assert a.published_at.tzinfo is not None
    assert a.keywords == ["ставка"]


def test_article_forbids_extra() -> None:
    with pytest.raises(ValidationError):
        Article.model_validate(_article(unknown="field"))


def test_article_requires_title() -> None:
    with pytest.raises(ValidationError):
        Article.model_validate(_article(title=""))


def test_article_requires_datetime() -> None:
    with pytest.raises(ValidationError):
        Article.model_validate(_article(published_at="вчера"))


def test_query_params_defaults_and_bounds() -> None:
    q = QueryParams()
    assert q.limit == 50 and q.offset == 0 and q.source is None
    with pytest.raises(ValidationError):
        QueryParams(limit=0)
    with pytest.raises(ValidationError):
        QueryParams(limit=1000)
    with pytest.raises(ValidationError):
        QueryParams(offset=-1)


def test_summary_method_is_restricted() -> None:
    assert Summary(article_id="x", text="т", method="extractive").method == "extractive"
    with pytest.raises(ValidationError):
        Summary(article_id="x", text="т", method="magic")
