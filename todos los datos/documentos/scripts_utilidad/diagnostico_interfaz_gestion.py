"""
Diagnóstico de la interfaz de gestión de usuarios
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def test_pagina_html():
    """Verificar que la página HTML carga"""
    print("\n" + "="*80)
    print("1. VERIFICANDO PÁGINA HTML")
    print("="*80)
    
    try:
        response = requests.get(f'{BASE_URL}/admin/gestion-usuarios')
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Página HTML carga correctamente")
            
            # Verificar que contiene los elementos necesarios
            html = response.text
            elementos = [
                'selectPuestoTestigos',
                'selectPuestoCoordinador',
                'selectMunicipio',
                'selectDepartamento',
                'gestion-usuarios.js'
            ]
            
            for elemento in elementos:
                if elemento in html:
                    print(f"  ✓ Contiene: {elemento}")
                else:
                    print(f"  ✗ Falta: {elemento}")
        else:
            print(f"✗ Error: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error: {e}")

def test_endpoints_sin_auth():
    """Verificar respuesta de endpoints sin autenticación"""
    print("\n" + "="*80)
    print("2. VERIFICANDO ENDPOINTS SIN AUTENTICACIÓN")
    print("="*80)
    
    endpoints = [
        '/api/gestion-usuarios/puestos',
        '/api/gestion-usuarios/municipios',
        '/api/gestion-usuarios/departamentos'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f'{BASE_URL}{endpoint}')
            print(f"\n{endpoint}")
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 401:
                print("  ✓ Requiere autenticación (correcto)")
            elif response.status_code == 200:
                print("  ⚠ No requiere autenticación (revisar)")
            else:
                print(f"  ✗ Error inesperado")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")

def test_endpoints_con_auth():
    """Verificar endpoints con autenticación"""
    print("\n" + "="*80)
    print("3. VERIFICANDO ENDPOINTS CON AUTENTICACIÓN")
    print("="*80)
    
    # Login
    print("\nHaciendo login...")
    login_response = requests.post(f'{BASE_URL}/api/auth/login', json={
        'rol': 'super_admin',
        'password': 'admin123'
    })
    
    if login_response.status_code != 200:
        print("✗ Error en login")
        return
    
    token = login_response.json()['data']['access_token']
    print("✓ Login exitoso")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    endpoints = [
        '/api/gestion-usuarios/puestos',
        '/api/gestion-usuarios/municipios',
        '/api/gestion-usuarios/departamentos'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f'{BASE_URL}{endpoint}', headers=headers)
            print(f"\n{endpoint}")
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Determinar la clave de datos
                if 'puestos' in data:
                    count = len(data['puestos'])
                    key = 'puestos'
                elif 'municipios' in data:
                    count = len(data['municipios'])
                    key = 'municipios'
                elif 'departamentos' in data:
                    count = len(data['departamentos'])
                    key = 'departamentos'
                else:
                    count = 0
                    key = 'unknown'
                
                print(f"  ✓ Respuesta exitosa")
                print(f"  ✓ Total {key}: {count}")
                
                if count > 0:
                    print(f"  ✓ Primer elemento: {data[key][0].get('nombre_completo', 'N/A')}")
            else:
                print(f"  ✗ Error: {response.status_code}")
                print(f"  {response.text}")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")

def test_javascript():
    """Verificar que el archivo JavaScript existe"""
    print("\n" + "="*80)
    print("4. VERIFICANDO ARCHIVO JAVASCRIPT")
    print("="*80)
    
    try:
        response = requests.get(f'{BASE_URL}/static/js/gestion-usuarios.js')
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Archivo JavaScript existe")
            
            js_content = response.text
            
            # Verificar funciones clave
            funciones = [
                'cargarUbicaciones',
                'populateSelects',
                'crearTestigosPuesto',
                'crearCoordinadorPuesto',
                'crearUsuariosMunicipio'
            ]
            
            for funcion in funciones:
                if funcion in js_content:
                    print(f"  ✓ Contiene función: {funcion}")
                else:
                    print(f"  ✗ Falta función: {funcion}")
        else:
            print(f"✗ Error: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error: {e}")

def test_cors():
    """Verificar configuración CORS"""
    print("\n" + "="*80)
    print("5. VERIFICANDO CORS")
    print("="*80)
    
    try:
        response = requests.options(f'{BASE_URL}/api/gestion-usuarios/puestos')
        print(f"Status: {response.status_code}")
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        
        print("\nCORS Headers:")
        for header, value in cors_headers.items():
            if value:
                print(f"  ✓ {header}: {value}")
            else:
                print(f"  ⚠ {header}: No configurado")
                
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == '__main__':
    print("="*80)
    print("DIAGNÓSTICO DE INTERFAZ DE GESTIÓN DE USUARIOS")
    print("="*80)
    
    test_pagina_html()
    test_endpoints_sin_auth()
    test_endpoints_con_auth()
    test_javascript()
    test_cors()
    
    print("\n" + "="*80)
    print("DIAGNÓSTICO COMPLETADO")
    print("="*80)
    print("\nPara acceder a la interfaz:")
    print("1. Ir a: http://127.0.0.1:5000/auth/login")
    print("2. Login con: rol=super_admin, password=admin123")
    print("3. Navegar a: http://127.0.0.1:5000/admin/gestion-usuarios")
