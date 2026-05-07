"""Base exporter abstract class for portfolio output generation.

This module defines the BaseExporter ABC following the Strategy Pattern for
extensible output format generation.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from profile_generator.models.project import Project


class BaseExporter(ABC):
    """Abstract base class for project exporters.

    Exporters generate output files in specific formats (JSON, Markdown) from scanned projects.
    Each exporter implements the Strategy Pattern for format-specific generation logic.

    Constraints:
        - File size: ≤150 LOC (enforced by ruff)
        - All methods must have type hints (enforced by mypy --strict)
        - Atomic file writes (temp file + rename)
        - Graceful error handling with structured logging

    Example:
        class JSONExporter(BaseExporter):
            def export(self, projects: list[Project], output_path: Path) -> None:
                # Generate JSON output using Pydantic serialization
                ...
    """

    @abstractmethod
    def export(self, projects: list[Project], output_path: Path) -> None:
        """Export projects to output file in specific format.

        Args:
            projects: List of analyzed projects to export
            output_path: Absolute path for output file

        Raises:
            ValueError: If projects list is empty or output_path is invalid
            IOError: If file write fails
            PermissionError: If output directory is not writable

        Note:
            Implementations must use atomic writes (temp file + rename) to prevent
            partial writes on failure.
        """
        ...
