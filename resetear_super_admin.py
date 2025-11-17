"""Resetear contraseña del super_admin"""
from backend.database import db
from backend.models.user import User
from backend.app import create_app

app = create_app()

with app.app_context():
    super_admin = User.query.filter_by(rol='super_admin').first()
    
    if super_admin:
        nueva_password = 'admin123'
        super_admin.set_password(nueva_password)
        db.session.commit()
        
        print(f"✓ Contraseña reseteada para: {super_admin.nombre}")
        print(f"  Nueva contraseña: {nueva_password}")
        
        # Verificar
        if super_admin.check_password(nueva_password):
            print("✓ Verificación exitosa")
        else:
            print("✗ Error en verificación")
    else:
        print("✗ No se encontró usuario super_admin")
