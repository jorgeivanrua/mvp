#!/usr/bin/env python3
"""
Test del profile endpoint después de corregir las ubicaciones de testigos
"""

import requests
import json

def test_profile_after_fix():
    """Probar el profile endpoint después de la corrección"""
    print("🔍 PROBANDO PROFILE DESPUÉS DE CORRECCIÓN")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Login de testigo
    login_data = {
        "rol": "testigo_electoral",
        "cedula": "1000000001",
        "password": "test123",
        "departamento_codigo": "26",
        "municipio_codigo": "2601",
        "zona_codigo": "260101",
        "puesto_codigo": "26010103"
    }
    
    try:
        # Login
        response = requests.post(f"{base_url}/api/auth/login", json=login_data, timeout=10)
        if response.status_code != 200:
            print(f"❌ Error en login: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        data = response.json()
        token = data['data']['access_token']
        print("✅ Login exitoso")
        
        # Profile
        profile_response = requests.get(
            f"{base_url}/api/auth/profile",
            headers={'Authorization': f'Bearer {token}'},
            timeout=10
        )
        
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            print("✅ Profile endpoint exitoso")
            
            user = profile_data['data']['user']
            ubicacion = profile_data['data']['ubicacion']
            contexto = profile_data['data']['contexto']
            
            print(f"\n📋 DATOS DEL USUARIO:")
            print(f"   Nombre: {user['nombre']}")
            print(f"   Cédula: {user['cedula']}")
            print(f"   Rol: {user['rol']}")
            print(f"   Ubicación ID: {user['ubicacion_id']}")
            print(f"   Presencia verificada: {user['presencia_verificada']}")
            
            print(f"\n📍 DATOS DE UBICACIÓN:")
            if ubicacion:
                print(f"   ID: {ubicacion['id']}")
                print(f"   Tipo: {ubicacion['tipo']}")
                print(f"   Nombre: {ubicacion.get('puesto_nombre', ubicacion.get('nombre_completo', 'N/A'))}")
                print(f"   Departamento: {ubicacion.get('departamento_nombre', 'N/A')}")
                print(f"   Municipio: {ubicacion.get('municipio_nombre', 'N/A')}")
                print(f"   Zona: {ubicacion.get('zona_codigo', 'N/A')}")
                print(f"   Puesto: {ubicacion.get('puesto_codigo', 'N/A')}")
            else:
                print("   ❌ Ubicación es NULL")
            
            print(f"\n🎯 CONTEXTO:")
            if contexto:
                print(f"   Contexto disponible: ✅")
                print(f"   Keys: {list(contexto.keys()) if isinstance(contexto, dict) else 'N/A'}")
            else:
                print("   ❌ Contexto es NULL")
                
            # Ahora probar carga de mesas
            if ubicacion and ubicacion.get('puesto_codigo'):
                print(f"\n🗳️  PROBANDO CARGA DE MESAS:")
                puesto_codigo = ubicacion['puesto_codigo']
                
                mesa_response = requests.get(
                    f"{base_url}/api/locations/mesas/{puesto_codigo}",
                    headers={'Authorization': f'Bearer {token}'},
                    timeout=10
                )
                
                if mesa_response.status_code == 200:
                    mesa_data = mesa_response.json()
                    mesas = mesa_data.get('data', [])
                    print(f"   ✅ Mesas encontradas: {len(mesas)}")
                    if mesas:
                        mesa = mesas[0]
                        print(f"   📋 Ejemplo: Mesa {mesa['mesa_codigo']} - {mesa['mesa_nombre']}")
                else:
                    print(f"   ❌ Error cargando mesas: {mesa_response.status_code}")
            else:
                print(f"\n❌ No se puede probar carga de mesas - sin puesto_codigo")
                
        else:
            print(f"❌ Error en profile: {profile_response.status_code}")
            print(f"Response: {profile_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal"""
    test_profile_after_fix()
    
    print(f"\n🎯 RESULTADO:")
    print("Si la ubicación ya no es NULL, el problema está resuelto")
    print("El testigo debería poder ver y seleccionar mesas ahora")

if __name__ == "__main__":
    main()