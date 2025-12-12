#!/usr/bin/env python3
"""
Script para aplicar migración de fotos múltiples
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.app import create_app
from backend.migrations.add_formulario_fotos_table import aplicar_migracion

def main():
    """Aplicar migración de fotos múltiples"""
    print("=== APLICANDO MIGRACIÓN: FOTOS MÚLTIPLES ===")
    
    # Crear aplicación
    app = create_app()
    
    with app.app_context():
        success = aplicar_migracion()
        
        if success:
            print("\n✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print("\nFuncionalidades agregadas:")
            print("- Tabla formulario_fotos para múltiples fotos por formulario")
            print("- Migración de fotos existentes desde imagen_url")
            print("- Sistema de validación individual de fotos")
            print("- Soporte para fotos principales y ordenamiento")
            return 0
        else:
            print("\n❌ ERROR EN LA MIGRACIÓN")
            return 1

if __name__ == '__main__':
    exit(main())