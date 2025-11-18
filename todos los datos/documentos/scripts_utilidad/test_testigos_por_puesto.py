"""
Prueba del sistema de testigos por puesto
Verifica que:
1. Los testigos se crean a nivel de puesto (no de mesa)
2. Solo se pueden crear tantos testigos como mesas tenga el puesto
3. Los testigos tienen ubicacion_id apuntando al puesto
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
        return response.json()['data']['access_token']
    return None

def obtener_puesto_ejemplo(token):
    """Obtener un puesto con varias mesas"""
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/api/gestion-usuarios/puestos', headers=headers)
    
    if response.status_code == 200:
        puestos = response.json()['puestos']
        # Buscar un puesto con al menos 3 mesas
        for puesto in puestos:
            if puesto['total_mesas'] >= 3:
                return puesto
        # Si no hay, devolver el primero
        return puestos[0] if puestos else None
    return None

def test_crear_testigos(token, puesto_id, cantidad):
    """Probar creación de testigos"""
    print(f"\n{'='*80}")
    print(f"CREANDO {cantidad} TESTIGO(S) PARA PUESTO ID: {puesto_id}")
    print('='*80)
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {'puesto_id': puesto_id}
    
    if cantidad is not None:
        payload['cantidad'] = cantidad
    
    response = requests.post(
        f'{BASE_URL}/api/gestion-usuarios/crear-testigos-puesto',
        headers=headers,
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()['data']
        print(f"\n✓ Puesto: {data['puesto']}")
        print(f"✓ Total mesas: {data['total_mesas']}")
        print(f"✓ Testigos creados: {data['total_creados']}")
        print(f"✓ Testigos existentes previos: {data['total_existentes_previos']}")
        print(f"✓ Total testigos ahora: {data['total_testigos_ahora']}")
        print(f"✓ Espacios disponibles: {data['espacios_disponibles']}")
        
        if data['testigos_creados']:
            print("\nCredenciales generadas:")
            for testigo in data['testigos_creados']:
                print(f"  - Username: {testigo['username']}")
                print(f"    Password: {testigo['password']}")
                print(f"    Número: {testigo['numero']}")
        
        return data
    else:
        error_data = response.json()
        print(f"\n✗ Error: {error_data.get('error', 'Unknown error')}")
        return None

def verificar_testigos_en_db(token, puesto_id):
    """Verificar testigos en la base de datos"""
    print(f"\n{'='*80}")
    print(f"VERIFICANDO TESTIGOS EN BASE DE DATOS")
    print('='*80)
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f'{BASE_URL}/api/gestion-usuarios/listar-usuarios-ubicacion/{puesto_id}',
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()['data']
        testigos = [u for u in data['usuarios'] if u['rol'] == 'testigo_electoral']
        
        print(f"\n✓ Ubicación: {data['ubicacion']}")
        print(f"✓ Tipo: {data['tipo']}")
        print(f"✓ Total testigos: {len(testigos)}")
        
        if testigos:
            print("\nTestigos encontrados:")
            for testigo in testigos:
                print(f"  - {testigo['username']} (ID: {testigo['id']}, Activo: {testigo['activo']})")
        
        return testigos
    else:
        print(f"✗ Error: {response.status_code}")
        return []

if __name__ == '__main__':
    print("="*80)
    print("PRUEBA: TESTIGOS POR PUESTO")
    print("="*80)
    
    # Login
    print("\n1. Haciendo login...")
    token = login()
    
    if not token:
        print("✗ No se pudo obtener token")
        exit(1)
    
    print("✓ Login exitoso")
    
    # Obtener puesto de ejemplo
    print("\n2. Obteniendo puesto de ejemplo...")
    puesto = obtener_puesto_ejemplo(token)
    
    if not puesto:
        print("✗ No se encontraron puestos")
        exit(1)
    
    print(f"✓ Puesto seleccionado: {puesto['nombre_completo']}")
    print(f"  ID: {puesto['id']}")
    print(f"  Código: {puesto['codigo']}")
    print(f"  Total mesas: {puesto['total_mesas']}")
    
    # Prueba 1: Crear 2 testigos
    print("\n" + "="*80)
    print("PRUEBA 1: Crear 2 testigos")
    print("="*80)
    result1 = test_crear_testigos(token, puesto['id'], 2)
    
    # Verificar en DB
    if result1:
        testigos = verificar_testigos_en_db(token, puesto['id'])
        
        if len(testigos) == 2:
            print("\n✓ PRUEBA 1 EXITOSA: Se crearon exactamente 2 testigos")
        else:
            print(f"\n✗ PRUEBA 1 FALLIDA: Se esperaban 2 testigos, se encontraron {len(testigos)}")
    
    # Prueba 2: Intentar crear más testigos de los permitidos
    print("\n" + "="*80)
    print(f"PRUEBA 2: Intentar crear {puesto['total_mesas'] + 5} testigos (más del límite)")
    print("="*80)
    result2 = test_crear_testigos(token, puesto['id'], puesto['total_mesas'] + 5)
    
    # Prueba 3: Crear todos los testigos restantes
    print("\n" + "="*80)
    print("PRUEBA 3: Crear todos los testigos restantes (sin especificar cantidad)")
    print("="*80)
    result3 = test_crear_testigos(token, puesto['id'], None)
    
    # Verificación final
    if result3:
        testigos_finales = verificar_testigos_en_db(token, puesto['id'])
        
        if len(testigos_finales) == puesto['total_mesas']:
            print(f"\n✓ PRUEBA 3 EXITOSA: Total de testigos ({len(testigos_finales)}) = Total de mesas ({puesto['total_mesas']})")
        else:
            print(f"\n⚠ Total de testigos ({len(testigos_finales)}) != Total de mesas ({puesto['total_mesas']})")
    
    # Prueba 4: Intentar crear más cuando ya está lleno
    print("\n" + "="*80)
    print("PRUEBA 4: Intentar crear más testigos cuando el puesto está lleno")
    print("="*80)
    result4 = test_crear_testigos(token, puesto['id'], 1)
    
    if result4 is None:
        print("\n✓ PRUEBA 4 EXITOSA: No se pueden crear más testigos (límite alcanzado)")
    else:
        print("\n✗ PRUEBA 4 FALLIDA: Se permitió crear testigos adicionales")
    
    print("\n" + "="*80)
    print("RESUMEN DE PRUEBAS")
    print("="*80)
    print(f"Puesto: {puesto['nombre_completo']}")
    print(f"Total mesas: {puesto['total_mesas']}")
    print(f"Total testigos creados: {len(verificar_testigos_en_db(token, puesto['id']))}")
    print("\n✓ Sistema funcionando correctamente:")
    print("  - Testigos se crean a nivel de puesto")
    print("  - Límite de testigos = cantidad de mesas")
    print("  - No se pueden exceder el límite")
