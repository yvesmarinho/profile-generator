# Checklist: Qualidade de Requisitos — CLI Project Scanner

**Feature**: 001-cli-project-scanner
**Propósito**: Validar completude, clareza e consistência dos requisitos especificados (validação de requisitos, NÃO validação de implementação)
**Criado**: 2026-05-07
**Foco**: Qualidade de Requisitos
**Profundidade**: Padrão
**Audiência**: Revisor (PR review)

---

## Conceito: "Testes Unitários para Requisitos"

Este checklist **NÃO** valida se o código funciona. Ele valida se os **requisitos estão bem escritos**.

❌ **Errado**: "Verificar se a página inicial exibe 3 cards"
✅ **Correto**: "O número e layout de cards estão especificados com critérios mensuráveis?"

---

## Completude de Requisitos

Verifica se todos os requisitos necessários estão documentados.

- [ ] CHK001 - Os requisitos de detecção de tipo de projeto (Python, Node.js, Go) estão completos para todos os tipos suportados? [Completude, Spec §FR-002]
- [ ] CHK002 - Os requisitos de extração de metadados especificam todos os campos obrigatórios (name, description, technologies, statistics)? [Completude, Spec §FR-003]
- [ ] CHK003 - Os requisitos de exportação JSON definem a estrutura completa do schema (projects, generated_at, tool_version)? [Completude, Spec §FR-005]
- [ ] CHK004 - Os requisitos de análise Git especificam todos os campos necessários (commit count, top 5 contributors, branch, tags)? [Completude, Spec §FR-010, Clarification 3]
- [ ] CHK005 - Os requisitos de contagem de arquivos especificam quais tipos de arquivo são incluídos/excluídos (whitelist vs blacklist)? [Completude, Spec §FR-019, Clarification 4]
- [ ] CHK006 - Os comandos CLI obrigatórios (scan, config, version) estão todos especificados com seus parâmetros? [Completude, Spec §FR-021]
- [ ] CHK007 - As flags CLI (--dry-run, --verbose, --debug, --quiet, --help) têm comportamento definido? [Completude, Spec §FR-022]
- [ ] CHK008 - Os códigos de saída do CLI (0, 1, 2) estão mapeados para cenários específicos? [Completude, Spec §FR-023]
- [ ] CHK009 - Os requisitos de configuração especificam todas as fontes (CLI, ENV, config.yaml, defaults) e ordem de precedência? [Completude, Spec §FR-007, FR-008]
- [ ] CHK010 - Os requisitos definem comportamento para templates Jinja2 customizados e template padrão? [Completude, Spec §FR-012]

---

## Clareza e Especificidade

Verifica se requisitos vagos foram quantificados com critérios específicos.

- [ ] CHK011 - O termo "múltiplos diretórios" em FR-001 está quantificado com limite ou estratégia de processamento? [Clareza, Spec §FR-001]
- [ ] CHK012 - A expressão "scan all subdirectories" em User Story 1 especifica profundidade máxima ou tratamento de symlinks? [Clareza, Spec User Story 1]
- [ ] CHK013 - O termo "graceful degradation" em FR-013 está definido com comportamento específico (log + continue, fail fast, etc.)? [Clareza, Spec §FR-013]
- [ ] CHK014 - A métrica "< 5s para 100 projetos" está definida com hardware de referência e condições de teste? [Clareza, Spec §SC-001, Performance Criteria]
- [ ] CHK015 - O limite "< 500MB RAM" especifica se é pico, média ou uso sustentado? [Clareza, Spec Performance Criteria]
- [ ] CHK016 - A precisão "≥95% accuracy" na detecção de projetos está definida com metodologia de cálculo? [Clareza, Spec §SC-007]
- [ ] CHK017 - O termo "structured JSON logging" especifica formato de log (campos obrigatórios, nível de detalhe)? [Clareza, Spec §FR-014]
- [ ] CHK018 - Os requisitos de "atomicidade" na escrita de arquivos (FR-005) especificam estratégia (temp file + rename)? [Clareza, Spec §FR-005, User Story 2]
- [ ] CHK019 - O critério "100% compatible" com yves-profile-site está definido com método de validação? [Clareza, Spec §FR-006, SC-002]
- [ ] CHK020 - O limite de 100.000 arquivos especifica se aplica a total ou apenas source files? [Clareza, Spec §FR-019, Clarification 4]

