# 📝 TODO — Profile Generator

**Last Updated**: 2026-05-07T14:30:00Z
**Status**: 🟢 Em andamento

---

## 🎯 Objetivo

Ferramenta CLI para escanear projetos, compilar metadados e gerar outputs estruturados (JSON + Markdown) para portfólio/currículo.

---

## 🟠 Em Progresso

*(nenhum)*

## 🔵 P0 - MVP (Crítico)

- [ ] Definir JSON schema para output (compatível com yves-profile-site)
- [ ] Criar estrutura de módulos em `src/profile_generator/` (SOLID + Modularização)
  - [ ] `cli/` - Comandos Click/Typer (SRP)
  - [ ] `scanner/` - Lógica de scan (responsabilidade única)
  - [ ] `analyzers/` - Análise por tipo (Factory Pattern)
    - [ ] `base.py` - Abstract Base Class para analyzers (≤150 LOC)
    - [ ] `factory.py` - Factory para criar analyzers (≤100 LOC)
    - [ ] `python.py` - Analyzer Python (≤200 LOC)
    - [ ] `nodejs.py` - Analyzer Node.js (≤200 LOC)
    - [ ] `go.py` - Analyzer Go (≤200 LOC)
  - [ ] `models/` - Pydantic models (um por arquivo)
  - [ ] `exporters/` - JSON e Markdown (Strategy Pattern)
    - [ ] `base.py` - Abstract base exporter
    - [ ] `json.py` - JSON exporter
    - [ ] `markdown.py` - Markdown exporter
  - [ ] `config/` - Gerenciamento de configuração
- [ ] Implementar CLI básico (Click ou Typer)
  - [ ] Comando `scan` com args --input, --output, --format
  - [ ] Error handling com exit codes apropriados
  - [ ] Levels: --quiet, --verbose, --debug
  - [ ] Aplicar SRP: CLI separado de lógica de negócio
- [ ] Implementar scanner de diretórios (pathlib)
  - [ ] Módulo coeso com responsabilidade única
  - [ ] Dependency Injection para configuração
- [ ] Implementar Factory Pattern para detecção de tipo de projeto
  - [ ] Python (pyproject.toml, setup.py, requirements.txt)
  - [ ] Node.js (package.json)
  - [ ] Go (go.mod)
  - [ ] Factory retorna analyzer apropriado
- [ ] Implementar extração de metadados básicos
  - [ ] Nome, descrição (README)
  - [ ] Linguagem principal
  - [ ] Tecnologias/frameworks
  - [ ] Usar Strategy Pattern para diferentes tipos
- [ ] Implementar exportador JSON (Pydantic + Strategy)
- [ ] Implementar exportador Markdown (Jinja2 + Strategy)
- [ ] Garantir Dependency Injection em toda aplicação
- [ ] Adicionar testes unitários (≥80% coverage)
  - [ ] `tests/unit/` estruturado
  - [ ] Fixtures em `tests/fixtures/`
  - [ ] pytest configurado
  - [ ] Testar cada módulo isoladamente

## 🔵 P1 - Alta Prioridade

- [ ] Configuração via .env e config.yaml (Pydantic Settings)
- [ ] Análise Git avançada
  - [ ] Commits, contribuidores
  - [ ] Atividade, último update
- [ ] Estatísticas de código
  - [ ] LOC por linguagem
  - [ ] Complexidade, cobertura
- [ ] Templates Jinja2 customizáveis
- [ ] Documentar API com Sphinx
- [ ] Documentar design patterns aplicados
  - [ ] Factory Pattern (analyzers)
  - [ ] Strategy Pattern (exporters)
  - [ ] Builder Pattern (metadados)
  - [ ] Adapter Pattern (projeto → modelo comum)
- [ ] Criar ADR-001: Escolha de framework CLI (Click vs Typer)
- [ ] Criar ADR-002: Estratégia de detecção de projetos
- [ ] Criar ADR-003: Aplicação de SOLID e design patterns
- [ ] Criar ADR-004: Limites de tamanho de arquivo e modularização
- [ ] Configurar CI/CD (GitHub Actions)
  - [ ] Testes + coverage
  - [ ] Lint (ruff check)
  - [ ] Type check (mypy --strict)
  - [ ] Security scan (bandit + safety)
  - [ ] Quality gates: max LOC por arquivo, complexidade ciclomática
- [ ] Configurar ruff para detectar arquivos muito longos (>300 LOC)
- [ ] Code review checklist baseado em SOLID

## 🔵 P2 - Desejável

- [ ] Watch mode (watchdog)
- [ ] Filtros e exclusões (regex)
- [ ] Cache inteligente
- [ ] Dry-run mode (--dry-run)

## ✅ Concluído

- [x] Scaffold inicial gerado (2026-05-07T15:30:45Z)
- [x] Configurar repositório GitHub (2026-05-07T13:03:00Z)
- [x] Primeira sessão documentada (2026-05-07T12:55:00Z)
- [x] Push inicial para GitHub (2026-05-07T14:20:57Z)
- [x] Atualizar objetivo-init.yaml com specs detalhadas (2026-05-07T14:30:00Z)
