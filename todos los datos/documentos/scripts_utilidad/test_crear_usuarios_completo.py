"""
Script para probar la creación completa de usuarios
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
        return data['data']['access_token']
    return None

def test_crear_testigos_puesto(token, puesto_id):
    """Probar creación de testigos para un puesto"""
    print("\n" + "="*80)
    print(f"CREANDO TESTIGOS PARA PUESTO ID: {puesto_id}")
    print("="*80)
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    response = requests.post(
        f'{BASE_URL}/api/gestion-usuarios/crear-testigos-puesto',
        headers=headers,
        json={'puesto_id': puesto_id}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()['data']
        print(f"\n✓ Puesto: {data['puesto']}")
        print(f"✓ Testigos creados: {data['total_creados']}")
        print(f"✓ Testigos existentes: {data['total_existentes']}")
        
        if data['testigos_creados']:
            print("\nCredenciales generadas:")
            for testigo in data['testigos_creados']:
                print(f"\n  Mesa: {testigo['mesa']}")
                print(f"  Username: {testigo['username']}")
                print(f"  Password: {testigo['password']}")
                print(f"  Votantes: {testigo['votantes_registrados']}")
        
        return data
    else:
        print(f"✗ Error: {response.text}")
        return None

def test_crear_coordinador_puesto(token, puesto_id):
    """Probar creación de coordinador de puesto"""
    print("\n" + "="*80)
    print(f"CREANDO COORDINADOR PARA PUESTO ID: {puesto_id}")
    print("="*80)
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    response = requests.post(
        f'{BASE_URL}/api/gestion-usuarios/crear-coordinador-puesto',
        headers=headers,
        json={'puesto_id': puesto_id}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()['data']
        print(f"\n✓ Puesto: {data['puesto']}")
        print(f"✓ Username: {data['username']}")
        print(f"✓ Password: {data['password']}")
        print(f"✓ Rol: {data['rol']}")
        return data
    else:
        print(f"✗ Error: {response.text}")
        return None

def test_crear_usuarios_municipio(token, municipio_id):
    """Probar creación de usuarios municipales"""
    print("\n" + "="*80)
    print(f"CREANDO USUARIOS PARA MUNICIPIO ID: {municipio_id}")
    print("="*80)
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    response = requests.post(
        f'{BASE_URL}/api/gestion-usuarios/crear-usuarios-municipio',
        headers=headers,
        json={
            'municipio_id': municipio_id,
            'crear_coordinador': True,
            'crear_admin': True
        }
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()['data']
        print(f"\n✓ Municipio: {data['municipio']}")
        print(f"✓ Usuarios creados: {len(data['usuarios_creados'])}")
        
        for usuario in data['usuarios_creados']:
            print(f"\n  Rol: {usuario['rol']}")
            print(f"  Username: {usuario['username']}")
            print(f"  Password: {usuario['password']}")
        
        return data
    else:
        print(f"✗ Error: {response.text}")
        return None

def obtener_primer_puesto(token):
    """Obtener el primer puesto disponible"""
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/api/gestion-usuarios/puestos', headers=headers)
    
    if response.status_code == 200:
        puestos = response.json()['puestos']
        if puestos:
            return puestos[0]
    return None

def obtener_primer_municipio(token):
    """Obtener el primer municipio disponible"""
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/api/gestion-usuarios/municipios', headers=headers)
    
    if response.status_code == 200:
        municipios = response.json()['municipios']
        if municipios:
            return municipios[0]
    return None

if __name__ == '__main__':
    print("="*80)
    print("PRUEBA COMPLETA DE CREACIÓN DE USUARIOS")
    print("="*80)
    
    # Login
    print("\n1. Haciendo login...")
    token = login()
    
    if not token:
        print("✗ No se pudo obtener token. Abortando pruebas.")
        exit(1)
    
    print("✓ Login exitoso")
    
    # Obtener primer puesto
    print("\n2. Obteniendo primer puesto...")
    puesto = obtener_primer_puesto(token)
    
    if not puesto:
        print("✗ No se encontraron puestos")
        exit(1)
    
    print(f"✓ Puesto seleccionado: {puesto['nombre_completo']}")
    print(f"  ID: {puesto['id']}, Mesas: {puesto['total_mesas']}")
    
    # Crear testigos para el puesto
    testigos_data = test_crear_testigos_puesto(token, puesto['id'])
    
    # Crear coordinador para el puesto
    coordinador_data = test_crear_coordinador_puesto(token, puesto['id'])
    
    # Obtener primer municipio
    print("\n3. Obteniendo primer municipio...")
    municipio = obtener_primer_municipio(token)
    
    if municipio:
        print(f"✓ Municipio seleccionado: {municipio['nombre_completo']}")
        print(f"  ID: {municipio['id']}, Puestos: {municipio['total_puestos']}")
        
        # Crear usuarios municipales
        municipio_data = test_crear_usuarios_municipio(token, municipio['id'])
    
    print("\n" + "="*80)
    print("PRUEBA COMPLETADA")
    print("="*80)
    print("\nRESUMEN:")
    if testigos_data:
        print(f"  - Testigos creados: {testigos_data['total_creados']}")
    if coordinador_data:
        print(f"  - Coordinador de puesto: 1")
    if municipio_data:
        print(f"  - Usuarios municipales: {len(municipio_data['usuarios_creados'])}")
