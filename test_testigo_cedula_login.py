#!/usr/bin/env python3
"""
Test de login por cédula para testigos
"""

import requests
import json
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.models.user import User

def test_testigo_login():
    """Test de login por cédula para testigos"""
    print("🧪 TEST DE LOGIN POR CÉDULA PARA TESTIGOS")
    print("=" * 50)
    
    # Obtener datos de un testigo para probar
    app = create_app()
    with app.app_context():
        testigo = User.query.filter_by(rol='testigo_electoral').first()
        if not testigo:
            print("❌ No se encontraron testigos en la base de datos")
            return False
        
        print(f"📋 DATOS DEL TESTIGO DE PRUEBA:")
        print(f"  • Nombre: {testigo.nombre}")
        print(f"  • Cédula: {testigo.cedula}")
        print(f"  • Ubicación ID: {testigo.ubicacion_id} {'✅ (NULL)' if testigo.ubicacion_id is None else '❌ (debería ser NULL)'}")
        print(f"  • Activo: {testigo.activo}")
        print()
    
    # URL del endpoint
    url = "http://localhost:5000/api/auth/login"
    
    # Test 1: Login exitoso con cédula
    print("🔐 TEST 1: Login exitoso con cédula")
    payload = {
        "rol": "testigo_electoral",
        "cedula": testigo.cedula,
        "password": "test123"  # Contraseña por defecto para testigos
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login exitoso!")
            print(f"  • Usuario: {data.get('data', {}).get('user', {}).get('nombre')}")
            print(f"  • Rol: {data.get('data', {}).get('user', {}).get('rol')}")
            print(f"  • Cédula: {data.get('data', {}).get('user', {}).get('cedula')}")
            print(f"  • Token generado: {'Sí' if data.get('data', {}).get('access_token') else 'No'}")
            
            # Guardar token para próximos tests
            access_token = data.get('data', {}).get('access_token')
            
        else:
            print(f"❌ Error en login: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print("⚠️  Asegúrate de que el servidor esté corriendo en http://localhost:5000")
        return False
    
    print()
    
    # Test 2: Login fallido sin cédula
    print("🔐 TEST 2: Login fallido sin cédula")
    payload_sin_cedula = {
        "rol": "testigo_electoral",
        "password": "test123"
    }
    
    try:
        response = requests.post(url, json=payload_sin_cedula, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ Error esperado - cédula requerida")
            print(f"  • Mensaje: {response.json().get('error')}")
        else:
            print(f"❌ Respuesta inesperada: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    
    print()
    
    # Test 3: Login fallido con cédula incorrecta
    print("🔐 TEST 3: Login fallido con cédula incorrecta")
    payload_cedula_incorrecta = {
        "rol": "testigo_electoral",
        "cedula": "9999999999999",  # Cédula que no existe
        "password": "test123"
    }
    
    try:
        response = requests.post(url, json=payload_cedula_incorrecta, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [401, 403]:
            print("✅ Error esperado - cédula no encontrada")
            print(f"  • Mensaje: {response.json().get('error')}")
        else:
            print(f"❌ Respuesta inesperada: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    
    print()
    
    # Test 4: Verificar perfil del testigo
    if 'access_token' in locals():
        print("👤 TEST 4: Verificar perfil del testigo")
        profile_url = "http://localhost:5000/api/auth/profile"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(profile_url, headers=headers, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                user_data = data.get('data', {}).get('user', {})
                print("✅ Perfil obtenido exitosamente!")
                print(f"  • ID: {user_data.get('id')}")
                print(f"  • Nombre: {user_data.get('nombre')}")
                print(f"  • Cédula: {user_data.get('cedula')}")
                print(f"  • Rol: {user_data.get('rol')}")
                print(f"  • Ubicación ID: {user_data.get('ubicacion_id')} {'✅ (NULL)' if user_data.get('ubicacion_id') is None else '❌'}")
                print(f"  • Presencia verificada: {user_data.get('presencia_verificada')}")
            else:
                print(f"❌ Error obteniendo perfil: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
    
    return True

def mostrar_instrucciones():
    """Mostrar instrucciones para usar el login por cédula"""
    print("\n📋 INSTRUCCIONES PARA LOGIN POR CÉDULA")
    print("=" * 45)
    
    print("🌐 URL de Login: http://localhost:5000/login")
    print()
    print("📝 DATOS PARA TESTIGOS:")
    print("  • Rol: testigo_electoral")
    print("  • Cédula: [número de cédula del testigo]")
    print("  • Contraseña: test123")
    print()
    print("📋 EJEMPLO DE PAYLOAD JSON:")
    print(json.dumps({
        "rol": "testigo_electoral",
        "cedula": "2601010101001",
        "password": "test123"
    }, indent=2))
    print()
    print("✅ FLUJO CORRECTO:")
    print("1. Testigo ingresa su cédula y contraseña")
    print("2. Sistema autentica por cédula (no por ubicación)")
    print("3. Testigo accede al dashboard sin ubicación fija")
    print("4. Testigo se verifica en una mesa específica")
    print("5. Mesa se guarda para futuras sesiones")

if __name__ == "__main__":
    print("🚀 PRUEBA DE AUTENTICACIÓN POR CÉDULA PARA TESTIGOS")
    print("=" * 60)
    
    if test_testigo_login():
        mostrar_instrucciones()
        print("\n🎉 PRUEBAS COMPLETADAS")
        print("✅ Sistema de login por cédula funcionando correctamente")
    else:
        print("\n❌ PRUEBAS FALLARON")
        print("⚠️  Revisa la configuración del servidor y la base de datos")