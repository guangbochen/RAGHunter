# Makefile for RAGHunter

# Python interpreter
PYTHON = python3

# Project name
PROJECT_NAME = raghunter

# Default target
.PHONY: all
all: run

# Create/update virtual environment with uv
.PHONY: venv
venv:
	uv venv

# Run the application
.PHONY: run
run:
	uv run raghunter $(ARGS)


# Run the application
.PHONY: convert
convert:
	uv run raghunter convert $(ARGS)

# Install dependencies with uv
.PHONY: install
install:
	uv pip install -e .

# Run linting with ruff
.PHONY: lint
lint:
	ruff check .

# Run formatting with ruff
.PHONY: format
format:
	ruff format .

# Clean up Python cache files
.PHONY: clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

# Help target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  run      - Run the application"
	@echo "  install  - Install dependencies using uv"
	@echo "  venv     - Create/update virtual environment with uv"
	@echo "  lint     - Run linting with ruff"
	@echo "  format   - Run formatting with ruff"
	@echo "  clean    - Clean up Python cache files"
	@echo "  help     - Show this help message"