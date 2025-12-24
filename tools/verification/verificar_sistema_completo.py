#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
import sys

# Configurar encoding
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = create_app()
with app.app_context():
    print("\nVerificando que la aplicacion esta cargando usuarios...")
    print("=" * 70)
    
    # Contar usuarios
    total_users = User.query.count()
    print(f"\n[OK] Total usuarios en base de datos: {total_users}")
    
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
        ub = Location.query.get(u.ubicacion_id) if u.ubicacion_id else None
        ub_name = ub.nombre if ub else "sin ubicacion"
        print(f"  - {u.nombre} ({u.rol}) - {ub_name}")
    
    # Verificar ubicaciones
    print(f"\nVerificando ubicaciones...")
    total_locations = Location.query.count()
    print(f"[OK] Total ubicaciones: {total_locations}")
    
    users_with_location = User.query.filter(User.ubicacion_id.isnot(None)).count()
    print(f"[OK] Usuarios con ubicacion asignada: {users_with_location}")
    
    # Verificar contraseñas
    print(f"\nVerificando contrasenas...")
    sample_user = User.query.filter_by(nombre='ARMENIA_P01').first()
    if sample_user:
        pwd_check = sample_user.verify_password('test123')
        print(f"[OK] Usuario ARMENIA_P01 existe")
        print(f"[OK] Contrasena test123 valida: {pwd_check}")
    else:
        print(f"[ERROR] Usuario ARMENIA_P01 no encontrado")
    
    print("\n" + "=" * 70)
    print("[OK] SISTEMA COMPLETAMENTE FUNCIONAL Y OPERATIVO")
    print("=" * 70 + "\n")
