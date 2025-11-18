"""
Script para diagnosticar todos los endpoints críticos
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_login():
    """Probar login y obtener token"""
    print("\n" + "="*60)
    print("1. PROBANDO LOGIN")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "rol": "testigo_electoral",
            "departamento_codigo": "44",
            "municipio_codigo": "01",
            "zona_codigo": "01",
            "puesto_codigo": "01",
            "password": "test123"
        }
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Login exitoso")
        return data['data']['access_token']
    else:
        print(f"❌ Login falló: {response.json()}")
        return None

def test_profile(token):
    """Probar endpoint de perfil"""
    print("\n" + "="*60)
    print("2. PROBANDO PERFIL")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Perfil cargado")
        print(f"   Usuario: {data['data']['user']['nombre']}")
        print(f"   Ubicación: {data['data']['ubicacion']['nombre_completo'] if data['data']['ubicacion'] else 'Sin ubicación'}")
        return data['data']['ubicacion']
    else:
        print(f"❌ Perfil falló: {response.json()}")
        return None

def test_mesas(token, ubicacion):
    """Probar endpoint de mesas"""
    print("\n" + "="*60)
    print("3. PROBANDO MESAS")
    print("="*60)
    
    if not ubicacion:
        print("❌ No hay ubicación")
        return
    
    params = {
        "departamento_codigo": ubicacion['departamento_codigo'],
        "municipio_codigo": ubicacion['municipio_codigo'],
        "zona_codigo": ubicacion['zona_codigo'],
        "puesto_codigo": ubicacion['puesto_codigo']
    }
    
    print(f"Parámetros: {params}")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/locations/mesas",
        params=params,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        mesas = data.get('data', [])
        print(f"✅ Mesas cargadas: {len(mesas)}")
        for mesa in mesas:
            print(f"   - Mesa {mesa['mesa_codigo']}: {mesa['mesa_nombre']}")
    else:
        print(f"❌ Mesas falló: {response.text}")

def test_tipos_eleccion(token):
    """Probar endpoint de tipos de elección"""
    print("\n" + "="*60)
    print("4. PROBANDO TIPOS DE ELECCIÓN")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/configuracion/tipos-eleccion",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        tipos = data.get('data', [])
        print(f"✅ Tipos cargados: {len(tipos)}")
    else:
        print(f"❌ Tipos falló: {response.text}")

def test_partidos(token):
    """Probar endpoint de partidos"""
    print("\n" + "="*60)
    print("5. PROBANDO PARTIDOS")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/configuracion/partidos",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        partidos = data.get('data', [])
        print(f"✅ Partidos cargados: {len(partidos)}")
    else:
        print(f"❌ Partidos falló: {response.text}")

def main():
    print("\n" + "="*60)
    print("DIAGNÓSTICO DE ENDPOINTS - TESTIGO ELECTORAL")
    print("="*60)
    
    # 1. Login
    token = test_login()
    if not token:
        print("\n❌ No se pudo obtener token. Abortando.")
        return
    
    # 2. Perfil
    ubicacion = test_profile(token)
    
    # 3. Mesas
    test_mesas(token, ubicacion)
    
    # 4. Tipos de elección
    test_tipos_eleccion(token)
    
    # 5. Partidos
    test_partidos(token)
    
    print("\n" + "="*60)
    print("DIAGNÓSTICO COMPLETADO")
    print("="*60)

if __name__ == '__main__':
    main()
