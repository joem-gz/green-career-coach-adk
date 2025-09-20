"""Tests for FastAPI health and readiness endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz_returns_ok() -> None:
    """The /healthz endpoint should report an ok status."""

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_returns_ready() -> None:
    """The /readyz endpoint should report a ready status."""

    response = client.get("/readyz")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
