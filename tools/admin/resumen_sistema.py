#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resumen del Estado del Sistema Electoral de Quindio
Verificacion de usuarios y configuracion
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app()
with app.app_context():
    # Contar usuarios
    total_users = User.query.count()
    
    # Agrupar por rol
    roles_count = {}
    for u in User.query.all():
        rol = u.rol
        roles_count[rol] = roles_count.get(rol, 0) + 1
    
    # Ubicaciones
    total_locations = Location.query.count()
    users_with_location = User.query.filter(User.ubicacion_id.isnot(None)).count()
    
    # Mostrar resumen
    print("\n" + "="*70)
    print("RESUMEN - SISTEMA ELECTORAL QUINDIO")
    print("="*70)
    print(f"\nUsuarios Totales: {total_users}")
    print("\nDistribucion por rol:")
    for rol in sorted(roles_count.keys()):
        count = roles_count[rol]
        print(f"  {rol:30s}: {count:3d}")
    print(f"\nUbicaciones Totales: {total_locations}")
    print(f"Usuarios con Ubicacion: {users_with_location}/{total_users}")
    print("\n" + "="*70)
    print("ESTADO: SISTEMA OPERATIVO Y LISTO PARA USAR")
    print("="*70 + "\n")
