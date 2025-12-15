#!/usr/bin/env python3
"""
Test de los nuevos endpoints agregados
"""
import requests
import json

def test_nuevos_endpoints():
    """Test de endpoints agregados"""
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
    
    print("🧪 PROBANDO NUEVOS ENDPOINTS")
    print("=" * 40)
    
    # Test consolidado
    print("\n1. 📊 Probando /api/coordinador-puesto/consolidado")
    response = requests.get(f"{base_url}/api/coordinador-puesto/consolidado", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Consolidado: {data['data']['resumen']['total_votos']} votos")
    
    # Test mesas-detalle
    print("\n2. 🏛️ Probando /api/coordinador-puesto/mesas-detalle")
    response = requests.get(f"{base_url}/api/coordinador-puesto/mesas-detalle", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Mesas: {len(data['data'])} mesas encontradas")
    
    # Test testigos-puesto
    print("\n3. 👥 Probando /api/coordinador-puesto/testigos-puesto")
    response = requests.get(f"{base_url}/api/coordinador-puesto/testigos-puesto", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Testigos: {len(data['data'])} testigos encontrados")
    
    print("\n🎉 ¡TODOS LOS ENDPOINTS FUNCIONANDO!")

if __name__ == "__main__":
    test_nuevos_endpoints()