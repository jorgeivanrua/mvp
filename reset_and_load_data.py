"""
Script para limpiar la base de datos y cargar datos de prueba
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.database import db

def reset_database():
    """Limpiar y recrear la base de datos"""
    app = create_app()
    
    with app.app_context():
        print("\n🔄 Limpiando base de datos...")
        db.drop_all()
        print("✅ Tablas eliminadas")
        
        print("\n🔨 Creando tablas...")
        db.create_all()
        print("✅ Tablas creadas")
        
        print("\n📦 Cargando datos de prueba...")
        # Importar y ejecutar el script de carga
        from backend.scripts.load_complete_test_data import load_complete_test_data
        load_complete_test_data()
        
        print("\n✅ ¡Base de datos lista!")
        print("\n🔑 Puedes iniciar sesión con:")
        print("   - admin_test / test123 (Super Admin)")
        print("   - testigo_test_1 / test123 (Testigo)")
        print("   - coord_puesto_test / test123 (Coordinador Puesto)")
        print()

if __name__ == '__main__':
    reset_database()
