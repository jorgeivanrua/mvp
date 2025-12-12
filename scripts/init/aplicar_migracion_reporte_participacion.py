"""
Script para aplicar la migración de reporte_participacion
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.migrations.create_reporte_participacion_table import upgrade

if __name__ == '__main__':
    print("=" * 60)
    print("APLICANDO MIGRACIÓN: Reporte de Participación")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        try:
            upgrade()
            print("\n✅ Migración aplicada exitosamente")
            print("\nTabla creada:")
            print("  - reporte_participacion")
            print("\nÍndices creados:")
            print("  - idx_reporte_participacion_mesa")
            print("  - idx_reporte_participacion_hora")
            print("  - idx_reporte_participacion_testigo")
        except Exception as e:
            print(f"\n❌ Error al aplicar migración: {e}")
            sys.exit(1)
