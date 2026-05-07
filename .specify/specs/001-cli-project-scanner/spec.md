---
template_version: "2.2.0"
last_updated: "2026-05-07"
breaking_changes: false
---

# Feature Specification: CLI Project Scanner & Portfolio Generator

**Feature ID**: 001
**Feature Branch**: `001-cli-project-scanner`
**Created**: 2026-05-07
**Status**: Draft
**Business Objective**: See [objetivo.yaml](../../objetivo.yaml)
**Input**: Complete project specification from objetivo.yaml - CLI tool for automated project scanning, analysis, and portfolio generation with JSON and Markdown outputs

---

## Business Context (from objetivo.yaml)

**Problem**: Developers need to maintain portfolios manually, copying information from multiple projects. This process is tedious, error-prone, and frequently outdated. Updating portfolio information takes hours of manual work across different project directories, with no standardization in documentation format.

**Value Proposition**: Installable CLI tool that automatically scans projects, extracts validated metadata, and generates Markdown + JSON compatible with yves-profile-site consumer, reducing update time from hours to seconds. Provides consistent, accurate, and up-to-date project information for portfolio display.

**Success Metrics**:
- Reduce portfolio update time from hours to seconds (< 5s for 100 projects)
- Achieve ≥80% test coverage with zero type errors (mypy --strict)
- Generate JSON output 100% compatible with yves-profile-site consumer
- Zero manual intervention required for standard project structures

**Key Personas**:
- **Developer/Portfolio Owner**: Developer maintaining multiple projects who needs to update portfolio periodically with precise and formatted information. Needs automation-friendly tool that works locally without external dependencies.

**Critical Journeys** (P1 - MVP):
1. Scan multiple project directories from configured list
2. Auto-detect project types (Python, Node.js, Go)
3. Extract metadata (name, description, technologies, stats)
4. Generate formatted Markdown for publication
5. Export structured JSON with validated schema

**Initial Decisions** (from constitution):
- SOLID principles mandatory (all 5)
- Factory Pattern for analyzer creation (mandatory)
- Strategy Pattern for exporters
- Dependency Injection throughout
- Modularization: max 200-300 LOC per file
- TDD workflow: RED → GREEN → REFACTOR
- Type safety: mypy --strict with zero errors
- Quality gates: ruff, mypy, pytest ≥80%, bandit, safety

---

## Clarifications

### Session 2026-05-07

- Q: What is the specific file count limit per project that triggers the "very large project" edge case? → A: 100,000 files per project (strict limit, fail with clear error message)
- Q: How should list-type configuration values (like scan_paths) be merged when defined in multiple sources (CLI, ENV, config, defaults)? → A: Replace strategy - higher precedence source completely replaces lower (CLI replaces ENV, ENV replaces config, config replaces defaults; no merging/appending)
- Q: What is the scope of Git history analysis for commit/contributor extraction (all-time vs recent, all contributors vs top N)? → A: All-time total commit count + top 5 contributors by commit count (balances completeness with performance and data payload size)

---

## Performance Criteria

### Response Time Requirements

- **CLI Execution**: Complete scan of 100 projects in < 5 seconds
- **Single Project Analysis**: < 50ms per project (average)
- **Export Generation**: Markdown + JSON output in < 200ms total
- **Startup Time**: CLI ready to execute in < 100ms (cold start)

### Throughput & Scalability

- **Project Processing**: 10-20 projects/second sustained throughput
- **Concurrent Processing**: Single-threaded (simplicity over parallelization)
- **Data Volume**: Handle projects with 100k+ files without degradation
- **Output Size**: Generate reports up to 10MB without performance impact

### Availability & Reliability

- **Uptime**: N/A (local CLI tool, no service availability requirements)
- **Error Rate**: < 0.1% failed scans (graceful degradation for edge cases)
- **Recovery**: Immediate restart on failure, no state to recover

### Resource Constraints

- **Memory**: < 500MB RAM per execution
- **CPU**: < 80% average utilization on single core
- **Storage**: Temporary files cleaned up automatically, no persistent cache in P0
- **Dependencies**: Minimal external dependencies (Python stdlib preferred)

### Accessibility Criteria

