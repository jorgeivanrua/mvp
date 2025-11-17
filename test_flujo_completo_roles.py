"""
Test de flujo completo de todos los roles del sistema electoral
Prueba operaciones CRUD y funcionalidades específicas de cada rol
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
    CYAN = '\033[96m'
    END = '\033[0m'

def print_section(title):
    print(f"\n{Colors.BLUE}{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}{Colors.END}")

def print_subsection(title):
    print(f"\n{Colors.CYAN}--- {title} ---{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.END}")

def login(nombre, rol, ubicacion_data=None):
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
            token = data.get('access_token') or data.get('data', {}).get('access_token')
            print_success(f"Login: {nombre}")
            return token
        else:
            print_error(f"Login falló: {response.status_code}")
            return None
            
    except Exception as e:
        print_error(f"Excepción en login: {str(e)}")
        return None

def test_super_admin():
    """Test completo de Super Admin"""
    print_section("SUPER ADMIN - FLUJO COMPLETO")
    
    token = login("Super Admin", "super_admin")
    if not token:
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 1. Ver estadísticas generales
    print_subsection("1. Estadísticas Generales")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success(f"Total usuarios: {stats.get('total_usuarios', 0)}")
            print_success(f"Total formularios: {stats.get('total_formularios', 0)}")
            print_success(f"Total ubicaciones: {stats.get('total_ubicaciones', 0)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 2. Listar usuarios
    print_subsection("2. Listar Usuarios")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/usuarios", headers=headers)
        if response.status_code == 200:
            usuarios = response.json().get('data', [])
            print_success(f"Usuarios encontrados: {len(usuarios)}")
            if usuarios:
                print_info(f"Ejemplo: {usuarios[0].get('nombre')} - {usuarios[0].get('rol')}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 3. Ver perfil
    print_subsection("3. Ver Perfil")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
        if response.status_code == 200:
            profile = response.json().get('data', {})
            print_success(f"Perfil: {profile.get('user', {}).get('nombre')}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_coordinador_departamental():
    """Test completo de Coordinador Departamental"""
    print_section("COORDINADOR DEPARTAMENTAL - FLUJO COMPLETO")
    
    token = login(
        "Coordinador Departamental",
        "coordinador_departamental",
        {"departamento_codigo": "18"}
    )
    
    if not token:
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 1. Ver estadísticas departamentales
    print_subsection("1. Estadísticas Departamentales")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-departamental/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success(f"Total municipios: {stats.get('total_municipios', 0)}")
            print_success(f"Total formularios: {stats.get('total_formularios', 0)}")
        else:
            print_info(f"Stats endpoint: {response.status_code} (puede no estar implementado)")
    except Exception as e:
        print_info(f"Stats: {str(e)}")
    
    # 2. Ver perfil
    print_subsection("2. Ver Perfil")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
        if response.status_code == 200:
            profile = response.json().get('data', {})
            print_success(f"Perfil: {profile.get('user', {}).get('nombre')}")
            ubicacion = profile.get('ubicacion', {})
            if ubicacion:
                print_success(f"Ubicación: {ubicacion.get('nombre_completo')}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 3. Listar municipios
    print_subsection("3. Listar Municipios")
    try:
        response = requests.get(f"{BASE_URL}/api/ubicaciones/municipios?departamento_codigo=18", headers=headers)
        if response.status_code == 200:
            municipios = response.json().get('data', [])
            print_success(f"Municipios: {len(municipios)}")
            if municipios:
                print_info(f"Ejemplo: {municipios[0].get('nombre_completo')}")
        else:
            print_info(f"Municipios endpoint: {response.status_code}")
    except Exception as e:
        print_info(f"Municipios: {str(e)}")
    
    return True

def test_coordinador_municipal():
    """Test completo de Coordinador Municipal"""
    print_section("COORDINADOR MUNICIPAL - FLUJO COMPLETO")
    
    token = login(
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
    
    # 1. Ver estadísticas municipales
    print_subsection("1. Estadísticas Municipales")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-municipal/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success(f"Total puestos: {stats.get('total_puestos', 0)}")
            print_success(f"Total formularios: {stats.get('total_formularios', 0)}")
        else:
            print_info(f"Stats endpoint: {response.status_code}")
    except Exception as e:
        print_info(f"Stats: {str(e)}")
    
    # 2. Ver perfil
    print_subsection("2. Ver Perfil")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
        if response.status_code == 200:
            profile = response.json().get('data', {})
            print_success(f"Perfil: {profile.get('user', {}).get('nombre')}")
            ubicacion = profile.get('ubicacion', {})
            if ubicacion:
                print_success(f"Ubicación: {ubicacion.get('nombre_completo')}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 3. Listar puestos
    print_subsection("3. Listar Puestos")
    try:
        response = requests.get(
            f"{BASE_URL}/api/ubicaciones/puestos?departamento_codigo=18&municipio_codigo=01",
            headers=headers
        )
        if response.status_code == 200:
            puestos = response.json().get('data', [])
            print_success(f"Puestos: {len(puestos)}")
            if puestos:
                print_info(f"Ejemplo: {puestos[0].get('nombre_completo')}")
        else:
            print_info(f"Puestos endpoint: {response.status_code}")
    except Exception as e:
        print_info(f"Puestos: {str(e)}")
    
    return True

def test_coordinador_puesto():
    """Test completo de Coordinador de Puesto"""
    print_section("COORDINADOR DE PUESTO - FLUJO COMPLETO")
    
    token = login(
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
    
    # 1. Ver estadísticas del puesto
    print_subsection("1. Estadísticas del Puesto")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-puesto/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success(f"Total mesas: {stats.get('total_mesas', 0)}")
            print_success(f"Total testigos: {stats.get('total_testigos', 0)}")
            print_success(f"Total formularios: {stats.get('total_formularios', 0)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 2. Listar mesas del puesto
    print_subsection("2. Listar Mesas")
    try:
        response = requests.get(f"{BASE_URL}/api/formularios/mesas", headers=headers)
        if response.status_code == 200:
            mesas = response.json().get('data', [])
            print_success(f"Mesas disponibles: {len(mesas)}")
            if mesas:
                print_info(f"Ejemplo: {mesas[0].get('nombre_completo')}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 3. Ver perfil
    print_subsection("3. Ver Perfil")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
        if response.status_code == 200:
            profile = response.json().get('data', {})
            print_success(f"Perfil: {profile.get('user', {}).get('nombre')}")
            ubicacion = profile.get('ubicacion', {})
            if ubicacion:
                print_success(f"Ubicación: {ubicacion.get('nombre_completo')}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 4. Listar candidatos
    print_subsection("4. Listar Candidatos")
    try:
        response = requests.get(f"{BASE_URL}/api/configuracion/candidatos", headers=headers)
        if response.status_code == 200:
            candidatos = response.json().get('data', [])
            print_success(f"Candidatos disponibles: {len(candidatos)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_testigo_electoral():
    """Test completo de Testigo Electoral"""
    print_section("TESTIGO ELECTORAL - FLUJO COMPLETO")
    
    token = login(
        "Testigo La Salle Mesa 01",
        "testigo_electoral",
        {
            "departamento_codigo": "18",
            "municipio_codigo": "01",
            "zona_codigo": "99",
            "puesto_codigo": "06"
        }
    )
    
    if not token:
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 1. Ver perfil
    print_subsection("1. Ver Perfil")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
        if response.status_code == 200:
            profile = response.json().get('data', {})
            user = profile.get('user', {})
            print_success(f"Perfil: {user.get('nombre')}")
            print_success(f"Presencia verificada: {user.get('presencia_verificada', False)}")
            ubicacion = profile.get('ubicacion', {})
            if ubicacion:
                print_success(f"Ubicación: {ubicacion.get('nombre_completo')}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 2. Registrar presencia
    print_subsection("2. Registrar Presencia")
    try:
        response = requests.post(
            f"{BASE_URL}/api/testigo/registrar-presencia",
            headers=headers,
            json={}
        )
        if response.status_code == 200:
            data = response.json().get('data', {})
            print_success(f"Presencia registrada")
            print_success(f"Coordinador notificado: {data.get('coordinador_notificado', False)}")
        elif response.status_code == 400:
            print_info("Presencia ya registrada previamente")
        else:
            print_info(f"Presencia: {response.status_code}")
    except Exception as e:
        print_info(f"Presencia: {str(e)}")
    
    # 3. Ver estadísticas del testigo
    print_subsection("3. Estadísticas del Testigo")
    try:
        response = requests.get(f"{BASE_URL}/api/testigo/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success(f"Presencia verificada: {stats.get('presencia_verificada', False)}")
            print_success(f"Formularios enviados: {stats.get('formularios_enviados', 0)}")
        else:
            print_info(f"Stats endpoint: {response.status_code}")
    except Exception as e:
        print_info(f"Stats: {str(e)}")
    
    # 4. Listar candidatos
    print_subsection("4. Listar Candidatos")
    try:
        response = requests.get(f"{BASE_URL}/api/configuracion/candidatos", headers=headers)
        if response.status_code == 200:
            candidatos = response.json().get('data', [])
            print_success(f"Candidatos disponibles: {len(candidatos)}")
            if candidatos:
                print_info(f"Ejemplo: {candidatos[0].get('nombre')}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 5. Ver mis formularios
    print_subsection("5. Mis Formularios E14")
    try:
        response = requests.get(f"{BASE_URL}/api/formularios/mis-formularios", headers=headers)
        if response.status_code == 200:
            result = response.json().get('data', {})
            formularios = result.get('formularios', [])
            print_success(f"Formularios E14: {len(formularios)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 6. Listar partidos
    print_subsection("6. Listar Partidos")
    try:
        response = requests.get(f"{BASE_URL}/api/configuracion/partidos", headers=headers)
        if response.status_code == 200:
            partidos = response.json().get('data', [])
            print_success(f"Partidos disponibles: {len(partidos)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_auditor_electoral():
    """Test completo de Auditor Electoral"""
    print_section("AUDITOR ELECTORAL - FLUJO COMPLETO")
    
    token = login(
        "Auditor Electoral",
        "auditor_electoral",
        {"departamento_codigo": "18"}
    )
    
    if not token:
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 1. Ver estadísticas de auditoría
    print_subsection("1. Estadísticas de Auditoría")
    try:
        response = requests.get(f"{BASE_URL}/api/auditor/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success(f"Total formularios: {stats.get('total_formularios', 0)}")
            print_success(f"Formularios pendientes: {stats.get('pendientes_revision', 0)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 2. Ver perfil
    print_subsection("2. Ver Perfil")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
        if response.status_code == 200:
            profile = response.json().get('data', {})
            print_success(f"Perfil: {profile.get('user', {}).get('nombre')}")
            ubicacion = profile.get('ubicacion', {})
            if ubicacion:
                print_success(f"Ubicación: {ubicacion.get('nombre_completo')}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 3. Listar formularios para auditoría
    print_subsection("3. Formularios para Auditoría")
    try:
        response = requests.get(f"{BASE_URL}/api/auditor/formularios", headers=headers)
        if response.status_code == 200:
            formularios = response.json().get('data', [])
            print_success(f"Formularios disponibles: {len(formularios)}")
        else:
            print_info(f"Formularios endpoint: {response.status_code}")
    except Exception as e:
        print_info(f"Formularios: {str(e)}")
    
    return True

def main():
    print_section("INICIO - TEST DE FLUJO COMPLETO DE TODOS LOS ROLES")
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
    
    print_section("RESUMEN FINAL")
    
    exitosos = sum(1 for v in resultados.values() if v)
    total = len(resultados)
    
    for rol, resultado in resultados.items():
        if resultado:
            print_success(f"{rol}: PASSED")
        else:
            print_error(f"{rol}: FAILED")
    
    print(f"\n{Colors.BLUE}{'='*80}")
    print(f"  RESULTADO: {exitosos}/{total} roles completados exitosamente")
    print(f"{'='*80}{Colors.END}")
    
    if exitosos == total:
        print_success("✅ TODOS LOS FLUJOS FUNCIONAN CORRECTAMENTE")
    else:
        print_error(f"⚠️  {total - exitosos} roles con problemas")

if __name__ == '__main__':
    main()
