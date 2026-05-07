# Tasks: CLI Project Scanner & Portfolio Generator

**Feature**: 001-cli-project-scanner
**Branch**: `001-cli-project-scanner`
**Input**: Design documents from `.specify/specs/001-cli-project-scanner/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Organization**: Tasks grouped by user story for independent implementation and testing
**Tests**: NOT included (TDD workflow requires writing tests during implementation, not pre-defining all test tasks)

---

## Format: `- [ ] [ID] [P?] [Story] Description`

- **Checkbox**: `- [ ]` for incomplete, `- [x]` when done
- **[ID]**: Sequential task number (T001, T002, T003...)
- **[P]**: Present ONLY if task can run in parallel (different files, no blocking dependencies)
- **[Story]**: User story label (US1, US2, etc.) for story-specific tasks only
- **Description**: Action with exact file path

**Example**: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`

---

## Implementation Strategy

**MVP First**: Focus on User Stories 1-6 (P1) before any P2/P3 work
**Independent Stories**: Each user story phase can be implemented and tested separately
**Parallel Opportunities**: Tasks marked [P] can be worked simultaneously
**TDD Workflow**: For each task: RED (write test) → GREEN (implement) → REFACTOR

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create project structure and foundational configuration
**Blocking**: Must complete before any user story implementation
**Test Criteria**: Project structure matches plan.md, all quality gates runnable

- [x] T001 Initialize Python project with pyproject.toml following plan.md specifications
- [x] T002 Create src/profile_generator/ package structure with __init__.py
- [x] T003 Configure uv tool with pyproject.toml dependencies (Typer, Pydantic 2.x, Jinja2, structlog)
- [x] T004 Create pytest configuration in pyproject.toml with coverage settings (≥80%)
- [x] T005 Configure ruff in pyproject.toml with --select ALL and file size limit checks
- [x] T006 Configure mypy in pyproject.toml with --strict mode enabled
- [x] T007 Create Makefile with targets: install-deps, dev, build, test, lint, format, clean
- [x] T008 Create .gitignore with Python-specific patterns (__pycache__, .venv/, dist/, .pytest_cache/)
- [x] T009 Create src/profile_generator/__init__.py with __version__ = "0.1.0"
- [x] T010 Create README.md with project description and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core abstractions and utilities needed by all user stories
**Blocking**: Must complete before user story implementations
**Test Criteria**: All base classes defined, utilities functional, models validated

### Data Models (from data-model.md)

- [x] T011 [P] Create src/profile_generator/models/__init__.py package
- [x] T012 [P] Create src/profile_generator/models/config.py with OutputFormat and LogLevel enums
- [x] T013 [P] Implement Configuration model in src/profile_generator/models/config.py using Pydantic BaseSettings
- [x] T014 [P] Add field validators to Configuration for scan_paths, template_path, max_files_per_project
- [x] T015 [P] Create src/profile_generator/models/project.py with TechCategory enum
- [x] T016 [P] Implement Technology model in src/profile_generator/models/project.py with Pydantic BaseModel
- [x] T017 [P] Implement Contributor model in src/profile_generator/models/project.py
- [x] T018 [P] Implement Repository model in src/profile_generator/models/project.py with validators
- [x] T019 [P] Implement Statistics model in src/profile_generator/models/project.py with LOC validation
- [x] T020 [P] Implement ProjectType enum in src/profile_generator/models/project.py with values: PYTHON, NODEJS, GO, UNKNOWN
- [x] T021 [P] Implement Project model (aggregate root) in src/profile_generator/models/project.py
- [x] T022 [P] Implement ProjectsOutput model in src/profile_generator/models/project.py for JSON export schema

### Base Abstractions (Factory + Strategy Patterns)

- [x] T023 Create src/profile_generator/analyzers/__init__.py package
- [x] T024 Implement BaseAnalyzer ABC in src/profile_generator/analyzers/base.py (≤150 LOC)
- [x] T025 Define abstract methods in BaseAnalyzer: can_analyze(path), analyze(path)
- [x] T026 Create src/profile_generator/exporters/__init__.py package
- [x] T027 Implement BaseExporter ABC in src/profile_generator/exporters/base.py (≤150 LOC)
- [x] T028 Define abstract method in BaseExporter: export(projects, output_path)

