#!/usr/bin/env python
"""
Verificar usuario específico
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models import User

app = create_app('production')

with app.app_context():
    # Buscar por cédula
    user = User.query.filter_by(cedula='2601010101001').first()
    if user:
        print(f"Usuario encontrado:")
        print(f"  ID: {user.id}")
        print(f"  Nombre: {user.nombre}")
        print(f"  Usuario/Field: {user.usuario if hasattr(user, 'usuario') else 'N/A'}")
        print(f"  Cedula: {user.cedula}")
        print(f"  Rol: {user.rol}")
        print(f"  Activo: {user.activo}")
        print(f"  Password Hash: {user.password_hash[:30]}..." if user.password_hash else "No hash")
    else:
        print("Usuario no encontrado")
        
    # Listar todas las columnas del modelo
    print("\nColumnas del modelo User:")
    for col in User.__table__.columns:
        print(f"  - {col.name}")
