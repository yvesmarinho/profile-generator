"""CLI interface using Typer for profile-generator.

This module implements the command-line interface with scan, config, and version commands.
"""

import atexit
import contextlib
import sys
from pathlib import Path
from typing import Annotated

import structlog
import typer

from profile_generator import __version__
from profile_generator.exporters.json_exporter import JSONExporter
from profile_generator.exporters.markdown_exporter import MarkdownExporter
from profile_generator.models.config import Configuration, LogLevel, OutputFormat
from profile_generator.models.project import Project
from profile_generator.scanner import Scanner
from profile_generator.utils.logging import setup_logging

app = typer.Typer(
    name="profile-gen",
    help="CLI tool for automated project scanning and portfolio generation",
    add_completion=False,
    rich_markup_mode="rich",
)

# Temporary files to clean up on exit
_temp_files: list[Path] = []


def _cleanup_temp_files() -> None:
    """Clean up temporary files on exit."""
    for temp_file in _temp_files:
        with contextlib.suppress(OSError):
            temp_file.unlink(missing_ok=True)


# Register cleanup handler
atexit.register(_cleanup_temp_files)


@app.command()
def scan(
    input_paths: Annotated[
        list[Path] | None,
        typer.Option(
            "--input",
            "-i",
            help="Directories to scan for projects (default: current directory)",
        ),
    ] = None,
    output_dir: Annotated[
        Path,
        typer.Option("--output", "-o", help="Output directory for generated files"),
    ] = Path("./output"),
    output_format: Annotated[
        OutputFormat,
        typer.Option("--format", "-f", help="Output format (json/markdown/both)"),
    ] = OutputFormat.BOTH,
    template_path: Annotated[
        Path | None,
        typer.Option("--template", "-t", help="Custom Jinja2 template for Markdown"),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Preview scan without writing files"),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Verbose output (INFO level)"),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option("--debug", "-d", help="Debug output (DEBUG level)"),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option("--quiet", "-q", help="Quiet mode (ERROR level only)"),
    ] = False,
) -> None:
    """Scan project directories and generate portfolio outputs.

    Examples:
        # Scan current directory
        $ profile-gen scan

        # Scan multiple directories
        $ profile-gen scan --input ~/projects --input ~/work

        # Generate JSON only
        $ profile-gen scan --format json --output ./output

        # Dry run (preview)
        $ profile-gen scan --dry-run
    """
    try:
        # Determine log level
        log_level = LogLevel.INFO
        if debug:
            log_level = LogLevel.DEBUG
        elif verbose:
            log_level = LogLevel.INFO
        elif quiet:
            log_level = LogLevel.ERROR

        # Setup logging
        setup_logging(log_level)
        logger = structlog.get_logger()

        # Load configuration
        config = Configuration(
            scan_paths=input_paths or [Path.cwd()],
            output_format=output_format,
            output_dir=output_dir,
            template_path=template_path,
            log_level=log_level,
            dry_run=dry_run,
        )

        logger.info("scan_command_started", config=config.model_dump())

        # Initialize scanner
        scanner = Scanner(config)

        # Scan projects
        projects = scanner.scan()

        if not projects:
            logger.warning("no_projects_found")
            typer.echo("No projects found.", err=True)
            sys.exit(0)

        logger.info("scan_results", project_count=len(projects))

        # Export results
        if config.dry_run:
            typer.echo(f"\n[DRY RUN] Would export {len(projects)} projects")
            for project in projects:
                typer.echo(f"  - {project.name} ({project.type.value})")
        else:
            _export_projects(projects, config)

        logger.info("scan_command_completed", project_count=len(projects))

    except ValueError as e:
        logger.exception("configuration_invalid", error=str(e))
        typer.echo(f"Configuration error: {e}", err=True)
        sys.exit(2)
    except Exception as e:
        logger.exception("scan_command_failed", error=str(e))
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)


@app.command()
def config() -> None:
    """Show effective configuration.

    Displays the current configuration with sources (CLI, ENV, defaults).
    """
    setup_logging(LogLevel.INFO)
    logger = structlog.get_logger()

    try:
        # Load default configuration
        cfg = Configuration()

        logger.info("configuration_loaded", config=cfg.model_dump())

        typer.echo("\n[bold]Effective Configuration[/bold]\n")
        typer.echo(f"Scan Paths: {cfg.scan_paths}")
        typer.echo(f"Output Format: {cfg.output_format.value}")
        typer.echo(f"Output Directory: {cfg.output_dir}")
        typer.echo(f"Template Path: {cfg.template_path or 'default'}")
        typer.echo(f"Log Level: {cfg.log_level.value}")
        typer.echo(f"Dry Run: {cfg.dry_run}")
        typer.echo(f"Max Files Per Project: {cfg.max_files_per_project:,}")

    except Exception as e:
        logger.exception("config_command_failed", error=str(e))
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)


@app.command()
def version() -> None:
    """Display version information."""
    typer.echo(f"profile-generator version {__version__}")


def _export_projects(projects: list[Project], config: Configuration) -> None:
    """Export projects based on configuration.

    Args:
        projects: List of analyzed projects
        config: Tool configuration
    """
    structlog.get_logger()

    # Create output directory
    config.output_dir.mkdir(parents=True, exist_ok=True)

    # Export JSON
    if config.output_format in (OutputFormat.JSON, OutputFormat.BOTH):
        json_output = config.output_dir / "projects.json"
        exporter = JSONExporter(tool_version=__version__)
        exporter.export(projects, json_output)
        typer.echo(f"✅ JSON exported to: {json_output}")

    # Export Markdown
    if config.output_format in (OutputFormat.MARKDOWN, OutputFormat.BOTH):
        md_output = config.output_dir / "portfolio.md"
        exporter_md = MarkdownExporter(
            tool_version=__version__,
            template_path=config.template_path,
        )
        exporter_md.export(projects, md_output)
        typer.echo(f"✅ Markdown exported to: {md_output}")


if __name__ == "__main__":
    app()
