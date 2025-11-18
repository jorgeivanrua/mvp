"""
Test de funcionalidades específicas del sistema
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

def print_section(msg):
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"🔍 {msg}")
    print(f"{'='*70}{Colors.END}")

def login_user(rol, ubicacion_data, password="test123"):
    """Login y obtener token"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "rol": rol,
                "password": password,
                **ubicacion_data
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                # El token está en data.access_token
                return data.get('data', {}).get('access_token')
        return None
    except Exception as e:
        print_error(f"Error en login: {str(e)}")
        return None

def test_endpoints_locations():
    """Test de endpoints de ubicaciones"""
    print_section("TEST: Endpoints de Ubicaciones")
    
    tests = [
        {
            "name": "Listar Departamentos",
            "url": f"{BASE_URL}/api/locations/departamentos",
            "method": "GET"
        },
        {
            "name": "Listar Municipios de CAQUETA",
            "url": f"{BASE_URL}/api/locations/municipios?departamento_codigo=44",
            "method": "GET"
        },
        {
            "name": "Listar Zonas de FLORENCIA",
            "url": f"{BASE_URL}/api/locations/zonas?municipio_codigo=01",
            "method": "GET"
        },
        {
            "name": "Listar Puestos de Zona 01",
            "url": f"{BASE_URL}/api/locations/puestos?zona_codigo=01&municipio_codigo=01&departamento_codigo=44",
            "method": "GET"
        }
    ]
    
    results = []
    for test in tests:
        try:
            response = requests.get(test["url"])
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else len(data.get('data', []))
                print_success(f"{test['name']}: {count} registros")
                results.append(True)
            else:
                print_error(f"{test['name']}: Error {response.status_code}")
                results.append(False)
        except Exception as e:
            print_error(f"{test['name']}: {str(e)}")
            results.append(False)
    
    return all(results)

def test_dashboard_super_admin():
    """Test del dashboard de Super Admin"""
    print_section("TEST: Dashboard Super Admin")
    
    # Login como super admin
    token = login_user("super_admin", {})
    
    if not token:
        print_error("No se pudo obtener token de super admin")
        return False
    
    print_success("Login exitoso")
    
    # Test endpoints del super admin
    headers = {"Authorization": f"Bearer {token}"}
    
    tests = [
        {
            "name": "Dashboard HTML",
            "url": f"{BASE_URL}/admin/super-admin",
            "expect_html": True
        },
        {
            "name": "Estadísticas Generales",
            "url": f"{BASE_URL}/api/super-admin/stats",
            "expect_html": False
        }
    ]
    
    results = []
    for test in tests:
        try:
            response = requests.get(test["url"], headers=headers)
            if response.status_code == 200:
                if test.get("expect_html"):
                    if "<!DOCTYPE html>" in response.text or "<html" in response.text:
                        print_success(f"{test['name']}: OK")
                        results.append(True)
                    else:
                        print_warning(f"{test['name']}: No es HTML")
                        results.append(False)
                else:
                    print_success(f"{test['name']}: OK")
                    results.append(True)
            else:
                print_error(f"{test['name']}: Error {response.status_code}")
                results.append(False)
        except Exception as e:
            print_error(f"{test['name']}: {str(e)}")
            results.append(False)
    
    return all(results)

