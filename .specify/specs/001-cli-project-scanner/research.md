# Research: CLI Project Scanner Technology Decisions

**Feature**: 001-cli-project-scanner
**Date**: 2026-05-07
**Purpose**: Resolve technical unknowns identified in plan.md Technical Context

---

## Decision 1: CLI Framework (Click vs Typer)

### Context

Need to choose between two mature Python CLI frameworks:
- **Click 8.x**: Established, decorator-based, widely used
- **Typer 0.12+**: Modern, type-hint-based, built on Click

### Requirements from Specification

- Commands: `scan`, `config`, `version` (FR-021)
- Flags: `--dry-run`, `--verbose`, `--debug`, `--quiet`, `--help` (FR-022)
- Type safety: mypy --strict compliance required (SC-004)
- Configuration precedence: CLI args > ENV > config > defaults (FR-008)
- Clear help messages and documentation (FR-020)
- Exit codes: 0 (success), 1 (error), 2 (config invalid) (FR-023)

### Evaluation Criteria

| Criterion | Weight | Click 8.x | Typer 0.12+ |
|-----------|--------|-----------|-------------|
| **Type Hints Support** | HIGH | ⚠️ Partial (via annotations) | ✅ Native (uses type hints directly) |
| **mypy --strict Compatibility** | HIGH | ⚠️ Requires extra effort | ✅ Excellent (designed for type safety) |
| **Developer Experience** | HIGH | ✅ Mature, well-documented | ✅ Modern, intuitive API |
| **Maturity & Stability** | MEDIUM | ✅ Very mature (10+ years) | ✅ Stable (built on Click, 3+ years) |
| **Community & Ecosystem** | MEDIUM | ✅ Large ecosystem | ✅ Growing rapidly |
| **Learning Curve** | LOW | ⚠️ Decorator complexity | ✅ Simpler if using type hints |
| **Performance** | LOW | ✅ Fast | ✅ Fast (same Click internals) |
| **Backwards Compatibility** | LOW | ✅ Very stable API | ✅ Stable (1.0 released) |

### Analysis

**Click 8.x Strengths**:
- Battle-tested in production (Flask, pip, many others)
- Extensive plugin ecosystem
- Well-established patterns and best practices
- Very stable API (minimal breaking changes)

**Click 8.x Weaknesses**:
- Type hints support is partial (requires manual type declarations)
- mypy --strict requires extra configuration and boilerplate
- Decorator-based API can be verbose for complex CLIs
- Less ergonomic for modern Python 3.12+ codebases

**Typer 0.12+ Strengths**:
- Native type hint support (perfect fit for mypy --strict requirement)
- Automatic help generation from type hints and docstrings
- Less boilerplate (no need for @click.option decorators)
- Modern Python 3.6+ first approach
- Built on Click (inherits stability)
- Excellent autocomplete support in IDEs

**Typer 0.12+ Weaknesses**:
- Smaller ecosystem (fewer plugins, though Click plugins often work)
- Less widely adopted (though adoption growing rapidly)
- Some advanced Click features require falling back to Click API

### Decision

**RECOMMENDED: Typer 0.12+**

**Rationale**:

1. **Type Safety Alignment** (CRITICAL): Constitution requires mypy --strict with zero errors (Principle V). Typer's native type hint support makes this trivial, while Click requires significant boilerplate.

2. **Code Quality**: Typer's type-first approach results in:
   - Clearer function signatures
   - Better IDE autocomplete
   - Automatic validation
   - Less boilerplate code

3. **Constitution Compliance**: Modularization principle favors concise code. Typer typically requires 30-40% fewer lines for equivalent functionality.

4. **Maintainability**: Type hints serve as inline documentation, improving long-term maintenance.

5. **Risk Mitigation**: Built on Click internals, so we get Click's stability with modern ergonomics. Can fall back to Click API for advanced features if needed.

**Example Comparison**:

**Click 8.x**:
```python
import click

@click.command()
@click.option('--input', type=click.Path(exists=True), help='Input directory')
@click.option('--output', type=click.Path(), help='Output directory')
@click.option('--format', type=click.Choice(['json', 'markdown']), default='json')
@click.option('--dry-run', is_flag=True, help='Preview without writing')
def scan(input: str, output: str, format: str, dry_run: bool) -> None:
    """Scan projects and generate portfolio data."""
    # Type hints required manually for mypy
    ...
```

**Typer 0.12+**:
```python
import typer
from pathlib import Path
from typing import Annotated
from enum import Enum

class OutputFormat(str, Enum):
    json = "json"
    markdown = "markdown"

def scan(
    input: Annotated[Path, typer.Option(help="Input directory", exists=True)],
    output: Annotated[Path, typer.Option(help="Output directory")],
    format: Annotated[OutputFormat, typer.Option(help="Output format")] = OutputFormat.json,
    dry_run: Annotated[bool, typer.Option(help="Preview without writing")] = False,
) -> None:
    """Scan projects and generate portfolio data."""
    # Type hints native, mypy --strict happy
    ...
```

**Typer provides**:
- Automatic validation (Path exists check)
- Enum support for choices
- Native type hints (mypy --strict compliant)
- Less boilerplate
- Better IDE support

