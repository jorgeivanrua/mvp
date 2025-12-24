#!/usr/bin/env python
"""
Verificar estructura exacta de usuarios testigos
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models import User

app = create_app('production')

with app.app_context():
    # Obtener un testigo con su ubicación
    testigo = User.query.filter_by(rol='testigo_electoral').first()
    if testigo:
        from backend.models import Location
        loc = Location.query.get(testigo.ubicacion_id) if testigo.ubicacion_id else None
        
        print("TESTIGO ENCONTRADO:")
        print(f"  ID: {testigo.id}")
        print(f"  Nombre (usuario): {testigo.nombre}")
        print(f"  Cedula: {testigo.cedula}")
        print(f"  Ubicacion_ID: {testigo.ubicacion_id}")
        
        if loc:
            print(f"\nUBICACION ASOCIADA:")
            print(f"  Nombre ubicacion: {loc.nombre}")
            print(f"  Tipo: {loc.tipo}")
            print(f"  Codigo: {loc.codigo}")
            
            # Obtener jerarquía completa
            parent = loc
            hierarchy = []
            while parent:
                hierarchy.append(f"{parent.codigo}-{parent.nombre}")
                parent = Location.query.get(parent.parent_id) if parent.parent_id else None
            
            print(f"  Jerarquia completa:")
            for h in reversed(hierarchy):
                print(f"    - {h}")
    else:
        print("No se encontraron testigos")
