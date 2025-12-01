#!/usr/bin/env python3
"""
Script para probar todos los endpoints de API de cada rol
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from flask_jwt_extended import create_access_token

def test_all_roles():
    """Probar que todos los roles tienen endpoints funcionando"""
    app = create_app('development')
    
    with app.app_context():
        print("=" * 60)
        print("PRUEBA DE ENDPOINTS POR ROL")
        print("=" * 60)
        
        roles = [
            'super_admin',
            'monitoreo',
            'coordinador_departamental',
            'coordinador_municipal',
            'coordinador_puesto',
            'auditor_electoral',
            'testigo_electoral'
        ]
        
        for rol in roles:
            print(f"\n{rol.upper()}")
            print("-" * 40)
            
            # Buscar usuario con este rol
            user = User.query.filter_by(rol=rol, activo=True).first()
            
            if user:
                print(f"✓ Usuario encontrado: {user.nombre}")
                print(f"  ID: {user.id}")
                print(f"  Ubicacion ID: {user.ubicacion_id}")
                print(f"  Activo: {user.activo}")
                
                # Crear token para este usuario
                token = create_access_token(
                    identity=str(user.id),
                    additional_claims={
                        'rol': user.rol,
                        'nombre': user.nombre,
                        'ubicacion_id': user.ubicacion_id
                    }
                )
                print(f"  Token generado: {token[:50]}...")
                
            else:
                print(f"✗ No se encontró usuario con rol: {rol}")
        
        print("\n" + "=" * 60)
        print("RESUMEN")
        print("=" * 60)
        
        total_users = User.query.filter_by(activo=True).count()
        print(f"Total usuarios activos: {total_users}")
        
        for rol in roles:
            count = User.query.filter_by(rol=rol, activo=True).count()
            status = "✓" if count > 0 else "✗"
            print(f"{status} {rol}: {count} usuario(s)")

if __name__ == '__main__':
    test_all_roles()
