#!/usr/bin/env python3
"""
Script para aplicar la migración de testigos registrados
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.app import create_app
from backend.migrations.create_testigos_registrados_tables import upgrade

def main():
    """Aplicar migración de testigos registrados"""
    print("🚀 Aplicando migración de testigos registrados...")
    
    # Crear aplicación
    app = create_app()
    
    with app.app_context():
        try:
            # Ejecutar migración
            upgrade()
            print("✅ Migración aplicada exitosamente")
            
        except Exception as e:
            print(f"❌ Error aplicando migración: {e}")
            return 1
    
    return 0

if __name__ == '__main__':
    exit(main())