### Utilities

- [x] T029 [P] Create src/profile_generator/utils/__init__.py package
- [x] T030 [P] Implement structured logging setup in src/profile_generator/utils/logging.py using structlog (≤100 LOC)
- [x] T031 [P] Implement path validation and security checks in src/profile_generator/utils/validators.py (≤100 LOC)
- [x] T032 [P] Add path traversal prevention logic to validators.py (check for .., absolute symlinks)

---

## Phase 3: User Story 1 - Basic Project Scanning (P1 - MVP)

**Story Goal**: Scan project directories and detect project types automatically
**Independent Test**: Configure scan paths, run scan, verify projects detected with correct types
**Deliverable**: Working scanner that identifies Python/Node.js/Go projects

- [ ] T033 [US1] Create src/profile_generator/scanner.py module (≤200 LOC)
- [ ] T034 [US1] Implement Scanner class with __init__(config: Configuration) using DI
- [ ] T035 [US1] Implement directory walking logic in Scanner.scan() method
- [ ] T036 [US1] Add symlink detection and circular symlink prevention in Scanner
- [ ] T037 [US1] Implement 100k source file limit enforcement per project in Scanner (whitelist approach)
- [ ] T038 [US1] Add graceful error handling for inaccessible directories in Scanner
- [ ] T039 [US1] Integrate AnalyzerFactory in Scanner to detect project types
- [ ] T040 [US1] Implement project collection and aggregation logic in Scanner.scan()
- [ ] T041 [US1] Add structured logging to Scanner for scan progress and errors

---

## Phase 4: User Story 2 - JSON Export with Schema Validation (P1 - MVP)

**Story Goal**: Export scanned projects as JSON compatible with yves-profile-site
**Independent Test**: Generate JSON from sample projects, validate against schema, verify all fields present
**Deliverable**: JSONExporter with Pydantic validation and atomic writes

- [ ] T042 [US2] Create src/profile_generator/exporters/json_exporter.py module (≤200 LOC)
- [ ] T043 [US2] Implement JSONExporter class extending BaseExporter with DI
- [ ] T044 [US2] Implement export() method with Pydantic model_dump_json() serialization
- [ ] T045 [US2] Add ProjectsOutput model validation before export in JSONExporter
- [ ] T046 [US2] Implement atomic file write (temp file + rename) in JSONExporter.export()
- [ ] T047 [US2] Add JSON schema validation against contracts/projects-output-v1.schema.json
- [ ] T048 [US2] Implement graceful handling of serialization errors with null values and warnings
- [ ] T049 [US2] Add structured logging for export success/failure in JSONExporter

---

## Phase 5: User Story 3 - Markdown Generation with Templates (P1 - MVP)

**Story Goal**: Generate human-readable Markdown portfolio from scanned projects
**Independent Test**: Generate Markdown from sample projects, verify formatting and completeness
**Deliverable**: MarkdownExporter with Jinja2 templating and custom template support

- [ ] T050 [US3] Create src/profile_generator/templates/ directory for Jinja2 templates
- [ ] T051 [US3] Create default.md.jinja2 template with project listing format
- [ ] T052 [US3] Add sections to template: header, project loop, technology display, statistics
- [ ] T053 [US3] Create src/profile_generator/exporters/markdown_exporter.py module (≤200 LOC)
- [ ] T054 [US3] Implement MarkdownExporter class extending BaseExporter with DI
- [ ] T055 [US3] Implement Jinja2 template loading logic (default vs custom) in MarkdownExporter
- [ ] T056 [US3] Implement export() method with template rendering in MarkdownExporter
- [ ] T057 [US3] Add special character escaping for Markdown syntax in template rendering
- [ ] T058 [US3] Implement fallback to default template on custom template errors
- [ ] T059 [US3] Add structured logging for template loading and rendering in MarkdownExporter

---

## Phase 6: User Story 4 - Python Project Analysis (P1 - MVP)

