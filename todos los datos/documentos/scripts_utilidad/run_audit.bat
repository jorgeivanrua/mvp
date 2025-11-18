@echo off
REM Script para ejecutar auditoría completa del sistema
REM Windows Batch Script

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  SISTEMA DE AUDITORÍA ELECTORAL                          ║
echo ║  Auditoría Completa Automatizada                         ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Verificar que colorama está instalado
python -c "import colorama" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Instalando dependencia colorama...
    pip install colorama
    if errorlevel 1 (
        echo ❌ Error al instalar colorama
        pause
        exit /b 1
    )
)

echo ✅ Dependencias verificadas
echo.

REM Menú de opciones
:menu
echo ═══════════════════════════════════════════════════════════
echo   MENÚ DE AUDITORÍA
echo ═══════════════════════════════════════════════════════════
echo.
echo   1. Cargar datos de prueba completos
echo   2. Ejecutar auditoría automatizada
echo   3. Cargar datos Y ejecutar auditoría (completo)
echo   4. Limpiar base de datos
echo   5. Salir
echo.
set /p option="Selecciona una opción (1-5): "

if "%option%"=="1" goto load_data
if "%option%"=="2" goto run_audit
if "%option%"=="3" goto full_audit
if "%option%"=="4" goto clean_db
if "%option%"=="5" goto end
echo ❌ Opción inválida
goto menu

:load_data
echo.
echo ═══════════════════════════════════════════════════════════
echo   CARGANDO DATOS DE PRUEBA
echo ═══════════════════════════════════════════════════════════
echo.
python backend/scripts/load_complete_test_data.py
if errorlevel 1 (
    echo.
    echo ❌ Error al cargar datos de prueba
    pause
    goto menu
)
echo.
echo ✅ Datos cargados exitosamente
echo.
pause
goto menu

:run_audit
echo.
echo ═══════════════════════════════════════════════════════════
echo   EJECUTANDO AUDITORÍA AUTOMATIZADA
echo ═══════════════════════════════════════════════════════════
echo.
echo ⚠️  IMPORTANTE: Asegúrate de que el servidor esté corriendo
echo    en http://localhost:5000
echo.
set /p continue="¿El servidor está corriendo? (S/N): "
if /i not "%continue%"=="S" (
    echo.
    echo ℹ️  Inicia el servidor con: python run.py
    echo    Luego ejecuta esta opción nuevamente
    pause
    goto menu
)
echo.
python backend/tests/test_audit_system.py
if errorlevel 1 (
    echo.
    echo ⚠️  Auditoría completada con errores
) else (
    echo.
    echo ✅ Auditoría completada exitosamente
)
echo.
pause
goto menu

:full_audit
echo.
echo ═══════════════════════════════════════════════════════════
echo   AUDITORÍA COMPLETA (Datos + Pruebas)
echo ═══════════════════════════════════════════════════════════
echo.
echo Paso 1/2: Cargando datos de prueba...
echo.
python backend/scripts/load_complete_test_data.py
if errorlevel 1 (
    echo.
    echo ❌ Error al cargar datos de prueba
    pause
    goto menu
)
echo.
echo ✅ Datos cargados
echo.
echo Paso 2/2: Ejecutando auditoría...
echo.
echo ⚠️  IMPORTANTE: Asegúrate de que el servidor esté corriendo
echo    en http://localhost:5000
echo.
set /p continue="¿El servidor está corriendo? (S/N): "
if /i not "%continue%"=="S" (
    echo.
    echo ℹ️  Inicia el servidor con: python run.py
    echo    Luego ejecuta esta opción nuevamente
    pause
    goto menu
)
echo.
python backend/tests/test_audit_system.py
if errorlevel 1 (
    echo.
    echo ⚠️  Auditoría completada con errores
) else (
    echo.
    echo ✅ Auditoría completa exitosa
)
echo.
pause
goto menu

:clean_db
echo.
echo ═══════════════════════════════════════════════════════════
echo   LIMPIAR BASE DE DATOS
echo ═══════════════════════════════════════════════════════════
echo.
echo ⚠️  ADVERTENCIA: Esto eliminará TODOS los datos de la base de datos
echo.
set /p confirm="¿Estás seguro? (S/N): "
if /i not "%confirm%"=="S" (
    echo Operación cancelada
    pause
    goto menu
)
echo.
echo Limpiando base de datos...
python -c "from backend.app import create_app; from backend.database import db; app = create_app(); app.app_context().push(); db.drop_all(); db.create_all(); print('✅ Base de datos limpia')"
if errorlevel 1 (
    echo ❌ Error al limpiar base de datos
) else (
    echo ✅ Base de datos limpiada exitosamente
)
echo.
pause
goto menu

:end
echo.
echo ¡Hasta luego!
echo.
exit /b 0
