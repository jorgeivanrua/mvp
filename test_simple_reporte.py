#!/usr/bin/env python3
"""
Test simple para verificar endpoint de reporte de participación
"""
import requests
import json

def test_simple():
    """Test simple del endpoint"""
    
    # Login
    print("🔐 Haciendo login...")
    login_response = requests.post("http://localhost:5000/api/auth/login", json={
        "cedula": "1000000001",
        "password": "test123"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Error en login: {login_response.status_code}")
        return
    
    token = login_response.json()['access_token']
    print("✅ Login exitoso")
    
    # Test reporte
    print("\n🧪 Probando reporte de participación...")
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    reporte_data = {
        "mesa_id": 5,
        "hora_reporte": "2025-12-27T15:30:00.000Z",
        "personas_votadas": 3,
        "observaciones": "Test simple"
    }
    
    response = requests.post("http://localhost:5000/api/reporte-participacion", 
                           json=reporte_data, headers=headers)
    
    print(f"📥 Status: {response.status_code}")
    
    try:
        result = response.json()
        print(f"📄 Respuesta: {json.dumps(result, indent=2)}")
    except:
        print(f"📄 Respuesta (texto): {response.text}")
    
    if response.status_code == 201:
        print("✅ ¡Reporte creado exitosamente!")
    else:
        print("❌ Error creando reporte")

if __name__ == "__main__":
    test_simple()