**Story Goal**: Accurately analyze Python projects extracting metadata from pyproject.toml, setup.py, README
**Independent Test**: Scan Python project with pyproject.toml, verify extracted name/version/dependencies
**Deliverable**: PythonAnalyzer with complete metadata extraction

- [ ] T060 [US4] Create src/profile_generator/analyzers/python.py module (≤200 LOC)
- [ ] T061 [US4] Implement PythonAnalyzer class extending BaseAnalyzer with DI
- [ ] T062 [US4] Implement can_analyze() method detecting pyproject.toml, setup.py, requirements.txt
- [ ] T063 [US4] Implement pyproject.toml parsing using tomli library in PythonAnalyzer
- [ ] T064 [US4] Extract name, version, dependencies from pyproject.toml in analyze() method
- [ ] T065 [US4] Implement setup.py parsing as fallback when pyproject.toml unavailable
- [ ] T066 [US4] Implement requirements.txt parsing for dependency extraction
- [ ] T067 [US4] Extract Python version requirement from project metadata
- [ ] T068 [US4] Create Technology instances for Python language and dependencies
- [ ] T069 [US4] Implement README.md parsing for project description (first paragraph)
- [ ] T070 [US4] Add graceful handling of malformed TOML/Python files in PythonAnalyzer
- [ ] T071 [US4] Return Project model instance from analyze() method

---

## Phase 7: User Story 5 - Node.js Project Analysis (P1 - MVP)

**Story Goal**: Accurately analyze Node.js projects extracting metadata from package.json
**Independent Test**: Scan Node.js project with package.json, verify extracted name/version/dependencies/scripts
**Deliverable**: NodeJSAnalyzer with complete metadata extraction

- [ ] T072 [US5] Create src/profile_generator/analyzers/nodejs.py module (≤200 LOC)
- [ ] T073 [US5] Implement NodeJSAnalyzer class extending BaseAnalyzer with DI
- [ ] T074 [US5] Implement can_analyze() method detecting package.json
- [ ] T075 [US5] Implement package.json parsing in NodeJSAnalyzer.analyze()
- [ ] T076 [US5] Extract name, version, dependencies, devDependencies from package.json
- [ ] T077 [US5] Extract scripts section from package.json
- [ ] T078 [US5] Detect package manager from package-lock.json or yarn.lock presence
- [ ] T079 [US5] Create Technology instances for Node.js runtime and dependencies
- [ ] T080 [US5] Distinguish runtime dependencies from devDependencies in Technology categorization
- [ ] T081 [US5] Implement README.md parsing for project description
- [ ] T082 [US5] Handle monorepo case: treat each package.json as separate project
- [ ] T083 [US5] Add graceful handling of malformed JSON in NodeJSAnalyzer
- [ ] T084 [US5] Return Project model instance from analyze() method

---

## Phase 8: User Story 6 - Go Project Analysis (P1 - MVP)

**Story Goal**: Accurately analyze Go projects extracting metadata from go.mod
**Independent Test**: Scan Go project with go.mod, verify extracted module name/version/dependencies
**Deliverable**: GoAnalyzer with complete metadata extraction

- [ ] T085 [US6] Create src/profile_generator/analyzers/go.py module (≤200 LOC)
- [ ] T086 [US6] Implement GoAnalyzer class extending BaseAnalyzer with DI
- [ ] T087 [US6] Implement can_analyze() method detecting go.mod
- [ ] T088 [US6] Implement go.mod parsing in GoAnalyzer.analyze()
- [ ] T089 [US6] Extract module name and Go version from go.mod
- [ ] T090 [US6] Extract dependencies from require directives in go.mod
- [ ] T091 [US6] Extract module replacements from replace directives
- [ ] T092 [US6] Create Technology instances for Go language and dependencies
- [ ] T093 [US6] Implement README.md parsing for project description
- [ ] T094 [US6] Handle pre-modules Go projects (no go.mod) with directory structure detection
- [ ] T095 [US6] Add graceful handling of malformed go.mod files
- [ ] T096 [US6] Return Project model instance from analyze() method

---

## Phase 9: Analyzer Factory & Project Detection (P1 - MVP)

