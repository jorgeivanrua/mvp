@echo off
echo ========================================
echo   Sistema Electoral - Inicio Local
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist .venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call .venv\Scripts\activate.bat
) else (
    echo Advertencia: No se encontro entorno virtual
)

REM Configurar variables de entorno para desarrollo
set FLASK_ENV=development
set DEBUG=True

echo.
echo Iniciando aplicacion en modo desarrollo...
echo URL: http://localhost:5000
echo.

REM Iniciar aplicación
python run.py

pause
