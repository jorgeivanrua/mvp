"""
Script para probar los endpoints de gestión de usuarios
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def login():
    """Login como super_admin"""
    response = requests.post(f'{BASE_URL}/api/auth/login', json={
        'rol': 'super_admin',
        'password': 'admin123'
    })
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'access_token' in data['data']:
            return data['data']['access_token']
        return data.get('access_token') or data.get('token')
    else:
        print(f"Error en login: {response.status_code}")
        print(response.text)
        return None

def test_listar_puestos(token):
    """Probar endpoint de listar puestos"""
    print("\n" + "="*80)
    print("PROBANDO: GET /api/gestion-usuarios/puestos")
    print("="*80)
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/api/gestion-usuarios/puestos', headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Total puestos: {len(data['puestos'])}")
        
        if data['puestos']:
            print("\nPrimeros 3 puestos:")
            for puesto in data['puestos'][:3]:
                print(f"  - {puesto['nombre_completo']}")
                print(f"    ID: {puesto['id']}, Mesas: {puesto['total_mesas']}")
    else:
        print(f"✗ Error: {response.text}")

def test_listar_municipios(token):
    """Probar endpoint de listar municipios"""
    print("\n" + "="*80)
    print("PROBANDO: GET /api/gestion-usuarios/municipios")
    print("="*80)
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/api/gestion-usuarios/municipios', headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Total municipios: {len(data['municipios'])}")
        
        if data['municipios']:
            print("\nPrimeros 3 municipios:")
            for municipio in data['municipios'][:3]:
                print(f"  - {municipio['nombre_completo']}")
                print(f"    ID: {municipio['id']}, Puestos: {municipio['total_puestos']}")
    else:
        print(f"✗ Error: {response.text}")

def test_listar_departamentos(token):
    """Probar endpoint de listar departamentos"""
    print("\n" + "="*80)
    print("PROBANDO: GET /api/gestion-usuarios/departamentos")
    print("="*80)
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/api/gestion-usuarios/departamentos', headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Total departamentos: {len(data['departamentos'])}")
        
        if data['departamentos']:
            for dept in data['departamentos']:
                print(f"  - {dept['nombre_completo']}")
                print(f"    ID: {dept['id']}, Municipios: {dept['total_municipios']}")
    else:
        print(f"✗ Error: {response.text}")

if __name__ == '__main__':
    print("="*80)
    print("PRUEBA DE ENDPOINTS DE GESTIÓN DE USUARIOS")
    print("="*80)
    
    # Login
    print("\n1. Haciendo login...")
    token = login()
    
    if not token:
        print("✗ No se pudo obtener token. Abortando pruebas.")
        exit(1)
    
    print("✓ Login exitoso")
    
    # Probar endpoints
    test_listar_departamentos(token)
    test_listar_municipios(token)
    test_listar_puestos(token)
    
    print("\n" + "="*80)
    print("PRUEBAS COMPLETADAS")
    print("="*80)
