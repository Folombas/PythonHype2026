"""API-тесты на TestClient с временной DuckDB (httpx)."""

from datetime import datetime, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from hype.api.app import create_app
from hype.models import Article

pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")


def _article(i: int, source: str = "Demo") -> Article:
    return Article(
        id=f"a-{i:03d}",
        title=f"Новость {i}",
        source=source,
        url=f"https://example.com/a-{i:03d}",
        published_at=datetime(2026, 11, 3 + i, 10, tzinfo=timezone.utc),
        summary="Регулятор сохранил ставку. Рынок отреагировал спокойно.",
        keywords=["ставка"],
    )


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    app = create_app(db_path=str(tmp_path / "api.duckdb"))
    with TestClient(app) as c:
        c.app.state.repository.upsert_many([_article(1), _article(2, source="Other")])
        yield c


def test_health_and_version(client: TestClient) -> None:
    health = client.get("/health")
    assert health.status_code == 200 and health.json() == {"status": "ok"}
    version = client.get("/version")
    assert version.json() == {"app": "finpulse-hype", "version": "0.1.0"}


def test_request_id_header(client: TestClient) -> None:
    response = client.get("/health")
    assert response.headers.get("x-request-id")


def test_articles_list_and_filter(client: TestClient) -> None:
    items = client.get("/articles").json()
    assert len(items) == 2
    filtered = client.get("/articles", params={"source": "Demo"}).json()
    assert {a["id"] for a in filtered} == {"a-001"}
    ordering = client.get("/articles").json()
    assert ordering[0]["published_at"] >= ordering[1]["published_at"]


def test_article_pagination(client: TestClient) -> None:
    page = client.get("/articles", params={"limit": 1, "offset": 1}).json()
    assert len(page) == 1 and page[0]["id"] == "a-001"


def test_article_404_envelope(client: TestClient) -> None:
    response = client.get("/articles/ghost")
    assert response.status_code == 404
    body = response.json()
    assert body["error"]["reason"] == "article-not-found"
    assert "request_id" in body


def test_analytics_endpoints(client: TestClient) -> None:
    assert client.get("/analytics/top-sources").status_code == 200
    assert client.get("/analytics/per-day").status_code == 200
    assert client.get("/analytics/keywords").status_code == 200
    assert client.get("/analytics/keywords", params={"top": 1}).status_code == 200


def test_summarize_uses_fallback(client: TestClient) -> None:
    response = client.get("/summarize/a-001")
    assert response.status_code == 200
    body = response.json()
    assert body["method"] == "extractive" and body["text"]
