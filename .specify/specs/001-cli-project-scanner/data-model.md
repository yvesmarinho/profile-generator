# Data Model: CLI Project Scanner

**Feature**: 001-cli-project-scanner
**Date**: 2026-05-07
**Purpose**: Define entity relationships, schemas, and validation rules for portfolio generation

---

## Overview

The data model consists of 5 primary entities organized in a hierarchical structure:

```
Configuration
    ↓ (configures)
Scanner
    ↓ (scans multiple)
Project (1..N)
    ├── has many → Technology
    ├── has one  → Repository (optional)
    └── has one  → Statistics
```

---

## Entities

### 1. Configuration

**Purpose**: Tool settings and runtime configuration with precedence handling

**Attributes**:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `scan_paths` | `list[Path]` | Yes | `[Path.cwd()]` | Directories to scan for projects |
| `output_format` | `OutputFormat` | Yes | `OutputFormat.BOTH` | Export format (json/markdown/both) |
| `output_dir` | `Path` | Yes | `Path("./output")` | Output directory for generated files |
| `template_path` | `Path \| None` | No | `None` | Custom Jinja2 template (None = use default) |
| `log_level` | `LogLevel` | Yes | `LogLevel.INFO` | Logging level (debug/info/warning/error) |
| `dry_run` | `bool` | Yes | `False` | Preview mode (no file writes) |
| `max_files_per_project` | `int` | Yes | `100_000` | File count limit (source files only) |

**Enums**:
```python
class OutputFormat(str, Enum):
    JSON = "json"
    MARKDOWN = "markdown"
    BOTH = "both"

class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
```