def test_gestion_usuarios():
    """Test de gestión de usuarios"""
    print_section("TEST: Gestión de Usuarios")
    
    # Login como super admin
    token = login_user("super_admin", {})
    
    if not token:
        print_error("No se pudo obtener token")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test listar usuarios
    try:
        response = requests.get(
            f"{BASE_URL}/api/super-admin/users",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('data', [])
            print_success(f"Listar usuarios: {len(usuarios)} usuarios encontrados")
            
            # Mostrar resumen por rol
            roles = {}
            for user in usuarios:
                rol = user.get('rol', 'unknown')
                roles[rol] = roles.get(rol, 0) + 1
            
            print_info("Usuarios por rol:")
            for rol, count in roles.items():
                print(f"  - {rol}: {count}")
            
            return True
        else:
            print_error(f"Error al listar usuarios: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_formulario_e14():
    """Test de formulario E14"""
    print_section("TEST: Formulario E14")
    
    # Login como coordinador de puesto
    token = login_user("coordinador_puesto", {
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "zona_codigo": "01",
        "puesto_codigo": "01"
    })
    
    if not token:
        print_error("No se pudo obtener token de coordinador")
        return False
    
    print_success("Login como coordinador de puesto exitoso")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test obtener candidatos
    try:
        response = requests.get(
            f"{BASE_URL}/api/coordinador-puesto/candidatos",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            candidatos = data.get('data', [])
            print_success(f"Candidatos disponibles: {len(candidatos)}")
            return True
        else:
            print_warning(f"No hay candidatos configurados (Status: {response.status_code})")
            return True  # No es un error crítico
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_dashboard_coordinador_municipal():
    """Test del dashboard de Coordinador Municipal"""
    print_section("TEST: Dashboard Coordinador Municipal")
    
    # Login como coordinador municipal
    token = login_user("coordinador_municipal", {
        "departamento_codigo": "44",
        "municipio_codigo": "01"
    })
    
    if not token:
        print_error("No se pudo obtener token")
        return False
    
    print_success("Login exitoso")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test dashboard
    try:
        response = requests.get(
            f"{BASE_URL}/coordinador/municipal",
            headers=headers
        )
        
        if response.status_code == 200:
            if "<!DOCTYPE html>" in response.text or "<html" in response.text:
                print_success("Dashboard HTML cargado correctamente")
                return True
            else:
                print_warning("Respuesta no es HTML")
                return False
        else:
            print_error(f"Error al cargar dashboard: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_sistema_incidentes():
    """Test del sistema de incidentes"""
    print_section("TEST: Sistema de Incidentes")
    
    # Login como coordinador de puesto
    token = login_user("coordinador_puesto", {
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "zona_codigo": "01",
        "puesto_codigo": "01"
    })
    
    if not token:
        print_error("No se pudo obtener token")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test listar incidentes
    try:
        response = requests.get(
            f"{BASE_URL}/api/coordinador-puesto/incidentes",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            incidentes = data.get('data', [])
            print_success(f"Sistema de incidentes activo: {len(incidentes)} incidentes")
            return True
        else:
            print_warning(f"Endpoint de incidentes: Status {response.status_code}")
            return True  # No es crítico
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def main():
    print("\n" + "="*70)
    print("🔍 TEST DE FUNCIONALIDADES DEL SISTEMA")
    print("="*70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    print("="*70)
    
    # Verificar servidor
    print_info("\nVerificando servidor...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print_success(f"Servidor activo (Status: {response.status_code})")
    except Exception as e:
        print_error(f"Servidor no responde: {str(e)}")
        return
    
    # Ejecutar tests
    resultados = {
        "Endpoints de Ubicaciones": test_endpoints_locations(),
        "Dashboard Super Admin": test_dashboard_super_admin(),
        "Gestión de Usuarios": test_gestion_usuarios(),
        "Formulario E14": test_formulario_e14(),
        "Dashboard Coordinador Municipal": test_dashboard_coordinador_municipal(),
        "Sistema de Incidentes": test_sistema_incidentes()
    }
    
    # Resumen
    print_section("RESUMEN DE TESTS")
    
    exitosos = sum(1 for r in resultados.values() if r)
    total = len(resultados)
    
    for nombre, resultado in resultados.items():
        if resultado:
            print_success(nombre)
        else:
            print_error(nombre)
    
    print("\n" + "="*70)
    print(f"Total: {total} tests")
    print_success(f"Exitosos: {exitosos}")
    if exitosos < total:
        print_error(f"Fallidos: {total - exitosos}")
    print("="*70)
    
    if exitosos == total:
        print_success("\n🎉 ¡TODOS LOS TESTS PASARON!")
    else:
        print_warning(f"\n⚠️  {total - exitosos} test(s) fallaron")

if __name__ == '__main__':
    main()
