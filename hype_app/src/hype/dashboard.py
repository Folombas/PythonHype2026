"""Streamlit-дашборд FinPulse Hype.

Запуск: uv run streamlit run src/hype/dashboard.py
"""

from __future__ import annotations

import polars as pl
import streamlit as st

from hype.analytics import keyword_score, per_day, top_sources
from hype.config import get_settings
from hype.ingest import load_articles
from hype.models import QueryParams
from hype.storage import ArticleRepository

st.set_page_config(page_title="FinPulse Hype", page_icon="📈", layout="wide")
st.title("📈 FinPulse Hype")
st.caption("Хайповый дашборд над пайплайном новостей: Polars + DuckDB")

settings = get_settings()
db_path = st.sidebar.text_input("База DuckDB", settings.db_path)
seed_path = st.sidebar.text_input("Seed JSON", settings.seed_path)


@st.cache_resource
def open_repo(path: str) -> ArticleRepository:
    """Репозиторий как ресурс сессии."""
    return ArticleRepository(path)


repo = open_repo(db_path)
if repo.count() == 0:
    st.info("База пуста. Залей демо-датасет одной кнопкой (данные синтетические).")
    if st.button(f"Залить seed из {seed_path}"):
        repo.upsert_many(load_articles(seed_path))
        st.rerun()
    st.stop()

all_articles = repo.query(QueryParams(limit=500))
sources = ["(все)"] + sorted({a.source for a in all_articles})
source = st.sidebar.selectbox("Источник", sources)
limit = st.sidebar.slider("Сколько статей", 10, 500, 100)
articles = repo.query(QueryParams(source=None if source == "(все)" else source, limit=limit))
st.caption(f"Выбрано статей: {len(articles)} из {len(all_articles)}")

if not articles:
    st.warning("Под фильтры ничего не нашлось.")
    st.stop()

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Топ источников")
    st.bar_chart(pl.DataFrame(top_sources(articles, 10)).to_pandas().set_index("source")["count"])
with col2:
    st.subheader("Публикации по дням")
    st.line_chart(pl.DataFrame(per_day(articles)).to_pandas().set_index("day")["count"])
with col3:
    st.subheader("Ключевые слова")
    st.bar_chart(pl.DataFrame(keyword_score(articles, 10)).to_pandas().set_index("keyword")["score"])

st.subheader("Статьи")
st.dataframe(
    pl.DataFrame(
        [
            {
                "id": a.id,
                "дата": f"{a.published_at:%Y-%m-%d %H:%M}",
                "источник": a.source,
                "заголовок": a.title,
                "ключевые слова": ", ".join(a.keywords),
            }
            for a in articles
        ]
    ).to_pandas(),
    use_container_width=True,
    hide_index=True,
)

with st.expander("🤖 AI-суммаризация", expanded=False):
    options = {a.id: f"{a.id} · {a.title[:70]}" for a in articles}
    picked = st.selectbox("Статья", list(options), format_func=lambda i: options[i])
    if st.button("Суммаризировать"):
        from hype.api.app import build_summarizer

        by_id = {a.id: a for a in articles}
        summarizer = build_summarizer(settings)
        with st.spinner("Думаю..."):
            result = summarizer.summarize(by_id[picked])
        st.write(f"**[{result.method}]** {result.text}")
