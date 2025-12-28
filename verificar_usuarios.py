#!/usr/bin/env python3
"""
Script para verificar usuarios disponibles en el sistema
"""
import sys
import os
sys.path.append('.')

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def main():
    app = create_app('development')
    
    with app.app_context():
        print("🔍 VERIFICANDO USUARIOS DISPONIBLES")
        print("="*50)
        
        # Verificar testigos en Armenia
        print("\n📍 TESTIGOS EN ARMENIA:")
        armenia_users = User.query.filter(
            User.rol == 'testigo_electoral'
        ).join(Location, User.ubicacion_id == Location.id).filter(
            Location.municipio_codigo == '2601'
        ).all()
        
        print(f"Total testigos en Armenia: {len(armenia_users)}")
        
        for user in armenia_users[:10]:  # Mostrar primeros 10
            location = Location.query.get(user.ubicacion_id)
            print(f"  - Usuario: {user.nombre}")
            print(f"    Cédula: {user.cedula}")
            print(f"    Puesto: {location.nombre_completo if location else 'Sin ubicación'}")
            print()
        
        if len(armenia_users) > 10:
            print(f"  ... y {len(armenia_users) - 10} testigos más")
        
        # Verificar usuarios por rol
        print("\n👥 RESUMEN POR ROL:")
        roles = ['super_admin', 'coordinador_departamental', 'coordinador_municipal', 
                'coordinador_puesto', 'testigo_electoral']
        
        for rol in roles:
            count = User.query.filter_by(rol=rol).count()
            print(f"  {rol}: {count} usuarios")
        
        # Mostrar algunos usuarios de ejemplo
        print("\n🔑 USUARIOS DE EJEMPLO:")
        
        # Super admin
        super_admin = User.query.filter_by(rol='super_admin').first()
        if super_admin:
            print(f"  Super Admin: {super_admin.nombre} (sin cédula)")
        
        # Coordinador departamental
        coord_dept = User.query.filter_by(rol='coordinador_departamental').first()
        if coord_dept:
            print(f"  Coord. Departamental: {coord_dept.nombre}")
        
        # Coordinador municipal Armenia
        coord_mun = User.query.filter(
            User.rol == 'coordinador_municipal'
        ).join(Location, User.ubicacion_id == Location.id).filter(
            Location.municipio_codigo == '2601'
        ).first()
        if coord_mun:
            print(f"  Coord. Municipal Armenia: {coord_mun.nombre}")
        
        # Primer testigo de Armenia
        if armenia_users:
            testigo = armenia_users[0]
            print(f"  Testigo ejemplo: {testigo.nombre} - Cédula: {testigo.cedula}")

if __name__ == "__main__":
    main()