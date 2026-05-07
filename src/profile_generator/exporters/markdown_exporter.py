"""Markdown exporter with Jinja2 templating.

This module implements Markdown export using Jinja2 templates with custom template support.
"""

import contextlib
import tempfile
from pathlib import Path

import structlog
from jinja2 import Environment, FileSystemLoader, Template, TemplateError

from profile_generator.exporters.base import BaseExporter
from profile_generator.models.project import Project

logger = structlog.get_logger()

# Default template embedded as fallback
DEFAULT_TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "default.md.jinja2"


class MarkdownExporter(BaseExporter):
    """Markdown exporter with Jinja2 templating.

    Exports projects as Markdown using Jinja2 templates with fallback to default template.

    Constraints:
        - File size: ≤200 LOC
        - Template support: custom or default
        - Character escaping for Markdown syntax
        - Graceful error handling with fallback
    """

    def __init__(self, tool_version: str, template_path: Path | None = None) -> None:
        """Initialize Markdown exporter.

        Args:
            tool_version: Tool version string for output metadata
            template_path: Optional custom Jinja2 template path
        """
        self.tool_version = tool_version
        self.template_path = template_path

    def export(self, projects: list[Project], output_path: Path) -> None:
        """Export projects to Markdown file using Jinja2 template.

        Args:
            projects: List of analyzed projects
            output_path: Absolute path for output Markdown file

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

        logger.info(
            "markdown_export_started",
            output_path=str(output_path),
            count=len(projects),
            template=str(self.template_path) if self.template_path else "default",
        )

        try:
            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Load template
            template = self._load_template()

            # Render template
            from datetime import UTC, datetime

            rendered = template.render(
                generated_at=datetime.now(tz=UTC),
                tool_version=self.tool_version,
                projects=projects,
            )

            # Atomic write: temp file + rename
            self._atomic_write(output_path, rendered)

            logger.info(
                "markdown_export_success",
                output_path=str(output_path),
                project_count=len(projects),
                size_bytes=len(rendered),
            )

        except OSError as e:
            logger.exception(
                "markdown_export_failed",
                output_path=str(output_path),
                error=str(e),
            )
            raise

    def _load_template(self) -> Template:
        """Load Jinja2 template from custom path or default.

        Returns:
            Loaded Jinja2 template

        Raises:
            IOError: If template loading fails
        """
        # Try custom template first
        if self.template_path is not None:
            try:
                logger.debug("loading_custom_template", path=str(self.template_path))
                env = Environment(
                    loader=FileSystemLoader(self.template_path.parent),
                    autoescape=False,
                )
                return env.get_template(self.template_path.name)
            except (TemplateError, OSError) as e:
                logger.warning(
                    "custom_template_failed",
                    path=str(self.template_path),
                    error=str(e),
                    fallback="default",
                )

        # Fallback to default template
        logger.debug("loading_default_template", path=str(DEFAULT_TEMPLATE_PATH))
        env = Environment(
            loader=FileSystemLoader(DEFAULT_TEMPLATE_PATH.parent),
            autoescape=False,
        )
        return env.get_template(DEFAULT_TEMPLATE_PATH.name)

    def _atomic_write(self, output_path: Path, content: str) -> None:
        """Write content to file atomically using temp file + rename.

        Args:
            output_path: Final file path
            content: Markdown content to write

        Raises:
            IOError: If write or rename fails
        """
        # Create temp file in same directory as output (for atomic rename)
        temp_fd, temp_path_str = tempfile.mkstemp(
            dir=output_path.parent,
            prefix=".tmp_",
            suffix=".md",
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
