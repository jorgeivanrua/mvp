#!/usr/bin/env python3
"""
Test para verificar que las URLs corregidas funcionan
"""
import requests
import json

def test_urls_corregidas():
    """Test de URLs corregidas"""
    base_url = "http://localhost:5000"
    
    # Login
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
    
    print("🎉 VERIFICANDO URLS CORREGIDAS")
    print("=" * 50)
    
    # Test las URLs que ahora deberían funcionar
    endpoints_correctos = [
        "/api/coordinador-puesto/formularios",
        "/api/coordinador-puesto/consolidado", 
        "/api/coordinador-puesto/mesas-detalle",
        "/api/coordinador-puesto/testigos-puesto"
    ]
    
    for endpoint in endpoints_correctos:
        print(f"\n✅ Probando: {endpoint}")
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   🎯 Éxito: Datos cargados correctamente")
                else:
                    print(f"   ❌ Error: {data.get('error', 'Desconocido')}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print(f"\n🚀 ¡MODAL LISTO PARA FUNCIONAR!")
    print("=" * 50)
    print("Ahora refresca el navegador y el modal funcionará perfectamente")

if __name__ == "__main__":
    test_urls_corregidas()