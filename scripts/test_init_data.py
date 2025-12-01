"""
Script de prueba para verificar la inicialización de datos
"""
import requests
import json

# Configuración
BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
INIT_DATA_URL = f"{BASE_URL}/api/super-admin/init-test-data"

# Credenciales del super admin
USERNAME = "admin"
PASSWORD = "admin123"

def test_init_data():
    print("=" * 60)
    print("TEST: Inicialización de Datos Electorales")
    print("=" * 60)
    
    # 1. Login
    print("\n1. Iniciando sesión como Super Admin...")
    login_response = requests.post(LOGIN_URL, json={
        "nombre": USERNAME,
        "password": PASSWORD,
        "rol": "super_admin"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Error en login: {login_response.status_code}")
        print(login_response.text)
        return
    
    login_data = login_response.json()
    if not login_data.get('success'):
        print(f"❌ Login fallido: {login_data.get('error')}")
        return
    
    token = login_data['data']['access_token']
    print(f"✅ Login exitoso. Token obtenido.")
    
    # 2. Inicializar datos
    print("\n2. Inicializando datos electorales...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    init_response = requests.post(INIT_DATA_URL, headers=headers, json={})
    
    if init_response.status_code != 200:
        print(f"❌ Error en inicialización: {init_response.status_code}")
        print(init_response.text)
        return
    
    init_data = init_response.json()
    
    if not init_data.get('success'):
        print(f"❌ Inicialización fallida: {init_data.get('error')}")
        return
    
    print(f"✅ {init_data['message']}")
    
    # 3. Mostrar resultados
    print("\n3. Resultados detallados:")
    results = init_data['data']
    
    print(f"\n   Tipos de Elección:")
    print(f"   - Creados: {results['tipos_eleccion']['created']}")
    print(f"   - Ya existían: {results['tipos_eleccion']['existing']}")
    
    print(f"\n   Partidos:")
    print(f"   - Creados: {results['partidos']['created']}")
    print(f"   - Ya existían: {results['partidos']['existing']}")
    
    print(f"\n   Candidatos:")
    print(f"   - Creados: {results['candidatos']['created']}")
    print(f"   - Ya existían: {results['candidatos']['existing']}")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETADO EXITOSAMENTE")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_init_data()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
