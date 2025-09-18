"""Tests for Pydantic domain models and schema generation utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from app.models import (
    ApprenticeshipPosting,
    Course,
    JobPosting,
    SearchRequest,
    SearchResponse,
    SourceBreakdown,
)
from scripts.generate_schema import build_schema, write_schema


def test_job_posting_defaults() -> None:
    """JobPosting should provide sensible defaults for optional fields."""

    posting = JobPosting(
        id="job-001",
        title="Net Zero Consultant",
        employer="Green Careers",
        location="Bristol, UK",
        url="https://example.com/job-001",
        source="internal",
    )

    assert posting.description == ""
    assert posting.skills == []
    assert posting.salary is None
    assert posting.posted_at is None


def test_job_posting_from_fixture(job_posting_data: dict[str, Any]) -> None:
    """JobPosting should load data from the fixture payload."""

    posting = JobPosting(**job_posting_data)

    assert posting.employer == "Green Future Ltd"
    assert posting.skills == [
        "Analysis",
        "Stakeholder Engagement",
        "Carbon Accounting",
    ]
    assert posting.posted_at is not None


def test_apprenticeship_posting_includes_extension(
    apprenticeship_posting_data: dict[str, Any],
) -> None:
    """ApprenticeshipPosting extends the base job posting fields."""

    apprenticeship = ApprenticeshipPosting(**apprenticeship_posting_data)

    assert apprenticeship.provider == "Green Training Consortium"
    assert apprenticeship.level == "Level 4"
    assert apprenticeship.standard_code == "ST0123"


def test_course_model(course_data: dict[str, Any]) -> None:
    """Courses should accept optional metadata while enforcing required fields."""

    course = Course(**course_data)

    assert course.mode == "online"
    assert course.duration == "6 weeks"
    assert course.start_date is not None


def test_search_request_defaults(search_request_data: dict[str, Any]) -> None:
    """SearchRequest should coerce nested filter structures correctly."""

    request = SearchRequest(**search_request_data)

    assert request.filters.radius == pytest.approx(25.0)
    assert request.filters.keywords == ["solar", "photovoltaic"]


def test_search_response_generic(job_posting_data: dict[str, Any]) -> None:
    """SearchResponse should support generic typing across resources."""

    response = SearchResponse[JobPosting](
        items=[JobPosting(**job_posting_data)],
        total=1,
        source_breakdown=[SourceBreakdown(source="example-board", count=1)],
    )

    assert response.total == 1
    assert response.items[0].id == "job-123"
    assert response.source_breakdown[0].count == 1


def test_build_schema_contains_expected_models() -> None:
    """Schema builder should expose all registered models."""

    schema = build_schema()

    assert set(schema) >= {
        "JobPosting",
        "ApprenticeshipPosting",
        "Course",
        "SearchRequest",
        "SearchResponse[JobPosting]",
    }
    assert "properties" in schema["JobPosting"]


def test_write_schema_to_disk(tmp_path: Path) -> None:
    """write_schema should persist the combined schema as JSON."""

    output_path = tmp_path / "schemas" / "openapi.json"
    path = write_schema(output_path)

    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["Course"]["title"] == "Course"
