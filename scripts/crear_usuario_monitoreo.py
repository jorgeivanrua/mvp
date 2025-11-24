"""
Script para crear usuario de monitoreo
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User

app = create_app()

with app.app_context():
    print("🔍 Creando usuario de monitoreo...")
    
    # Verificar si ya existe
    existing = User.query.filter_by(rol='monitoreo').first()
    if existing:
        print(f"⚠️  Ya existe un usuario de monitoreo: {existing.nombre}")
        print(f"   ID: {existing.id}")
        print(f"   Activo: {existing.activo}")
        
        # Actualizar contraseña
        existing.set_password('monitoreo123')
        db.session.commit()
        print("✅ Contraseña actualizada a: monitoreo123")
    else:
        # Crear nuevo usuario
        usuario = User(
            nombre='monitoreo',
            rol='monitoreo',
            ubicacion_id=None,  # No necesita ubicación
            activo=True
        )
        usuario.set_password('monitoreo123')
        
        db.session.add(usuario)
        db.session.commit()
        
        print("✅ Usuario de monitoreo creado exitosamente")
        print(f"   Nombre: monitoreo")
        print(f"   Rol: monitoreo")
        print(f"   Contraseña: monitoreo123")
        print(f"   ID: {usuario.id}")