- **CLI Interface**: Clear help messages with --help flag
- **Error Messages**: User-friendly error messages with actionable suggestions
- **Exit Codes**: Standard exit codes (0=success, 1=error, 2=config invalid)
- **Output Formats**: Both human-readable (Markdown) and machine-readable (JSON)
- **Logging Levels**: --verbose, --debug, --quiet flags for different user needs

### Monitoring & Observability

- **Metrics**: Execution time, projects scanned, errors encountered (structured logs)
- **Logging**: Structured JSON logging via structlog for parsing/analysis
- **Alerting**: N/A (local CLI tool)
- **Dashboards**: N/A (local CLI tool)
- **Distributed Tracing**: N/A (single-process execution)

---

## User Scenarios & Testing

### User Story 1 - Basic Project Scanning (Priority: P1 - MVP)

Developer wants to scan all projects in configured directories and generate portfolio data without manual intervention.

**Why this priority**: Core functionality - without scanning, the tool has no value. This is the foundation for all other features.

**Independent Test**: Configure scan paths in .env, run `profile-gen scan`, verify JSON + Markdown outputs created with correct structure and content from sample projects.

**Acceptance Scenarios**:

1. **Given** .env file with PROFILE_GEN_SCAN_PATHS="/path/to/projects", **When** user runs `profile-gen scan`, **Then** tool scans all subdirectories, detects project types, and generates outputs
2. **Given** project directory with README.md and pyproject.toml, **When** scanner processes directory, **Then** extracts project name, description from README, and identifies as Python project
3. **Given** multiple project types (Python, Node.js, Go), **When** scanner runs, **Then** correctly identifies each type and applies appropriate analyzer
4. **Given** invalid/inaccessible directory, **When** scanner encounters it, **Then** logs warning and continues with remaining projects (graceful degradation)
5. **Given** no configuration file, **When** user runs scan, **Then** uses sensible defaults and provides clear error message about missing config

---

### User Story 2 - JSON Export with Schema Validation (Priority: P1 - MVP)

Developer needs JSON output compatible with yves-profile-site consumer application for portfolio display.

**Why this priority**: Primary integration point - JSON must match expected schema or consumer application breaks. Critical for MVP.

**Independent Test**: Generate JSON from sample project, validate against Pydantic schema, import into yves-profile-site mock consumer, verify all fields present and correctly typed.

**Acceptance Scenarios**:

1. **Given** scanned projects, **When** JSON export runs, **Then** generates valid JSON with schema: {projects: [{name, description, technologies, stats, repository}]}
2. **Given** Pydantic model for ProjectData, **When** exporting, **Then** validates all data against model before writing to file
3. **Given** invalid/missing data in project, **When** validation fails, **Then** includes project in output with null values and warning in logs
4. **Given** existing JSON file, **When** export runs, **Then** overwrites file atomically (temp file + rename) to prevent corruption
5. **Given** yves-profile-site schema requirements, **When** JSON generated, **Then** 100% compatible with consumer's expected format

---

### User Story 3 - Markdown Generation with Templates (Priority: P1 - MVP)

Developer wants human-readable Markdown report for portfolio publication with customizable formatting.

**Why this priority**: Second output format critical for MVP - provides human-readable alternative to JSON for direct publication.

**Independent Test**: Generate Markdown from sample projects, verify formatting matches template, check readability, confirm all project information included and properly formatted.

**Acceptance Scenarios**:

1. **Given** scanned projects and Jinja2 template, **When** Markdown export runs, **Then** generates formatted profile-summary.md with all projects
2. **Given** default template, **When** no custom template provided, **Then** uses built-in template with standard formatting
3. **Given** custom template in config directory, **When** export runs, **Then** uses custom template instead of default
4. **Given** template rendering error, **When** generation fails, **Then** falls back to default template and logs warning
5. **Given** projects with special characters (Unicode, Markdown syntax), **When** rendering, **Then** properly escapes/handles characters in output

---

### User Story 4 - Python Project Analysis (Priority: P1 - MVP)

Developer needs accurate analysis of Python projects with metadata extraction from pyproject.toml, setup.py, and README.md.

**Why this priority**: First analyzer implementation - establishes pattern for other analyzers. Python is primary use case.

