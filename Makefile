# Makefile — Profile Generator
# Gerado por scaffold.py em 2026-05-07T15:30:45Z

.PHONY: help init dev build test lint format clean

## Mostra esta ajuda
help:
	@grep -E '^## ' Makefile | sed 's/## //'

## [DEPRECATED] — use: uv run scripts/scaffold.py
init:
	@echo ""
	@echo " ⚠️  Para criar/configurar o projeto, use diretamente:"
	@echo "      uv run scripts/scaffold.py"
	@echo "      python scripts/scaffold.py"
	@echo ""

## Instala dependências
install-deps:
	@echo "📦 Instalando dependências com uv..."
	uv venv
	uv pip install -e ".[dev]"

## Inicia servidor de desenvolvimento (instala em modo editable)
dev:
	@echo "🔧 Instalando em modo desenvolvimento..."
	uv pip install -e .

## Build de produção
build:
	@echo "🏗️  Buildando pacote..."
	uv pip install build
	python -m build

## Executa testes com coverage
test:
	@echo "🧪 Executando testes com coverage..."
	pytest

## Lint do código (ruff check + mypy + bandit + safety)
lint:
	@echo "🔍 Executando linters..."
	ruff check src/ tests/
	mypy src/ --strict
	bandit -r src/
	safety check

## Formata código com ruff
format:
	@echo "✨ Formatando código..."
	ruff format src/ tests/
	ruff check --fix src/ tests/

## Remove arquivos gerados
clean:
	@echo "🧹 Limpando arquivos gerados..."
	@rm -rf dist/ build/ __pycache__/ .pytest_cache/ *.egg-info/ .coverage htmlcov/ .mypy_cache/ .ruff_cache/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
## Carrega variáveis MCP do .secrets/.env e orienta a abrir o VS Code
mcp:
	@bash scripts/load-mcp.sh