---

## Consistência e Alinhamento

Verifica se requisitos em diferentes seções estão alinhados sem conflitos.

- [ ] CHK021 - A estratégia de configuração "replace" (Clarification 2) está consistente com FR-008 e todos os User Stories? [Consistência, Spec §FR-008, Clarification 2]
- [ ] CHK022 - Os requisitos de análise Git (all-time + top 5) em FR-010 estão alinhados com Clarification 3? [Consistência, Spec §FR-010, Clarification 3]
- [ ] CHK023 - O limite de arquivos (whitelist approach) está consistente entre FR-019, Clarification 4 e Edge Cases? [Consistência, Spec §FR-019, Clarification 4, Edge Cases]
- [ ] CHK024 - Os níveis de log (debug/info/warning/error) em FR-014 estão alinhados com flags CLI (--verbose, --debug, --quiet) em FR-022? [Consistência, Spec §FR-014, FR-022]
- [ ] CHK025 - As prioridades P1/P2/P3 nos User Stories estão alinhadas com os Success Criteria obrigatórios? [Consistência, Spec User Stories, Success Criteria]
- [ ] CHK026 - Os padrões SOLID exigidos (FR-015, FR-016, FR-017) estão refletidos em todos os Success Criteria arquiteturais? [Consistência, Spec §FR-015-017, SC-005]
- [ ] CHK027 - O limite de LOC (≤300) em SC-015 está alinhado com limites específicos em Technical Context (base.py ≤150, factory.py ≤100)? [Consistência, Spec §SC-015, Plan Technical Context]
- [ ] CHK028 - Os requisitos de exportação (JSON + Markdown) estão consistentes entre FR-004, FR-005 e User Stories 2-3? [Consistência, Spec §FR-004-005, User Stories 2-3]

---

## Mensurabilidade e Aceitação

Verifica se requisitos podem ser objetivamente verificados.

- [ ] CHK029 - Os Success Criteria (SC-001 a SC-015) são mensuráveis com métricas objetivas ou podem ser subjetivos? [Mensurabilidade, Spec Success Criteria]
- [ ] CHK030 - As Performance Criteria definem como medir "< 5s" (wall time, CPU time, user time)? [Mensurabilidade, Spec Performance Criteria]
- [ ] CHK031 - O critério "human-readable" para Markdown em SC-011 pode ser testado objetivamente? [Mensurabilidade, Spec §SC-011]
- [ ] CHK032 - O requisito "actionable error messages" em SC-012 tem critérios de aceitação mensuráveis? [Mensurabilidade, Spec §SC-012]
- [ ] CHK033 - A "intuitive CLI interface" em SC-013 pode ser validada objetivamente ou é subjetiva? [Mensurabilidade, Spec §SC-013]
- [ ] CHK034 - Todos os cenários Given/When/Then nos User Stories têm resultados verificáveis? [Mensurabilidade, Spec User Stories]
- [ ] CHK035 - Os requisitos de segurança (FR-018, SC-008) especificam ferramentas e thresholds de validação? [Mensurabilidade, Spec §FR-018, SC-008]

---

## Cobertura de Cenários

Verifica se todos os fluxos principais, alternativos, exceções e recuperação estão cobertos.

### Cenários Primários