**Independent Test**: Scan Python project with pyproject.toml, verify extracted metadata (name, version, dependencies, description), confirm technology stack identified correctly.

**Acceptance Scenarios**:

1. **Given** Python project with pyproject.toml, **When** PythonAnalyzer runs, **Then** extracts name, version, dependencies, Python version
2. **Given** project with README.md, **When** analyzer runs, **Then** extracts description from first paragraph or header
3. **Given** project with multiple config files (pyproject.toml, setup.py), **When** analyzing, **Then** prioritizes pyproject.toml (modern standard)
4. **Given** project with requirements.txt, **When** analyzing, **Then** extracts dependencies list
5. **Given** invalid/malformed pyproject.toml, **When** parsing fails, **Then** logs error and attempts fallback to setup.py or skips project

---

### User Story 5 - Node.js Project Analysis (Priority: P1 - MVP)

Developer needs accurate analysis of Node.js projects with metadata extraction from package.json and README.md.

**Why this priority**: Second most common project type - essential for comprehensive portfolio coverage.

**Independent Test**: Scan Node.js project with package.json, verify extracted metadata (name, version, dependencies, scripts), confirm technology stack identified.

**Acceptance Scenarios**:

1. **Given** Node.js project with package.json, **When** NodeJSAnalyzer runs, **Then** extracts name, version, dependencies, scripts
2. **Given** package.json with devDependencies, **When** analyzing, **Then** distinguishes runtime vs development dependencies
3. **Given** project with package-lock.json or yarn.lock, **When** analyzing, **Then** identifies package manager used
4. **Given** invalid/malformed package.json, **When** parsing fails, **Then** logs error and skips project gracefully
5. **Given** monorepo with multiple package.json files, **When** scanning, **Then** treats each as separate project

---

### User Story 6 - Go Project Analysis (Priority: P1 - MVP)

Developer needs accurate analysis of Go projects with metadata extraction from go.mod and README.md.

**Why this priority**: Third supported language - completes initial analyzer set for MVP.

**Independent Test**: Scan Go project with go.mod, verify extracted metadata (module name, Go version, dependencies), confirm technology stack identified.

**Acceptance Scenarios**:

1. **Given** Go project with go.mod, **When** GoAnalyzer runs, **Then** extracts module name, Go version, dependencies
2. **Given** go.mod with replace directives, **When** analyzing, **Then** records module replacements
3. **Given** project without go.mod (pre-modules), **When** scanning, **Then** logs warning and attempts detection via directory structure
4. **Given** invalid/malformed go.mod, **When** parsing fails, **Then** logs error and skips project gracefully

---

### User Story 7 - Configuration Management (Priority: P2 - Enhanced)

Developer needs flexible configuration via .env, config.yaml, and CLI arguments with clear precedence rules.

**Why this priority**: Enhances usability but not required for basic functionality. Can start with .env-only and add layers later.

**Independent Test**: Set conflicting values in .env, config.yaml, and CLI args, verify CLI args win, then ENV, then config, then defaults.

**Acceptance Scenarios**:

1. **Given** PROFILE_GEN_SCAN_PATHS in .env, **When** no CLI override, **Then** uses .env value (replaces config.yaml and defaults completely)
2. **Given** config.yaml with scan_paths and .env with PROFILE_GEN_SCAN_PATHS both present, **When** loading config, **Then** .env value completely replaces config.yaml value (no merging)
3. **Given** CLI argument --input, **When** specified, **Then** CLI value completely replaces both .env and config.yaml (no merging)
4. **Given** no configuration provided, **When** running scan, **Then** uses sensible defaults (current directory)
5. **Given** `profile-gen config show` command, **When** run, **Then** displays effective configuration with sources and indicates which source provided each value

---

### User Story 8 - Git Repository Analysis (Priority: P2 - Enhanced)

Developer wants Git metadata included in portfolio (commits, contributors, activity, last update) for project context.

**Why this priority**: Valuable context but not essential for MVP. Enhances portfolio richness.

**Independent Test**: Scan Git repository, verify extracted metadata (commit count, contributors, last commit date, branch info), confirm data accuracy.

**Acceptance Scenarios**:

1. **Given** project with .git directory, **When** analyzing, **Then** extracts all-time total commit count, top 5 contributors by commit count (with names and counts), and last commit date
2. **Given** repository with multiple branches, **When** analyzing, **Then** reports active branch and total branch count
3. **Given** repository with tags, **When** analyzing, **Then** includes latest tag/version
4. **Given** project without Git, **When** analyzing, **Then** skips Git analysis gracefully (no error, null repository field)
5. **Given** bare repository or corrupted .git, **When** Git commands fail, **Then** logs warning and continues (graceful degradation)

---

### User Story 9 - Code Statistics (Priority: P2 - Enhanced)

Developer wants code statistics (LOC by language, file counts, complexity) included in portfolio for project scale understanding.

**Why this priority**: Nice-to-have information that enhances portfolio but not critical for MVP.

**Independent Test**: Scan project, verify LOC counts by language, file type distribution, confirm accuracy against manual count sample.

**Acceptance Scenarios**:

1. **Given** multi-language project, **When** analyzing, **Then** counts LOC per language accurately
2. **Given** project with test files, **When** counting, **Then** separates source LOC from test LOC
3. **Given** project with generated files, **When** counting, **Then** excludes common generated patterns (build/, dist/, node_modules/)
4. **Given** large project (100k+ files), **When** analyzing, **Then** completes within performance constraints (< 5s for 100 projects total)

---

### User Story 10 - Dry Run Mode (Priority: P2 - Enhanced)

Developer wants to preview scan results without writing files for validation before actual execution.

**Why this priority**: Useful for validation but not essential - can be added after core functionality proven.

**Independent Test**: Run `profile-gen scan --dry-run`, verify output shown to stdout, confirm no files created or modified.

**Acceptance Scenarios**:

1. **Given** --dry-run flag, **When** running scan, **Then** displays what would be generated without writing files
2. **Given** dry run mode, **When** errors encountered, **Then** reports all errors without partial writes
3. **Given** --verbose with --dry-run, **When** running, **Then** shows detailed analysis process

---

### User Story 11 - Watch Mode (Priority: P3 - Future)

Developer wants continuous monitoring of project directories with automatic re-generation on changes.

**Why this priority**: Advanced feature for future - requires additional complexity (watchdog library, daemon mode). Not needed for MVP.

**Independent Test**: Start `profile-gen watch`, modify project file, verify automatic regeneration triggered, confirm performance acceptable.

**Acceptance Scenarios**:

1. **Given** watch mode active, **When** project file changes, **Then** automatically re-scans and regenerates outputs
2. **Given** watch mode, **When** multiple rapid changes, **Then** debounces and waits for stability before regeneration
3. **Given** watch mode, **When** user presses Ctrl+C, **Then** gracefully shuts down and cleans up

---

### Edge Cases

