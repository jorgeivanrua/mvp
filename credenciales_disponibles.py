#!/usr/bin/env python3
"""
Script para mostrar credenciales disponibles para login
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
        print("🔑 CREDENCIALES DISPONIBLES PARA LOGIN")
        print("="*60)
        
        # Testigos en Armenia - Zona 01
        print("\n📍 TESTIGOS DISPONIBLES EN ARMENIA - ZONA 01:")
        print("Contraseña para todos: test123")
        print("-" * 40)
        
        armenia_testigos = User.query.filter(
            User.rol == 'testigo_electoral'
        ).join(Location, User.ubicacion_id == Location.id).filter(
            Location.municipio_codigo == '2601',
            Location.zona_codigo == '260101'
        ).limit(10).all()
        
        for i, testigo in enumerate(armenia_testigos, 1):
            location = Location.query.filter_by(id=testigo.ubicacion_id).first()
            print(f"{i:2d}. Cédula: {testigo.cedula}")
            print(f"    Usuario: {testigo.nombre}")
            print(f"    Puesto: {location.puesto_nombre if location else 'N/A'}")
            print()
        
        # Otros roles disponibles
        print("\n👑 OTROS ROLES DISPONIBLES:")
        print("-" * 40)
        
        # Super Admin
        super_admin = User.query.filter_by(rol='super_admin').first()
        if super_admin:
            print(f"Super Admin:")
            print(f"  Usuario: {super_admin.nombre}")
            print(f"  Contraseña: admin123")
            print()
        
        # Coordinador Departamental
        coord_dept = User.query.filter_by(rol='coordinador_departamental').first()
        if coord_dept:
            print(f"Coordinador Departamental:")
            print(f"  Usuario: {coord_dept.nombre}")
            print(f"  Contraseña: test123")
            print()
        
        # Coordinador Municipal Armenia
        coord_mun = User.query.filter(
            User.rol == 'coordinador_municipal'
        ).join(Location, User.ubicacion_id == Location.id).filter(
            Location.municipio_codigo == '2601'
        ).first()
        if coord_mun:
            print(f"Coordinador Municipal Armenia:")
            print(f"  Usuario: {coord_mun.nombre}")
            print(f"  Contraseña: test123")
            print()
        
        print("\n💡 INSTRUCCIONES DE USO:")
        print("="*60)
        print("1. Selecciona el rol 'Testigo Electoral'")
        print("2. Selecciona Departamento: Quindío")
        print("3. Selecciona Municipio: Armenia")
        print("4. Selecciona Zona: 260101")
        print("5. Selecciona cualquier puesto")
        print("6. Usa una de las cédulas mostradas arriba")
        print("7. Contraseña: test123")
        print()
        print("🎯 EJEMPLO DE LOGIN:")
        if armenia_testigos:
            ejemplo = armenia_testigos[0]
            print(f"   Cédula: {ejemplo.cedula}")
            print(f"   Contraseña: test123")

if __name__ == "__main__":
    main()