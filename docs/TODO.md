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
- [ ] Criar estrutura de módulos em `src/profile_generator/`
  - [ ] `cli/` - Comandos Click/Typer
  - [ ] `scanner/` - Lógica de scan
  - [ ] `analyzers/` - Análise por tipo de projeto
  - [ ] `models/` - Pydantic models
  - [ ] `exporters/` - JSON e Markdown
  - [ ] `config/` - Gerenciamento de configuração
- [ ] Implementar CLI básico (Click ou Typer)
  - [ ] Comando `scan` com args --input, --output, --format
  - [ ] Error handling com exit codes apropriados
  - [ ] Levels: --quiet, --verbose, --debug
- [ ] Implementar scanner de diretórios (pathlib)
- [ ] Implementar detecção de tipo de projeto
  - [ ] Python (pyproject.toml, setup.py, requirements.txt)
  - [ ] Node.js (package.json)
  - [ ] Go (go.mod)
  - [ ] Outros conforme necessidade
- [ ] Implementar extração de metadados básicos
  - [ ] Nome, descrição (README)
  - [ ] Linguagem principal
  - [ ] Tecnologias/frameworks
- [ ] Implementar exportador JSON (Pydantic)
- [ ] Implementar exportador Markdown (Jinja2)
- [ ] Adicionar testes unitários (≥80% coverage)
  - [ ] `tests/unit/` estruturado
  - [ ] Fixtures em `tests/fixtures/`
  - [ ] pytest configurado

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
- [ ] Criar ADR-001: Escolha de framework CLI
- [ ] Criar ADR-002: Estratégia de detecção de projetos
- [ ] Configurar CI/CD (GitHub Actions)
  - [ ] Testes + coverage
  - [ ] Lint (ruff check)
  - [ ] Type check (mypy --strict)
  - [ ] Security scan (bandit + safety)

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
