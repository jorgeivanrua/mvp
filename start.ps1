# Script de inicio completo para el Sistema Electoral MVP
# Autor: Sistema de Desarrollo
# Fecha: Diciembre 24, 2025

Write-Host "🚀 Iniciando Sistema Electoral MVP..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan

# Función para verificar si un comando existe
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Verificar Python
Write-Host "📋 Verificando requisitos del sistema..." -ForegroundColor Yellow
if (-not (Test-Command "python")) {
    Write-Host "❌ Python no encontrado. Instala Python 3.8+ desde https://python.org" -ForegroundColor Red
    exit 1
}

$pythonVersion = python --version 2>&1
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Verificar/crear entorno virtual
Write-Host "🔧 Configurando entorno virtual..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creando entorno virtual..." -ForegroundColor Blue
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error creando entorno virtual" -ForegroundColor Red
        exit 1
    }
}

# Activar entorno virtual
Write-Host "🔌 Activando entorno virtual..." -ForegroundColor Blue
try {
    & .\.venv\Scripts\Activate.ps1
    Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Usando Python del sistema (entorno virtual no disponible)" -ForegroundColor Yellow
    $env:PYTHON_PATH = "python"
}

# Verificar/instalar dependencias
Write-Host "📚 Verificando dependencias..." -ForegroundColor Yellow
$requirementsFile = "requirements.txt"
if (Test-Path $requirementsFile) {
    # Verificar si las dependencias están instaladas
    $pipList = & python -m pip list 2>$null
    if ($pipList -notmatch "Flask") {
        Write-Host "📦 Instalando dependencias..." -ForegroundColor Blue
        python -m pip install -r $requirementsFile
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Error instalando dependencias" -ForegroundColor Red
            exit 1
        }
        Write-Host "✅ Dependencias instaladas" -ForegroundColor Green
    } else {
        Write-Host "✅ Dependencias ya instaladas" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  Archivo requirements.txt no encontrado" -ForegroundColor Yellow
}

# Verificar base de datos
Write-Host "🗄️  Verificando base de datos..." -ForegroundColor Yellow
if (-not (Test-Path "instance")) {
    Write-Host "📁 Creando directorio instance..." -ForegroundColor Blue
    New-Item -ItemType Directory -Path "instance" -Force | Out-Null
}

# Configurar variables de entorno
Write-Host "⚙️  Configurando variables de entorno..." -ForegroundColor Yellow
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
$env:PYTHONPATH = "."

# Verificar archivos de configuración
Write-Host "📋 Verificando configuración..." -ForegroundColor Yellow
$configFiles = @("backend/config.py", "backend/app.py", "run.py")
foreach ($file in $configFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file no encontrado" -ForegroundColor Red
    }
}

# Inicializar base de datos si es necesario
Write-Host "🔧 Inicializando sistema..." -ForegroundColor Yellow
if (Test-Path "scripts/init_system.py") {
    Write-Host "📊 Ejecutando inicialización del sistema..." -ForegroundColor Blue
    python scripts/init_system.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Sistema inicializado correctamente" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Advertencias durante la inicialización (continuando...)" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Script de inicialización no encontrado" -ForegroundColor Yellow
}

# Mostrar información del sistema
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🎯 SISTEMA LISTO PARA INICIAR" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "📍 Puerto: 5000" -ForegroundColor White
Write-Host "🌐 URL: http://localhost:5000" -ForegroundColor White
Write-Host "🔧 Modo: Desarrollo" -ForegroundColor White
Write-Host "📊 Base de datos: SQLite (instance/app.db)" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Cyan

# Preguntar si iniciar el servidor
$response = Read-Host "¿Iniciar el servidor ahora? (S/n)"
if ($response -eq "" -or $response -eq "S" -or $response -eq "s" -or $response -eq "Y" -or $response -eq "y") {
    Write-Host "🚀 Iniciando servidor..." -ForegroundColor Green
    Write-Host "💡 Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
    Write-Host "================================================" -ForegroundColor Cyan
    
    # Iniciar la aplicación
    python run.py
} else {
    Write-Host "✅ Sistema configurado. Ejecuta 'python run.py' para iniciar el servidor." -ForegroundColor Green
}

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🏁 Script completado" -ForegroundColor Green