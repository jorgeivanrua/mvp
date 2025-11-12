"""
Script para inicializar la base de datos del MVP
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app, db
from app.models.user import User
from app.models.location import Location
from app.models.form_e14 import FormE14, FormE14History
from app.models.enums import UserRole, LocationType

def init_database():
    """Inicializar base de datos con estructura básica"""
    print("🚀 Inicializando base de datos MVP...")
    
    app = create_app('development')
    
    with app.app_context():
        # Eliminar tablas existentes
        print("📦 Eliminando tablas existentes...")
        db.drop_all()
        
        # Crear todas las tablas
        print("🔨 Creando tablas...")
        db.create_all()
        
        print("✅ Base de datos inicializada correctamente")
        print("\n📊 Tablas creadas:")
        print("  - users")
        print("  - locations")
        print("  - forms_e14")
        print("  - forms_e14_history")
        
        # Crear usuario superadmin por defecto
        print("\n👤 Creando usuario superadmin...")
        admin = User(
            nombre="Administrador del Sistema",
            email="admin@sistema.com",
            rol=UserRole.SISTEMAS,
            activo=True
        )
        admin.set_password("Admin123!")
        admin.save()
        
        print(f"✅ Superadmin creado: {admin.email}")
        print(f"   Contraseña: Admin123!")
        
        print("\n✨ Inicialización completada")
        print("\n📝 Próximos pasos:")
        print("  1. Ejecutar: python mvp/scripts/load_sample_data.py")
        print("  2. Ejecutar: python run.py")
        print("  3. Acceder a: http://localhost:5000")

if __name__ == '__main__':
    init_database()
