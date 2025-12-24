#!/usr/bin/env python3
"""
Verificar y crear el partido 'testigos' si no existe
"""

import requests
import json

def verificar_y_crear_partido_testigos():
    """Verificar si existe el partido testigos y crearlo si no existe"""
    print("🔍 VERIFICANDO PARTIDO 'TESTIGOS'")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    
    # Login como super admin
    admin_creds = {
        "rol": "super_admin",
        "password": "admin123"
    }
    
    try:
        # Autenticarse
        response = requests.post(f"{base_url}/api/auth/login", json=admin_creds)
        if response.status_code != 200:
            print("❌ Error en login de super admin")
            return False
        
        data = response.json()
        if not data.get('success'):
            print("❌ Login fallido")
            return False
        
        token = data.get('access_token')
        headers = {"Authorization": f"Bearer {token}"}
        
        # Obtener partidos existentes
        response = requests.get(f"{base_url}/api/configuracion/partidos", headers=headers)
        if response.status_code == 200:
            partidos = response.json().get('data', [])
            print(f"📊 Partidos existentes: {len(partidos)}")
            
            # Buscar partido 'testigos'
            partido_testigos = None
            for partido in partidos:
                print(f"   • {partido.get('sigla')}: {partido.get('nombre')}")
                if partido.get('sigla', '').lower() == 'testigos' or partido.get('nombre', '').lower() == 'testigos':
                    partido_testigos = partido
                    break
            
            if partido_testigos:
                print(f"✅ Partido 'testigos' encontrado:")
                print(f"   • ID: {partido_testigos.get('id')}")
                print(f"   • Nombre: {partido_testigos.get('nombre')}")
                print(f"   • Sigla: {partido_testigos.get('sigla')}")
                print(f"   • Color: {partido_testigos.get('color')}")
                return True
            else:
                print("⚠️  Partido 'testigos' NO encontrado. Creando...")
                
                # Crear partido testigos
                nuevo_partido = {
                    "nombre": "Testigos Electorales",
                    "sigla": "TESTIGOS",
                    "color": "#28a745",  # Verde
                    "descripcion": "Partido especial para testigos electorales del sistema",
                    "orden": 999,  # Al final de la lista
                    "activo": True
                }
                
                response = requests.post(f"{base_url}/api/configuracion/partidos", 
                                       json=nuevo_partido, headers=headers)
                
                if response.status_code == 201:
                    result = response.json()
                    if result.get('success'):
                        partido_creado = result.get('data', {})
                        print(f"✅ Partido 'testigos' creado exitosamente:")
                        print(f"   • ID: {partido_creado.get('id')}")
                        print(f"   • Nombre: {partido_creado.get('nombre')}")
                        print(f"   • Sigla: {partido_creado.get('sigla')}")
                        return True
                    else:
                        print(f"❌ Error creando partido: {result.get('error')}")
                else:
                    print(f"❌ Error HTTP creando partido: {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"   Error: {error_data.get('error', 'Error desconocido')}")
                    except:
                        print(f"   Respuesta: {response.text}")
        else:
            print(f"❌ Error obteniendo partidos: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

def verificar_testigos_en_partido():
    """Verificar si hay testigos asignados al partido testigos"""
    print("\n👥 VERIFICANDO TESTIGOS EN PARTIDO")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    
    # Login como super admin
    admin_creds = {
        "rol": "super_admin", 
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=admin_creds)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            headers = {"Authorization": f"Bearer {token}"}
            
            # Obtener usuarios testigos
            response = requests.get(f"{base_url}/api/admin/users", headers=headers)
            if response.status_code == 200:
                users = response.json().get('data', [])
                testigos = [u for u in users if u.get('rol') == 'testigo_electoral']
                
                print(f"📊 Total usuarios: {len(users)}")
                print(f"🗳️  Testigos electorales: {len(testigos)}")
                
                if testigos:
                    print("   Testigos encontrados:")
                    for testigo in testigos[:5]:  # Mostrar primeros 5
                        print(f"   • {testigo.get('nombre')} (Cédula: {testigo.get('cedula')})")
                else:
                    print("⚠️  No hay testigos registrados en el sistema")
                    print("   Los testigos se deben crear desde el Super Admin")
            else:
                print(f"⚠️  No se pudieron obtener usuarios: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def mostrar_instrucciones():
    """Mostrar instrucciones para crear testigos"""
    print("\n📋 INSTRUCCIONES PARA CREAR TESTIGOS")
    print("=" * 45)
    print("1. Accede como Super Admin:")
    print("   • URL: http://localhost:5000/login")
    print("   • Rol: super_admin")
    print("   • Contraseña: admin123")
    print()
    print("2. Ve a la sección de gestión de usuarios")
    print()
    print("3. Crea testigos con:")
    print("   • Rol: testigo_electoral")
    print("   • Cédula: número de cédula del testigo")
    print("   • Contraseña: contraseña del testigo")
    print("   • Mesa asignada: mesa donde votará")
    print()
    print("4. Los testigos podrán acceder con:")
    print("   • URL: http://localhost:5000/login")
    print("   • Rol: testigo_electoral")
    print("   • Cédula: su número de cédula")
    print("   • Contraseña: la asignada")

if __name__ == "__main__":
    print("🔧 CONFIGURACIÓN DEL PARTIDO TESTIGOS")
    print("=" * 50)
    
    if verificar_y_crear_partido_testigos():
        verificar_testigos_en_partido()
        mostrar_instrucciones()
        print("\n✅ CONFIGURACIÓN COMPLETADA")
        print("El partido 'testigos' está listo para usar")
    else:
        print("\n❌ ERROR EN CONFIGURACIÓN")
        print("No se pudo configurar el partido testigos")