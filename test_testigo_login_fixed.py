#!/usr/bin/env python3
"""
Test del login de testigo con el frontend corregido
"""

import requests
import json

def test_testigo_login():
    """Probar el login de testigo usando el endpoint correcto"""
    print("🔍 PROBANDO LOGIN DE TESTIGO CORREGIDO")
    print("=" * 45)
    
    base_url = "http://localhost:5000"
    
    # Datos de login de testigo
    login_data = {
        "rol": "testigo_electoral",
        "cedula": "1000000001",  # Cédula de 10 dígitos
        "password": "test123",
        "departamento_codigo": "26",
        "municipio_codigo": "2601",
        "zona_codigo": "260101",
        "puesto_codigo": "26010103"
    }
    
    print("📋 Datos de login:")
    print(f"   Cédula: {login_data['cedula']}")
    print(f"   Rol: {login_data['rol']}")
    print(f"   Puesto: {login_data['puesto_codigo']}")
    
    try:
        print(f"\n📡 Enviando request a: {base_url}/api/auth/login")
        
        response = requests.post(
            f"{base_url}/api/auth/login",
            headers={'Content-Type': 'application/json'},
            json=login_data,
            timeout=10
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login exitoso!")
            print(f"📋 Usuario: {data['data']['user']['nombre']}")
            print(f"📋 Rol: {data['data']['user']['rol']}")
            print(f"📋 Ubicación: {data['data']['user'].get('ubicacion_nombre', 'N/A')}")
            
            # Probar endpoint de mesas para este testigo
            token = data['data']['access_token']
            print(f"\n🗳️  Probando carga de mesas...")
            
            mesa_response = requests.get(
                f"{base_url}/api/locations/mesas/{login_data['puesto_codigo']}",
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            
            if mesa_response.status_code == 200:
                mesa_data = mesa_response.json()
                mesas = mesa_data.get('data', [])
                print(f"✅ Mesas cargadas: {len(mesas)}")
                if mesas:
                    print(f"📋 Ejemplo: Mesa {mesas[0]['mesa_codigo']} - {mesas[0]['mesa_nombre']}")
            else:
                print(f"❌ Error cargando mesas: {mesa_response.status_code}")
                print(f"📄 Respuesta: {mesa_response.text}")
                
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 TEST DE LOGIN DE TESTIGO CORREGIDO")
    print("=" * 50)
    
    test_testigo_login()
    
    print("\n🎯 CONCLUSIONES:")
    print("- Si el login funciona aquí, el problema está resuelto")
    print("- Si no funciona, revisar la configuración de testigos")
    print("- El frontend ahora usa el endpoint correcto /api/auth/login")

if __name__ == "__main__":
    main()