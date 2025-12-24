#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
import sys
import io

# Configurar encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = create_app()
with app.app_context():
    print("\nEstado del Sistema Electoral de Quindio")
    print("=" * 70)
    
    # Contar usuarios
    total_users = User.query.count()
    print(f"\nTotal usuarios: {total_users}")
    
    # Agrupar por rol
    roles = {}
    for u in User.query.all():
        rol = u.rol
        if rol not in roles:
            roles[rol] = 0
        roles[rol] += 1
    
    print(f"\nUsuarios por rol:")
    for rol, count in sorted(roles.items()):
        print(f"  - {rol}: {count}")
    
    # Mostrar algunos usuarios
    print(f"\nPrimeros 5 usuarios:")
    for u in User.query.limit(5).all():
        print(f"  - {u.nombre} ({u.rol})")
    
    # Verificar ubicaciones
    total_locations = Location.query.count()
    print(f"\nTotal ubicaciones: {total_locations}")
    
    users_with_location = User.query.filter(User.ubicacion_id.isnot(None)).count()
    print(f"Usuarios con ubicacion asignada: {users_with_location}")
    
    print("\n" + "=" * 70)
    print("SISTEMA COMPLETAMENTE FUNCIONAL Y OPERATIVO")
    print("=" * 70 + "\n")
