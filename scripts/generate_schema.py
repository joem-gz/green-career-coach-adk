#!/usr/bin/env python3
"""Generate a combined JSON Schema document for the project's domain models."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from app.models import (
    ApprenticeshipPosting,
    Course,
    JobPosting,
    SearchRequest,
    SearchResponse,
)

SCHEMA_MODELS: dict[str, type[BaseModel]] = {
    "JobPosting": JobPosting,
    "ApprenticeshipPosting": ApprenticeshipPosting,
    "Course": Course,
    "SearchRequest": SearchRequest,
    "SearchResponse[JobPosting]": SearchResponse[JobPosting],
    "SearchResponse[ApprenticeshipPosting]": SearchResponse[ApprenticeshipPosting],
    "SearchResponse[Course]": SearchResponse[Course],
}


def build_schema() -> dict[str, Any]:
    """Assemble JSON schema definitions for each registered model."""

    return {name: model.model_json_schema() for name, model in SCHEMA_MODELS.items()}


def write_schema(output_path: Path) -> Path:
    """Write the combined schema to the requested path.

    Args:
        output_path: Destination path for the JSON schema document.

    Returns:
        The path where the schema was written.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    schema = build_schema()
    output_path.write_text(
        json.dumps(schema, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    """Generate schemas and save them under the repository's `schemas` directory."""

    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "schemas" / "openapi_schemas.json"
    path = write_schema(output_path)
    print(f"Wrote schema to {path}")


if __name__ == "__main__":
    main()
