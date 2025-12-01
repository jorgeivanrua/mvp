"""Test del endpoint de municipios"""
import requests

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("TEST DE ENDPOINT DE MUNICIPIOS")
print("=" * 60)

# Test 1: Obtener departamentos
print("\n1. Obteniendo departamentos...")
try:
    response = requests.get(f"{BASE_URL}/api/locations/departamentos", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Obtener municipios del Caquetá
print("\n2. Obteniendo municipios del Caquetá (código 44)...")
try:
    response = requests.get(f"{BASE_URL}/api/locations/municipios/44", timeout=5)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"Municipios encontrados: {len(data.get('data', []))}")
        if data.get('data'):
            print("Primeros 3 municipios:")
            for muni in data['data'][:3]:
                print(f"  - {muni['municipio_codigo']}: {muni['municipio_nombre']}")
    else:
        print(f"Error: {data.get('error')}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
