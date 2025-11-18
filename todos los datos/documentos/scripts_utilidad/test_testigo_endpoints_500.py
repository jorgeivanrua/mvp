#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test endpoints que dan error 500"""
import requests
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:5000"

# Login primero
login_data = {
    "rol": "testigo_electoral",
    "departamento_codigo": "44",
    "municipio_codigo": "01",
    "zona_codigo": "01",
    "puesto_codigo": "01",
    "password": "test123"
}

print("Haciendo login...")
response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=10)
token = response.json().get('data', {}).get('access_token')

if not token:
    print("Error en login")
    sys.exit(1)

print(f"Token obtenido\n")

# Probar endpoints con error 500
endpoints = [
    "/api/testigo/tipos-eleccion",
    "/api/testigo/partidos"
]

headers = {"Authorization": f"Bearer {token}"}

for endpoint in endpoints:
    print(f"\n{'='*60}")
    print(f"Probando: {endpoint}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Respuesta:")
        print(response.text[:500])
    except Exception as e:
        print(f"Error: {e}")