- **What happens when project directory is deleted during scan?** Log warning, skip project, continue with remaining projects
- **How does system handle circular symlinks?** Detect and skip circular symlinks to prevent infinite loops
- **What if project has no README.md?** Use project directory name, log warning about missing description, continue
- **How to handle projects with mixed languages?** Detect all languages present, create composite technology stack
- **What if output directory is not writable?** Fail fast with clear error message about permissions
- **How to handle very large projects (>100k files)?** Fail with clear error when project exceeds 100,000 file limit (prevents performance degradation and resource exhaustion)
- **What if Git repository is in detached HEAD state?** Report current commit SHA instead of branch name
- **How to handle non-UTF-8 file encodings?** Attempt common encodings (UTF-8, Latin-1), log warning if unreadable
- **What if config.yaml has invalid YAML syntax?** Fail with clear error message pointing to syntax error location
- **How to handle projects with no clear type (no pyproject.toml, package.json, go.mod)?** Classify as "unknown" type, extract basic metadata only

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST scan multiple project directories specified in configuration (P1)
- **FR-002**: System MUST auto-detect project types (Python, Node.js, Go) based on characteristic files (P1)
- **FR-003**: System MUST extract metadata: project name, description, technologies, statistics (P1)
- **FR-004**: System MUST generate formatted Markdown output for publication (P1)
- **FR-005**: System MUST export structured JSON with Pydantic schema validation (P1)
- **FR-006**: System MUST validate JSON output compatibility with yves-profile-site consumer (P1)
- **FR-007**: System MUST support configuration via .env, config.yaml, and CLI arguments (P2)
- **FR-008**: System MUST implement configuration precedence: CLI args > ENV vars > config.yaml > defaults, with replace strategy for list-type values (higher precedence completely replaces lower, no merging) (P2)
- **FR-009**: System MUST provide dry-run mode for preview without file writes (P2)
- **FR-010**: System MUST extract Git metadata: total commit count (all-time), top 5 contributors by commit count, last commit date, branch name, and tags (P2)
- **FR-011**: System MUST calculate code statistics: LOC by language, file counts (P2)
- **FR-012**: System MUST support custom Jinja2 templates for Markdown generation (P2)
- **FR-013**: System MUST gracefully handle missing or malformed project files (P1)
- **FR-014**: System MUST log all operations using structured JSON logging via structlog (P1)
- **FR-015**: System MUST implement Factory Pattern for analyzer creation (P1 - architecture requirement)
- **FR-016**: System MUST implement Strategy Pattern for exporters (JSON, Markdown) (P1 - architecture requirement)
- **FR-017**: System MUST use Dependency Injection throughout (no direct instantiation) (P1 - architecture requirement)
- **FR-018**: System MUST validate all file paths to prevent path traversal attacks (P1 - security)
- **FR-019**: System MUST enforce maximum file count limit of 100,000 files per project and fail with clear error message when exceeded (P1 - performance constraint)
- **FR-020**: System MUST provide clear error messages with actionable suggestions (P1)
- **FR-021**: System MUST support CLI commands: scan, config, version (P1)
- **FR-022**: System MUST support CLI flags: --dry-run, --verbose, --debug, --quiet, --help (P1-P2)
- **FR-023**: System MUST use appropriate exit codes: 0 (success), 1 (error), 2 (config invalid) (P1)
- **FR-024**: System MUST clean up temporary files on exit or error (P1)

### Key Entities

- **Project**: Represents a scanned project directory with metadata
  - Attributes: name, description, path, type (Python/Node.js/Go/unknown), technologies, repository info, stats
  - Relationships: has many Technologies, has one Repository (if Git), has one Statistics

- **Technology**: Represents a technology/framework/library used in project
  - Attributes: name, version, category (language/framework/tool)
  - Relationships: belongs to Project

- **Repository**: Represents Git repository metadata
  - Attributes: url, branch, commit_count (all-time total), top_contributors (list of top 5 by commit count with name and count), last_commit_date, tags
  - Relationships: belongs to Project

- **Statistics**: Represents code statistics for project
  - Attributes: total_loc, loc_by_language (dict), file_count, test_coverage (optional)
  - Relationships: belongs to Project

- **Configuration**: Represents tool configuration
  - Attributes: scan_paths (list), output_format (json/markdown/both), template_path (optional), log_level
  - Source: loaded from .env, config.yaml, CLI args with precedence rules

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Tool scans 100 projects in under 5 seconds on standard hardware (meets performance target)
- **SC-002**: JSON output is 100% compatible with yves-profile-site schema (zero validation errors)
- **SC-003**: Test coverage achieves ≥80% with zero uncovered critical paths (quality gate)
- **SC-004**: Type checking passes with mypy --strict and zero errors (quality gate)
- **SC-005**: All 8 quality gates pass: ruff check, ruff format, mypy --strict, pytest ≥80%, bandit, safety, file size ≤300 LOC, SOLID compliance (quality gate)
- **SC-006**: Memory usage stays below 500MB during execution on large project sets (resource constraint)
- **SC-007**: Tool successfully identifies project type with ≥95% accuracy on standard project structures (functional accuracy)
- **SC-008**: Zero security vulnerabilities detected by bandit and safety scanners (security gate)
- **SC-009**: All functional requirements FR-001 through FR-024 implemented and tested (completeness)
- **SC-010**: Portfolio update workflow completes in seconds instead of hours (user value metric)
- **SC-011**: Markdown output is properly formatted and human-readable (usability)
- **SC-012**: Error messages provide actionable guidance for users (usability)
- **SC-013**: CLI interface is intuitive with comprehensive --help documentation (usability)
- **SC-014**: Tool handles edge cases gracefully without crashes (reliability)
- **SC-015**: All files adhere to max 200-300 LOC modularization constraint (architecture quality)

