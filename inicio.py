#!/usr/bin/env python3
"""
Script de inicio universal para el Sistema Electoral MVP
Configura automáticamente el entorno y ejecuta la aplicación

Uso:
    python inicio.py

Autor: Sistema de Desarrollo
Fecha: Diciembre 24, 2025
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Mostrar banner de inicio"""
    print("\n" + "="*50)
    print("🚀 Sistema Electoral MVP - Inicio Automático")
    print("="*50)

def print_step(step, message):
    """Imprimir paso con formato"""
    print(f"\n{step} {message}...")

def print_success(message):
    """Imprimir mensaje de éxito"""
    print(f"✅ {message}")

def print_warning(message):
    """Imprimir advertencia"""
    print(f"⚠️  {message}")

def print_error(message):
    """Imprimir error"""
    print(f"❌ {message}")

def check_python():
    """Verificar versión de Python"""
    print_step("📋", "Verificando Python")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python {version.major}.{version.minor} no soportado. Requiere Python 3.8+")
        return False
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro}")
    return True

def setup_venv():
    """Configurar entorno virtual"""
    print_step("🔧", "Configurando entorno virtual")
    
    venv_path = Path(".venv")
    
    if not venv_path.exists():
        print("📦 Creando entorno virtual...")
        try:
            subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
            print_success("Entorno virtual creado")
        except subprocess.CalledProcessError:
            print_error("Error creando entorno virtual")
            return False
    else:
        print_success("Entorno virtual ya existe")
    
    return True

def get_venv_python():
    """Obtener ruta del Python del entorno virtual"""
    system = platform.system()
    if system == "Windows":
        return Path(".venv/Scripts/python.exe")
    else:
        return Path(".venv/bin/python")

def install_dependencies():
    """Instalar dependencias"""
    print_step("📚", "Verificando dependencias")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print_warning("requirements.txt no encontrado")
        return True
    
    venv_python = get_venv_python()
    
    # Verificar si Flask está instalado
    try:
        result = subprocess.run([
            str(venv_python), "-c", "import flask; print('ok')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0 and "ok" in result.stdout:
            print_success("Dependencias ya instaladas")
            return True
    except:
        pass
    
    print("📦 Instalando dependencias...")
    try:
        subprocess.run([
            str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print_success("Dependencias instaladas")
        return True
    except subprocess.CalledProcessError:
        print_error("Error instalando dependencias")
        return False

def setup_directories():
    """Crear directorios necesarios"""
    print_step("📁", "Configurando directorios")
    
    directories = ["instance", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print_success("Directorios configurados")

def setup_environment():
    """Configurar variables de entorno"""
    print_step("⚙️", "Configurando variables de entorno")
    
    os.environ["FLASK_ENV"] = "development"
    os.environ["FLASK_DEBUG"] = "1"
    os.environ["PYTHONPATH"] = "."
    
    print_success("Variables de entorno configuradas")

def initialize_system():
    """Inicializar sistema si es necesario"""
    print_step("🔧", "Inicializando sistema")
    
    init_script = Path("scripts/init_system.py")
    if not init_script.exists():
        print_warning("Script de inicialización no encontrado")
        return True
    
    venv_python = get_venv_python()
    
    try:
        subprocess.run([str(venv_python), str(init_script)], check=True)
        print_success("Sistema inicializado")
        return True
    except subprocess.CalledProcessError:
        print_warning("Advertencias durante la inicialización (continuando...)")
        return True

def show_info():
    """Mostrar información del sistema"""
    print("\n" + "="*50)
    print("🎯 SISTEMA LISTO PARA INICIAR")
    print("="*50)
    print("📍 Puerto: 5000")
    print("🌐 URL: http://localhost:5000")
    print("🔧 Modo: Desarrollo")
    print("📊 Base de datos: SQLite (instance/app.db)")
    print("="*50)

def start_application():
    """Iniciar la aplicación"""
    print_step("🚀", "Iniciando servidor")
    print("💡 Presiona Ctrl+C para detener el servidor")
    print("="*50)
    
    venv_python = get_venv_python()
    
    try:
        subprocess.run([str(venv_python), "run.py"])
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print_error(f"Error iniciando servidor: {e}")

def main():
    """Función principal"""
    print_banner()
    
    # Verificar Python
    if not check_python():
        return 1
    
    # Configurar entorno virtual
    if not setup_venv():
        return 1
    
    # Instalar dependencias
    if not install_dependencies():
        return 1
    
    # Configurar directorios
    setup_directories()
    
    # Configurar variables de entorno
    setup_environment()
    
    # Inicializar sistema
    if not initialize_system():
        return 1
    
    # Mostrar información
    show_info()
    
    # Preguntar si iniciar
    try:
        response = input("\n¿Iniciar el servidor ahora? (S/n): ").strip().lower()
        if response in ["", "s", "y", "si", "yes"]:
            start_application()
        else:
            print_success("Sistema configurado. Ejecuta 'python run.py' para iniciar el servidor.")
    except KeyboardInterrupt:
        print("\n\n🏁 Configuración completada")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())