"""Configuration models for profile_generator.

This module defines the Configuration model and related enums for tool settings.
"""

from enum import StrEnum
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class OutputFormat(StrEnum):
    """Output format options for portfolio generation."""

    JSON = "json"
    MARKDOWN = "markdown"
    BOTH = "both"


class LogLevel(StrEnum):
    """Logging level options."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class Configuration(BaseSettings):
    """Tool configuration with precedence: CLI > ENV > config.yaml > defaults.

    Environment variables use the prefix PROFILE_GEN_ (e.g., PROFILE_GEN_SCAN_PATHS).
    """

    scan_paths: list[Path] = Field(default_factory=lambda: [Path.cwd()])
    output_format: OutputFormat = OutputFormat.BOTH
    output_dir: Path = Path("./output")
    template_path: Path | None = None
    log_level: LogLevel = LogLevel.INFO
    dry_run: bool = False
    max_files_per_project: int = Field(default=100_000, ge=1, le=1_000_000)

    @field_validator("scan_paths")
    @classmethod
    def validate_scan_paths(cls, v: list[Path]) -> list[Path]:
        """Ensure all scan paths exist and are directories."""
        for path in v:
            if not path.exists():
                msg = f"Scan path does not exist: {path}"
                raise ValueError(msg)
            if not path.is_dir():
                msg = f"Scan path is not a directory: {path}"
                raise ValueError(msg)
        return v

    @field_validator("template_path")
    @classmethod
    def validate_template_path(cls, v: Path | None) -> Path | None:
        """Ensure template file exists and has correct extension."""
        if v is not None:
            if not v.exists():
                msg = f"Template file does not exist: {v}"
                raise ValueError(msg)
            if v.suffix != ".jinja2":
                msg = f"Template must have .jinja2 extension: {v}"
                raise ValueError(msg)
        return v

    model_config = {
        "env_prefix": "PROFILE_GEN_",
        "env_file": ".env",
        "case_sensitive": False,
    }
