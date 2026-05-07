<!--
Sync Impact Report (2026-05-07):
Version: 1.0.0 → 1.0.0 (initial constitution)
Principles defined: 7 core principles
Sections added: Technology Stack, Development Workflow, Quality Standards
Templates status:
  ✅ spec-template.md - aligned (scope, requirements)
  ✅ plan-template.md - aligned (architecture, patterns)
  ✅ tasks-template.md - aligned (P0/P1/P2 structure)
  ✅ commands/*.md - verified (no agent-specific references)
-->
---
template_version: "1.0.0"
last_updated: "2026-05-07"
breaking_changes: false
---

# Profile Generator Constitution

**Purpose**: CLI tool for automated project scanning, analysis, and portfolio generation

## Core Principles

### I. SOLID Architecture (NON-NEGOTIABLE)

**All code MUST adhere to SOLID principles:**

- **Single Responsibility**: Each class/module has exactly ONE responsibility
  - `PythonAnalyzer` only analyzes Python projects
  - `Scanner` only scans directories
  - `JSONExporter` only exports to JSON
- **Open/Closed**: Open for extension, closed for modification
  - New analyzers via inheritance from `BaseAnalyzer`
  - No modification of base classes when adding features
- **Liskov Substitution**: Subclasses substitutable for base classes
  - All analyzers interchangeable via `BaseAnalyzer` interface
  - Factory Pattern ensures correct substitution
- **Interface Segregation**: Small, specific interfaces
  - No monolithic interfaces
  - Clients depend only on methods they use
- **Dependency Inversion**: Depend on abstractions, not implementations
  - CLI depends on `BaseAnalyzer`, not `PythonAnalyzer`
  - Dependency Injection via constructor ALWAYS

**Rationale**: SOLID ensures maintainable, extensible architecture. Violations lead to fragile code, difficult testing, and high coupling.

### II. Modularization First (NON-NEGOTIABLE)

**File size limits are strictly enforced:**

- **Hard limit**: 300 LOC maximum (ruff blocks violations)
- **Soft limit**: 200 LOC recommended for optimal cohesion
- **Specific limits**:
  - `analyzers/base.py`: ≤150 LOC (ABCs must be lean)
  - `analyzers/factory.py`: ≤100 LOC (creation logic only)
  - Concrete analyzers: ≤200 LOC each
- **No circular imports allowed**

**When approaching limits**:

1. Extract Module: new file for isolated responsibility
2. Extract Class: move related methods to new class
3. Extract Function: break large functions into smaller ones
4. Use Composition: compose from multiple small modules

**Rationale**: Small files improve readability, testability, and maintainability. Large files indicate design problems.

### III. Test-Driven Development (NON-NEGOTIABLE)

**TDD workflow MUST be followed:**

1. Write test (fails - RED)
2. Implement minimum code (passes - GREEN)
3. Refactor (maintains GREEN)

**Coverage requirements**:

- Target: ≥80% (blocking gate)
- Ideal: ≥90%
- All public APIs MUST have tests
- Critical paths MUST have integration tests

**Test structure**:

- `tests/unit/` - isolated tests with mocks
- `tests/integration/` - end-to-end workflows
- `tests/fixtures/` - test data and sample projects

**Rationale**: Tests define behavior, prevent regressions, enable confident refactoring. No test = no merge.

### IV. Design Patterns (MANDATORY)

**Required patterns**:

- **Factory Pattern (MANDATORY)**: Create analyzers based on detected project type
  - Located in `analyzers/factory.py` (≤100 LOC)
  - NO direct instantiation of analyzers elsewhere
- **Strategy Pattern**: Different export strategies (JSON, Markdown, future HTML)
  - All exporters inherit from `BaseExporter`
  - Runtime selection of export strategy
- **Dependency Injection**: Pass dependencies via constructor
  - NO internal instantiation of dependencies
  - Constructor injection ONLY
- **Builder Pattern**: Progressive metadata construction
- **Adapter Pattern**: Adapt different project structures to common model

**Rationale**: Patterns provide proven solutions to common problems, improve code organization, enable flexibility and testing.

### V. Type Safety (NON-NEGOTIABLE)

**Type checking requirements**:

- `mypy --strict` with ZERO errors (blocking gate)
- Modern type hints (Python 3.12+):
  - PEP 484: Type Hints
  - PEP 585: Generic types (`list[str]`, not `List[str]`)
  - PEP 604: Union syntax (`str | None`, not `Optional[str]`)
- All function signatures MUST have type hints
- All class attributes MUST have type hints
- No `Any` types except justified with comment

**Rationale**: Type safety prevents runtime errors, improves IDE support, serves as documentation, enables refactoring confidence.

### VI. CLI-First Interface

**CLI requirements**:

- Text in/out protocol: args/stdin → stdout, errors → stderr
- Support JSON + human-readable formats
- Exit codes: 0 (success), 1 (error), 2 (config invalid)
- Commands: `scan`, `config`, `version`
- Flags: `--dry-run`, `--verbose`, `--debug`, `--quiet`, `--help`
- Configuration precedence: CLI args > ENV vars > config.yaml > defaults

**Output formats**:

- JSON: structured, machine-readable, Pydantic-validated
- Markdown: human-readable, Jinja2-templated, customizable

**Rationale**: CLI provides automation-friendly interface, text I/O ensures debuggability and composability.

### VII. Quality Gates (BLOCKING)

**All gates MUST pass before merge**:

1. **Linting**: `ruff check --select ALL` (zero warnings)
2. **Formatting**: `ruff format` (auto-applied)
3. **Type checking**: `mypy --strict src/` (zero errors)
4. **Tests**: `pytest --cov` (≥80% coverage)
5. **Security**: `bandit` (zero vulnerabilities)
6. **Dependencies**: `safety check` (zero vulnerabilities)
7. **File size**: All files ≤300 LOC
8. **SOLID compliance**: Manual review checklist

**Rationale**: Quality gates prevent technical debt, ensure consistency, maintain high code quality.

## Technology Stack

**Runtime (required)**:

- Python 3.12+ (type hints, performance)
- uv package manager (NOT pip/poetry)
- Click 8.x OR Typer 0.12+ (decision in ADR-001)
- Pydantic 2.x (validation, settings)
- Jinja2 (template generation)
- structlog (structured JSON logging)

**Development (required)**:

- pytest + pytest-cov (testing framework)
- ruff (linter + formatter all-in-one)
- mypy (type checker)
- Sphinx + autodoc + Napoleon (documentation)
- bandit (security scanner)
- safety (dependency vulnerability scanner)

**Rationale**: Modern, stable, well-maintained tools with strong type support and community backing.

## Development Workflow

**Specification-Driven Development**:

1. Define specification in `objetivo.yaml`
2. Generate `spec.md` via SpecKit (speckit.specify)
3. Generate `plan.md` via SpecKit (speckit.plan)
4. Generate `tasks.md` via SpecKit (speckit.tasks)
5. Create ADRs for architectural decisions
6. Implement tasks following TDD

**Architecture Decision Records**:

- ADR-001: CLI framework choice (Click vs Typer)
- ADR-002: Project detection strategy
- ADR-003: SOLID + design patterns application
- ADR-004: File size limits + modularization strategy

**Commit conventions**:

- Conventional Commits format: `type(scope): description`
- Types: feat, fix, docs, chore, test, refactor
- Via `./scripts/git-commit-with-file.sh` (NO `git commit -m`)

**Versioning**:

- Semantic Versioning 2.0.0: MAJOR.MINOR.PATCH
- MAJOR: breaking changes
- MINOR: new features (backward compatible)
- PATCH: bug fixes

**Rationale**: Structured workflow ensures alignment, reduces ambiguity, maintains quality throughout development lifecycle.

## Quality Standards

**Code organization**:

- Source code: `src/profile_generator/`
- Tests: `tests/unit/`, `tests/integration/`
- Documentation: `docs/` (sessions in `docs/SESSIONS/YYYY-MM-DD/`)
- Scripts: `scripts/`
- ADRs: `docs/decisions/`

**Documentation**:

- Google Style Docstrings for all public APIs
- Sphinx documentation auto-generated
- README with examples and usage
- ADRs for all architectural decisions
- Session reports in `docs/SESSIONS/`

**Security**:

- NO secrets in code or version control
- Use `.secrets/` folder (in .gitignore)
- Environment variables via `PROFILE_GEN_*` prefix
- Input validation (prevent path traversal)
- Pre-commit hooks validate secrets

**Performance**:

- < 5s to scan 100 projects
- < 500MB RAM usage
- Single-threaded (simplicity > performance)

**Rationale**: Standards ensure consistency, security, and professional quality across all aspects of the project.

## Governance

**Constitution Authority**:

- This constitution supersedes all other project guidelines
- All code reviews MUST verify compliance with constitution
- Violations MUST be justified and documented

**Amendment Process**:

1. Propose amendment with rationale
2. Document impact on existing code/templates
3. Update version (MAJOR for breaking, MINOR for additions, PATCH for clarifications)
4. Update dependent templates (spec, plan, tasks)
5. Approve by project owner (yvesmarinho)
6. Apply to all new code immediately
7. Create migration plan for existing code if needed

**Version Policy**:

- Semantic versioning for constitution itself
- Breaking changes require MAJOR version bump
- New principles/sections require MINOR version bump
- Clarifications/fixes require PATCH version bump

**Compliance Review**:

- Every PR reviewed against constitution checklist
- Quality gates automated in CI/CD
- Manual SOLID principles verification
- Architecture patterns validation

**Guidance Documents**:

- `.copilot-rules-profile-generator.md` - runtime development guidance
- `/memories/repo/profile-generator-rules.md` - quick reference
- `/memories/repo/profile-generator-roadmap.md` - implementation roadmap

**Rationale**: Strong governance ensures constitution is living document, enforced consistently, evolving with project needs.

---

**Version**: 1.0.0 | **Ratified**: 2026-05-07 | **Last Amended**: 2026-05-07
