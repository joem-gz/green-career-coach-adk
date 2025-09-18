"""Domain models for career search entities."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class JobPosting(BaseModel):
    """Represents a single job posting sourced from an external provider."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., description="Unique identifier for the job posting.")
    title: str = Field(..., description="Job title or role name.")
    employer: str = Field(..., description="Name of the hiring organization.")
    location: str = Field(..., description="Primary location of the job opportunity.")
    salary: str | None = Field(
        default=None,
        description="Salary or compensation description when available.",
    )
    url: HttpUrl = Field(..., description="Canonical URL to the job posting detail page.")
    source: str = Field(..., description="Identifier for the system or board providing the job.")
    posted_at: datetime | None = Field(
        default=None, description="Timestamp indicating when the job was posted."
    )
    description: str = Field(
        default="",
        description="Full job description including responsibilities and qualifications.",
    )
    skills: list[str] = Field(
        default_factory=list,
        description="Key skills or keywords associated with the job posting.",
    )


class ApprenticeshipPosting(JobPosting):
    """Extends a job posting with apprenticeship specific metadata."""

    provider: str = Field(..., description="Training provider delivering the apprenticeship program.")
    level: str | None = Field(
        default=None,
        description="Apprenticeship level as defined by the awarding body.",
    )
    standard_code: str | None = Field(
        default=None,
        description="Standard code identifying the apprenticeship framework.",
    )


class Course(BaseModel):
    """Describes an educational course relevant to career development."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., description="Unique identifier for the course.")
    title: str = Field(..., description="Official course title.")
    provider: str = Field(..., description="Organization delivering the course.")
    mode: str = Field(
        default="in-person",
        description="Delivery mode such as in-person, online, or hybrid.",
    )
    duration: str | None = Field(
        default=None,
        description="Duration or time commitment summary for the course.",
    )
    location: str | None = Field(
        default=None,
        description="Location where the course is offered, if applicable.",
    )
    url: HttpUrl = Field(..., description="URL with detailed course information and enrollment instructions.")
    start_date: date | None = Field(
        default=None,
        description="Start date for the next available course cohort when known.",
    )


class SearchFilters(BaseModel):
    """Filters that can be applied to a search request."""

    model_config = ConfigDict(extra="forbid")

    radius: float | None = Field(
        default=None, ge=0, description="Search radius in kilometers from the target location."
    )
    contract: str | None = Field(
        default=None,
        description="Preferred contract type such as permanent, temporary, or apprenticeship.",
    )
    level: str | None = Field(
        default=None,
        description="Desired seniority, qualification, or apprenticeship level filter.",
    )
    keywords: list[str] = Field(
        default_factory=list,
        description="Additional free-form keywords to refine the search results.",
    )


class SearchRequest(BaseModel):
    """Represents a structured request for discovering opportunities."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(..., description="Primary free-text query for the search.")
    location: str | None = Field(
        default=None,
        description="Location string to anchor the search, such as a city or postal code.",
    )
    filters: SearchFilters = Field(
        default_factory=SearchFilters,
        description="Optional filters applied to shape the search results.",
    )


class SourceBreakdown(BaseModel):
    """Aggregated information about result counts per data source."""

    model_config = ConfigDict(extra="forbid")

    source: str = Field(..., description="Identifier of the upstream data provider.")
    count: int = Field(
        default=0,
        ge=0,
        description="Number of results contributed by the provider.",
    )


T = TypeVar("T", bound=BaseModel)


class SearchResponse(BaseModel, Generic[T]):
    """Generic search response containing results of a specific resource type."""

    model_config = ConfigDict(extra="forbid")

    items: list[T] = Field(
        default_factory=list,
        description="Collection of resources that satisfy the search request.",
    )
    total: int = Field(
        default=0,
        ge=0,
        description="Total number of resources available for the provided query and filters.",
    )
    source_breakdown: list[SourceBreakdown] = Field(
        default_factory=list,
        description="Breakdown of result counts grouped by source provider.",
    )
    debug: dict[str, Any] | None = Field(
        default=None,
        description="Optional diagnostic metadata useful for debugging searches.",
    )


__all__ = [
    "ApprenticeshipPosting",
    "Course",
    "JobPosting",
    "SearchFilters",
    "SearchRequest",
    "SearchResponse",
    "SourceBreakdown",
]
