"""
Verificación completa de todos los endpoints del sistema
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def print_header(title):
    print("\n" + "="*80)
    print(title)
    print("="*80)

def test_endpoint(method, endpoint, data=None, headers=None, description=""):
    """Probar un endpoint y mostrar resultado"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        
        status_icon = "✅" if response.status_code < 400 else "❌"
        print(f"\n{status_icon} {method} {endpoint}")
        if description:
            print(f"   Descripción: {description}")
        print(f"   Status: {response.status_code}")
        
        try:
            json_data = response.json()
            if 'data' in json_data:
                if isinstance(json_data['data'], list):
                    print(f"   Datos: {len(json_data['data'])} elementos")
                    if json_data['data']:
                        print(f"   Primer elemento: {json.dumps(json_data['data'][0], indent=2)[:200]}...")
                else:
                    print(f"   Datos: {type(json_data['data']).__name__}")
            elif 'success' in json_data:
                print(f"   Success: {json_data['success']}")
                if 'error' in json_data:
                    print(f"   Error: {json_data['error']}")
        except:
            print(f"   Response: {response.text[:200]}")
        
        return response.status_code < 400
    except Exception as e:
        print(f"❌ {method} {endpoint}")
        print(f"   Error: {str(e)}")
        return False

def main():
    print("="*80)
    print("VERIFICACIÓN COMPLETA DE ENDPOINTS DEL SISTEMA")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    
    results = {
        'passed': 0,
        'failed': 0
    }
    
    # ==========================================
    # 1. ENDPOINTS DE LOCATIONS (SIN AUTH)
    # ==========================================
    print_header("1. ENDPOINTS DE LOCATIONS (Públicos)")
    
    tests = [
        ('GET', '/api/locations/departamentos', None, None, 'Listar departamentos'),
        ('GET', '/api/locations/municipios', None, None, 'Listar todos los municipios'),
        ('GET', '/api/locations/municipios?departamento_codigo=44', None, None, 'Municipios de CAQUETA'),
        ('GET', '/api/locations/zonas', None, None, 'Listar todas las zonas'),
        ('GET', '/api/locations/zonas?municipio_codigo=01', None, None, 'Zonas de FLORENCIA'),
        ('GET', '/api/locations/puestos', None, None, 'Listar todos los puestos'),
        ('GET', '/api/locations/puestos?zona_codigo=01', None, None, 'Puestos de zona 01'),
        ('GET', '/api/locations/mesas', None, None, 'Listar todas las mesas'),
        ('GET', '/api/locations/mesas?puesto_codigo=01', None, None, 'Mesas del puesto 01'),
    ]
    
    for method, endpoint, data, headers, desc in tests:
        if test_endpoint(method, endpoint, data, headers, desc):
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # ==========================================
    # 2. LOGIN Y OBTENER TOKEN
    # ==========================================
    print_header("2. AUTENTICACIÓN")
    
    print("\nIntentando login como super_admin...")
    login_response = requests.post(f'{BASE_URL}/api/auth/login', json={
        'rol': 'super_admin',
        'password': 'admin123'
    })
    
    if login_response.status_code == 200:
        token = login_response.json()['data']['access_token']
        print("✅ Login exitoso")
        print(f"   Token obtenido: {token[:50]}...")
        results['passed'] += 1
    else:
        print(f"❌ Login fallido: {login_response.status_code}")
        print(f"   Response: {login_response.text}")
        token = None
        results['failed'] += 1
    
    # ==========================================
    # 3. ENDPOINTS DE GESTIÓN DE USUARIOS
    # ==========================================
    if token:
        print_header("3. ENDPOINTS DE GESTIÓN DE USUARIOS (Con Auth)")
        
        headers = {'Authorization': f'Bearer {token}'}
        
        tests = [
            ('GET', '/api/gestion-usuarios/departamentos', None, headers, 'Listar departamentos para gestión'),
            ('GET', '/api/gestion-usuarios/municipios', None, headers, 'Listar municipios para gestión'),
            ('GET', '/api/gestion-usuarios/puestos', None, headers, 'Listar puestos para gestión'),
        ]
        
        for method, endpoint, data, hdrs, desc in tests:
            if test_endpoint(method, endpoint, data, hdrs, desc):
                results['passed'] += 1
            else:
                results['failed'] += 1
    
    # ==========================================
    # 4. VERIFICAR PÁGINA DE LOGIN
    # ==========================================
    print_header("4. PÁGINAS WEB")
    
    pages = [
        ('/', 'Página principal'),
        ('/auth/login', 'Página de login'),
        ('/admin/gestion-usuarios', 'Gestión de usuarios'),
    ]
    
    for path, desc in pages:
        try:
            response = requests.get(f'{BASE_URL}{path}')
            status_icon = "✅" if response.status_code == 200 else "❌"
            print(f"\n{status_icon} GET {path}")
            print(f"   Descripción: {desc}")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                results['passed'] += 1
            else:
                results['failed'] += 1
        except Exception as e:
            print(f"❌ GET {path}")
            print(f"   Error: {str(e)}")
            results['failed'] += 1
    
    # ==========================================
    # 5. VERIFICAR ARCHIVOS ESTÁTICOS
    # ==========================================
    print_header("5. ARCHIVOS JAVASCRIPT")
    
    js_files = [
        '/static/js/api-client.js',
        '/static/js/utils.js',
        '/static/js/login-fixed.js',
        '/static/js/gestion-usuarios.js',
    ]
    
    for js_file in js_files:
        try:
            response = requests.get(f'{BASE_URL}{js_file}')
            status_icon = "✅" if response.status_code == 200 else "❌"
            print(f"\n{status_icon} {js_file}")
            print(f"   Status: {response.status_code}")
            print(f"   Size: {len(response.text)} bytes")
            
            if response.status_code == 200:
                results['passed'] += 1
            else:
                results['failed'] += 1
        except Exception as e:
            print(f"❌ {js_file}")
            print(f"   Error: {str(e)}")
            results['failed'] += 1
    
    # ==========================================
    # RESUMEN FINAL
    # ==========================================
    print_header("RESUMEN FINAL")
    
    total = results['passed'] + results['failed']
    percentage = (results['passed'] / total * 100) if total > 0 else 0
    
    print(f"\nTotal de pruebas: {total}")
    print(f"✅ Exitosas: {results['passed']}")
    print(f"❌ Fallidas: {results['failed']}")
    print(f"📊 Porcentaje de éxito: {percentage:.1f}%")
    
    if results['failed'] == 0:
        print("\n🎉 ¡TODOS LOS ENDPOINTS FUNCIONAN CORRECTAMENTE!")
    else:
        print(f"\n⚠️  Hay {results['failed']} endpoint(s) con problemas")
    
    print("\n" + "="*80)
    print("VERIFICACIÓN COMPLETADA")
    print("="*80)

if __name__ == '__main__':
    main()
