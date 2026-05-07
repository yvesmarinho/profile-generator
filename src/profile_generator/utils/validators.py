"""Path validation and security checks.

This module provides utilities for validating file paths and preventing
path traversal attacks.
"""

from pathlib import Path


def validate_path(path: Path, base_path: Path | None = None) -> Path:
    """Validate path and check for security issues.

    Performs validation to prevent path traversal attacks by checking for:
    - Presence of ".." components (directory traversal)
    - Absolute symlinks that point outside the base path
    - Invalid or non-existent paths

    Args:
        path: Path to validate
        base_path: Optional base path to restrict access (for path traversal prevention)

    Returns:
        Resolved absolute path (with symlinks resolved)

    Raises:
        ValueError: If path contains "..", is outside base_path, or is invalid

    Example:
        >>> from pathlib import Path
        >>> validate_path(Path("/tmp/test"))
        PosixPath('/tmp/test')
        >>> validate_path(Path("../etc/passwd"), Path("/home/user"))
        Traceback (most recent call last):
            ...
        ValueError: Path traversal detected: ../etc/passwd
    """
    # Check for ".." components (path traversal attempt)
    if ".." in path.parts:
        msg = f"Path traversal detected: {path}"
        raise ValueError(msg)

    # Resolve path (follow symlinks)
    try:
        resolved_path = path.resolve(strict=False)
    except (OSError, RuntimeError) as e:
        msg = f"Failed to resolve path: {path}"
        raise ValueError(msg) from e

    # If base_path provided, ensure resolved path is within base_path
    if base_path is not None:
        try:
            base_resolved = base_path.resolve(strict=False)
            # Check if resolved_path is relative to base_resolved
            resolved_path.relative_to(base_resolved)
        except (ValueError, OSError) as e:
            msg = f"Path outside allowed directory: {path} not in {base_path}"
            raise ValueError(msg) from e

    # Check for absolute symlinks that point outside base_path
    if path.is_symlink() and base_path is not None:
        link_target = path.readlink()
        if link_target.is_absolute():
            try:
                link_target.relative_to(base_path)
            except ValueError as e:
                msg = f"Absolute symlink points outside base path: {path} -> {link_target}"
                raise ValueError(msg) from e

    return resolved_path