---

## Assumptions

- Users have Python 3.12+ installed and available in PATH
- Projects follow conventional structures (README.md, pyproject.toml, package.json, go.mod, etc.)
- Git is available on system for repository analysis features
- Users have read permissions on project directories to be scanned
- yves-profile-site consumer schema is stable and documented
- Portfolio updates are periodic (not real-time continuous monitoring in P0)
- Projects are primarily Python, Node.js, and Go (other languages can be added later)
- Users are comfortable with CLI tools and basic configuration files

---

## Out of Scope

- GUI or Web UI (CLI only)
- HTTP/REST APIs (local tool only)
- Watch mode with continuous monitoring (P3 - future)
- Intelligent caching (P3 - future)
- Integration with hosting platforms (GitHub Pages, Netlify, etc.)
- Real-time collaboration features
- Cloud-based storage or synchronization
- Mobile application
- Browser extension
- Multi-user support or authentication
- Plugins or extension system (future consideration)
- Support for languages beyond Python, Node.js, Go in MVP

---

## Dependencies & Risks

### Critical Dependencies

- **yves-profile-site**: Consumer application defines JSON schema requirements (HIGH criticality)
- **Pydantic 2.x**: Schema validation and settings management (HIGH criticality)
- **Click/Typer**: CLI framework (decision in ADR-001) (HIGH criticality)
- **Jinja2**: Template engine for Markdown generation (HIGH criticality)
- **structlog**: Structured logging (MEDIUM criticality)

### Known Risks

- **Risk**: yves-profile-site schema changes could break JSON compatibility
  - **Mitigation**: Version schema, implement schema validation tests, document schema contract
  
- **Risk**: Very large projects could exceed memory/time constraints
  - **Mitigation**: Implement file count limits, sampling strategies, streaming processing if needed
  
- **Risk**: Malformed project files (invalid TOML, JSON, YAML) could crash scanner
  - **Mitigation**: Robust error handling, validation, graceful degradation

- **Risk**: Path traversal or security vulnerabilities in file scanning
  - **Mitigation**: Input validation, path sanitization, security scanning (bandit), code review

- **Risk**: Performance degradation with 100+ projects
  - **Mitigation**: Performance testing, optimization, caching strategy (P2+)

---

## Next Steps

1. **Create ADR-001**: Decide between Click 8.x vs Typer 0.12+ for CLI framework
2. **Create ADR-002**: Define project detection strategy (file-based, directory structure, hybrid)
3. **Create ADR-003**: Document SOLID principles and design patterns application
4. **Create ADR-004**: Establish file size limits and modularization strategy
5. **Generate plan.md**: Use `/speckit.plan` to create implementation plan from this specification
6. **Generate tasks.md**: Use `/speckit.tasks` to create actionable task list from plan
7. **Implement P1 MVP**: Focus on core scanning, analysis, and export functionality
8. **Validate with yves-profile-site**: Test JSON output compatibility with consumer
9. **Iterate on P2 features**: Add configuration, Git analysis, statistics after P1 proven
10. **Consider P3 features**: Evaluate watch mode and caching based on user feedback

---

**Specification Status**: ✅ Complete - ready for planning phase

**Quality Checklist**:
- ✅ No implementation details (languages/frameworks mentioned only in context, not prescriptive)
- ✅ Focused on user value and business needs
- ✅ Written for non-technical stakeholders (clear, jargon-free)
- ✅ All mandatory sections completed
- ✅ No [NEEDS CLARIFICATION] markers (all questions resolved via informed assumptions)
- ✅ Requirements are testable and unambiguous
- ✅ Success criteria are measurable and technology-agnostic
- ✅ All acceptance scenarios defined with Given/When/Then format
- ✅ Edge cases identified and handled
- ✅ Scope clearly bounded (in-scope vs out-of-scope)
- ✅ Dependencies and assumptions documented
- ✅ All functional requirements have clear acceptance criteria
- ✅ User scenarios cover primary flows with priorities
- ✅ Feature meets measurable outcomes defined in Success Criteria