- [ ] CHK036 - Os requisitos cobrem o fluxo completo de scan → análise → exportação para todos os tipos de projeto? [Cobertura, Spec User Stories 1-6]
- [ ] CHK037 - Os requisitos de detecção automática de tipo (FR-002) cobrem projetos multi-linguagem ou mistos? [Cobertura, Spec §FR-002, Edge Cases]
- [ ] CHK038 - Os requisitos de extração de README cobrem variações de nome (README.md, readme.md, README.txt, README.rst)? [Cobertura, Gap]

### Cenários Alternativos

- [ ] CHK039 - Os requisitos definem comportamento quando projeto não tem README.md? [Cobertura, Spec Edge Cases]
- [ ] CHK040 - Os requisitos especificam comportamento quando projeto não tem tipo identificável (unknown type)? [Cobertura, Spec §FR-002, Edge Cases]
- [ ] CHK041 - Os requisitos cobrem cenário de múltiplos arquivos de configuração conflitantes (pyproject.toml + setup.py)? [Cobertura, Spec User Story 4]

### Cenários de Exceção/Erro

- [ ] CHK042 - Os requisitos definem tratamento de erro para arquivo de configuração YAML malformado? [Cobertura, Spec Edge Cases]
- [ ] CHK043 - Os requisitos especificam comportamento quando diretório de saída não tem permissão de escrita? [Cobertura, Spec Edge Cases]
- [ ] CHK044 - Os requisitos cobrem tratamento de symlinks circulares durante scan? [Cobertura, Spec Edge Cases]
- [ ] CHK045 - Os requisitos definem comportamento quando projeto é deletado durante scan? [Cobertura, Spec Edge Cases]
- [ ] CHK046 - Os requisitos especificam tratamento de repositório Git corrompido ou em detached HEAD? [Cobertura, Spec Edge Cases]
- [ ] CHK047 - Os requisitos cobrem cenário de arquivos com encoding não-UTF-8? [Cobertura, Spec Edge Cases]
- [ ] CHK048 - Os requisitos definem comportamento quando projeto excede limite de 100k arquivos? [Cobertura, Spec §FR-019, Edge Cases, Clarification 1]

### Cenários de Recuperação

- [ ] CHK049 - Os requisitos especificam estratégia de rollback quando exportação JSON falha parcialmente? [Gap, Recuperação]
- [ ] CHK050 - Os requisitos definem limpeza de arquivos temporários quando processo é interrompido (Ctrl+C)? [Cobertura, Spec §FR-024]
- [ ] CHK051 - Os requisitos especificam comportamento quando validação Pydantic falha (continuar, skip, abortar)? [Cobertura, Spec §FR-005, User Story 2]

---

## Requisitos Não-Funcionais

Verifica se requisitos de performance, segurança, acessibilidade, etc. estão especificados.

### Performance

- [ ] CHK052 - Os requisitos de performance especificam degradação aceitável com diferentes tamanhos de projeto (10 vs 100 vs 1000 projetos)? [Gap, Performance]
- [ ] CHK053 - Os requisitos definem se processamento sequencial vs paralelo é permitido (atualmente single-threaded)? [Clareza, Spec Performance Criteria]
- [ ] CHK054 - Os requisitos especificam timeout máximo para operações Git (commit count, contributors)? [Gap, Performance]

### Segurança

- [ ] CHK055 - Os requisitos de validação de path (FR-018) especificam como prevenir path traversal (.., symlinks absolutos)? [Clareza, Spec §FR-018]
- [ ] CHK056 - Os requisitos especificam se execução de código arbitrário é permitida (eval, exec, subprocess)? [Gap, Segurança]
- [ ] CHK057 - Os requisitos definem tratamento de arquivos binários executáveis durante scan? [Gap, Segurança]

### Acessibilidade

- [ ] CHK058 - Os requisitos de mensagens de erro (FR-020) especificam suporte a i18n/l10n? [Gap, Acessibilidade]
- [ ] CHK059 - Os requisitos de help messages (--help) especificam formato e completude esperados? [Clareza, Spec §SC-013]

