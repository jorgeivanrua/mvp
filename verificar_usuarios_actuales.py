#!/usr/bin/env python3
"""Verificar usuarios actuales en el sistema"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def verificar_usuarios():
    """Verificar usuarios en el sistema"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("USUARIOS EN EL SISTEMA")
        print("=" * 80)
        
        usuarios = User.query.all()
        print(f"\nTotal usuarios: {len(usuarios)}\n")
        
        # Agrupar por rol
        roles = {}
        for user in usuarios:
            if user.rol not in roles:
                roles[user.rol] = []
            roles[user.rol].append(user)
        
        for rol, users in sorted(roles.items()):
            print(f"\n{rol.upper()}: {len(users)} usuarios")
            print("-" * 80)
            for user in users:
                ubicacion = Location.query.get(user.ubicacion_id) if user.ubicacion_id else None
                print(f"  Username: {user.nombre}")
                print(f"  Ubicación ID: {user.ubicacion_id}")
                if ubicacion:
                    print(f"  Ubicación: {ubicacion.nombre_completo}")
                    print(f"  Tipo: {ubicacion.tipo}")
                    if ubicacion.tipo == 'mesa':
                        print(f"  Votantes: {ubicacion.total_votantes_registrados}")
                print()

if __name__ == '__main__':
    verificar_usuarios()
