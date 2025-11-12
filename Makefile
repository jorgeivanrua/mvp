.PHONY: help test test-unit test-integration test-cov clean install run

help:
	@echo "Comandos disponibles:"
	@echo "  make install       - Instalar dependencias con uv"
	@echo "  make test          - Ejecutar todos los tests"
	@echo "  make test-unit     - Ejecutar solo tests unitarios"
	@echo "  make test-cov      - Ejecutar tests con cobertura"
	@echo "  make run           - Ejecutar aplicación"
	@echo "  make clean         - Limpiar archivos temporales"

install:
	uv venv
	uv pip install -r requirements.txt

test:
	.venv/Scripts/python.exe -m pytest

test-unit:
	.venv/Scripts/python.exe -m pytest -m unit

test-integration:
	.venv/Scripts/python.exe -m pytest -m integration

test-cov:
	.venv/Scripts/python.exe -m pytest --cov=backend --cov-report=html

run:
	.venv/Scripts/python.exe run.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
