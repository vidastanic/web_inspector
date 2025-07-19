.PHONY: help install install-dev test test-cov lint type-check format clean run-example run-test

help: ## Show this help message
	@echo "WebChecker - Development Commands"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	poetry install --only main

install-dev: ## Install all dependencies including development tools
	poetry install --with test

test: ## Run tests
	poetry run pytest

test-cov: ## Run tests with coverage
	poetry run pytest --cov=webchecker --cov-report=html --cov-report=term

lint: ## Run linting
	poetry run flake8 webchecker/ tests/

type-check: ## Run type checking
	poetry run mypy webchecker/

format: ## Format code with black and isort
	poetry run black webchecker/ tests/
	poetry run isort webchecker/ tests/

clean: ## Clean up generated files
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	rm -rf webchecker/__pycache__/
	rm -rf tests/__pycache__/
	find . -name "*.pyc" -delete

run-example: ## Run the trademark finding example
	poetry run python examples/find_trademarks.py

run-test: ## Run the installation test
	poetry run python test_installation.py

web: ## Start the web interface
	poetry run python run_web_server.py

web-dev: ## Start the web interface in development mode
	poetry run python -m webchecker.web_app

demo: ## Start web interface demo with browser auto-open
	poetry run python demo_web_interface.py

test-web: ## Test the web interface functionality
	poetry run python test_web_interface.py

test-extraction: ## Test the improved text extraction
	poetry run python test_text_extraction.py

test-url: ## Test URL normalization
	poetry run python test_url_normalization.py

check: ## Run all quality checks (lint, type-check, test)
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) test

build: ## Build the package
	poetry build

publish: ## Publish to PyPI (use with caution)
	poetry publish

shell: ## Activate poetry shell
	poetry shell

update: ## Update dependencies
	poetry update

lock: ## Lock dependencies
	poetry lock

# Development shortcuts
dev: install-dev ## Setup development environment
	@echo "Development environment ready!"
	@echo "Run 'make shell' to activate the virtual environment"

quick-test: ## Quick test run
	poetry run pytest tests/ -v --tb=short

# Documentation
docs: ## Generate documentation (placeholder)
	@echo "Documentation generation not yet implemented"
	@echo "See README.md and DEVELOPMENT.md for documentation"

# Docker (if needed in the future)
docker-build: ## Build Docker image
	docker build -t webchecker .

docker-run: ## Run WebChecker in Docker
	docker run -it webchecker python -m webchecker.main --help 