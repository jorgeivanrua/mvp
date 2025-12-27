@echo off
REM Script de inicio completo para el Sistema Electoral MVP
REM Autor: Sistema de Desarrollo  
REM Fecha: Diciembre 24, 2025

echo.
echo ================================================
echo 🚀 Iniciando Sistema Electoral MVP...
echo ================================================
echo.

REM Verificar Python
echo 📋 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)
echo ✅ Python encontrado

REM Crear entorno virtual si no existe
echo.
echo 🔧 Configurando entorno virtual...
if not exist ".venv" (
    echo 📦 Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Error creando entorno virtual
        pause
        exit /b 1
    )
)

REM Activar entorno virtual
echo 🔌 Activando entorno virtual...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ⚠️  Usando Python del sistema
) else (
    echo ✅ Entorno virtual activado
)

REM Instalar dependencias
echo.
echo 📚 Verificando dependencias...
if exist "requirements.txt" (
    echo 📦 Instalando/actualizando dependencias...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
    echo ✅ Dependencias instaladas
) else (
    echo ⚠️  Archivo requirements.txt no encontrado
)

REM Crear directorio instance si no existe
echo.
echo 🗄️  Verificando estructura de directorios...
if not exist "instance" (
    echo 📁 Creando directorio instance...
    mkdir instance
)

REM Configurar variables de entorno
echo ⚙️  Configurando variables de entorno...
set FLASK_ENV=development
set FLASK_DEBUG=1
set PYTHONPATH=.

REM Inicializar sistema si es necesario
echo.
echo 🔧 Inicializando sistema...
if exist "scripts\init_system.py" (
    echo 📊 Ejecutando inicialización del sistema...
    python scripts\init_system.py
    echo ✅ Sistema inicializado
) else (
    echo ⚠️  Script de inicialización no encontrado
)

REM Mostrar información
echo.
echo ================================================
echo 🎯 SISTEMA LISTO PARA INICIAR
echo ================================================
echo 📍 Puerto: 5000
echo 🌐 URL: http://localhost:5000  
echo 🔧 Modo: Desarrollo
echo 📊 Base de datos: SQLite (instance/app.db)
echo ================================================
echo.

REM Preguntar si iniciar
set /p "response=¿Iniciar el servidor ahora? (S/n): "
if /i "%response%"=="" goto start
if /i "%response%"=="s" goto start
if /i "%response%"=="y" goto start
if /i "%response%"=="si" goto start
goto end

:start
echo.
echo 🚀 Iniciando servidor...
echo 💡 Presiona Ctrl+C para detener el servidor
echo ================================================
python run.py
goto finish

:end
echo ✅ Sistema configurado. Ejecuta 'python run.py' para iniciar el servidor.

:finish
echo.
echo ================================================
echo 🏁 Script completado
echo ================================================
pause