"""Project domain models for profile_generator.

This module defines the core domain entities: Project, Technology, Repository, Statistics.
"""

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator


class TechCategory(StrEnum):
    """Technology category classification."""

    LANGUAGE = "language"
    FRAMEWORK = "framework"
    LIBRARY = "library"
    TOOL = "tool"
    RUNTIME = "runtime"


class ProjectType(StrEnum):
    """Detected project type classification."""

    PYTHON = "python"
    NODEJS = "nodejs"
    GO = "go"
    UNKNOWN = "unknown"


class Technology(BaseModel):
    """Technology/framework/library used in a project.

    Technologies are immutable value objects that represent a detected technology
    with optional version information.
    """

    name: str = Field(min_length=1, max_length=100)
    version: str | None = None
    category: TechCategory

    model_config = {
        "frozen": True,  # Immutable after creation
    }


class Contributor(BaseModel):
    """Top contributor by commit count.

    Used in Repository to track the top 5 contributors to a project.
    """

    name: str = Field(min_length=1, max_length=200)
    commit_count: int = Field(ge=1)


class Repository(BaseModel):
    """Git repository metadata.

    Contains information about the repository, including remote URL, branch,
    commit statistics, and top contributors.
    """

    url: str | None = None
    branch: str = Field(min_length=1, max_length=200)
    commit_count: int = Field(ge=1)
    top_contributors: list[Contributor] = Field(max_length=5)
    last_commit_date: datetime
    tags: list[str] = Field(default_factory=list)

    @field_validator("top_contributors")
    @classmethod
    def validate_contributors_sorted(cls, v: list[Contributor]) -> list[Contributor]:
        """Ensure contributors are sorted by commit count descending."""
        if v != sorted(v, key=lambda c: c.commit_count, reverse=True):
            msg = "Contributors must be sorted by commit_count descending"
            raise ValueError(msg)
        return v

    @field_validator("last_commit_date")
    @classmethod
    def validate_past_date(cls, v: datetime) -> datetime:
        """Ensure last commit date is not in the future."""
        if v > datetime.now(tz=UTC):
            msg = "Last commit date cannot be in the future"
            raise ValueError(msg)
        return v


class Statistics(BaseModel):
    """Code statistics for a project.

    Contains aggregated statistics about source code, including lines of code,
    file counts, and optional test coverage.
    """

    total_loc: int = Field(ge=0)
    loc_by_language: dict[str, int] = Field(min_length=1)
    file_count: int = Field(ge=1)
    test_coverage: float | None = Field(default=None, ge=0.0, le=100.0)

    @field_validator("loc_by_language")
    @classmethod
    def validate_loc_counts(cls, v: dict[str, int]) -> dict[str, int]:
        """Verify all language LOCs are non-negative."""
        for lang, count in v.items():
            if count < 0:
                msg = f"LOC for {lang} cannot be negative: {count}"
                raise ValueError(msg)
        return v


class Project(BaseModel):
    """Root entity representing a scanned project.

    Project is the aggregate root that contains all project metadata,
    including technologies, repository information, and statistics.
    """

    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    path: Path
    type: ProjectType
    technologies: list[Technology] = Field(min_length=1)
    repository: Repository | None = None
    statistics: Statistics

    @field_validator("path")
    @classmethod
    def validate_path_absolute(cls, v: Path) -> Path:
        """Ensure project path is absolute and exists."""
        if not v.is_absolute():
            msg = f"Project path must be absolute: {v}"
            raise ValueError(msg)
        if not v.exists():
            msg = f"Project path does not exist: {v}"
            raise ValueError(msg)
        return v

    def model_dump_json(self, **kwargs: Any) -> str:
        """Custom JSON serialization with Path handling.

        Converts Path objects to strings and includes None values for optional fields.
        """
        return super().model_dump_json(
            exclude_none=False,
            by_alias=True,
            **kwargs,
        )


class ProjectsOutput(BaseModel):
    """Output schema for JSON export compatible with yves-profile-site.

    This model represents the complete output structure with metadata
    and a list of scanned projects.
    """

    generated_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    tool_version: str
    projects: list[Project]

    def model_dump_json(self, **kwargs: Any) -> str:
        """Custom JSON serialization for output schema."""
        return super().model_dump_json(
            exclude_none=False,
            by_alias=True,
            **kwargs,
        )
