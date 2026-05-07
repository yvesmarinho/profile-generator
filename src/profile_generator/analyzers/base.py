"""Base analyzer abstract class for project type detection and analysis.

This module defines the BaseAnalyzer ABC following the Strategy Pattern for
extensible project type detection.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from profile_generator.models.project import Project


class BaseAnalyzer(ABC):
    """Abstract base class for project analyzers.

    Analyzers detect and extract metadata from specific project types (Python, Node.js, Go).
    Each analyzer implements the Strategy Pattern for project-specific analysis logic.

    Constraints:
        - File size: ≤150 LOC (enforced by ruff)
        - All methods must have type hints (enforced by mypy --strict)
        - No side effects (read-only operations)

    Example:
        class PythonAnalyzer(BaseAnalyzer):
            def can_analyze(self, path: Path) -> bool:
                return (path / "pyproject.toml").exists()

            def analyze(self, path: Path) -> Project:
                # Extract metadata from pyproject.toml
                ...
    """

    @abstractmethod
    def can_analyze(self, path: Path) -> bool:
        """Determine if this analyzer can analyze the given project path.

        Args:
            path: Absolute path to project directory

        Returns:
            True if analyzer can handle this project type, False otherwise

        Raises:
            No exceptions should be raised (graceful detection)
        """
        ...

    @abstractmethod
    def analyze(self, path: Path) -> Project:
        """Analyze project and extract metadata.

        Args:
            path: Absolute path to project directory

        Returns:
            Project model with extracted metadata

        Raises:
            ValueError: If path is invalid or analysis fails
            FileNotFoundError: If required metadata files are missing
        """
        ...
