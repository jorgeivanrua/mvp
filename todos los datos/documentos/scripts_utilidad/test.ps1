# Script de PowerShell para ejecutar tests
param(
    [string]$Command = "all"
)

$venvPython = ".venv\Scripts\python.exe"

switch ($Command) {
    "all" {
        Write-Host "Ejecutando todos los tests..." -ForegroundColor Green
        & $venvPython -m pytest
    }
    "unit" {
        Write-Host "Ejecutando tests unitarios..." -ForegroundColor Green
        & $venvPython -m pytest -m unit
    }
    "integration" {
        Write-Host "Ejecutando tests de integración..." -ForegroundColor Green
        & $venvPython -m pytest -m integration
    }
    "cov" {
        Write-Host "Ejecutando tests con cobertura..." -ForegroundColor Green
        & $venvPython -m pytest --cov=backend --cov-report=html --cov-report=term
        Write-Host "`nReporte de cobertura generado en htmlcov/index.html" -ForegroundColor Cyan
    }
    "watch" {
        Write-Host "Ejecutando tests en modo watch..." -ForegroundColor Green
        & $venvPython -m pytest-watch
    }
    default {
        Write-Host "Uso: .\test.ps1 [all|unit|integration|cov|watch]" -ForegroundColor Yellow
        Write-Host "  all         - Ejecutar todos los tests (default)"
        Write-Host "  unit        - Ejecutar solo tests unitarios"
        Write-Host "  integration - Ejecutar solo tests de integración"
        Write-Host "  cov         - Ejecutar tests con reporte de cobertura"
        Write-Host "  watch       - Ejecutar tests en modo watch"
    }
}
