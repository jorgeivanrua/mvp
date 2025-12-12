#!/usr/bin/env python3
"""
Script para aplicar migración de evidencias fotográficas múltiples
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.app import create_app
from backend.migrations.add_incidentes_delitos_fotos_table import aplicar_migracion

def main():
    """Aplicar migración de evidencias fotográficas múltiples"""
    print("=== APLICANDO MIGRACIÓN: EVIDENCIAS FOTOGRÁFICAS MÚLTIPLES ===")
    
    # Crear aplicación
    app = create_app()
    
    with app.app_context():
        success = aplicar_migracion()
        
        if success:
            print("\n✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print("\nFuncionalidades agregadas:")
            print("- Tabla incidentes_delitos_fotos para múltiples evidencias por reporte")
            print("- Migración de evidencias existentes desde evidencia_url")
            print("- Sistema de validación individual de evidencias")
            print("- Categorización y clasificación de evidencias")
            print("- Soporte para metadatos de captura y geolocalización")
            print("- Niveles de relevancia para evidencias")
            return 0
        else:
            print("\n❌ ERROR EN LA MIGRACIÓN")
            return 1

if __name__ == '__main__':
    exit(main())