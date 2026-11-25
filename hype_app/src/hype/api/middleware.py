"""Сквозная инфраструктура: request-id, единый error-envelope, CORS."""

from __future__ import annotations

import logging
import uuid
from typing import Callable, Awaitable

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from hype.config import Settings

logger = logging.getLogger("hype.api")


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Каждому запросу - идентификатор: в заголовке ответа и в request.state."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Any]]

    ) -> Any:
        request_id = request.headers.get("x-request-id") or uuid.uuid4().hex[:12]
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        return response


def install_middleware(app: FastAPI, settings: Settings) -> None:
    """Подключает CORS, request-id и глобальный error-envelope."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins or ["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIdMiddleware)

    @app.exception_handler(HTTPException)
    async def http_envelope(request: Request, exc: HTTPException) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "-")
        detail = exc.detail if isinstance(exc.detail, dict) else {"reason": str(exc.detail)}
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": detail, "request_id": request_id},
        )

    @app.exception_handler(Exception)
    async def error_envelope(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "-")
        logger.exception("unhandled error, request_id=%s", request_id)
        return JSONResponse(
            status_code=500,
            content={"error": {"type": type(exc).__name__, "message": "internal error"},
                     "request_id": request_id},
        )
