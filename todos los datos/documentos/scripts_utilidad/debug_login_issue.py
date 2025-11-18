"""
Debug del problema de login
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("\n" + "="*70)
print("DEBUG: Problema de Login")
print("="*70)

# Test 1: Login Super Admin
print("\n1. Intentando login como Super Admin...")
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "rol": "super_admin",
        "password": "test123"
    }
)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 2: Login Coordinador Municipal
print("\n2. Intentando login como Coordinador Municipal...")
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "rol": "coordinador_municipal",
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "password": "test123"
    }
)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

print("\n" + "="*70)