**Validation Rules**:
- `scan_paths`: All paths must exist and be readable
- `output_dir`: Must be writable (or creatable if doesn't exist)
- `template_path`: If provided, file must exist and have `.jinja2` extension
- `max_files_per_project`: Must be > 0 and <= 1,000,000

**Pydantic Model**:
```python
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings
from pathlib import Path
from enum import Enum

class OutputFormat(str, Enum):
    JSON = "json"
    MARKDOWN = "markdown"
    BOTH = "both"

class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class Configuration(BaseSettings):
    """Tool configuration with precedence: CLI > ENV > config.yaml > defaults"""

    scan_paths: list[Path] = Field(default_factory=lambda: [Path.cwd()])
    output_format: OutputFormat = OutputFormat.BOTH
    output_dir: Path = Path("./output")
    template_path: Path | None = None
    log_level: LogLevel = LogLevel.INFO
    dry_run: bool = False
    max_files_per_project: int = Field(default=100_000, ge=1, le=1_000_000)

    @field_validator("scan_paths")
    @classmethod
    def validate_scan_paths(cls, v: list[Path]) -> list[Path]:
        for path in v:
            if not path.exists():
                raise ValueError(f"Scan path does not exist: {path}")
            if not path.is_dir():
                raise ValueError(f"Scan path is not a directory: {path}")
        return v

    @field_validator("template_path")
    @classmethod
    def validate_template_path(cls, v: Path | None) -> Path | None:
        if v is not None:
            if not v.exists():
                raise ValueError(f"Template file does not exist: {v}")
            if v.suffix != ".jinja2":
                raise ValueError(f"Template must have .jinja2 extension: {v}")
        return v

    class Config:
        env_prefix = "PROFILE_GEN_"  # PROFILE_GEN_SCAN_PATHS, etc.
        env_file = ".env"
        case_sensitive = False
```

**Source**: FR-007 (configuration support), FR-008 (precedence), Clarification 2 (replace strategy for lists)

---

### 2. Technology

**Purpose**: Represents a technology/framework/library used in a project

**Attributes**:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | `str` | Yes | - | Technology name (e.g., "FastAPI", "React") |
| `version` | `str \| None` | No | `None` | Version string (e.g., "0.104.1", "18.2.0") |
| `category` | `TechCategory` | Yes | - | Category (language/framework/tool) |

**Enums**:
```python
class TechCategory(str, Enum):
    LANGUAGE = "language"          # Python, JavaScript, Go
    FRAMEWORK = "framework"        # FastAPI, React, Gin
    LIBRARY = "library"            # requests, axios, uuid
    TOOL = "tool"                  # pytest, eslint, golangci-lint
    RUNTIME = "runtime"            # Node.js, Python runtime
```

**Validation Rules**:
- `name`: Non-empty string, max 100 characters
- `version`: If provided, must be valid semver or version string
- `category`: Must be one of defined categories

**Pydantic Model**:
```python
class TechCategory(str, Enum):
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    LIBRARY = "library"
    TOOL = "tool"
    RUNTIME = "runtime"

class Technology(BaseModel):
    """Technology/framework/library used in a project"""

    name: str = Field(min_length=1, max_length=100)
    version: str | None = None
    category: TechCategory

    class Config:
        frozen = True  # Immutable after creation
```

**Relationships**:
- Belongs to exactly one `Project` (many-to-one)
- A `Project` can have multiple `Technology` instances

**Source**: FR-003 (extract technologies), Key Entities section in spec

---

### 3. Repository

**Purpose**: Git repository metadata for project

**Attributes**:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `url` | `str \| None` | No | `None` | Remote URL (e.g., "git@github.com:user/repo.git") |
| `branch` | `str` | Yes | - | Active branch name |
| `commit_count` | `int` | Yes | - | Total commit count (all-time) |
| `top_contributors` | `list[Contributor]` | Yes | - | Top 5 contributors by commit count |
| `last_commit_date` | `datetime` | Yes | - | Date of last commit |
| `tags` | `list[str]` | No | `[]` | Git tags (versions) |

**Nested Entity**:
```python
class Contributor(BaseModel):
    """Top contributor to a repository"""
    name: str = Field(min_length=1, max_length=200)
    commit_count: int = Field(ge=1)
```

**Validation Rules**:
- `url`: If provided, must be valid Git URL format
- `commit_count`: Must be >= 1
- `top_contributors`: Exactly 5 items (or fewer if < 5 contributors total), sorted by commit_count descending
- `last_commit_date`: Must be in the past
- `tags`: Each tag must be non-empty string

**Pydantic Model**:
```python
from datetime import datetime
from pydantic import HttpUrl, field_validator

class Contributor(BaseModel):
    """Top contributor by commit count"""
    name: str = Field(min_length=1, max_length=200)
    commit_count: int = Field(ge=1)

class Repository(BaseModel):
    """Git repository metadata"""

    url: str | None = None
    branch: str = Field(min_length=1, max_length=200)
    commit_count: int = Field(ge=1)
    top_contributors: list[Contributor] = Field(max_length=5)
    last_commit_date: datetime
    tags: list[str] = Field(default_factory=list)

    @field_validator("top_contributors")
    @classmethod
    def validate_contributors_sorted(cls, v: list[Contributor]) -> list[Contributor]:
        """Ensure contributors are sorted by commit count descending"""
        if v != sorted(v, key=lambda c: c.commit_count, reverse=True):
            raise ValueError("Contributors must be sorted by commit_count descending")
        return v

    @field_validator("last_commit_date")
    @classmethod
    def validate_past_date(cls, v: datetime) -> datetime:
        if v > datetime.now():
            raise ValueError("Last commit date cannot be in the future")
        return v
```

**Relationships**:
- Belongs to exactly one `Project` (one-to-one, optional)
- A `Project` may have zero or one `Repository` (None if not a Git project)

**Source**: FR-010 (Git metadata extraction), Clarification 3 (all-time + top 5), User Story 8

---

### 4. Statistics

**Purpose**: Code statistics for a project

**Attributes**:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `total_loc` | `int` | Yes | - | Total lines of code (all languages) |
| `loc_by_language` | `dict[str, int]` | Yes | - | LOC breakdown by language |
| `file_count` | `int` | Yes | - | Total source file count |
| `test_coverage` | `float \| None` | No | `None` | Test coverage percentage (0-100) |

**Validation Rules**:
- `total_loc`: Must be >= 0
- `loc_by_language`: Each language name non-empty, each count >= 0, sum should equal total_loc
- `file_count`: Must be >= 1 (at least README or one source file)
- `test_coverage`: If provided, must be 0.0 <= value <= 100.0

**Pydantic Model**:
```python
class Statistics(BaseModel):
    """Code statistics for a project"""

    total_loc: int = Field(ge=0)
    loc_by_language: dict[str, int] = Field(min_length=1)
    file_count: int = Field(ge=1)
    test_coverage: float | None = Field(default=None, ge=0.0, le=100.0)

    @field_validator("loc_by_language")
    @classmethod
    def validate_loc_sum(cls, v: dict[str, int], info) -> dict[str, int]:
        """Verify all language LOCs are non-negative"""
        for lang, count in v.items():
            if count < 0:
                raise ValueError(f"LOC for {lang} cannot be negative: {count}")
        return v
```

**Relationships**:
- Belongs to exactly one `Project` (one-to-one)
- A `Project` has exactly one `Statistics`

**Source**: FR-011 (code statistics), User Story 9

---

### 5. Project (Root Entity)

**Purpose**: Represents a scanned project directory with all metadata

**Attributes**:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | `str` | Yes | - | Project name (from metadata or directory) |
| `description` | `str \| None` | No | `None` | Project description (from README) |
| `path` | `Path` | Yes | - | Absolute path to project directory |
| `type` | `ProjectType` | Yes | - | Detected project type |
| `technologies` | `list[Technology]` | Yes | - | List of detected technologies |
| `repository` | `Repository \| None` | No | `None` | Git metadata (None if not Git project) |
| `statistics` | `Statistics` | Yes | - | Code statistics |

**Enums**:
```python
class ProjectType(str, Enum):
    PYTHON = "python"
    NODEJS = "nodejs"
    GO = "go"
    UNKNOWN = "unknown"
```

**Validation Rules**:
- `name`: Non-empty string, max 200 characters
- `description`: If provided, max 2000 characters
- `path`: Must be absolute path, must exist
- `type`: Must be one of defined types
- `technologies`: At least one technology (the primary language)
- `repository`: Optional (None for non-Git projects)
- `statistics`: Required (always calculated)

**Pydantic Model**:
```python
class ProjectType(str, Enum):
    PYTHON = "python"
    NODEJS = "nodejs"
    GO = "go"
    UNKNOWN = "unknown"

class Project(BaseModel):
    """Root entity representing a scanned project"""

    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    path: Path
    type: ProjectType
    technologies: list[Technology] = Field(min_length=1)
    repository: Repository | None = None
    statistics: Statistics

    @field_validator("path")
    @classmethod
    def validate_path_absolute(cls, v: Path) -> Path:
        if not v.is_absolute():
            raise ValueError(f"Project path must be absolute: {v}")
        if not v.exists():
            raise ValueError(f"Project path does not exist: {v}")
        return v

    def model_dump_json(self, **kwargs) -> str:
        """Custom JSON serialization with Path handling"""
        return super().model_dump_json(
            exclude_none=False,  # Include None values for optional fields
            by_alias=True,
            **kwargs
        )
```

**Relationships**:
- Has many `Technology` instances (composition, 1..N)
- Has one `Repository` (composition, optional 0..1)
- Has one `Statistics` (composition, required 1)

**Source**: FR-001 to FR-006 (core requirements), Key Entities section in spec

---

## Aggregate Root

**Project** is the aggregate root:
- All operations start from Project
- Repository and Statistics are value objects (no independent existence)
- Technologies are entities but always accessed through Project
- Consistency boundary: A Project and all its composed entities form a transactional unit

---

## JSON Schema

### Output Format (for yves-profile-site)

```json
{
  "generated_at": "2026-05-07T15:45:00Z",
  "tool_version": "0.1.0",
  "projects": [
    {
      "name": "example-project",
      "description": "Example Python web API",
      "path": "/home/user/projects/example-project",
      "type": "python",
      "technologies": [
        {
          "name": "Python",
          "version": "3.12.0",
          "category": "language"
        },
        {
          "name": "FastAPI",
          "version": "0.104.1",
          "category": "framework"
        }
      ],
      "repository": {
        "url": "git@github.com:user/example-project.git",
        "branch": "main",
        "commit_count": 347,
        "top_contributors": [
          {"name": "Alice", "commit_count": 210},
          {"name": "Bob", "commit_count": 87},
          {"name": "Charlie", "commit_count": 50}
        ],
        "last_commit_date": "2026-05-06T18:30:00Z",
        "tags": ["v1.0.0", "v1.1.0"]
      },
      "statistics": {
        "total_loc": 5420,
        "loc_by_language": {
          "Python": 4800,
          "YAML": 320,
          "Markdown": 300
        },
        "file_count": 87,
        "test_coverage": 85.5
      }
    }
  ]
}
```

**Root Schema**:
```python
class ProjectsOutput(BaseModel):
    """Root output schema for JSON export"""
    generated_at: datetime = Field(default_factory=datetime.now)
    tool_version: str
    projects: list[Project]
```

---

## Validation Strategy

### Input Validation
- Configuration: Pydantic Settings with field validators
- File paths: Check existence, permissions before processing
- File counts: Enforce 100k source file limit (Clarification 4)

### Business Logic Validation
- Project type confidence scoring (research.md Decision 2)
- Git metadata extraction with fallback for corrupted repos
- LOC counting with language detection

### Output Validation
- Pydantic model_validate() before export
- JSON schema validation against yves-profile-site contract
- Atomic file writes (temp file + rename)

---

## Performance Considerations

**Memory Management**:
- Process projects one at a time (no batch loading)
- Stream file reading for LOC counting
- Limit Git log query depth (all-time count but shallow clone support)

**Caching**:
- Phase 0 (P0): No caching
- Phase 2 (P2): Consider caching Git metadata if performance issues

**Indexing**:
- N/A (no database, in-memory only)

---

## Testing Strategy

**Unit Tests**:
- Each Pydantic model with valid/invalid data
- Field validators with edge cases
- Relationship constraints

**Integration Tests**:
- Full Project creation with all nested entities
- JSON serialization/deserialization
- Schema compatibility with yves-profile-site

**Contract Tests**:
- JSON output validates against published schema
- yves-profile-site can successfully import generated JSON

---

## Migration Strategy

**Version 0.1.0 (Initial)**:
- All entities defined in this document
- No migrations needed (greenfield)

**Future Versions**:
- Schema versioning via `tool_version` field in output
- Backwards compatibility for yves-profile-site maintained
- Deprecation policy: 2 minor versions notice before breaking changes

---

**Status**: ✅ Complete - all entities defined with validation rules and relationships
