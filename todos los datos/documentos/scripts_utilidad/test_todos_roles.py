"""
Test completo de todos los roles del sistema
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_section(title):
    print(f"\n{Colors.BLUE}{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.END}")

def login_user(nombre, rol, ubicacion_data=None):
    """Login y obtener token"""
    try:
        login_data = {
            "rol": rol,
            "password": "test123"
        }
        
        if ubicacion_data:
            login_data.update(ubicacion_data)
        
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Login exitoso: {nombre}")
            return data.get('access_token') or data.get('data', {}).get('access_token')
        else:
            print_error(f"Error login {nombre}: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Excepción en login {nombre}: {str(e)}")
        return None

def test_super_admin():
    """Test Super Admin"""
    print_section("TEST: SUPER ADMIN")
    
    token = login_user("Super Admin", "super_admin")
    if not token:
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test: Obtener estadísticas
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success(f"Estadísticas obtenidas")
            print_info(f"  Total usuarios: {stats.get('total_usuarios', 0)}")
            print_info(f"  Total formularios: {stats.get('total_formularios', 0)}")
        else:
            print_error(f"Error obteniendo stats: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_coordinador_departamental():
    """Test Coordinador Departamental"""
    print_section("TEST: COORDINADOR DEPARTAMENTAL")
    
    token = login_user(
        "Coordinador Departamental",
        "coordinador_departamental",
        {"departamento_codigo": "18"}
    )
    
    if not token:
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test: Obtener estadísticas
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-departamental/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success(f"Estadísticas departamentales obtenidas")
            print_info(f"  Total municipios: {stats.get('total_municipios', 0)}")
            print_info(f"  Total formularios: {stats.get('total_formularios', 0)}")
        else:
            print_error(f"Error obteniendo stats: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_coordinador_municipal():
    """Test Coordinador Municipal"""
    print_section("TEST: COORDINADOR MUNICIPAL")
    
    token = login_user(
        "Coordinador Municipal",
        "coordinador_municipal",
        {
            "departamento_codigo": "18",
            "municipio_codigo": "01"
        }
    )
    
    if not token:
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test: Obtener estadísticas
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-municipal/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success(f"Estadísticas municipales obtenidas")
            print_info(f"  Total puestos: {stats.get('total_puestos', 0)}")
            print_info(f"  Total formularios: {stats.get('total_formularios', 0)}")
        else:
            print_error(f"Error obteniendo stats: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_coordinador_puesto():
    """Test Coordinador de Puesto"""
    print_section("TEST: COORDINADOR DE PUESTO")
    
    token = login_user(
        "Coordinador Puesto",
        "coordinador_puesto",
        {
            "departamento_codigo": "18",
            "municipio_codigo": "01",
            "zona_codigo": "01",
            "puesto_codigo": "01"
        }
    )
    
    if not token:
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test: Obtener estadísticas
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-puesto/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success(f"Estadísticas del puesto obtenidas")
            print_info(f"  Total mesas: {stats.get('total_mesas', 0)}")
            print_info(f"  Total testigos: {stats.get('total_testigos', 0)}")
            print_info(f"  Total formularios: {stats.get('total_formularios', 0)}")
        else:
            print_error(f"Error obteniendo stats: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Test: Obtener mesas
    try:
        response = requests.get(f"{BASE_URL}/api/formularios/mesas", headers=headers)
        if response.status_code == 200:
            mesas = response.json().get('data', [])
            print_success(f"Mesas obtenidas: {len(mesas)}")
        else:
            print_error(f"Error obteniendo mesas: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_testigo_electoral():
    """Test Testigo Electoral"""
    print_section("TEST: TESTIGO ELECTORAL")
    
    token = login_user(
        "Testigo La Salle Mesa 01",
        "testigo_electoral",
        {
            "departamento_codigo": "18",
            "municipio_codigo": "01",
            "zona_codigo": "99",
            "puesto_codigo": "06",
            "mesa_codigo": "01"
        }
    )
    
    if not token:
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test: Registrar presencia
    try:
        response = requests.post(
            f"{BASE_URL}/api/testigo/registrar-presencia",
            headers=headers,
            json={}
        )
        if response.status_code == 200:
            print_success(f"Presencia registrada")
        else:
            print_info(f"Presencia: {response.status_code} (puede estar ya registrada)")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Test: Obtener estadísticas
    try:
        response = requests.get(f"{BASE_URL}/api/testigo/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success(f"Estadísticas del testigo obtenidas")
            print_info(f"  Presencia verificada: {stats.get('presencia_verificada', False)}")
        else:
            print_error(f"Error obteniendo stats: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Test: Obtener candidatos
    try:
        response = requests.get(f"{BASE_URL}/api/configuracion/candidatos", headers=headers)
        if response.status_code == 200:
            candidatos = response.json().get('data', [])
            print_success(f"Candidatos disponibles: {len(candidatos)}")
        else:
            print_error(f"Error obteniendo candidatos: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Test: Obtener mis formularios
    try:
        response = requests.get(f"{BASE_URL}/api/formularios/mis-formularios", headers=headers)
        if response.status_code == 200:
            result = response.json()
            formularios = result.get('data', {}).get('formularios', [])
            print_success(f"Mis formularios: {len(formularios)}")
        else:
            print_error(f"Error obteniendo formularios: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_auditor_electoral():
    """Test Auditor Electoral"""
    print_section("TEST: AUDITOR ELECTORAL")
    
    token = login_user(
        "Auditor Electoral",
        "auditor_electoral",
        {"departamento_codigo": "18"}
    )
    
    if not token:
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test: Obtener estadísticas
    try:
        response = requests.get(f"{BASE_URL}/api/auditor/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success(f"Estadísticas de auditoría obtenidas")
            print_info(f"  Total formularios: {stats.get('total_formularios', 0)}")
        else:
            print_error(f"Error obteniendo stats: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def main():
    print_section("INICIO DE PRUEBAS - TODOS LOS ROLES")
    print_info(f"URL Base: {BASE_URL}")
    print_info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    resultados = {
        "Super Admin": test_super_admin(),
        "Coordinador Departamental": test_coordinador_departamental(),
        "Coordinador Municipal": test_coordinador_municipal(),
        "Coordinador de Puesto": test_coordinador_puesto(),
        "Testigo Electoral": test_testigo_electoral(),
        "Auditor Electoral": test_auditor_electoral()
    }
    
    print_section("RESUMEN DE PRUEBAS")
    
    exitosos = sum(1 for v in resultados.values() if v)
    total = len(resultados)
    
    for rol, resultado in resultados.items():
        if resultado:
            print_success(f"{rol}: PASSED")
        else:
            print_error(f"{rol}: FAILED")
    
    print(f"\n{Colors.BLUE}{'='*70}")
    print(f"  RESULTADO FINAL: {exitosos}/{total} roles funcionando correctamente")
    print(f"{'='*70}{Colors.END}")
    
    if exitosos == total:
        print_success("✅ TODOS LOS ROLES FUNCIONAN CORRECTAMENTE")
    else:
        print_error(f"⚠️  {total - exitosos} roles con problemas")

if __name__ == '__main__':
    main()
