"""Verificar usuario super_admin"""
from backend.database import db
from backend.models.user import User
from backend.app import create_app

app = create_app()

with app.app_context():
    super_admin = User.query.filter_by(rol='super_admin').first()
    
    if super_admin:
        print(f"Usuario encontrado: {super_admin.nombre}")
        print(f"Rol: {super_admin.rol}")
        print(f"Activo: {super_admin.activo}")
        
        # Probar contraseñas comunes
        passwords = ['admin123', 'Admin123', 'password', 'super_admin']
        
        for pwd in passwords:
            if super_admin.check_password(pwd):
                print(f"\n✓ Contraseña correcta: {pwd}")
                break
        else:
            print("\n✗ Ninguna contraseña común funciona")
    else:
        print("✗ No se encontró usuario super_admin")
