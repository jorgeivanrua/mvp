#!/usr/bin/env python3
"""
Script para verificar los datos correctos del usuario para login
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.database import db

def verificar_usuario_login():
    app = create_app()
    
    with app.app_context():
        try:
            print("🔍 VERIFICANDO DATOS DE LOGIN DEL USUARIO")
            print("=" * 50)
            
            # Buscar el usuario coordinador
            coordinador = User.query.filter_by(nombre='COORD_PUESTO_TEST').first()
            if not coordinador:
                print("❌ Usuario coordinador NO encontrado")
                return
            
            print(f"✅ Usuario encontrado:")
            print(f"   ID: {coordinador.id}")
            print(f"   Nombre: {coordinador.nombre}")
            print(f"   Cédula: {coordinador.cedula}")
            print(f"   Rol: {coordinador.rol}")
            print(f"   Ubicación ID: {coordinador.ubicacion_id}")
            print(f"   Activo: {coordinador.activo}")
            
            # Obtener datos de ubicación
            puesto = Location.query.get(coordinador.ubicacion_id)
            if puesto:
                print(f"\n📍 Datos de ubicación:")
                print(f"   Puesto ID: {puesto.id}")
                print(f"   Nombre completo: {puesto.nombre_completo}")
                print(f"   Tipo: {puesto.tipo}")
                print(f"   Departamento código: {puesto.departamento_codigo}")
                print(f"   Municipio código: {puesto.municipio_codigo}")
                print(f"   Zona código: {puesto.zona_codigo}")
                print(f"   Puesto código: {puesto.puesto_codigo}")
                
                print(f"\n🔐 Datos para login:")
                print(f"   rol: 'coordinador_puesto'")
                print(f"   departamento_codigo: '{puesto.departamento_codigo}'")
                print(f"   municipio_codigo: '{puesto.municipio_codigo}'")
                if puesto.zona_codigo:
                    print(f"   zona_codigo: '{puesto.zona_codigo}'")
                print(f"   puesto_codigo: '{puesto.puesto_codigo}'")
                print(f"   password: 'test123'")
                
                # Generar JSON para prueba
                login_json = {
                    "rol": "coordinador_puesto",
                    "departamento_codigo": puesto.departamento_codigo,
                    "municipio_codigo": puesto.municipio_codigo,
                    "puesto_codigo": puesto.puesto_codigo,
                    "password": "test123"
                }
                
                if puesto.zona_codigo:
                    login_json["zona_codigo"] = puesto.zona_codigo
                
                print(f"\n📋 JSON para login:")
                import json
                print(json.dumps(login_json, indent=2))
                
            else:
                print("❌ Ubicación NO encontrada")
            
            # Verificar contraseña
            from werkzeug.security import check_password_hash
            password_correcta = check_password_hash(coordinador.password_hash, 'test123')
            print(f"\n🔑 Verificación de contraseña:")
            print(f"   Contraseña 'test123' es correcta: {'✅ SÍ' if password_correcta else '❌ NO'}")
            
            if not password_correcta:
                print("   Probando otras contraseñas comunes...")
                for pwd in ['password', '123456', 'admin', 'test', coordinador.cedula]:
                    if check_password_hash(coordinador.password_hash, pwd):
                        print(f"   ✅ Contraseña correcta encontrada: '{pwd}'")
                        break
                else:
                    print("   ❌ No se encontró la contraseña correcta")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    verificar_usuario_login()