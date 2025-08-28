.PHONY: help install dev-install test lint format clean build publish docs

# Default target
help:
	@echo "Available commands:"
	@echo "  install     Install the package"
	@echo "  dev-install Install for development"
	@echo "  test        Run tests"
	@echo "  lint        Run linting"
	@echo "  format      Format code"
	@echo "  clean       Clean build artifacts"
	@echo "  build       Build the package"
	@echo "  publish     Publish to PyPI"
	@echo "  docs        Build documentation"

install:
	poetry install --only=main

dev-install:
	poetry install --with=dev,docs
	poetry run pre-commit install

test:
	poetry run pytest

lint:
	poetry run flake8 televoltaic tests
	poetry run mypy televoltaic

format:
	poetry run black televoltaic tests
	poetry run isort televoltaic tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:
	poetry build

publish:
	poetry publish

docs:
	cd docs && poetry run make html
