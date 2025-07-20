.PHONY: help install install-dev test test-cov lint format clean build dist docs

help: ## Show this help message
	@echo "Transmission Pusher - Development Commands"
	@echo "=========================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install the package in development mode
	pip install -e .

install-dev: ## Install the package with development dependencies
	pip install -e ".[dev]"

test: ## Run tests
	python scripts/run_tests.py

test-cov: ## Run tests with coverage
	pytest --cov=src/transmission_pusher --cov-report=html --cov-report=term-missing

lint: lint-black lint-flake8 lint-isort lint-mypy ## Run all linting checks

format: ## Format code with black and isort
	black src/ tests/ scripts/ examples/ transmission_client.py diagnose_connection.py
	isort src/ tests/ scripts/ examples/ transmission_client.py diagnose_connection.py

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build the package
	python -m build

dist: clean build ## Create distribution packages

docs: ## Build documentation
	cd docs && make html

check: lint-black lint-flake8 lint-isort lint-mypy test ## Run all checks (lint + test)

pre-commit: venv deps lint-black lint-flake8 lint-isort lint-mypy test ## Run pre-commit checks

.PHONY: venv deps coverage lint-black lint-flake8 lint-isort lint-mypy verify

venv: ## Create virtual environment if it doesn't exist
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv .venv; \
		echo "Virtual environment created successfully!"; \
	else \
		echo "Virtual environment already exists."; \
	fi

deps: venv ## Install/update all dependencies in the venv
	@echo "Installing/updating dependencies..."
	pip install --upgrade pip
	@if [ -f "dev-requirements.txt" ]; then \
		echo "Installing from dev-requirements.txt..."; \
		pip install -r dev-requirements.txt; \
	else \
		echo "Installing from pyproject.toml..."; \
		pip install -e ".[dev]"; \
	fi

coverage: ## Run tests with coverage and generate HTML report
	pytest --cov=src/transmission_pusher --cov-report=html --cov-report=term-missing

lint-black: ## Check code style with black
	black --check src/ examples/ scripts/ transmission_client.py diagnose_connection.py

lint-flake8: ## Check code style with flake8
	flake8 src/ examples/ scripts/ transmission_client.py diagnose_connection.py

lint-isort: ## Check import order with isort
	isort --check-only src/ examples/ scripts/ transmission_client.py diagnose_connection.py

lint-mypy: ## Check types with mypy
	mypy src/ transmission_client.py diagnose_connection.py

verify: venv deps lint-black lint-flake8 lint-isort lint-mypy test coverage
	@echo "🎉 All verification steps passed!"