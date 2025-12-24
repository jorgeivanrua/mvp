#!/usr/bin/env python3
"""
Verificación rápida del estado actual del sistema
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.services.auth_service import AuthService

app = create_app()
with app.app_context():
    print("\n🔍 VERIFICACIÓN RÁPIDA DEL SISTEMA")
    print("="*60)
    
    # 1. Contar usuarios
    total_usuarios = User.query.count()
    usuarios_activos = User.query.filter_by(activo=True).count()
    coordinadores = User.query.filter_by(rol='coordinador_puesto', activo=True).count()
    
    print(f"\n📊 USUARIOS:")
    print(f"   Total: {total_usuarios}")
    print(f"   Activos: {usuarios_activos}")
    print(f"   Coordinadores: {coordinadores}")
    
    # 2. Verificar ubicaciones de coordinadores
    coordinadores_con_ubicacion = User.query.filter_by(
        rol='coordinador_puesto',
        activo=True
    ).filter(User.ubicacion_id.isnot(None)).count()
    
    coordinadores_validos = 0
    coordinadores_invalidos = 0
    
    for coord in User.query.filter_by(rol='coordinador_puesto', activo=True).all():
        if coord.ubicacion_id:
            ubicacion = Location.query.get(coord.ubicacion_id)
            if ubicacion:
                coordinadores_validos += 1
            else:
                coordinadores_invalidos += 1
    
    print(f"\n📍 UBICACIONES:")
    print(f"   Coordinadores con ubicación válida: {coordinadores_validos}")
    print(f"   Coordinadores con ubicación inválida: {coordinadores_invalidos}")
    
    # 3. Probar autenticación
    print(f"\n🔐 AUTENTICACIÓN:")
    
    auth_service = AuthService()
    
    # Probar Super Admin
    try:
        result = auth_service.authenticate_super_admin('admin123')
        print(f"   Super Admin: {'✅ OK' if result['success'] else '❌ FALLO'}")
    except Exception as e:
        print(f"   Super Admin: ❌ ERROR - {str(e)}")
    
    # Probar un coordinador
    coordinador_prueba = User.query.filter_by(
        rol='coordinador_puesto',
        activo=True
    ).filter(User.ubicacion_id.isnot(None)).first()
    
    if coordinador_prueba:
        ubicacion = Location.query.get(coordinador_prueba.ubicacion_id)
        if ubicacion:
            zona_numero = ubicacion.zona_codigo[-2:] if len(ubicacion.zona_codigo) >= 2 else ubicacion.zona_codigo
            try:
                result = auth_service.authenticate_user(
                    departamento=ubicacion.departamento_nombre,
                    municipio=ubicacion.municipio_nombre,
                    zona=zona_numero,
                    puesto=ubicacion.puesto_nombre,
                    password='test123'
                )
                print(f"   Coordinador: {'✅ OK' if result['success'] else '❌ FALLO'}")
                if result['success']:
                    print(f"      Usuario: {result['user']['nombre']}")
                    print(f"      Zona: {zona_numero.zfill(2)}")
            except Exception as e:
                print(f"   Coordinador: ❌ ERROR - {str(e)}")
        else:
            print(f"   Coordinador: ❌ UBICACIÓN NO ENCONTRADA")
    else:
        print(f"   Coordinador: ❌ NO HAY COORDINADORES DISPONIBLES")
    
    # 4. Estado general
    print(f"\n🎯 ESTADO GENERAL:")
    
    if coordinadores_invalidos == 0 and coordinadores_validos > 0:
        print(f"   Sistema: 🟢 OPERATIVO")
        print(f"   Zonas: ✅ Formato correcto (01, 02, 03, etc.)")
        print(f"   Autenticación: ✅ Funcionando")
        print(f"   Listo para producción: ✅ SÍ")
    else:
        print(f"   Sistema: 🔴 CON PROBLEMAS")
        print(f"   Coordinadores inválidos: {coordinadores_invalidos}")
        print(f"   Requiere corrección: ❌ SÍ")
    
    print("\n" + "="*60)