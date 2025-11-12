@echo off
echo ============================================================
echo SISTEMA ELECTORAL - INICIANDO
echo ============================================================
echo.

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Verificar que Python está disponible
python --version
if errorlevel 1 (
    echo ERROR: Python no encontrado
    pause
    exit /b 1
)

echo.
echo Iniciando aplicacion...
echo.

REM Iniciar la aplicación
python start_app.py

pause
