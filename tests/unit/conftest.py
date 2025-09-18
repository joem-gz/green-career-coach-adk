"""Pytest fixtures for domain model tests."""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest


@pytest.fixture()
def job_posting_data() -> dict[str, object]:
    """Sample payload representing a job posting."""

    return {
        "id": "job-123",
        "title": "Sustainability Analyst",
        "employer": "Green Future Ltd",
        "location": "London, UK",
        "salary": "£45,000 - £55,000",
        "url": "https://example.com/jobs/job-123",
        "source": "example-board",
        "posted_at": datetime(2025, 1, 15, 9, 30, tzinfo=timezone.utc),
        "description": "Drive sustainability initiatives across the organisation.",
        "skills": ["Analysis", "Stakeholder Engagement", "Carbon Accounting"],
    }


@pytest.fixture()
def apprenticeship_posting_data(job_posting_data: dict[str, object]) -> dict[str, object]:
    """Sample payload for an apprenticeship posting."""

    enriched = job_posting_data.copy()
    enriched.update(
        {
            "provider": "Green Training Consortium",
            "level": "Level 4",
            "standard_code": "ST0123",
        }
    )
    return enriched


@pytest.fixture()
def course_data() -> dict[str, object]:
    """Sample payload for a course offering."""

    return {
        "id": "course-456",
        "title": "Renewable Energy Fundamentals",
        "provider": "Eco Learning Hub",
        "mode": "online",
        "duration": "6 weeks",
        "location": "Remote",
        "url": "https://example.com/courses/course-456",
        "start_date": date(2025, 2, 1),
    }


@pytest.fixture()
def search_request_data() -> dict[str, object]:
    """Sample payload for a search request."""

    return {
        "query": "solar engineer",
        "location": "Manchester, UK",
        "filters": {
            "radius": 25.0,
            "contract": "permanent",
            "level": "mid",
            "keywords": ["solar", "photovoltaic"],
        },
    }
