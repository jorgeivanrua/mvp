#!/usr/bin/env python3
"""
Script para probar el endpoint de reporte de participación
"""
import requests
import json
from datetime import datetime, timezone
import sys

def test_reporte_participacion():
    """Probar el endpoint de reporte de participación"""
    
    # Primero hacer login para obtener el token
    login_url = "http://localhost:5000/api/auth/login"
    login_data = {
        "cedula": "1000000001",
        "password": "test123"
    }
    
    print("🔐 Haciendo login...")
    login_response = requests.post(login_url, json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Error en login: {login_response.status_code}")
        print(f"Respuesta: {login_response.text}")
        return
    
    login_result = login_response.json()
    token = login_result['access_token']
    print(f"✅ Login exitoso, token obtenido")
    
    # Preparar datos del reporte
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Probar diferentes horas
    test_cases = [
        {
            "name": "Hora actual (3:21 PM)",
            "hora": "2025-12-27T15:21:00.000Z",
            "personas": 2
        },
        {
            "name": "Hora 3:00 PM",
            "hora": "2025-12-27T15:00:00.000Z", 
            "personas": 5
        },
        {
            "name": "Hora 8:00 PM (problemática)",
            "hora": "2025-12-27T20:00:00.000Z",
            "personas": 2
        }
    ]
    
    reporte_url = "http://localhost:5000/api/reporte-participacion"
    
    for test_case in test_cases:
        print(f"\n🧪 Probando: {test_case['name']}")
        
        reporte_data = {
            "mesa_id": 5,
            "hora_reporte": test_case["hora"],
            "personas_votadas": test_case["personas"],
            "observaciones": f"Prueba - {test_case['name']}"
        }
        
        print(f"📤 Enviando datos: {json.dumps(reporte_data, indent=2)}")
        
        response = requests.post(reporte_url, json=reporte_data, headers=headers)
        
        print(f"📥 Respuesta: {response.status_code}")
        
        try:
            result = response.json()
            print(f"📄 Contenido: {json.dumps(result, indent=2)}")
        except:
            print(f"📄 Contenido (texto): {response.text}")
        
        if response.status_code == 201:
            print("✅ Reporte creado exitosamente")
        else:
            print("❌ Error creando reporte")
        
        print("-" * 50)

if __name__ == "__main__":
    test_reporte_participacion()