**Story Goal**: Implement Factory Pattern for analyzer creation with confidence-based project detection
**Independent Test**: Test detection logic with various project structures, verify correct analyzer selected
**Deliverable**: AnalyzerFactory implementing hybrid confidence scoring from research.md

- [X] T097 Create src/profile_generator/analyzers/factory.py module (≤100 LOC)
- [X] T098 Implement ProjectDetector class with confidence scoring logic from research.md
- [X] T099 Add detection signals with weights: pyproject.toml +50, setup.py +30, requirements.txt +20
- [X] T100 Add detection signals for Node.js: package.json +50
- [X] T101 Add detection signals for Go: go.mod +50
- [X] T102 Implement calculate_confidence(path) method returning dict[ProjectType, int]
- [X] T103 Set confidence threshold to 40 points for project type determination
- [X] T104 Implement AnalyzerFactory class with analyzer registration
- [X] T105 Register PythonAnalyzer, NodeJSAnalyzer, GoAnalyzer in factory
- [X] T106 Implement AnalyzerFactory.create(path) method using ProjectDetector
- [X] T107 Return appropriate analyzer instance based on detected project type
- [X] T108 Handle unknown project type gracefully (log warning, return None or UnknownAnalyzer)

---

## Phase 10: CLI Interface (P1 - MVP)

**Story Goal**: Implement Typer-based CLI with scan, config, version commands
**Independent Test**: Run CLI commands, verify outputs, exit codes, help messages
**Deliverable**: Complete CLI interface with all P1 functionality

- [X] T109 Create src/profile_generator/cli.py module (≤200 LOC)
- [X] T110 Import Typer and create app instance with CLI configuration
- [X] T111 Implement scan command with Typer decorators and type hints
- [X] T112 Add --input option to scan command (list of paths, optional)
- [X] T113 Add --output option to scan command (output directory, default ./output)
- [X] T114 Add --format option to scan command (json/markdown/both, default both)
- [X] T115 Add --verbose flag to scan command (structured logging level INFO)
- [X] T116 Add --debug flag to scan command (structured logging level DEBUG)
- [X] T117 Add --quiet flag to scan command (structured logging level ERROR)
- [X] T118 Implement config command showing effective configuration with sources
- [X] T119 Implement version command displaying __version__ from __init__.py
- [X] T120 Implement main() function orchestrating Scanner and Exporters
- [X] T121 Add configuration loading with precedence: CLI > ENV > defaults
- [X] T122 Implement exit code logic: 0 (success), 1 (error), 2 (config invalid)
- [X] T123 Add error handling with actionable error messages in CLI
- [X] T124 Configure Typer to show rich help messages with --help
- [X] T124a Implement temporary file cleanup in main() with try/finally and atexit handler

---

## Phase 11: Configuration Management (P1 - MVP Core)

**Story Goal**: Load configuration from multiple sources with correct precedence
**Independent Test**: Set conflicting values in ENV and CLI, verify CLI wins
**Deliverable**: Configuration loading with replace strategy from Clarification 2

- [X] T125 Create src/profile_generator/config.py module (≤200 LOC)  [ALREADY IMPLEMENTED via models/config.py]
- [X] T126 Implement load_configuration() function with precedence logic [IMPLEMENTED via Pydantic + CLI instantiation]
- [X] T127 Load configuration from ENV vars with PROFILE_GEN_ prefix [IMPLEMENTED via model_config]
- [X] T128 Load default configuration values [IMPLEMENTED via Field defaults]
- [X] T129 Implement CLI arguments override (replace strategy for lists) [IMPLEMENTED in cli.py scan()]
- [X] T130 Validate loaded configuration using Configuration model [IMPLEMENTED via Pydantic validators]
- [X] T131 Add structured logging for configuration source and final values [IMPLEMENTED in cli.py]
- [X] T132 Return validated Configuration instance from load_configuration() [IMPLEMENTED in cli.py]

---

## Phase 12: Test Fixtures & Integration Tests (P1 - MVP)

**Story Goal**: Create test fixtures and integration tests for end-to-end validation
**Independent Test**: Run integration tests, verify all P1 user stories pass
**Deliverable**: Complete test suite for MVP functionality

