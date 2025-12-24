#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app()
with app.app_context():
    print("\n🔐 SISTEMA DE LOGIN BASADO EN UBICACIÓN")
    print("="*80)
    print("Los usuarios se autentican usando su UBICACIÓN como identificador")
    print("="*80)
    
    # Super Admin (sin ubicación)
    admin = User.query.filter_by(rol='super_admin').first()
    if admin:
        print(f"\n✅ SUPER ADMIN:")
        print(f"   - Rol: super_admin")
        print(f"   - Usuario: {admin.nombre}")
        print(f"   - Password: admin123")
        print(f"   - Ubicación: No requiere")
    
    # Coordinador Departamental
    coord_dept = User.query.filter_by(rol='coordinador_departamental').first()
    if coord_dept:
        ubicacion = Location.query.get(coord_dept.ubicacion_id)
        print(f"\n✅ COORDINADOR DEPARTAMENTAL:")
        print(f"   - Rol: coordinador_departamental")
        print(f"   - Departamento: {ubicacion.departamento_nombre if ubicacion else 'N/A'}")
        print(f"   - Password: test123")
    
    # Coordinadores Municipales
    print(f"\n✅ COORDINADORES MUNICIPALES:")
    coords_mun = User.query.filter_by(rol='coordinador_municipal').limit(3).all()
    for coord in coords_mun:
        ubicacion = Location.query.get(coord.ubicacion_id) if coord.ubicacion_id else None
        print(f"   - Municipio: {ubicacion.municipio_nombre if ubicacion else coord.nombre}")
        print(f"     Código: {ubicacion.municipio_codigo if ubicacion else 'N/A'}")
        print(f"     Password: test123")
    
    # Coordinadores de Puesto
    print(f"\n✅ COORDINADORES DE PUESTO:")
    coords_puesto = User.query.filter_by(rol='coordinador_puesto').limit(3).all()
    for coord in coords_puesto:
        ubicacion = Location.query.get(coord.ubicacion_id) if coord.ubicacion_id else None
        if ubicacion:
            print(f"   - Puesto: {ubicacion.puesto_nombre}")
            print(f"     Municipio: {ubicacion.municipio_nombre} ({ubicacion.municipio_codigo})")
            print(f"     Zona: {ubicacion.zona_codigo}")
            print(f"     Puesto: {ubicacion.puesto_codigo}")
            print(f"     Password: test123")
    
    # Testigos Electorales
    print(f"\n✅ TESTIGOS ELECTORALES:")
    testigos = User.query.filter_by(rol='testigo_electoral').limit(3).all()
    for testigo in testigos:
        ubicacion = Location.query.get(testigo.ubicacion_id) if testigo.ubicacion_id else None
        print(f"   - Cédula: {testigo.cedula}")
        if ubicacion:
            print(f"     Puesto: {ubicacion.puesto_nombre}")
            print(f"     Municipio: {ubicacion.municipio_nombre} ({ubicacion.municipio_codigo})")
            print(f"     Zona: {ubicacion.zona_codigo}")
            print(f"     Puesto: {ubicacion.puesto_codigo}")
        print(f"     Password: test123")
    
    print("\n" + "="*80)
    print("📋 INSTRUCCIONES PARA EL LOGIN:")
    print("="*80)
    print("1. Selecciona el ROL en el formulario")
    print("2. Selecciona la UBICACIÓN (Departamento → Municipio → Zona → Puesto)")
    print("3. Ingresa la CONTRASEÑA:")
    print("   - Super Admin: admin123")
    print("   - Todos los demás: test123")
    print("4. Para testigos: también ingresa tu CÉDULA")
    print("="*80)