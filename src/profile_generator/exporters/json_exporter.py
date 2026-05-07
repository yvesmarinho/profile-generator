"""JSON exporter with Pydantic validation and atomic writes.

This module implements JSON export compatible with yves-profile-site schema.
"""

import contextlib
import tempfile
from pathlib import Path

import structlog

from profile_generator.exporters.base import BaseExporter
from profile_generator.models.project import Project, ProjectsOutput

logger = structlog.get_logger()


class JSONExporter(BaseExporter):
    """JSON exporter with schema validation and atomic writes.

    Exports projects as JSON using Pydantic serialization with atomic file operations.

    Constraints:
        - File size: ≤200 LOC
        - Atomic writes: temp file + rename
        - Schema validation against ProjectsOutput model
        - Graceful error handling with structured logging
    """

    def __init__(self, tool_version: str) -> None:
        """Initialize JSON exporter.

        Args:
            tool_version: Tool version string for output metadata
        """
        self.tool_version = tool_version

    def export(self, projects: list[Project], output_path: Path) -> None:
        """Export projects to JSON file with atomic write.

        Args:
            projects: List of analyzed projects
            output_path: Absolute path for output JSON file

        Raises:
            ValueError: If projects list is empty or output_path invalid
            IOError: If file write fails
            PermissionError: If output directory is not writable
        """
        if not projects:
            msg = "Cannot export empty projects list"
            raise ValueError(msg)

        if not output_path.is_absolute():
            msg = f"Output path must be absolute: {output_path}"
            raise ValueError(msg)

        logger.info("json_export_started", output_path=str(output_path), count=len(projects))

        try:
            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Validate output schema
            output_data = ProjectsOutput(
                tool_version=self.tool_version,
                projects=projects,
            )

            # Serialize to JSON
            json_content = output_data.model_dump_json(indent=2)

            # Atomic write: temp file + rename
            self._atomic_write(output_path, json_content)

            logger.info(
                "json_export_success",
                output_path=str(output_path),
                project_count=len(projects),
                size_bytes=len(json_content),
            )

        except OSError as e:
            logger.exception(
                "json_export_failed",
                output_path=str(output_path),
                error=str(e),
            )
            raise

    def _atomic_write(self, output_path: Path, content: str) -> None:
        """Write content to file atomically using temp file + rename.

        Args:
            output_path: Final file path
            content: JSON content to write

        Raises:
            IOError: If write or rename fails
        """
        # Create temp file in same directory as output (for atomic rename)
        temp_fd, temp_path_str = tempfile.mkstemp(
            dir=output_path.parent,
            prefix=".tmp_",
            suffix=".json",
        )

        temp_path = Path(temp_path_str)

        try:
            # Write to temp file
            with open(temp_fd, "w", encoding="utf-8") as f:
                f.write(content)

            # Atomic rename
            temp_path.replace(output_path)

        except Exception:
            # Clean up temp file on error
            with contextlib.suppress(OSError):
                temp_path.unlink(missing_ok=True)
            raise