- [X] T133 [P] Create tests/fixtures/python_project/ directory structure
- [X] T134 [P] Add sample pyproject.toml, README.md, Python files to python_project fixture
- [X] T135 [P] Create tests/fixtures/nodejs_project/ directory structure
- [X] T136 [P] Add sample package.json, README.md, JavaScript files to nodejs_project fixture
- [X] T137 [P] Create tests/fixtures/go_project/ directory structure
- [X] T138 [P] Add sample go.mod, README.md, Go files to go_project fixture
- [ ] T139 Create tests/integration/test_cli.py for end-to-end CLI workflows
- [ ] T140 Create tests/integration/test_python_project.py for Python analyzer integration
- [ ] T141 Create tests/integration/test_nodejs_project.py for Node.js analyzer integration
- [ ] T142 Create tests/integration/test_go_project.py for Go analyzer integration
- [ ] T143 Implement integration test: scan fixtures, verify JSON output structure
- [ ] T144 Implement integration test: scan fixtures, verify Markdown output formatting
- [ ] T145 Implement integration test: test configuration precedence (ENV vs CLI)
- [ ] T146 Implement integration test: test error handling for invalid paths
- [ ] T147 Verify ≥80% test coverage requirement met for all P1 code

---

## Phase 13: User Story 7 - Enhanced Configuration (P2 - Enhanced)

**Story Goal**: Add config.yaml support with full precedence chain
**Independent Test**: Set values in config.yaml, ENV, CLI; verify precedence
**Deliverable**: Full configuration system with config.yaml support

- [ ] T148 [US7] Add PyYAML dependency to pyproject.toml for YAML parsing
- [ ] T149 [US7] Implement config.yaml loading in src/profile_generator/config.py
- [ ] T150 [US7] Update precedence logic: CLI > ENV > config.yaml > defaults
- [ ] T151 [US7] Implement replace strategy for list-type values (scan_paths)
- [ ] T152 [US7] Add validation for config.yaml syntax errors with clear error messages
- [ ] T153 [US7] Update config command to show which source provided each value
- [ ] T154 [US7] Add structured logging for config.yaml loading and parsing

---

## Phase 14: User Story 8 - Git Repository Analysis (P2 - Enhanced)

**Story Goal**: Extract Git metadata (all-time commits, top 5 contributors, branch, tags)
**Independent Test**: Scan Git repository, verify commit count and contributors accuracy
**Deliverable**: GitAnalyzer extracting all metadata from Clarification 3

- [ ] T155 [US8] Create src/profile_generator/git/__init__.py package
- [ ] T156 [US8] Create src/profile_generator/git/analyzer.py module (≤200 LOC)
- [ ] T157 [US8] Implement GitAnalyzer class with __init__(path: Path) using DI
- [ ] T158 [US8] Implement is_git_repo() method checking for .git directory
- [ ] T159 [US8] Implement get_commit_count() method for all-time commit count using git rev-list
- [ ] T160 [US8] Implement get_top_contributors() method for top 5 contributors by commit count
- [ ] T161 [US8] Use git shortlog -sn --all for contributor extraction
- [ ] T162 [US8] Implement get_branch() method for active branch name
- [ ] T163 [US8] Implement get_remote_url() method for remote repository URL
- [ ] T164 [US8] Implement get_last_commit_date() method using git log
- [ ] T165 [US8] Implement get_tags() method for Git tags list
- [ ] T166 [US8] Handle detached HEAD state: return commit SHA instead of branch name
- [ ] T167 [US8] Add graceful handling of corrupted Git repositories
- [ ] T168 [US8] Integrate GitAnalyzer into Scanner for projects with .git/
- [ ] T169 [US8] Update Project model population with Repository data when Git available
- [ ] T170 [US8] Add structured logging for Git analysis success/failure

---

## Phase 15: User Story 9 - Code Statistics (P2 - Enhanced)

**Story Goal**: Calculate LOC by language and file counts for project statistics
**Independent Test**: Scan multi-language project, verify LOC counts match manual count
**Deliverable**: StatsCalculator with accurate language detection and counting

