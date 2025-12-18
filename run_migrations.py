#!/usr/bin/env python3
"""
Script para ejecutar migraciones automáticamente en Render
"""
import sys
import os
import subprocess

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

def ejecutar_comando(comando, descripcion):
    """Ejecutar un comando y manejar errores"""
    print(f"🔄 {descripcion}...")
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {descripcion} completado")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"⚠️  {descripcion} - Warning")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Excepción en {descripcion}: {e}")
        return False

def main():
    """Ejecutar migraciones"""
    print("🚀 Ejecutando migraciones para Render...")
    
    # Configurar variables de entorno para Flask
    os.environ['FLASK_APP'] = 'run.py'
    
    # 1. Inicializar migraciones si no existen
    if not os.path.exists('migrations'):
        ejecutar_comando('flask db init', 'Inicializar migraciones')
    
    # 2. Crear migración automática
    ejecutar_comando('flask db migrate -m "Auto migration for Render"', 'Crear migración')
    
    # 3. Aplicar migraciones
    ejecutar_comando('flask db upgrade', 'Aplicar migraciones')
    
    # 4. Ejecutar migraciones personalizadas
    migraciones_personalizadas = [
        'backend/migrations/add_incidentes_delitos_fotos_table.py'
    ]
    
    for migracion in migraciones_personalizadas:
        if os.path.exists(migracion):
            ejecutar_comando(f'python {migracion}', f'Migración: {os.path.basename(migracion)}')
    
    print("✅ Migraciones completadas")

if __name__ == '__main__':
    main()