### Alternative Considered

**Click 8.x with click-type-test**: Rejected because it adds external dependency just to patch type safety, defeating the purpose of using a mature framework.

### Implementation Notes

- Use `typer[all]` to get full feature set including rich output support
- Leverage `Annotated` for option metadata (Python 3.9+ feature, we have 3.12+)
- Use Enums for restricted choices (type-safe)
- Create custom validators as Annotated constraints
- Fall back to Click API only if truly needed (advanced features)

### Success Criteria

- ✅ All CLI commands implemented with native type hints
- ✅ mypy --strict passes with zero errors
- ✅ Help messages auto-generated from type hints and docstrings
- ✅ Autocomplete works in shells (fish, zsh, bash)
- ✅ Exit codes properly handled (0/1/2)
- ✅ Configuration precedence logic clear and testable

---

## Decision 2: Project Detection Strategy

### Context

Need to determine how to detect project type (Python, Node.js, Go, etc.) when scanning directories.

### Requirements from Specification

- Auto-detect project types (Python, Node.js, Go) - FR-002
- Support characteristic files: pyproject.toml, package.json, go.mod
- Handle edge cases: missing README.md, mixed languages, no clear type
- Performance: < 50ms per project average

### Options

**Option A: File-based detection (characteristic files)**
- Scan for pyproject.toml → Python
- Scan for package.json → Node.js
- Scan for go.mod → Go

**Option B: Directory structure heuristics**
- Look for src/main.py → Python
- Look for node_modules/ → Node.js
- Look for go.sum → Go

**Option C: Hybrid approach (file-based with confidence scoring)**
- Check multiple signals per language
- Assign confidence scores
- Select highest confidence

### Decision

**RECOMMENDED: Option C (Hybrid with confidence scoring)**

**Rationale**:

1. **Robustness**: Single file missing doesn't fail detection
2. **Accuracy**: Multiple signals reduce false positives
3. **Edge Case Handling**: Handles mixed-language projects (select highest confidence)
4. **Future Extensibility**: Easy to add new languages by defining new signal sets

**Detection Rules**:

**Python** (confidence scoring):
- pyproject.toml present: +50 points
- setup.py present: +30 points
- requirements.txt present: +20 points
- src/*.py files: +10 points
- Threshold: 40 points

**Node.js**:
- package.json present: +50 points
- package-lock.json present: +20 points
- yarn.lock present: +20 points
- node_modules/ present: +10 points
- Threshold: 40 points

**Go**:
- go.mod present: +50 points
- go.sum present: +20 points
- *.go files: +20 points
- Threshold: 40 points

**Mixed Language**: If multiple languages score above threshold, classify as composite (list all detected technologies).

**Unknown**: If no language scores above threshold, classify as "unknown" and extract basic metadata only (name from directory, description from README if present).

### Implementation

```python
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class ProjectType(str, Enum):
    PYTHON = "python"
    NODEJS = "nodejs"
    GO = "go"
    UNKNOWN = "unknown"

@dataclass
class DetectionSignal:
    file_pattern: str
    points: int

class ProjectDetector:
    SIGNALS = {
        ProjectType.PYTHON: [
            DetectionSignal("pyproject.toml", 50),
            DetectionSignal("setup.py", 30),
            DetectionSignal("requirements.txt", 20),
            DetectionSignal("src/**/*.py", 10),
        ],
        ProjectType.NODEJS: [
            DetectionSignal("package.json", 50),
            DetectionSignal("package-lock.json", 20),
            DetectionSignal("yarn.lock", 20),
            DetectionSignal("node_modules/", 10),
        ],
        ProjectType.GO: [
            DetectionSignal("go.mod", 50),
            DetectionSignal("go.sum", 20),
            DetectionSignal("**/*.go", 20),
        ],
    }

    THRESHOLD = 40

    def detect(self, project_path: Path) -> ProjectType:
        scores = {ptype: 0 for ptype in ProjectType}

        for ptype, signals in self.SIGNALS.items():
            for signal in signals:
                if self._check_signal(project_path, signal):
                    scores[ptype] += signal.points

        # Return highest scoring type if above threshold
        best = max(scores.items(), key=lambda x: x[1])
        return best[0] if best[1] >= self.THRESHOLD else ProjectType.UNKNOWN
```

---

## Research Summary

### Resolved Unknowns

| Unknown | Decision | Documented In |
|---------|----------|---------------|
| CLI framework | Typer 0.12+ | ADR-001 (to be created) |
| Project detection | Hybrid with confidence scoring | ADR-002 (to be created) |

### Next Steps

1. Create ADR-001: Document Click vs Typer decision with full rationale
2. Create ADR-002: Document project detection strategy with scoring rules
3. Create ADR-003: Document SOLID principles and design patterns application
4. Create ADR-004: Document file size limits and modularization enforcement strategy

### Updated Technical Context

All NEEDS CLARIFICATION items resolved:
- **Primary Dependencies**: Typer 0.12+ (decision finalized)
- **Project Detection**: Hybrid confidence-based approach (strategy defined)

Ready to proceed to Phase 1: Design & Contracts.
