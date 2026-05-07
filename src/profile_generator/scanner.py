"""Project directory scanner with symlink detection and file limits.

This module implements directory scanning logic with security features and performance constraints.
"""

import os
from pathlib import Path

import structlog

from profile_generator.analyzers.factory import AnalyzerFactory
from profile_generator.models.config import Configuration
from profile_generator.models.project import Project
from profile_generator.utils.validators import validate_path

logger = structlog.get_logger()

# Source file whitelist (FR-019)
SOURCE_FILE_EXTENSIONS = {
    ".py",
    ".js",
    ".go",
    ".ts",
    ".jsx",
    ".tsx",
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".txt",
    ".sh",
    ".bash",
    ".css",
    ".html",
    ".xml",
    ".sql",
    ".graphql",
    ".proto",
}


class Scanner:
    """Directory scanner for project detection.

    Scans configured directories, detects projects, and enforces security and performance limits.
    Uses AnalyzerFactory (injected) for project type detection.

    Constraints:
        - File size: ≤200 LOC
        - Symlink detection: prevents circular references
        - File limit: 100k source files per project (whitelist approach)
        - Graceful error handling for inaccessible directories
    """

    def __init__(self, config: Configuration) -> None:
        """Initialize scanner with configuration.

        Args:
            config: Tool configuration with scan paths and limits
        """
        self.config = config
        self.factory = AnalyzerFactory()
        self._visited_inodes: set[tuple[int, int]] = set()  # (device, inode) pairs

    def scan(self) -> list[Project]:
        """Scan configured directories and detect projects.

        Returns:
            List of detected Project instances

        Raises:
            ValueError: If scan paths are invalid
        """
        projects: list[Project] = []

        logger.info("scan_started", paths=self.config.scan_paths)

        for scan_path in self.config.scan_paths:
            try:
                validated_path = validate_path(scan_path)
                logger.info("scanning_directory", path=str(validated_path))

                # Walk directory and detect projects
                detected = self._scan_directory(validated_path)
                projects.extend(detected)

            except (ValueError, OSError) as e:
                logger.warning(
                    "scan_path_error",
                    path=str(scan_path),
                    error=str(e),
                )
                continue

        logger.info("scan_completed", project_count=len(projects))
        return projects

    def _scan_directory(self, path: Path) -> list[Project]:
        """Scan a single directory for projects.

        Args:
            path: Directory to scan

        Returns:
            List of detected projects in this directory
        """
        projects: list[Project] = []

        try:
            # Check if this path is a project root
            analyzer = self.factory.create(path)
            if analyzer is not None:
                try:
                    project = analyzer.analyze(path)
                    projects.append(project)
                    logger.info(
                        "project_detected",
                        path=str(path),
                        type=project.type.value,
                        name=project.name,
                    )
                    # Don't recurse into detected projects
                    return projects
                except Exception as e:
                    logger.warning(
                        "project_analysis_failed",
                        path=str(path),
                        error=str(e),
                    )

            # Walk subdirectories
            for entry in path.iterdir():
                if not entry.is_dir():
                    continue

                # Skip hidden directories
                if entry.name.startswith("."):
                    continue

                # Check for symlinks
                if entry.is_symlink() and not self._is_safe_symlink(entry):
                    logger.warning("circular_symlink_detected", path=str(entry))
                    continue

                # Check file count limit before recursing
                file_count = self._count_source_files(entry)
                if file_count > self.config.max_files_per_project:
                    logger.warning(
                        "project_exceeds_file_limit",
                        path=str(entry),
                        count=file_count,
                        limit=self.config.max_files_per_project,
                    )
                    continue

                # Recurse into subdirectory
                try:
                    sub_projects = self._scan_directory(entry)
                    projects.extend(sub_projects)
                except PermissionError:
                    logger.warning("permission_denied", path=str(entry))
                    continue
                except OSError as e:
                    logger.warning("directory_error", path=str(entry), error=str(e))
                    continue

        except PermissionError:
            logger.warning("permission_denied", path=str(path))
        except OSError as e:
            logger.warning("directory_error", path=str(path), error=str(e))

        return projects

    def _is_safe_symlink(self, path: Path) -> bool:
        """Check if symlink is safe (no circular references).

        Uses inode tracking to detect circular symlinks.

        Args:
            path: Symlink path to check

        Returns:
            True if safe, False if circular reference detected
        """
        try:
            stat_info = path.stat()
            inode_key = (stat_info.st_dev, stat_info.st_ino)

            if inode_key in self._visited_inodes:
                return False

            self._visited_inodes.add(inode_key)
            return True

        except OSError:
            return False

    def _count_source_files(self, path: Path) -> int:
        """Count source files in directory (whitelist approach).

        Args:
            path: Directory to count files in

        Returns:
            Number of source files matching whitelist
        """
        count = 0
        try:
            for root, _dirs, files in os.walk(path, followlinks=False):
                for file_name in files:
                    file_path = Path(root) / file_name
                    if file_path.suffix.lower() in SOURCE_FILE_EXTENSIONS:
                        count += 1

                # Early exit if limit exceeded
                if count > self.config.max_files_per_project:
                    break

        except (PermissionError, OSError):
            pass

        return count
