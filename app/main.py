"""FastAPI application exposing agent lifecycle endpoints."""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="My Green Career Agent",
    summary="API surface for health and readiness probes.",
    version="0.1.0",
)


@app.get("/healthz", tags=["system"], summary="Service liveness probe")
def healthz() -> dict[str, str]:
    """Return a simple status payload confirming the service is reachable."""

    return {"status": "ok"}


@app.get("/readyz", tags=["system"], summary="Service readiness probe")
def readyz() -> dict[str, str]:
    """Return readiness information for upstream health checks."""

    return {"status": "ready"}
