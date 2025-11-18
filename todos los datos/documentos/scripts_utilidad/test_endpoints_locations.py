#!/usr/bin/env python3
"""Probar endpoints de locations"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app

def test_endpoints():
    app = create_app()
    
    with app.test_client() as client:
        print("=" * 80)
        print("PROBANDO ENDPOINTS DE LOCATIONS")
        print("=" * 80)
        
        # 1. Departamentos
        print("\n1. GET /api/locations/departamentos")
        print("-" * 80)
        response = client.get('/api/locations/departamentos')
        print(f"Status: {response.status_code}")
        data = response.get_json()
        print(f"Success: {data.get('success')}")
        print(f"Total: {len(data.get('data', []))}")
        if data.get('data'):
            print(f"Ejemplo: {data['data'][0]}")
        
        # 2. Municipios
        print("\n2. GET /api/locations/municipios?departamento_codigo=18")
        print("-" * 80)
        response = client.get('/api/locations/municipios?departamento_codigo=18')
        print(f"Status: {response.status_code}")
        data = response.get_json()
        print(f"Success: {data.get('success')}")
        print(f"Total: {len(data.get('data', []))}")
        if data.get('data'):
            print(f"Ejemplo: {data['data'][0]}")
        
        # 3. Zonas
        print("\n3. GET /api/locations/zonas?municipio_codigo=18001")
        print("-" * 80)
        response = client.get('/api/locations/zonas?municipio_codigo=18001')
        print(f"Status: {response.status_code}")
        data = response.get_json()
        print(f"Success: {data.get('success')}")
        print(f"Total: {len(data.get('data', []))}")
        if data.get('data'):
            print(f"Ejemplo: {data['data'][0]}")
        
        # 4. Puestos
        print("\n4. GET /api/locations/puestos?zona_codigo=01")
        print("-" * 80)
        response = client.get('/api/locations/puestos?zona_codigo=01')
        print(f"Status: {response.status_code}")
        data = response.get_json()
        print(f"Success: {data.get('success')}")
        print(f"Total: {len(data.get('data', []))}")
        if data.get('data'):
            print(f"Ejemplo: {data['data'][0]}")

if __name__ == '__main__':
    test_endpoints()
