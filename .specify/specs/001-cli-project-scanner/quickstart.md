# Quickstart: Implementing CLI Project Scanner

**Feature**: 001-cli-project-scanner
**Date**: 2026-05-07
**Purpose**: Step-by-step guide for implementing the feature following TDD and constitution principles

---

## Prerequisites

Before starting implementation:

✅ **Read these documents in order**:
1. [spec.md](spec.md) - Feature specification with requirements
2. [plan.md](plan.md) - Implementation plan with technical context
3. [research.md](research.md) - Technology decisions (Typer, detection strategy)
4. [data-model.md](data-model.md) - Entity relationships and Pydantic models
5. [contracts/projects-output-v1.schema.json](contracts/projects-output-v1.schema.json) - JSON schema

✅ **Environment setup**:
```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone git@github.com:yvesmarinho/profile-generator.git
cd profile-generator

# Checkout feature branch
git checkout 001-cli-project-scanner

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -e ".[dev]"
```

✅ **Tools installed**:
- Python 3.12+
- Git
- VS Code with Copilot (recommended)

---

## Implementation Order (TDD Workflow)

Follow this sequence to implement features in dependency order, using Test-Driven Development (RED → GREEN → REFACTOR):

### Phase 1: Core Data Models (Day 1)

**Goal**: Define Pydantic models with validation

1. **Create `src/profile_generator/models/` package**
   ```bash
   mkdir -p src/profile_generator/models
   touch src/profile_generator/models/__init__.py
   ```

2. **Implement models in TDD order**:

   **Step 1.1**: `models/config.py` (Configuration model)
   - RED: Write test for valid configuration
   - GREEN: Implement `OutputFormat`, `LogLevel`, `Configuration` (Pydantic BaseSettings)
   - REFACTOR: Add field validators
   - Test coverage: env var loading, precedence, path validation

   **Step 1.2**: `models/project.py` (Entity models)
   - RED: Write test for Technology creation
   - GREEN: Implement `TechCategory`, `Technology`
   - RED: Write test for Contributor, Repository
   - GREEN: Implement `Contributor`, `Repository` with validators
   - RED: Write test for Statistics
   - GREEN: Implement `Statistics` with LOC validation
   - RED: Write test for Project (aggregate root)
   - GREEN: Implement `ProjectType`, `Project` with all relationships
   - REFACTOR: Extract common validators
   - Test coverage: validation rules, relationships, JSON serialization

3. **Verify**:
   ```bash
   pytest tests/unit/test_models.py -v
   mypy src/profile_generator/models/ --strict
   ruff check src/profile_generator/models/
   ```

**Checkpoint**: All models defined, validated, ≥80% coverage

---

### Phase 2: Project Analyzer Foundation (Day 2-3)

**Goal**: Implement Factory + Strategy patterns for analyzers

4. **Create `src/profile_generator/analyzers/` package**

   **Step 2.1**: `analyzers/base.py` (ABC)
   - RED: Write test for BaseAnalyzer interface
   - GREEN: Implement `BaseAnalyzer` ABC with abstract methods:
     - `can_analyze(path: Path) -> bool`
     - `analyze(path: Path) -> Project`
   - REFACTOR: Add common helper methods
   - File size: ≤150 LOC

   **Step 2.2**: `analyzers/factory.py` (Factory Pattern)
   - RED: Write test for project type detection (Python, Node.js, Go)
   - GREEN: Implement `ProjectDetector` with confidence scoring (from research.md)
   - RED: Write test for AnalyzerFactory.create()
   - GREEN: Implement `AnalyzerFactory` with analyzer registration
   - REFACTOR: Extract detection signals to constants
   - File size: ≤100 LOC

   **Step 2.3**: `analyzers/python.py` (First concrete analyzer)
   - RED: Write test for Python project detection (pyproject.toml, setup.py)
   - GREEN: Implement `PythonAnalyzer.can_analyze()`
   - RED: Write test for metadata extraction
   - GREEN: Implement `PythonAnalyzer.analyze()`:
     - Extract name, version from pyproject.toml
     - Extract description from README.md
     - Identify Python version and dependencies
     - Create Technology instances
   - REFACTOR: Extract file parsing to helper functions
   - File size: ≤200 LOC

5. **Implement remaining analyzers**:
   - `analyzers/nodejs.py` (Node.js) - ≤200 LOC
   - `analyzers/go.py` (Go) - ≤200 LOC

6. **Verify**:
   ```bash
   pytest tests/unit/test_analyzers.py -v
   pytest tests/integration/test_python_project.py -v
   mypy src/profile_generator/analyzers/ --strict
   ```

**Checkpoint**: All analyzers working, Factory Pattern validated, ≥80% coverage

---

### Phase 3: Exporters (Strategy Pattern) (Day 4)

**Goal**: Implement export strategies for JSON and Markdown

7. **Create `src/profile_generator/exporters/` package**

   **Step 3.1**: `exporters/base.py` (ABC)
   - RED: Write test for BaseExporter interface
   - GREEN: Implement `BaseExporter` ABC with:
     - `export(projects: list[Project], output_path: Path) -> None`
   - File size: ≤150 LOC

   **Step 3.2**: `exporters/json_exporter.py`
   - RED: Write test for JSON schema validation
   - GREEN: Implement `JSONExporter.export()`:
     - Serialize projects to JSON via Pydantic
     - Validate against schema (contracts/projects-output-v1.schema.json)
     - Atomic write (temp file + rename)
   - REFACTOR: Extract validation to separate method
   - File size: ≤200 LOC

   **Step 3.3**: `exporters/markdown_exporter.py`
   - RED: Write test for Markdown generation
   - GREEN: Implement `MarkdownExporter.export()`:
     - Load Jinja2 template (default or custom)
     - Render template with project data
     - Write to output file
   - File size: ≤200 LOC

