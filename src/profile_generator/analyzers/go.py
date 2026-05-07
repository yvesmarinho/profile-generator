"""Go project analyzer with go.mod support.

This module implements Go project detection and metadata extraction.
"""

import re
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


class GoAnalyzer(BaseAnalyzer):
    """Go project analyzer.

    Detects Go projects and extracts metadata from:
    - go.mod (preferred for modules)
    - Directory structure (fallback for pre-modules projects)
    - README.md (description)

    Constraints:
        - File size: ≤200 LOC
        - Graceful handling of malformed go.mod
        - Support for modules and pre-modules projects
    """

    def can_analyze(self, path: Path) -> bool:
        """Determine if this is a Go project.

        Args:
            path: Absolute path to project directory

        Returns:
            True if go.mod exists or .go files found
        """
        if (path / "go.mod").exists():
            return True

        # Fallback: check for .go files in root directory
        return any(path.glob("*.go"))

    def analyze(self, path: Path) -> Project:
        """Analyze Go project and extract metadata.

        Args:
            path: Absolute path to project directory

        Returns:
            Project model with extracted metadata

        Raises:
            ValueError: If analysis fails
        """
        logger.debug("analyzing_go_project", path=str(path))

        name = path.name
        description: str | None = None
        go_version: str | None = None
        technologies: list[Technology] = []

        # Parse go.mod if present
        if (path / "go.mod").exists():
            try:
                metadata = self._parse_go_mod(path / "go.mod")
                module_name_obj = metadata.get("module_name", name)
                if isinstance(module_name_obj, str):
                    name = module_name_obj.split("/")[-1]  # Use last part
                go_version = metadata.get("go_version")  # type: ignore[assignment]
                technologies.extend(metadata.get("dependencies", []))  # type: ignore[arg-type]
            except Exception as e:
                logger.warning("go_mod_parse_failed", path=str(path), error=str(e))

        # Try to extract description from README.md
        if (path / "README.md").exists():
            description = self._extract_readme_description(path / "README.md")

        # Add Go language as primary technology
        go_tech = Technology(
            name="Go",
            version=go_version,
            category=TechCategory.LANGUAGE,
        )
        technologies.insert(0, go_tech)

        # Calculate statistics (placeholder)
        statistics = Statistics(
            total_loc=0,
            loc_by_language={"Go": 0},
            file_count=1,
        )

        return Project(
            name=name,
            description=description,
            path=path,
            type=ProjectType.GO,
            technologies=technologies,
            repository=None,  # Will be added by git module
            statistics=statistics,
        )

    def _parse_go_mod(self, go_mod_path: Path) -> dict[str, object]:
        """Parse go.mod for metadata.

        Args:
            go_mod_path: Path to go.mod

        Returns:
            Dictionary with module_name, go_version, dependencies
        """
        content = go_mod_path.read_text(encoding="utf-8")
        metadata: dict[str, object] = {}

        # Extract module name
        module_match = re.search(r"^module\s+(.+)$", content, re.MULTILINE)
        if module_match:
            metadata["module_name"] = module_match.group(1).strip()

        # Extract Go version
        go_match = re.search(r"^go\s+(\d+\.\d+)", content, re.MULTILINE)
        if go_match:
            metadata["go_version"] = go_match.group(1)

        # Extract dependencies from require blocks
        dependencies: list[Technology] = []

        # Single-line requires: require github.com/foo/bar v1.2.3
        for match in re.finditer(r"^require\s+(\S+)\s+v?(\S+)", content, re.MULTILINE):
            dep_name = match.group(1)
            dep_version = match.group(2)
            dependencies.append(
                Technology(
                    name=dep_name,
                    version=dep_version,
                    category=TechCategory.LIBRARY,
                ),
            )

        # Multi-line requires: require ( ... )
        require_block_match = re.search(
            r"require\s+\(\s*\n(.*?)\n\s*\)",
            content,
            re.MULTILINE | re.DOTALL,
        )
        if require_block_match:
            for line in require_block_match.group(1).splitlines():
                line = line.strip()
                if not line or line.startswith("//"):
                    continue

                # Parse: github.com/foo/bar v1.2.3
                parts = line.split()
                if len(parts) >= 2:  # noqa: PLR2004
                    dep_name = parts[0]
                    dep_version = parts[1].lstrip("v")
                    dependencies.append(
                        Technology(
                            name=dep_name,
                            version=dep_version,
                            category=TechCategory.LIBRARY,
                        ),
                    )

        metadata["dependencies"] = dependencies
        return metadata

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
