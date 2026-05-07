"""Python project analyzer with pyproject.toml, setup.py, and requirements.txt support.

This module implements Python project detection and metadata extraction.
"""

import re
import tomllib
from pathlib import Path

import structlog

from profile_generator.analyzers.base import BaseAnalyzer
from profile_generator.models.project import (
    Project,
    ProjectType,
    Statistics,
    TechCategory,
    Technology,
)

logger = structlog.get_logger()


class PythonAnalyzer(BaseAnalyzer):
    """Python project analyzer.

    Detects Python projects and extracts metadata from:
    - pyproject.toml (preferred)
    - setup.py (fallback)
    - requirements.txt (dependencies)
    - README.md (description)

    Constraints:
        - File size: ≤200 LOC
        - Graceful handling of malformed files
        - Fallback chain: pyproject.toml → setup.py → requirements.txt
    """

    def can_analyze(self, path: Path) -> bool:
        """Determine if this is a Python project.

        Checks for presence of:
        - pyproject.toml (preferred)
        - setup.py (fallback)
        - requirements.txt (minimal)

        Args:
            path: Absolute path to project directory

        Returns:
            True if Python project detected
        """
        return (
            (path / "pyproject.toml").exists()
            or (path / "setup.py").exists()
            or (path / "requirements.txt").exists()
        )

    def analyze(self, path: Path) -> Project:
        """Analyze Python project and extract metadata.

        Args:
            path: Absolute path to project directory

        Returns:
            Project model with extracted metadata

        Raises:
            ValueError: If analysis fails or required files missing
        """
        logger.debug("analyzing_python_project", path=str(path))

        # Extract metadata from pyproject.toml or setup.py
        name = path.name
        description: str | None = None
        python_version: str | None = None
        technologies: list[Technology] = []

        # Try pyproject.toml first
        if (path / "pyproject.toml").exists():
            try:
                metadata = self._parse_pyproject_toml(path / "pyproject.toml")
                name = metadata.get("name", name)  # type: ignore[assignment]
                description = metadata.get("description")  # type: ignore[assignment]
                python_version = metadata.get("python_version")  # type: ignore[assignment]
                technologies.extend(metadata.get("dependencies", []))  # type: ignore[arg-type]
            except Exception as e:
                logger.warning("pyproject_toml_parse_failed", path=str(path), error=str(e))

        # Fallback to setup.py
        elif (path / "setup.py").exists():
            try:
                metadata = self._parse_setup_py(path / "setup.py")  # type: ignore[assignment]
                name = metadata.get("name", name)  # type: ignore[assignment]
                description = metadata.get("description")  # type: ignore[assignment]
            except Exception as e:
                logger.warning("setup_py_parse_failed", path=str(path), error=str(e))

        # Parse requirements.txt for dependencies
        if (path / "requirements.txt").exists():
            try:
                deps = self._parse_requirements_txt(path / "requirements.txt")
                technologies.extend(deps)
            except Exception as e:
                logger.warning("requirements_txt_parse_failed", path=str(path), error=str(e))

        # Try to extract description from README.md
        if description is None and (path / "README.md").exists():
            description = self._extract_readme_description(path / "README.md")

        # Add Python language as primary technology
        python_tech = Technology(
            name="Python",
            version=python_version,
            category=TechCategory.LANGUAGE,
        )
        technologies.insert(0, python_tech)

        # Calculate statistics (placeholder - will be implemented with git/stats modules)
        statistics = Statistics(
            total_loc=0,
            loc_by_language={"Python": 0},
            file_count=1,
        )

        return Project(
            name=name,
            description=description,
            path=path,
            type=ProjectType.PYTHON,
            technologies=technologies,
            repository=None,  # Will be added by git module
            statistics=statistics,
        )

    def _parse_pyproject_toml(self, toml_path: Path) -> dict[str, object]:
        """Parse pyproject.toml for metadata.

        Args:
            toml_path: Path to pyproject.toml

        Returns:
            Dictionary with name, description, python_version, dependencies
        """
        with toml_path.open("rb") as f:
            data = tomllib.load(f)

        project = data.get("project", {})
        metadata: dict[str, object] = {}

        metadata["name"] = project.get("name")
        metadata["description"] = project.get("description")

        # Extract Python version requirement
        requires_python = project.get("requires-python")
        if requires_python:
            # Extract version like ">=3.12" → "3.12+"
            match = re.search(r"(\d+\.\d+)", str(requires_python))
            if match:
                metadata["python_version"] = f"{match.group(1)}+"

        # Extract dependencies
        dependencies_list: list[Technology] = []
        for dep in project.get("dependencies", []):
            dep_name = str(dep).split("[")[0].split(">=")[0].split("==")[0].strip()
            dependencies_list.append(
                Technology(
                    name=dep_name,
                    version=None,
                    category=TechCategory.LIBRARY,
                ),
            )

        metadata["dependencies"] = dependencies_list
        return metadata

    def _parse_setup_py(self, setup_path: Path) -> dict[str, str | None]:
        """Parse setup.py for metadata (basic extraction).

        Args:
            setup_path: Path to setup.py

        Returns:
            Dictionary with name and description
        """
        content = setup_path.read_text(encoding="utf-8")

        metadata: dict[str, str | None] = {}

        # Extract name from setup(name="...")
        name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
        if name_match:
            metadata["name"] = name_match.group(1)

        # Extract description from setup(description="...")
        desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
        if desc_match:
            metadata["description"] = desc_match.group(1)

        return metadata

    def _parse_requirements_txt(self, req_path: Path) -> list[Technology]:
        """Parse requirements.txt for dependencies.

        Args:
            req_path: Path to requirements.txt

        Returns:
            List of Technology instances for dependencies
        """
        dependencies: list[Technology] = []
        content = req_path.read_text(encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Extract package name (before ==, >=, etc.)
            dep_name = line.split("==")[0].split(">=")[0].split("<=")[0].strip()
            dependencies.append(
                Technology(
                    name=dep_name,
                    version=None,
                    category=TechCategory.LIBRARY,
                ),
            )

        return dependencies

    def _extract_readme_description(self, readme_path: Path) -> str | None:
        """Extract project description from README.md (first paragraph).

        Args:
            readme_path: Path to README.md

        Returns:
            First paragraph of README or None
        """
        try:
            content = readme_path.read_text(encoding="utf-8")

            # Remove markdown headers and find first paragraph
            lines = content.splitlines()
            description_lines: list[str] = []

            for line in lines:
                stripped = line.strip()
                # Skip headers and empty lines
                if not stripped or stripped.startswith("#"):
                    continue
                # Break on second paragraph
                if description_lines and not stripped:
                    break
                description_lines.append(stripped)

            return " ".join(description_lines[:10])  # Limit to first 10 lines

        except Exception:
            return None
