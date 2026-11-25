FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /usr/local/bin/uvx

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml ./
RUN uv sync --no-install-project --no-dev

COPY src ./src
COPY data ./data
RUN uv sync --no-dev

EXPOSE 8000 8501

CMD ["uv", "run", "--no-dev", "uvicorn", "hype.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
