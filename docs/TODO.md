# 📝 TODO — Profile Generator

**Last Updated**: 2026-05-07T18:30:00Z — MVP Implementation ✅ Complete (Phases 1-12)
**Status**: 🟢 MVP Funcional | 124/220 tasks (56%)

---

## 🎯 Objetivo

Ferramenta CLI para escanear projetos, compilar metadados e gerar outputs estruturados (JSON + Markdown) para portfólio/currículo.

---

## 🟢 MVP Completo (Phases 1-12)

✅ **User Stories MVP (6/6 complete)**
- ✅ US1: Directory scanning com symlink detection
- ✅ US2: JSON export com Pydantic validation
- ✅ US3: Markdown export com Jinja2 templates
- ✅ US4: Python project analysis (pyproject.toml, setup.py, requirements.txt)
- ✅ US5: Node.js project analysis (package.json, package manager detection)
- ✅ US6: Go project analysis (go.mod parsing)

**Resultado**: CLI funcional, 3 analyzers, 2 exporters, end-to-end validated ✅

---

## 🟠 Em Progresso

*(nenhum)*

---

## 🔵 P0 - Próximas Implementações (Crítico)

### Phase 13: Git Metadata Module (T147-T162)
- [ ] Criar `src/profile_generator/git/` module
- [ ] Implementar extração de commit history
- [ ] Implementar extração de contributors (top N)
- [ ] Implementar last commit date
- [ ] Integrar com analyzers para popular Repository fields
- [ ] Testar com fixture projects

### Phase 14: Code Statistics Module (T163-T173)
- [ ] Criar `src/profile_generator/stats/` module
- [ ] Implementar LOC calculation por linguagem
- [ ] Implementar file counting
- [ ] Integrar com analyzers para popular Statistics fields
- [ ] Substituir placeholders (total_loc=0)

### Phase 15: Integration Tests (T139-T146)
- [ ] Criar `tests/integration/` directory
- [ ] Test scanner com fixtures
- [ ] Test analyzers individualmente
- [ ] Test exporters com sample data
- [ ] Test CLI end-to-end
- [ ] Atingir ≥80% coverage requirement
- [ ] Configurar pytest-cov com branch coverage

---

## 🔵 P1 - Alta Prioridade

### Code Quality & CI/CD
- [ ] Configurar GitHub Actions
  - [ ] Workflow: tests + coverage
  - [ ] Workflow: lint (ruff check)
  - [ ] Workflow: type check (mypy --strict)
  - [ ] Workflow: security scan (bandit + safety)
  - [ ] Quality gates: max LOC por arquivo, complexidade ciclomática
- [ ] Criar ADR-001: Escolha de framework CLI (Typer)
- [ ] Criar ADR-002: Estratégia de detecção de projetos (confidence scoring)
- [ ] Criar ADR-003: Aplicação de SOLID e design patterns
- [ ] Criar ADR-004: Limites de tamanho de arquivo e modularização
- [ ] Code review checklist baseado em SOLID

### Features P1
- [ ] Configuração via .env e config.yaml (Pydantic Settings)
- [ ] Templates Jinja2 customizáveis (path validation)
- [ ] Documentar API com Sphinx
- [ ] Documentar design patterns aplicados
  - [x] Factory Pattern (analyzers) ✅
  - [x] Strategy Pattern (exporters) ✅
  - [x] Builder Pattern (metadados) ✅
  - [x] Adapter Pattern (projeto → modelo comum) ✅

---

## 🔵 P2 - Desejável

- [ ] Watch mode (watchdog)
- [ ] Filtros e exclusões (regex)
- [ ] Cache inteligente
- [ ] Performance optimization (Phases 15+)
- [ ] Additional analyzers (Rust, Ruby, etc)
- [ ] Fix: Go README parsing (limitar a primeiro parágrafo)

---

## ✅ Concluído (Phases 1-12)

### Phase 1: Setup (T001-T010) ✅
- [x] pyproject.toml com hatchling build backend
- [x] Package structure (`src/profile_generator/`)
- [x] Makefile com automação uv-based
- [x] README.md completo
- [x] Dependencies instaladas

