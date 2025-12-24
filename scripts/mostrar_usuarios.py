#!/usr/bin/env python3
"""
Script para mostrar todos los usuarios del sistema con sus cédulas
"""

from backend.models.user import User
from backend.database import db
from backend.app import create_app

def main():
    app = create_app()
    with app.app_context():
        users = User.query.all()
        
        print("=" * 60)
        print("🗳️  USUARIOS DEL SISTEMA ELECTORAL")
        print("=" * 60)
        
        for user in users:
            password = "admin123" if user.rol == "super_admin" else "test123"
            print(f"👤 {user.rol.upper().replace('_', ' ')}")
            print(f"   Nombre: {user.nombre}")
            print(f"   Cédula: {user.cedula}")
            print(f"   Contraseña: {password}")
            print(f"   Estado: {'✅ Activo' if user.activo else '❌ Inactivo'}")
            print("-" * 40)
        
        print("\n🔑 CREDENCIALES PARA LOGIN:")
        print("=" * 40)
        for user in users:
            password = "admin123" if user.rol == "super_admin" else "test123"
            print(f"Cédula: {user.cedula} | Contraseña: {password} | Rol: {user.rol}")

if __name__ == "__main__":
    main()