- [ ] T171 [US9] Create src/profile_generator/stats/__init__.py package
- [ ] T172 [US9] Create src/profile_generator/stats/calculator.py module (≤200 LOC)
- [ ] T173 [US9] Implement StatsCalculator class with __init__(path: Path) using DI
- [ ] T174 [US9] Implement file type detection logic for language identification
- [ ] T175 [US9] Implement count_loc() method with streaming file reading for memory efficiency
- [ ] T176 [US9] Add LOC counting for Python (.py), JavaScript (.js, .jsx, .ts, .tsx), Go (.go)
- [ ] T177 [US9] Implement exclusion logic for binaries, build artifacts (dist/, build/, node_modules/)
- [ ] T178 [US9] Implement source file counting with whitelist approach (Clarification 4)
- [ ] T179 [US9] Enforce 100k source file limit per project
- [ ] T180 [US9] Implement loc_by_language dict aggregation
- [ ] T181 [US9] Separate source LOC from test LOC when possible (tests/, __tests__/)
- [ ] T182 [US9] Integrate StatsCalculator into analyzers to populate Statistics model
- [ ] T183 [US9] Add structured logging for statistics calculation progress

---

## Phase 16: User Story 10 - Dry Run Mode (P2 - Enhanced)

**Story Goal**: Preview scan results without writing files
**Independent Test**: Run with --dry-run, verify output to stdout and no files created
**Deliverable**: Dry run mode with complete preview functionality

- [ ] T184 [US10] Add --dry-run flag to scan command in src/profile_generator/cli.py
- [ ] T185 [US10] Update Configuration model to include dry_run field
- [ ] T186 [US10] Modify JSONExporter to skip file write when dry_run=True
- [ ] T187 [US10] Modify MarkdownExporter to skip file write when dry_run=True
- [ ] T188 [US10] Implement preview output to stdout showing what would be generated
- [ ] T189 [US10] Display all errors that would occur during actual execution
- [ ] T190 [US10] Add structured logging indicating dry run mode active
- [ ] T191 [US10] Update --help documentation to explain --dry-run behavior

---

## Phase 17: Polish & Cross-Cutting Concerns

**Purpose**: Final quality gates, documentation, and deployment preparation
**Deliverable**: Production-ready CLI tool passing all quality gates

### Documentation

- [ ] T192 [P] Update README.md with installation instructions using uv tool install
- [ ] T193 [P] Add usage examples to README.md for all CLI commands
- [ ] T194 [P] Add configuration documentation to README.md explaining precedence
- [ ] T195 [P] Create ADR-001: CLI framework choice (Typer 0.12+ selected) in docs/decisions/
- [ ] T196 [P] Create ADR-002: Project detection strategy (hybrid confidence scoring) in docs/decisions/
- [ ] T197 [P] Create ADR-003: SOLID principles and design patterns application in docs/decisions/
- [ ] T198 [P] Create ADR-004: File size limits and modularization strategy in docs/decisions/

### Quality Gates

- [ ] T199 Run ruff check --select ALL on entire codebase, fix all violations
- [ ] T200 Run ruff format on entire codebase
- [ ] T201 Run mypy --strict on src/ directory, achieve zero errors
- [ ] T202 Run pytest with coverage, verify ≥80% coverage on all modules
- [ ] T203 Run bandit security scanner, address all security findings
- [ ] T204 Run safety check on dependencies, update vulnerable packages
- [ ] T205 Verify all files ≤300 LOC (base.py ≤150, factory.py ≤100, analyzers ≤200)
- [ ] T206 Manual SOLID compliance review: verify Factory, Strategy, DI patterns implemented
- [ ] T207 Validate JSON output against contracts/projects-output-v1.schema.json schema
- [ ] T208 Integration test with yves-profile-site consumer (mock or actual)

### Performance Validation

- [ ] T209 Performance test: verify < 5s for 100 projects on standard hardware
- [ ] T210 Performance test: verify < 50ms per project average
- [ ] T211 Performance test: verify < 200ms for JSON + Markdown export
- [ ] T212 Memory profiling: verify < 500MB RAM usage during execution
- [ ] T213 Test edge case: verify 100k source file limit enforcement and error message

### Final Checks

