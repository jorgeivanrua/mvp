#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

print("Verificando que la aplicación está cargando usuarios...")
print("=" * 70)

try:
    # Verificar que el servidor está corriendo
    response = requests.get('http://localhost:5000/api/users')
    
    if response.status_code == 200:
        users = response.json()
        print(f"\n✓ Conexión exitosa a la API")
        print(f"✓ Total usuarios cargados: {len(users)}")
        
        # Agrupar por rol
        roles = {}
        for u in users:
            rol = u.get('rol', 'sin_rol')
            if rol not in roles:
                roles[rol] = 0
            roles[rol] += 1
        
        print(f"\nUsuarios por rol:")
        for rol, count in sorted(roles.items()):
            print(f"  - {rol}: {count}")
        
        # Mostrar algunos usuarios
        print(f"\nPrimeros 5 usuarios:")
        for u in users[:5]:
            print(f"  - {u.get('nombre', 'N/A')} ({u.get('rol', 'N/A')})")
        
        # Verificar ubicaciones
        print(f"\nVerificando ubicaciones...")
        ubicaciones_set = set()
        for u in users:
            ub = u.get('ubicacion_id')
            if ub:
                ubicaciones_set.add(ub)
        print(f"✓ Usuarios con ubicaciones: {len(ubicaciones_set)}")
        
    else:
        print(f"✗ Error al conectar: HTTP {response.status_code}")
        
except Exception as e:
    print(f"✗ Error de conexión: {e}")
    print("\nAsegúrate que la aplicación está corriendo en http://localhost:5000")

print("\n" + "=" * 70)
