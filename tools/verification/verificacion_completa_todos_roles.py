#!/usr/bin/env python3
"""
Verificación completa de todos los roles del sistema electoral
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app()
with app.app_context():
    print("\n🔍 VERIFICACIÓN COMPLETA DE TODOS LOS ROLES")
    print("="*80)
    
    # 1. Contar todos los usuarios por rol
    print("\n📊 RESUMEN GENERAL DE USUARIOS:")
    print("-" * 50)
    
    total_usuarios = User.query.count()
    usuarios_activos = User.query.filter_by(activo=True).count()
    
    print(f"Total usuarios en sistema: {total_usuarios}")
    print(f"Usuarios activos: {usuarios_activos}")
    
    # Contar por rol
    roles_count = {}
    for user in User.query.all():
        rol = user.rol
        if rol not in roles_count:
            roles_count[rol] = 0
        roles_count[rol] += 1
    
    print(f"\nDistribución por rol:")
    for rol, count in sorted(roles_count.items()):
        print(f"  - {rol}: {count}")
    
    # 2. Verificar cada tipo de usuario específicamente
    print(f"\n🔐 VERIFICACIÓN DETALLADA POR ROL:")
    print("="*80)
    
    # SUPER ADMIN
    print(f"\n1️⃣ SUPER ADMINISTRADOR:")
    print("-" * 40)
    super_admins = User.query.filter_by(rol='super_admin', activo=True).all()
    print(f"Cantidad: {len(super_admins)}")
    
    for admin in super_admins:
        print(f"  ✅ {admin.nombre}")
        print(f"     ID: {admin.id}")
        print(f"     Contraseña: admin123")
        print(f"     Ubicación: No requiere")
    
    # COORDINADOR DEPARTAMENTAL
    print(f"\n2️⃣ COORDINADOR DEPARTAMENTAL:")
    print("-" * 40)
    coord_dept = User.query.filter_by(rol='coordinador_departamental', activo=True).all()
    print(f"Cantidad: {len(coord_dept)}")
    
    for coord in coord_dept:
        ubicacion = Location.query.get(coord.ubicacion_id) if coord.ubicacion_id else None
        print(f"  ✅ {coord.nombre}")
        print(f"     ID: {coord.id}")
        print(f"     Contraseña: test123")
        if ubicacion:
            print(f"     Departamento: {ubicacion.departamento_nombre}")
            print(f"     Ubicación ID: {coord.ubicacion_id} ({'✅ VÁLIDA' if ubicacion else '❌ INVÁLIDA'})")
        else:
            print(f"     Ubicación: Sin asignar o inválida (ID: {coord.ubicacion_id})")
    
    # COORDINADORES MUNICIPALES
    print(f"\n3️⃣ COORDINADORES MUNICIPALES:")
    print("-" * 40)
    coord_mun = User.query.filter_by(rol='coordinador_municipal', activo=True).all()
    print(f"Cantidad: {len(coord_mun)}")
    
    municipales_validos = 0
    municipales_invalidos = 0
    
    for coord in coord_mun:
        ubicacion = Location.query.get(coord.ubicacion_id) if coord.ubicacion_id else None
        if ubicacion:
            municipales_validos += 1
            print(f"  ✅ {coord.nombre}")
            print(f"     Municipio: {ubicacion.municipio_nombre}")
            print(f"     Departamento: {ubicacion.departamento_nombre}")
            print(f"     Ubicación ID: {coord.ubicacion_id}")
        else:
            municipales_invalidos += 1
            print(f"  ❌ {coord.nombre}")
            print(f"     Ubicación: INVÁLIDA (ID: {coord.ubicacion_id})")
        print(f"     Contraseña: test123")
        print()
    
    print(f"Resumen Municipales: {municipales_validos} válidos, {municipales_invalidos} inválidos")
    
    # COORDINADORES DE PUESTO
    print(f"\n4️⃣ COORDINADORES DE PUESTO:")
    print("-" * 40)
    coord_puesto = User.query.filter_by(rol='coordinador_puesto', activo=True).all()
    print(f"Cantidad: {len(coord_puesto)}")
    
    puestos_validos = 0
    puestos_invalidos = 0
    
    # Mostrar solo los primeros 5 como ejemplo
    print(f"Mostrando primeros 5 coordinadores de puesto:")
    for i, coord in enumerate(coord_puesto[:5]):
        ubicacion = Location.query.get(coord.ubicacion_id) if coord.ubicacion_id else None
        if ubicacion:
            zona_numero = ubicacion.zona_codigo[-2:] if len(ubicacion.zona_codigo) >= 2 else ubicacion.zona_codigo
            print(f"  ✅ {coord.nombre}")
            print(f"     Puesto: {ubicacion.puesto_nombre}")
            print(f"     Municipio: {ubicacion.municipio_nombre}")
            print(f"     Zona: {zona_numero.zfill(2)}")
            print(f"     Ubicación ID: {coord.ubicacion_id}")
        else:
            print(f"  ❌ {coord.nombre}")
            print(f"     Ubicación: INVÁLIDA (ID: {coord.ubicacion_id})")
        print(f"     Contraseña: test123")
        print()
    
    # Contar todos los coordinadores de puesto
    for coord in coord_puesto:
        ubicacion = Location.query.get(coord.ubicacion_id) if coord.ubicacion_id else None
        if ubicacion:
            puestos_validos += 1
        else:
            puestos_invalidos += 1
    
    print(f"Resumen Puestos: {puestos_validos} válidos, {puestos_invalidos} inválidos")
    
    # TESTIGOS ELECTORALES
    print(f"\n5️⃣ TESTIGOS ELECTORALES:")
    print("-" * 40)
    testigos = User.query.filter_by(rol='testigo_electoral', activo=True).all()
    print(f"Cantidad: {len(testigos)}")
    
    testigos_validos = 0
    testigos_invalidos = 0
    
    # Mostrar solo los primeros 5 como ejemplo
    print(f"Mostrando primeros 5 testigos:")
    for i, testigo in enumerate(testigos[:5]):
        ubicacion = Location.query.get(testigo.ubicacion_id) if testigo.ubicacion_id else None
        if ubicacion:
            zona_numero = ubicacion.zona_codigo[-2:] if len(ubicacion.zona_codigo) >= 2 else ubicacion.zona_codigo
            print(f"  ✅ {testigo.nombre}")
            print(f"     Cédula: {testigo.cedula}")
            print(f"     Puesto: {ubicacion.puesto_nombre}")
            print(f"     Municipio: {ubicacion.municipio_nombre}")
            print(f"     Zona: {zona_numero.zfill(2)}")
            print(f"     Ubicación ID: {testigo.ubicacion_id}")
        else:
            print(f"  ❌ {testigo.nombre}")
            print(f"     Cédula: {testigo.cedula}")
            print(f"     Ubicación: INVÁLIDA (ID: {testigo.ubicacion_id})")
        print(f"     Contraseña: test123")
        print()
    
    # Contar todos los testigos
    for testigo in testigos:
        ubicacion = Location.query.get(testigo.ubicacion_id) if testigo.ubicacion_id else None
        if ubicacion:
            testigos_validos += 1
        else:
            testigos_invalidos += 1
    
    print(f"Resumen Testigos: {testigos_validos} válidos, {testigos_invalidos} inválidos")
    
    # MONITOREO
    print(f"\n6️⃣ USUARIOS DE MONITOREO:")
    print("-" * 40)
    monitoreo = User.query.filter_by(rol='monitoreo', activo=True).all()
    print(f"Cantidad: {len(monitoreo)}")
    
    for monitor in monitoreo:
        print(f"  ✅ {monitor.nombre}")
        print(f"     ID: {monitor.id}")
        print(f"     Contraseña: test123")
        print(f"     Ubicación: No requiere específica")
    
    # 3. RESUMEN FINAL
    print(f"\n🎯 RESUMEN FINAL DEL SISTEMA:")
    print("="*80)
    
    total_invalidos = municipales_invalidos + puestos_invalidos + testigos_invalidos
    total_validos = municipales_validos + puestos_validos + testigos_validos
    
    print(f"📊 ESTADÍSTICAS GENERALES:")
    print(f"   Total usuarios: {total_usuarios}")
    print(f"   Usuarios activos: {usuarios_activos}")
    print(f"   Super Admins: {len(super_admins)}")
    print(f"   Coordinador Departamental: {len(coord_dept)}")
    print(f"   Coordinadores Municipales: {len(coord_mun)} ({municipales_validos} válidos, {municipales_invalidos} inválidos)")
    print(f"   Coordinadores de Puesto: {len(coord_puesto)} ({puestos_validos} válidos, {puestos_invalidos} inválidos)")
    print(f"   Testigos Electorales: {len(testigos)} ({testigos_validos} válidos, {testigos_invalidos} inválidos)")
    print(f"   Usuarios de Monitoreo: {len(monitoreo)}")
    
    print(f"\n🔍 INTEGRIDAD DE UBICACIONES:")
    print(f"   Usuarios con ubicaciones válidas: {total_validos}")
    print(f"   Usuarios con ubicaciones inválidas: {total_invalidos}")
    
    if total_invalidos == 0:
        print(f"\n🟢 ESTADO DEL SISTEMA: COMPLETAMENTE OPERATIVO")
        print(f"✅ Todos los usuarios tienen ubicaciones válidas")
        print(f"✅ Sistema listo para producción")
    else:
        print(f"\n🔴 ESTADO DEL SISTEMA: REQUIERE CORRECCIÓN")
        print(f"❌ {total_invalidos} usuarios con ubicaciones inválidas")
        print(f"⚠️ Se requiere corrección antes de producción")
    
    print(f"\n📋 CREDENCIALES DE ACCESO:")
    print(f"   Super Admin: admin123")
    print(f"   Todos los demás usuarios: test123")
    print(f"   URL del sistema: http://127.0.0.1:5000")
    
    print("\n" + "="*80)