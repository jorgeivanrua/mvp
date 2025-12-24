#!/usr/bin/env python3
"""
Test rápido de los endpoints que estaban fallando
"""

import requests
import json

def test_endpoints():
    """Test de los endpoints problemáticos"""
    
    # Primero hacer login para obtener token
    login_data = {
        "rol": "coordinador_puesto",
        "departamento_codigo": "26",
        "municipio_codigo": "2601", 
        "zona_codigo": "260101",
        "puesto_codigo": "26010103",
        "password": "test123"
    }
    
    print("🔐 Haciendo login...")
    login_response = requests.post("http://localhost:5000/api/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login falló: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    token_data = login_response.json()
    if not token_data.get('success'):
        print(f"❌ Login falló: {token_data}")
        return
        
    token = token_data.get('access_token')
    print("✅ Login exitoso")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test endpoint de incidentes
    print("\n🔍 Probando endpoint de incidentes...")
    incidentes_response = requests.get("http://localhost:5000/api/coordinador-puesto/incidentes", headers=headers)
    print(f"Status: {incidentes_response.status_code}")
    
    if incidentes_response.status_code == 200:
        print("✅ Endpoint de incidentes funciona")
        data = incidentes_response.json()
        print(f"Incidentes encontrados: {len(data.get('data', []))}")
    else:
        print(f"❌ Endpoint de incidentes falló")
        print(f"Response: {incidentes_response.text}")
    
    # Test endpoint de delitos
    print("\n🔍 Probando endpoint de delitos...")
    delitos_response = requests.get("http://localhost:5000/api/coordinador-puesto/delitos", headers=headers)
    print(f"Status: {delitos_response.status_code}")
    
    if delitos_response.status_code == 200:
        print("✅ Endpoint de delitos funciona")
        data = delitos_response.json()
        print(f"Delitos encontrados: {len(data.get('data', []))}")
    else:
        print(f"❌ Endpoint de delitos falló")
        print(f"Response: {delitos_response.text}")

if __name__ == "__main__":
    test_endpoints()