### Manutenibilidade

- [ ] CHK060 - Os requisitos especificam versionamento do schema JSON para compatibilidade futura? [Gap, Spec Dependencies & Risks]
- [ ] CHK061 - Os requisitos definem política de deprecação para mudanças quebradas no schema? [Gap, Spec Dependencies & Risks]

---

## Dependências e Premissas

Verifica se dependências externas e premissas estão documentadas.

- [ ] CHK062 - As dependências críticas (Pydantic, Typer, Jinja2, structlog) têm versões mínimas especificadas? [Clareza, Spec Dependencies, Plan Technical Context]
- [ ] CHK063 - A dependência do schema yves-profile-site está documentada com estratégia de mitigação para mudanças? [Completude, Spec Dependencies & Risks]
- [ ] CHK064 - A premissa "Python 3.12+ available" está validada com requisito funcional (version check)? [Gap, Spec Assumptions]
- [ ] CHK065 - A premissa "Git available on system" tem requisito de graceful degradation se Git não está instalado? [Cobertura, Spec Assumptions, User Story 8]
- [ ] CHK066 - As premissas sobre permissões de leitura em diretórios de projeto têm tratamento de erro especificado? [Cobertura, Spec Assumptions, Edge Cases]

---

## Rastreabilidade

Verifica se requisitos podem ser rastreados de objetivos de negócio até implementação.

- [ ] CHK067 - Todos os Functional Requirements (FR-001 a FR-024) estão mapeados para User Stories correspondentes? [Rastreabilidade]
- [ ] CHK068 - Todos os Success Criteria (SC-001 a SC-015) estão vinculados a Functional Requirements específicos? [Rastreabilidade]
- [ ] CHK069 - Os Edge Cases identificados estão cobertos por requisitos funcionais ou cenários de teste? [Rastreabilidade, Spec Edge Cases]
- [ ] CHK070 - As métricas de sucesso em Business Context estão refletidas nos Success Criteria técnicos? [Rastreabilidade, Spec Business Context, Success Criteria]
- [ ] CHK071 - Os riscos identificados (Dependencies & Risks) têm requisitos de mitigação correspondentes? [Rastreabilidade, Spec Dependencies & Risks]

---

## Ambiguidades e Conflitos

Identifica termos ambíguos e requisitos conflitantes que precisam de clarificação.

- [ ] CHK072 - O termo "standard project structures" em Assumptions está definido com exemplos concretos? [Ambiguidade, Spec Assumptions]
- [ ] CHK073 - O termo "comprehensive --help" em SC-013 está quantificado (quais informações são obrigatórias)? [Ambiguidade, Spec §SC-013]
- [ ] CHK074 - O termo "gracefully" em Edge Cases está definido uniformemente em todos os contextos? [Ambiguidade, Spec Edge Cases]
- [ ] CHK075 - Existe conflito entre "single-threaded" em Performance Criteria e requisito de "< 5s para 100 projetos"? [Conflito, Spec Performance Criteria]
- [ ] CHK076 - O termo "zero manual intervention" em Success Metrics está alinhado com requisito de configuração manual (config.yaml)? [Conflito, Spec Business Context]
- [ ] CHK077 - A exclusão de "node_modules/" em FR-019 está alinhada com requisito de análise de Node.js em User Story 5? [Conflito, Spec §FR-019, User Story 5]

---

## Validação de Design

Verifica se decisões de design refletidas nos requisitos estão corretas.