### Phase 2: Foundational (T011-T032) ✅
- [x] `models/config.py` — Configuration com ENV support
- [x] `models/project.py` — Todas entidades (Project, Technology, Repository, Statistics)
- [x] `analyzers/base.py` — BaseAnalyzer ABC
- [x] `exporters/base.py` — BaseExporter ABC
- [x] `utils/logging.py` — Structured logging (structlog)
- [x] `utils/validators.py` — Path validation com security

### Phase 3: Scanner (T033-T041) ✅
- [x] `scanner.py` — Directory scanner completo
- [x] Symlink circular reference detection
- [x] File count limits (100k per project)
- [x] Path traversal protection
- [x] Structured logging

### Phase 4: JSON Export (T042-T049) ✅
- [x] `exporters/json_exporter.py` — JSONExporter
- [x] Pydantic validation (ProjectsOutput model)
- [x] Atomic file writes (tempfile + rename)
- [x] Tool version injection

### Phase 5: Markdown Export (T050-T059) ✅
- [x] `templates/default.md.jinja2` — Default template
- [x] `exporters/markdown_exporter.py` — MarkdownExporter
- [x] Custom template support com fallback
- [x] Atomic file writes

### Phase 6: Python Analyzer (T060-T071) ✅
- [x] `analyzers/python.py` — PythonAnalyzer
- [x] pyproject.toml parsing (tomllib)
- [x] setup.py parsing (regex)
- [x] requirements.txt parsing
- [x] README.md extraction
- [x] Python version extraction

### Phase 7: Node.js Analyzer (T072-T084) ✅
- [x] `analyzers/nodejs.py` — NodeJSAnalyzer
- [x] package.json parsing
- [x] Package manager detection (npm/yarn/pnpm)
- [x] Dependency categorization (dependencies vs devDependencies)
- [x] Node.js version from engines

### Phase 8: Go Analyzer (T085-T096) ✅
- [x] `analyzers/go.py` — GoAnalyzer
- [x] go.mod parsing com regex
- [x] Module name extraction
- [x] Single-line + multi-line require directives
- [x] Go version extraction

### Phase 9: Factory Pattern (T097-T108) ✅
- [x] `analyzers/factory.py` — AnalyzerFactory + ProjectDetector
- [x] Confidence-based detection (DETECTION_WEIGHTS)
- [x] Threshold = 40 pontos
- [x] Scanner integration (T039)
- [x] Graceful unknown project handling

### Phase 10: CLI Interface (T109-T124a) ✅
- [x] `cli.py` — Typer-based CLI
- [x] Commands: scan, config, version
- [x] Options: --input, --output, --format, --template, --dry-run
- [x] Flags: --verbose, --debug, --quiet
- [x] Exit code logic (0/1/2)
- [x] Temporary file cleanup (atexit handler)
- [x] Rich help messages

### Phase 11: Configuration (T125-T132) ✅
- [x] ENV variable support (PROFILE_GEN_ prefix)
- [x] CLI argument override
- [x] Pydantic validation
- [x] Default values

### Phase 12: Test Fixtures (T133-T138) ✅
- [x] `tests/fixtures/python_project/` completo
- [x] `tests/fixtures/nodejs_project/` completo
- [x] `tests/fixtures/go_project/` completo
- [x] End-to-end validation (3/3 projects detected)

### Quality Gates ✅
- [x] ruff check --select ALL → All checks passed
- [x] mypy --strict → Success: 19 files
- [x] CLI functional test → profile-gen version 0.1.0
- [x] End-to-end test → 3 projects detected and exported

---

## 📊 Progress Tracking

**Overall**: 124/220 tasks (56%)

| Phase | Tasks | Status |
|-------|-------|--------|
| 1-12 (MVP) | 124/220 | ✅ Complete |
| 13 (Git) | 0/16 | 🔵 Pending |
| 14 (Stats) | 0/11 | 🔵 Pending |
| 15+ (Polish) | 0/69 | 🔵 Pending |

---

*Last session: 2026-05-07 | MVP implementation complete | Next: Git metadata + Code statistics*

- [x] Scaffold inicial gerado (2026-05-07T15:30:45Z)
- [x] Configurar repositório GitHub (2026-05-07T13:03:00Z)
- [x] Primeira sessão documentada (2026-05-07T12:55:00Z)
- [x] Push inicial para GitHub (2026-05-07T14:20:57Z)
- [x] Atualizar objetivo-init.yaml com specs detalhadas (2026-05-07T14:30:00Z)
