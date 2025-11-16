#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test específico para testigo electoral"""
import requests
import sys
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:5000"

print("="*60)
print("TEST LOGIN TESTIGO ELECTORAL")
print("="*60)

# Datos de login
login_data = {
    "rol": "testigo_electoral",
    "departamento_codigo": "44",
    "municipio_codigo": "01",
    "zona_codigo": "01",
    "puesto_codigo": "01",
    "password": "test123"
}

print(f"\nDatos enviados:")
print(json.dumps(login_data, indent=2))

try:
    print(f"\nEnviando request a {BASE_URL}/api/auth/login...")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=login_data,
        timeout=15
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"\nRespuesta:")
    
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if response.status_code == 200 and data.get('success'):
            print("\n✓ LOGIN EXITOSO")
            user = data.get('data', {}).get('user', {})
            print(f"  Usuario: {user.get('nombre')}")
            print(f"  ID: {user.get('id')}")
            print(f"  Rol: {user.get('rol')}")
            
            # Probar endpoint de testigo
            token = data.get('data', {}).get('access_token')
            if token:
                print(f"\n\nProbando endpoint /api/testigo/info...")
                headers = {"Authorization": f"Bearer {token}"}
                test_response = requests.get(
                    f"{BASE_URL}/api/testigo/info",
                    headers=headers,
                    timeout=10
                )
                print(f"Status: {test_response.status_code}")
                if test_response.status_code == 200:
                    print("✓ Endpoint funciona")
                else:
                    print(f"✗ Endpoint error: {test_response.text[:200]}")
        else:
            print("\n✗ LOGIN FALLIDO")
            print(f"  Error: {data.get('error', 'Desconocido')}")
    except:
        print(response.text)
        
except requests.exceptions.Timeout:
    print("\n✗ TIMEOUT (15 segundos)")
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")

print("\n" + "="*60)