- [ ] CHK078 - Os requisitos de Factory Pattern (FR-015) especificam interfaces abstratas necessárias (BaseAnalyzer)? [Completude, Spec §FR-015, Plan]
- [ ] CHK079 - Os requisitos de Strategy Pattern (FR-016) especificam todos os exporters obrigatórios (JSON, Markdown)? [Completude, Spec §FR-016]
- [ ] CHK080 - Os requisitos de Dependency Injection (FR-017) especificam onde DI é obrigatório vs opcional? [Clareza, Spec §FR-017]
- [ ] CHK081 - Os limites de LOC (base.py ≤150, factory.py ≤100, analyzers ≤200) estão documentados como requisitos ou apenas guidelines? [Clareza, Plan Project Structure, SC-015]
- [ ] CHK082 - O requisito de "mypy --strict" em SC-004 especifica exceções permitidas (Any, cast, ignore)? [Clareza, Spec §SC-004]

---

## Qualidade da Especificação

Verifica meta-requisitos sobre a própria especificação.

- [ ] CHK083 - A seção "Clarifications" documenta todas as perguntas resolvidas com contexto suficiente? [Qualidade, Spec Clarifications]
- [ ] CHK084 - Todos os User Stories seguem formato Given/When/Then consistentemente? [Qualidade, Spec User Scenarios]
- [ ] CHK085 - Os Edge Cases identificados são realistas e baseados em experiência/análise de risco? [Qualidade, Spec Edge Cases]
- [ ] CHK086 - A seção "Out of Scope" está completa para evitar scope creep durante implementação? [Completude, Spec Out of Scope]
- [ ] CHK087 - Os Next Steps estão priorizados e têm dependências claras? [Qualidade, Spec Next Steps]
- [ ] CHK088 - O Quality Checklist da especificação está 100% validado (todos itens ✅)? [Rastreabilidade, Spec Quality Checklist]

---

## Integração com yves-profile-site

Verifica requisitos de integração com sistema consumidor.

- [ ] CHK089 - O contrato de schema JSON (contracts/json-schema.json) está validado contra requisitos de yves-profile-site? [Rastreabilidade, Spec §FR-006, Contracts]
- [ ] CHK090 - Os campos obrigatórios no JSON (generated_at, tool_version, projects) estão documentados como requisitos? [Completude, Data Model]
- [ ] CHK091 - Os requisitos especificam versionamento do schema para backward compatibility? [Gap, Spec Dependencies & Risks]
- [ ] CHK092 - Os requisitos definem testes de contrato para validar compatibilidade com consumidor? [Gap, Spec §SC-002]

---

## Prontidão para Implementação

Verifica se especificação está completa para começar implementação.

- [ ] CHK093 - Todos os artefatos de design obrigatórios estão criados (plan.md, research.md, data-model.md, contracts/, quickstart.md)? [Prontidão, Spec Next Steps]
- [ ] CHK094 - As decisões arquiteturais críticas (ADR-001 CLI framework) estão resolvidas? [Prontidão, Plan Constitution Check, Research]
- [ ] CHK095 - Os modelos de dados (Configuration, Technology, Repository, Statistics, Project) têm validação Pydantic especificada? [Prontidão, Data Model]
- [ ] CHK096 - O fluxo TDD (RED→GREEN→REFACTOR) está documentado para cada módulo? [Prontidão, Quickstart]
- [ ] CHK097 - As fixtures de teste (python_project, nodejs_project, go_project) estão especificadas? [Prontidão, Plan Project Structure]
- [ ] CHK098 - Os Quality Gates (ruff, mypy, pytest, bandit, safety, LOC, SOLID) têm comandos de verificação documentados? [Prontidão, Quickstart]

---

## Resumo

**Total de Itens**: 98
**Foco**: Qualidade de Requisitos (completude, clareza, consistência, mensurabilidade)
**Rastreabilidade**: ≥80% dos itens referenciam spec.md, plan.md, data-model.md ou contratos
**Cobertura de Cenários**: Primários, Alternativos, Exceções, Recuperação, NFRs

**Nota Importante**: Este checklist valida a **qualidade dos requisitos escritos**, NÃO a implementação do código. Use durante revisão de especificação, antes de começar implementação, ou durante revisão de PR da especificação.

---

**Status**: ✅ Checklist criado — pronto para revisão de qualidade de requisitos
