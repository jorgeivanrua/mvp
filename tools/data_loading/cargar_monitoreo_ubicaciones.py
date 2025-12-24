#!/usr/bin/env python3
"""
Cargar usuarios de monitoreo con ubicaciones asignadas
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def cargar_monitoreo_con_ubicaciones():
    app = create_app()
    
    with app.app_context():
        print("[*] Cargando usuarios de MONITOREO con ubicaciones...")
        print()
        
        # Obtener ubicaciones de municipios
        municipios = Location.query.filter_by(
            departamento_codigo='26',
            tipo='municipio',
            activo=True
        ).all()
        
        print(f"[*] Municipios encontrados: {len(municipios)}")
        print()
        
        # Crear usuarios de monitoreo para cada municipio
        count = 0
        for muni in municipios:
            user = User(
                nombre=f"Monitoreo {muni.municipio_nombre}",
                cedula=f"MON{muni.municipio_codigo}001",
                password_hash="temp",  # Se actualiza con set_password
                rol='monitoreo',
                ubicacion_id=muni.id,
                activo=True
            )
            user.set_password('test123')
            db.session.add(user)
            count += 1
            print(f"  [{count}] Monitoreo para {muni.municipio_nombre} (ubicación ID: {muni.id})")
        
        db.session.commit()
        
        print()
        print(f"[OK] Se crearon {count} usuarios de MONITOREO con ubicaciones")
        print()
        
        # Verificar
        monitoreo_count = User.query.filter_by(rol='monitoreo', activo=True).count()
        monitoreo_with_loc = User.query.filter(
            User.rol == 'monitoreo',
            User.activo == True,
            User.ubicacion_id != None
        ).count()
        
        print(f"[OK] Usuarios MONITOREO total: {monitoreo_count}")
        print(f"[OK] Usuarios MONITOREO con ubicación: {monitoreo_with_loc}")

if __name__ == '__main__':
    cargar_monitoreo_con_ubicaciones()
