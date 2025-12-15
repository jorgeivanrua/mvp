#!/usr/bin/env python3
"""
Test directo de endpoints para verificar que funcionan
"""
import requests
import json

def test_endpoints_directo():
    """Test directo de endpoints"""
    base_url = "http://localhost:5000"
    
    # Login para obtener token válido
    login_data = {
        "rol": "coordinador_puesto",
        "departamento_codigo": "44",
        "municipio_codigo": "01", 
        "zona_codigo": "01",
        "puesto_codigo": "01",
        "password": "test123"
    }
    
    response = requests.post(f"{base_url}/api/auth/login", json=login_data)
    result = response.json()
    token = result['data']['access_token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    print("🧪 PROBANDO ENDPOINTS DIRECTAMENTE")
    print("=" * 50)
    
    # Test endpoints uno por uno
    endpoints = [
        "/api/coordinador-puesto/formularios",
        "/api/coordinador-puesto/consolidado", 
        "/api/coordinador-puesto/mesas-detalle",
        "/api/coordinador-puesto/testigos-puesto"
    ]
    
    for endpoint in endpoints:
        print(f"\n📡 Probando: {endpoint}")
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   ✅ Éxito: {len(data.get('data', []))} elementos")
                else:
                    print(f"   ❌ Error: {data.get('error', 'Desconocido')}")
            else:
                print(f"   ❌ HTTP Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print(f"\n🔍 VERIFICANDO URLs DUPLICADAS")
    print("=" * 50)
    
    # Verificar si hay problema con URLs duplicadas
    bad_urls = [
        "/api/api/coordinador-puesto/consolidado",
        "/api/api/coordinador-puesto/mesas-detalle", 
        "/api/api/coordinador-puesto/testigos-puesto"
    ]
    
    for bad_url in bad_urls:
        print(f"\n❌ Probando URL incorrecta: {bad_url}")
        try:
            response = requests.get(f"{base_url}{bad_url}", headers=headers)
            print(f"   Status: {response.status_code} (debería ser 404)")
        except Exception as e:
            print(f"   Exception: {e}")

if __name__ == "__main__":
    test_endpoints_directo()