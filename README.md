# Profile Generator

> CLI tool for automated project scanning, analysis, and portfolio generation

**Status**: 🚧 Alpha | **Version**: 0.1.0
**Repository**: https://github.com/yvesmarinho/profile-generator
**Created**: 2026-05-07

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Overview

**Profile Generator** automatically scans project directories, detects project types (Python, Node.js, Go), extracts validated metadata, and generates both **Markdown** and **JSON** outputs compatible with portfolio websites.

**Key Features**:

- 🔍 **Auto-detect** project types (Python, Node.js, Go)
- 📊 **Extract metadata**: name, description, technologies, statistics
- 📄 **Markdown generation** with customizable Jinja2 templates
- 📦 **JSON export** with Pydantic schema validation (100% yves-profile-site compatible)
- ⚡ **Fast scanning**: <5s for 100 projects
- 🧪 **TDD-driven**: ≥80% test coverage with mypy --strict
- 🏗️ **SOLID architecture**: Factory Pattern, Strategy Pattern, Dependency Injection

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+ installed
- [uv package manager](https://github.com/astral-sh/uv) installed

### Installation

```bash
# Clone repository
git clone https://github.com/yvesmarinho/profile-generator.git
cd profile-generator

# Install dependencies
make install-deps

# Install in development mode
make dev
```

### Usage

```bash
# Scan current directory and generate portfolio
profile-gen scan

# Scan specific directories
profile-gen scan --input ~/projects --input ~/work

# Generate JSON only
profile-gen scan --format json --output ./output

# Generate Markdown only with custom template
profile-gen scan --format markdown --template ./my-template.md.jinja2

# Dry run (preview without writing files)
profile-gen scan --dry-run

# Show effective configuration
profile-gen config

# Show version
profile-gen version
```

---

## 📚 Documentation

### User Documentation

- [Installation Guide](docs/guides/installation.md)
- [Usage Examples](docs/guides/usage.md)
- [Configuration](docs/guides/configuration.md)
- [Custom Templates](docs/guides/templates.md)

### Developer Documentation

- **Specification**: [.specify/specs/001-cli-project-scanner/spec.md](.specify/specs/001-cli-project-scanner/spec.md)
- **Implementation Plan**: [.specify/specs/001-cli-project-scanner/plan.md](.specify/specs/001-cli-project-scanner/plan.md)
- **Data Model**: [.specify/specs/001-cli-project-scanner/data-model.md](.specify/specs/001-cli-project-scanner/data-model.md)
- **Quickstart Guide**: [.specify/specs/001-cli-project-scanner/quickstart.md](.specify/specs/001-cli-project-scanner/quickstart.md)
- [Architecture Documentation](docs/architecture/README.md)

---

## 🏗️ Project Structure

```
profile-generator/
├── src/profile_generator/      # Source code
│   ├── models/                 # Pydantic data models
│   ├── analyzers/             # Project type analyzers (Factory Pattern)
│   ├── exporters/             # Output exporters (Strategy Pattern)
│   ├── git/                   # Git metadata extraction
│   ├── stats/                 # Code statistics calculation
│   ├── utils/                 # Utilities (logging, validation)
│   ├── cli.py                 # CLI entrypoint (Typer)
│   ├── config.py              # Configuration management
│   └── scanner.py             # Directory scanner
├── tests/                     # Test suite (≥80% coverage)
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── fixtures/              # Test fixtures (sample projects)
├── .specify/                  # Specification-driven development artifacts
└── docs/                      # Documentation

```

---

## 🛠️ Development

### Setup

```bash
# Install dev dependencies
make install-deps

# Run tests with coverage
make test

# Run linters (ruff, mypy, bandit, safety)
make lint

# Format code
make format

# Clean build artifacts
make clean
```

### Quality Gates

All quality gates must pass before merge:

1. **Linting**: `ruff check --select ALL` (zero warnings)
2. **Formatting**: `ruff format` (auto-applied)
3. **Type checking**: `mypy --strict src/` (zero errors)
4. **Tests**: `pytest --cov` (≥80% coverage)
5. **Security**: `bandit -r src/` (zero vulnerabilities)
6. **Dependencies**: `safety check` (zero vulnerabilities)
7. **File size**: All files ≤300 LOC
8. **SOLID compliance**: Manual review checklist

### Architecture Principles

- **SOLID**: All 5 principles enforced
- **Design Patterns**: Factory (analyzers), Strategy (exporters), DI (throughout)
- **TDD**: RED → GREEN → REFACTOR workflow
- **Type Safety**: mypy --strict with zero errors
- **Modularization**: ≤300 LOC per file (base.py ≤150, factory.py ≤100)

---

## 📊 Performance

- **Scan speed**: < 5s for 100 projects on standard hardware (4-core CPU, 8GB RAM, SSD)
- **Per-project**: < 50ms average analysis time
- **Export generation**: < 200ms total for JSON + Markdown
- **Memory usage**: < 500MB RAM during execution
- **File limit**: 100,000 source files per project (whitelist approach)

---

## 🔒 Security

- Path traversal prevention (validates all file paths)
- No code execution (no eval/exec/subprocess of project code)
- Dependency scanning with `bandit` and `safety`
- Secure defaults for all configurations

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Follow TDD workflow (RED → GREEN → REFACTOR)
4. Ensure all quality gates pass
5. Commit changes following [Conventional Commits](https://www.conventionalcommits.org/)
6. Push to branch
7. Open Pull Request

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yvesmarinho/profile-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yvesmarinho/profile-generator/discussions)
- **Documentation**: [docs/](docs/)

---

**Built with** ❤️  **using Specification-Driven Development**
