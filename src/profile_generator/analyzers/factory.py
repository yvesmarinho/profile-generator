"""Analyzer factory with confidence-based project type detection.

This module implements the Factory Pattern for analyzer creation using hybrid confidence scoring.
"""

from pathlib import Path

import structlog

from profile_generator.analyzers.base import BaseAnalyzer
from profile_generator.analyzers.go import GoAnalyzer
from profile_generator.analyzers.nodejs import NodeJSAnalyzer
from profile_generator.analyzers.python import PythonAnalyzer
from profile_generator.models.project import ProjectType

logger = structlog.get_logger()

# Confidence scoring weights from research.md Decision 2
DETECTION_WEIGHTS = {
    ProjectType.PYTHON: {
        "pyproject.toml": 50,
        "setup.py": 30,
        "requirements.txt": 20,
    },
    ProjectType.NODEJS: {
        "package.json": 50,
    },
    ProjectType.GO: {
        "go.mod": 50,
    },
}

# Confidence threshold (40 points minimum)
CONFIDENCE_THRESHOLD = 40


class ProjectDetector:
    """Project type detector using confidence scoring.

    Implements hybrid confidence-based detection from research.md Decision 2.
    """

    @staticmethod
    def calculate_confidence(path: Path) -> dict[ProjectType, int]:
        """Calculate confidence scores for each project type.

        Args:
            path: Project directory path

        Returns:
            Dictionary mapping ProjectType to confidence score
        """
        scores: dict[ProjectType, int] = {
            ProjectType.PYTHON: 0,
            ProjectType.NODEJS: 0,
            ProjectType.GO: 0,
        }

        # Calculate Python confidence
        for signal, weight in DETECTION_WEIGHTS[ProjectType.PYTHON].items():
            if (path / signal).exists():
                scores[ProjectType.PYTHON] += weight

        # Calculate Node.js confidence
        for signal, weight in DETECTION_WEIGHTS[ProjectType.NODEJS].items():
            if (path / signal).exists():
                scores[ProjectType.NODEJS] += weight

        # Calculate Go confidence
        for signal, weight in DETECTION_WEIGHTS[ProjectType.GO].items():
            if (path / signal).exists():
                scores[ProjectType.GO] += weight

        return scores

    @staticmethod
    def detect_type(path: Path) -> ProjectType:
        """Detect project type based on confidence scores.

        Args:
            path: Project directory path

        Returns:
            Detected ProjectType or UNKNOWN if below threshold
        """
        scores = ProjectDetector.calculate_confidence(path)

        # Find highest scoring type
        max_score = max(scores.values())
        if max_score < CONFIDENCE_THRESHOLD:
            logger.debug(
                "project_type_unknown",
                path=str(path),
                scores=scores,
                threshold=CONFIDENCE_THRESHOLD,
            )
            return ProjectType.UNKNOWN

        # Return type with highest score
        for project_type, score in scores.items():
            if score == max_score:
                logger.debug(
                    "project_type_detected",
                    path=str(path),
                    type=project_type.value,
                    confidence=score,
                )
                return project_type

        return ProjectType.UNKNOWN


class AnalyzerFactory:
    """Factory for creating project analyzers.

    Implements Factory Pattern with analyzer registration and creation.
    File size constraint: ≤100 LOC
    """

    def __init__(self) -> None:
        """Initialize factory with registered analyzers."""
        self._analyzers: dict[ProjectType, type[BaseAnalyzer]] = {
            ProjectType.PYTHON: PythonAnalyzer,
            ProjectType.NODEJS: NodeJSAnalyzer,
            ProjectType.GO: GoAnalyzer,
        }

    def create(self, path: Path) -> BaseAnalyzer | None:
        """Create appropriate analyzer for project.

        Args:
            path: Project directory path

        Returns:
            Analyzer instance or None if unknown project type
        """
        # Detect project type
        project_type = ProjectDetector.detect_type(path)

        if project_type == ProjectType.UNKNOWN:
            logger.warning("no_analyzer_for_project", path=str(path))
            return None

        # Create analyzer instance
        analyzer_class = self._analyzers.get(project_type)
        if analyzer_class is None:
            logger.error("analyzer_not_registered", type=project_type.value)
            return None

        return analyzer_class()
