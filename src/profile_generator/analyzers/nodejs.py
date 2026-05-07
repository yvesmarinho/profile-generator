"""Node.js project analyzer with package.json support.

This module implements Node.js project detection and metadata extraction.
"""

import json
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


class NodeJSAnalyzer(BaseAnalyzer):
    """Node.js project analyzer.

    Detects Node.js projects and extracts metadata from:
    - package.json (required)
    - package-lock.json or yarn.lock (package manager detection)
    - README.md (description)

    Constraints:
        - File size: ≤200 LOC
        - Graceful handling of malformed JSON
        - Distinguishes runtime vs dev dependencies
    """

    def can_analyze(self, path: Path) -> bool:
        """Determine if this is a Node.js project.

        Args:
            path: Absolute path to project directory

        Returns:
            True if package.json exists
        """
        return (path / "package.json").exists()

    def analyze(self, path: Path) -> Project:
        """Analyze Node.js project and extract metadata.

        Args:
            path: Absolute path to project directory

        Returns:
            Project model with extracted metadata

        Raises:
            ValueError: If analysis fails or package.json invalid
        """
        logger.debug("analyzing_nodejs_project", path=str(path))

        # Parse package.json
        try:
            with (path / "package.json").open(encoding="utf-8") as f:
                package_data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.exception("package_json_parse_failed", path=str(path), error=str(e))
            msg = f"Failed to parse package.json: {e}"
            raise ValueError(msg) from e

        # Extract basic metadata
        name = package_data.get("name", path.name)
        description = package_data.get("description")
        package_data.get("version")

        # Detect package manager
        package_manager = self._detect_package_manager(path)

        # Extract technologies
        technologies: list[Technology] = []

        # Add Node.js runtime
        node_version = package_data.get("engines", {}).get("node")
        technologies.append(
            Technology(
                name="Node.js",
                version=node_version,
                category=TechCategory.RUNTIME,
            ),
        )

        # Add package manager as tool
        if package_manager:
            technologies.append(
                Technology(
                    name=package_manager,
                    version=None,
                    category=TechCategory.TOOL,
                ),
            )

        # Extract dependencies (runtime)
        dependencies = package_data.get("dependencies", {})
        for dep_name, dep_version in dependencies.items():
            technologies.append(
                Technology(
                    name=dep_name,
                    version=str(dep_version).lstrip("^~"),
                    category=TechCategory.LIBRARY,
                ),
            )

        # Extract devDependencies (tools)
        dev_dependencies = package_data.get("devDependencies", {})
        for dep_name, dep_version in dev_dependencies.items():
            technologies.append(
                Technology(
                    name=dep_name,
                    version=str(dep_version).lstrip("^~"),
                    category=TechCategory.TOOL,
                ),
            )

        # Try to extract description from README.md if not in package.json
        if description is None and (path / "README.md").exists():
            description = self._extract_readme_description(path / "README.md")

        # Calculate statistics (placeholder)
        statistics = Statistics(
            total_loc=0,
            loc_by_language={"JavaScript": 0},
            file_count=1,
        )

        return Project(
            name=name,
            description=description,
            path=path,
            type=ProjectType.NODEJS,
            technologies=technologies,
            repository=None,  # Will be added by git module
            statistics=statistics,
        )

    def _detect_package_manager(self, path: Path) -> str | None:
        """Detect package manager from lock files.

        Args:
            path: Project directory

        Returns:
            Package manager name or None
        """
        if (path / "package-lock.json").exists():
            return "npm"
        if (path / "yarn.lock").exists():
            return "yarn"
        if (path / "pnpm-lock.yaml").exists():
            return "pnpm"
        return None

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
