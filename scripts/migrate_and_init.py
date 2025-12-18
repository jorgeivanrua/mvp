#!/usr/bin/env python3
"""
Script de migración e inicialización para Render
Ejecuta migraciones y carga datos iniciales automáticamente

Este script se debe ejecutar en Render como parte del proceso de despliegue
"""
import sys
import os
import subprocess

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

def ejecutar_comando(comando, descripcion):
    """Ejecutar un comando y manejar errores"""
    print(f"\n🔄 {descripcion}...")
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {descripcion} completado")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error en {descripcion}")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Excepción en {descripcion}: {e}")
        return False

def main():
    """Función principal de migración e inicialización"""
    print("=" * 80)
    print("🚀 RENDER - MIGRACIÓN E INICIALIZACIÓN AUTOMÁTICA")
    print("=" * 80)
    
    # 1. Ejecutar migraciones de Flask-Migrate
    print("\n📋 PASO 1: MIGRACIONES DE BASE DE DATOS")
    
    # Inicializar migraciones si no existen
    if not os.path.exists('migrations'):
        if not ejecutar_comando('flask db init', 'Inicializar migraciones'):
            print("⚠️  Continuando sin inicializar migraciones...")
    
    # Crear migración si hay cambios
    ejecutar_comando('flask db migrate -m "Auto migration for Render"', 'Crear migración automática')
    
    # Aplicar migraciones
    if not ejecutar_comando('flask db upgrade', 'Aplicar migraciones'):
        print("❌ Error crítico en migraciones")
        return False
    
    # 2. Ejecutar migraciones personalizadas
    print("\n📋 PASO 2: MIGRACIONES PERSONALIZADAS")
    
    migraciones_personalizadas = [
        'backend/migrations/add_incidentes_delitos_fotos_table.py'
    ]
    
    for migracion in migraciones_personalizadas:
        if os.path.exists(migracion):
            ejecutar_comando(f'python {migracion}', f'Migración personalizada: {migracion}')
    
    # 3. Cargar datos iniciales (Quindío)
    print("\n📋 PASO 3: CARGA DE DATOS INICIALES")
    
    if not ejecutar_comando('python scripts/init_render_quindio.py', 'Cargar Quindío'):
        print("❌ Error cargando datos iniciales")
        return False
    
    print("\n✅ MIGRACIÓN E INICIALIZACIÓN COMPLETADA")
    print("🎉 Sistema listo para usar en Render")
    return True

if __name__ == '__main__':
    try:
        exitoso = main()
        sys.exit(0 if exitoso else 1)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)