8. **Create default Markdown template**:
   ```bash
   mkdir -p src/profile_generator/templates
   # Create default.md.jinja2 with project listing format
   ```

9. **Verify**:
   ```bash
   pytest tests/unit/test_exporters.py -v
   mypy src/profile_generator/exporters/ --strict
   ```

**Checkpoint**: Exporters working, outputs validated against schema

---

### Phase 4: Scanner & Orchestration (Day 5)

**Goal**: Tie everything together with directory scanner

10. **Implement `src/profile_generator/scanner.py`**
    - RED: Write test for directory scanning
    - GREEN: Implement `Scanner`:
      - Walk directory tree
      - Detect project directories
      - Use AnalyzerFactory to create appropriate analyzer
      - Collect Project instances
      - Enforce 100k source file limit per project (Clarification 4)
    - REFACTOR: Extract file counting logic
    - File size: ≤200 LOC

11. **Implement utility modules**:
    - `utils/logging.py`: structlog setup (≤100 LOC)
    - `utils/validators.py`: Path validation, security checks (≤100 LOC)

12. **Verify**:
    ```bash
    pytest tests/integration/test_scanner.py -v
    ```

**Checkpoint**: End-to-end scanning works from directory to Project instances

---

### Phase 5: CLI Interface (Day 6)

**Goal**: Implement Typer-based CLI

13. **Implement `src/profile_generator/cli.py`**
    - RED: Write test for `scan` command
    - GREEN: Implement CLI with Typer:
      - `scan` command with options (input, output, format, dry-run, verbose)
      - `config` command to show effective configuration
      - `version` command
      - Configuration loading with precedence
      - Exit codes (0/1/2)
    - REFACTOR: Extract command logic to separate functions
    - File size: ≤200 LOC

14. **Implement `src/profile_generator/config.py`**
    - RED: Write test for configuration precedence
    - GREEN: Implement configuration loading:
      - CLI args > ENV vars > config.yaml > defaults
      - Replace strategy for list values (Clarification 2)
    - File size: ≤200 LOC

15. **Verify**:
    ```bash
    pytest tests/integration/test_cli.py -v
    uv run profile-gen scan --help
    uv run profile-gen scan --input ./tests/fixtures --dry-run --verbose
    ```

**Checkpoint**: CLI working end-to-end, help messages clear

---

### Phase 6: Optional Features (P2) (Day 7+)

**Goal**: Implement Git analysis and statistics (if time permits)

16. **Git Analysis** (optional, P2):
    - `git/analyzer.py`: Extract repository metadata (≤200 LOC)
    - All-time commit count + top 5 contributors (Clarification 3)

17. **Statistics Calculator** (optional, P2):
    - `stats/calculator.py`: LOC counting by language (≤200 LOC)

---

## Quality Gates (Run Before Every Commit)

```bash
# 1. Linting
ruff check src/ tests/ --select ALL

# 2. Formatting (auto-fix)
ruff format src/ tests/

# 3. Type checking
mypy src/ --strict

# 4. Tests with coverage
pytest --cov=src/profile_generator --cov-report=term-missing --cov-fail-under=80

# 5. Security scanning
bandit -r src/

# 6. Dependency vulnerabilities
safety check

# 7. File size check
find src/ -name "*.py" -exec wc -l {} \; | awk '$1 > 300 {print "ERROR: " $2 " exceeds 300 LOC (" $1 " lines)"; exit 1}'
```

Or use the Makefile:
```bash
make lint      # ruff check
make format    # ruff format
make test      # pytest with coverage
make quality   # all gates
```

---

## Common Pitfalls

❌ **Don't**:
- Skip writing tests first (TDD is mandatory)
- Use `pip` or `poetry` (only `uv` allowed)
- Exceed 300 LOC per file (ruff will block)
- Use `Any` type without justification
- Instantiate dependencies directly (use DI)
- Write to files directly (use atomic writes: temp + rename)
- Commit secrets or credentials
- Use `git commit -m` (use `./scripts/git-commit-with-file.sh`)

✅ **Do**:
- Write tests before implementation (RED → GREEN → REFACTOR)
- Use Pydantic for all data models
- Validate all inputs
- Use type hints everywhere
- Follow SOLID principles
- Keep files small (≤200 LOC ideal)
- Run quality gates before every commit
- Document decisions in ADRs
- Ask clarifying questions in spec.md

---

## Getting Help

- **Spec unclear?** Add question to spec.md Clarifications section
- **Design decision needed?** Create ADR in `docs/decisions/`
- **Bug or issue?** Document in session notes `docs/SESSIONS/2026-05-07/`
- **Performance problem?** Check Performance Criteria in spec.md

---

## Next Steps After Implementation

1. **Generate tasks.md**: Run `/speckit.tasks` to break down implementation into granular tasks
2. **Create ADRs**: Document all architectural decisions (ADR-001 through ADR-004)
3. **Update documentation**: Ensure README.md has usage examples
4. **Integration test with yves-profile-site**: Verify JSON compatibility
5. **Performance testing**: Validate < 5s for 100 projects
6. **Security review**: Manual SOLID compliance check

---

**Status**: ✅ Complete - ready to begin implementation with TDD workflow