- [ ] T214 Verify all FR-001 through FR-024 implemented and tested
- [ ] T215 Verify all SC-001 through SC-015 success criteria met
- [ ] T216 Verify all P1 user stories (1-6) fully implemented and tested
- [ ] T217 Final code review: check for hardcoded paths, credentials, debug code
- [ ] T218 Update CHANGELOG.md with v0.1.0 release notes
- [ ] T219 Tag release v0.1.0 following semantic versioning

---

## Dependencies Between Phases

**Execution Order** (user story completion sequence):

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
Phase 3 (US1: Scanning) ←─────┐
    ↓                          │
Phase 9 (Analyzer Factory) ←───┤ (requires analyzers)
    ↓                          │
Phase 4 (US2: JSON Export)     │
    ∥                          │
Phase 5 (US3: Markdown Export) │
    ∥                          │
Phase 6 (US4: Python) ─────────┤
    ∥                          │
Phase 7 (US5: Node.js) ────────┤
    ∥                          │
Phase 8 (US6: Go) ─────────────┘
    ↓
Phase 10 (CLI Interface)
    ↓
Phase 11 (Configuration)
    ↓
Phase 12 (Tests)
    ↓
[P2 Features - Can be done in any order]
Phase 13 (US7: Enhanced Config)
    ∥
Phase 14 (US8: Git Analysis)
    ∥
Phase 15 (US9: Code Statistics)
    ∥
Phase 16 (US10: Dry Run)
    ↓
Phase 17 (Polish)
```

**Parallel Execution Examples**:

**After Phase 2 completes**, these can run in parallel:
- Phase 6 (US4: Python analyzer) + Phase 7 (US5: Node.js analyzer) + Phase 8 (US6: Go analyzer)
- Phase 4 (US2: JSON exporter) + Phase 5 (US3: Markdown exporter)

**Within Phase 2**, these can run in parallel:
- All model definitions (T011-T022)
- All utility modules (T029-T032)

**Within Phase 17**, these can run in parallel:
- All documentation tasks (T192-T198)
- All quality gate runs (T199-T208)

---

## Task Summary

**Total Tasks**: 220
**Phases**: 17 (1 Setup + 1 Foundational + 9 User Story Phases + 1 Polish)
**P1 MVP Tasks**: T001-T147 (148 tasks covering User Stories 1-6, includes T124a)
**P2 Enhanced Tasks**: T148-T191 (44 tasks covering User Stories 7-10)
**P3 Future Tasks**: None (User Story 11 deferred)
**Parallel Opportunities**: 32 tasks marked with [P]

**User Story Breakdown**:
- Setup & Foundational: 32 tasks (T001-T032)
- US1 (Scanning): 9 tasks (T033-T041)
- US2 (JSON Export): 8 tasks (T042-T049)
- US3 (Markdown Export): 10 tasks (T050-T059)
- US4 (Python): 12 tasks (T060-T071)
- US5 (Node.js): 13 tasks (T072-T084)
- US6 (Go): 12 tasks (T085-T096)
- Factory & Detection: 12 tasks (T097-T108)
- CLI Interface: 17 tasks (T109-T124a)
- Configuration: 8 tasks (T125-T132)
- Test Fixtures: 15 tasks (T133-T147)
- US7 (Enhanced Config): 7 tasks (T148-T154)
- US8 (Git Analysis): 16 tasks (T155-T170)
- US9 (Statistics): 13 tasks (T171-T183)
- US10 (Dry Run): 8 tasks (T184-T191)
- Polish: 28 tasks (T192-T219)

**MVP Scope** (recommended first release):
- Focus on T001-T147 (Phases 1-12, includes T124a for temporary file cleanup)
- Total: 148 MVP tasks delivering all 6 P1 user stories
- Achieves all critical success criteria
- Provides complete CLI tool with core functionality

**Next Steps**:
1. Begin implementation with Phase 1 (Setup)
2. Follow TDD workflow: RED → GREEN → REFACTOR for each task
3. Run quality gates after each phase
4. Track progress by marking tasks `- [x]` when complete
5. Focus on MVP (148 tasks: T001-T124a, T125-T147) before any P2 work

---

**Status**: ✅ Tasks generated — ready for implementation following TDD workflow
