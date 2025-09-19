# agents.md v1

## Purpose

Backend ADK agent service for Green Skills Coach in a **hybrid Dialogflow CX ↔ ADK** setup. CX routes and handles UI; ADK does tool-using reasoning.

## Runtime & region

Python 3.11, FastAPI, ADK. Default region: `europe-west2`.

## Contracts

* **Schemas (Pydantic v2):** `JobPosting`, `ApprenticeshipPosting`, `Course`, `SearchRequest{query,location,filters}`, `SearchResponse[T]{items,total,source_breakdown,debug?}`.
* **Adapters (plugins):**
  `JobSource.search(req) -> SearchResponse[JobPosting]`
  `ApprenticeshipSource.search(req) -> …`
  `CourseSource.search(req) -> …`
* **HTTP:**
  `GET /healthz`, `GET /readyz`
  `POST /agent/run` (JWT/IAM)
  `POST /cx/handoff` (maps CX parameters → `SearchRequest`, returns CX cards + canonical `payload`).
* **Tools (first wave):** `jobs.search`, `apprenticeships.search`, `courses.search`, `cv.parse`, `jd.parse`, `cv.tailor`, `cover_letter.compose`, `search.fallback`.

## Testing

Unit, integration (fan-out & dedupe), **golden conversation tests** (deterministic). **Determinism for tests:** `temperature=0.0`, fixed `seed`.

## Quality & CI

ruff, black, mypy, pytest (coverage ≥ 85%), bandit, pip-audit. Tag → Cloud Run deploy (staging → prod).

## Observability & safety

JSON logs (request\_id, route, latency\_ms, tool\_name, error); metrics (reqs, errors, P95). Circuit breakers per source. No scraping; fallback uses approved APIs only.

## Definition of Done

Contracts unchanged (or versioned), tests added/updated, CI green, docs updated.
