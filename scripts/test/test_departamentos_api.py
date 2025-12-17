#!/usr/bin/env python3
"""
Script para probar los endpoints de departamentos
"""
import requests
import json
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

BASE_URL = 'http://localhost:5000'

def login_super_admin():
    """Login como super admin"""
    login_data = {
        'rol': 'super_admin',
        'password': 'admin123'
    }
    
    print(f"Intentando login con: {login_data}")
    response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return data.get('data', {}).get('access_token')
    
    # Intentar con el endpoint de testigos si el principal falla
    print("Intentando con endpoint alternativo...")
    response2 = requests.post(f'{BASE_URL}/api/testigos/login-cedula-simple', json={'cedula': 'super_admin'})
    print(f"Response2 status: {response2.status_code}")
    print(f"Response2 text: {response2.text}")
    
    return None

def test_departamentos_disponibles(token):
    """Probar endpoint de departamentos disponibles"""
    headers = {'Authorization': f'Bearer {token}'}
    
    print("\n=== PROBANDO DEPARTAMENTOS DISPONIBLES ===")
    response = requests.get(f'{BASE_URL}/api/super-admin/departamentos/disponibles', headers=headers)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        if data.get('success'):
            departamentos = data.get('data', [])
            print(f"Departamentos encontrados: {len(departamentos)}")
            for depto in departamentos[:3]:  # Mostrar solo los primeros 3
                print(f"  - {depto.get('departamento_codigo')}: {depto.get('departamento_nombre')} ({depto.get('total_municipios')} municipios)")
        else:
            print(f"Error: {data.get('error')}")
    else:
        print(f"Error HTTP: {response.text}")

def test_departamentos_estado(token):
    """Probar endpoint de estado de departamentos"""
    headers = {'Authorization': f'Bearer {token}'}
    
    print("\n=== PROBANDO ESTADO DE DEPARTAMENTOS ===")
    response = requests.get(f'{BASE_URL}/api/super-admin/departamentos/estado', headers=headers)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        if data.get('success'):
            configs = data.get('data', [])
            print(f"Departamentos configurados: {len(configs)}")
            for config in configs:
                print(f"  - {config.get('departamento_nombre')} ({config.get('departamento_codigo')})")
                print(f"    Habilitado: {config.get('habilitado')}")
                print(f"    Principal: {config.get('es_principal')}")
                print(f"    Municipios: {config.get('total_municipios')}")
                print(f"    Puestos: {config.get('total_puestos')}")
                print(f"    Mesas: {config.get('total_mesas')}")
                print(f"    Usuarios: {config.get('total_usuarios_creados')}")
        else:
            print(f"Error: {data.get('error')}")
    else:
        print(f"Error HTTP: {response.text}")

def main():
    print("🧪 PROBANDO ENDPOINTS DE DEPARTAMENTOS")
    
    # Login
    token = login_super_admin()
    if not token:
        print("❌ No se pudo obtener token de autenticación")
        return
    
    print("✅ Login exitoso")
    
    # Probar endpoints
    test_departamentos_disponibles(token)
    test_departamentos_estado(token)
    
    print("\n✅ Pruebas completadas")

if __name__ == '__main__':
    main()