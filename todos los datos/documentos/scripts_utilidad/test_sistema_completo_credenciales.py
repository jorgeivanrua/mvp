"""
Test completo del sistema con las nuevas credenciales test123
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
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

# Configuración de usuarios a probar
USUARIOS_TEST = [
    {
        "nombre": "Super Admin",
        "rol": "super_admin",
        "password": "test123",
        "ubicacion": {},
        "dashboard_esperado": "/admin/super-admin"
    },
    {
        "nombre": "Admin Departamental",
        "rol": "admin_departamental",
        "password": "test123",
        "ubicacion": {
            "departamento_codigo": "44"
        },
        "dashboard_esperado": "/admin/departamental"
    },
    {
        "nombre": "Admin Municipal",
        "rol": "admin_municipal",
        "password": "test123",
        "ubicacion": {
            "departamento_codigo": "44",
            "municipio_codigo": "01"
        },
        "dashboard_esperado": "/admin/municipal"
    },
    {
        "nombre": "Coordinador Departamental",
        "rol": "coordinador_departamental",
        "password": "test123",
        "ubicacion": {
            "departamento_codigo": "44"
        },
        "dashboard_esperado": "/coordinador/departamental"
    },
    {
        "nombre": "Coordinador Municipal",
        "rol": "coordinador_municipal",
        "password": "test123",
        "ubicacion": {
            "departamento_codigo": "44",
            "municipio_codigo": "01"
        },
        "dashboard_esperado": "/coordinador/municipal"
    },
    {
        "nombre": "Coordinador Puesto",
        "rol": "coordinador_puesto",
        "password": "test123",
        "ubicacion": {
            "departamento_codigo": "44",
            "municipio_codigo": "01",
            "zona_codigo": "01",
            "puesto_codigo": "01"
        },
        "dashboard_esperado": "/coordinador/puesto"
    },
    {
        "nombre": "Auditor Electoral",
        "rol": "auditor_electoral",
        "password": "test123",
        "ubicacion": {
            "departamento_codigo": "44"
        },
        "dashboard_esperado": "/auditor/dashboard"
    }
]

def test_login(usuario):
    """Probar login de un usuario"""
    print(f"\n{'='*70}")
    print_info(f"Probando: {usuario['nombre']} ({usuario['rol']})")
    print(f"{'='*70}")
    
    # Preparar datos de login
    login_data = {
        "rol": usuario["rol"],
        "password": usuario["password"],
        **usuario["ubicacion"]
    }
    
    print_info(f"Datos de login: {json.dumps(login_data, indent=2)}")
    
    try:
        # Intentar login
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            allow_redirects=False
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print_success(f"Login exitoso")
                print_info(f"Token recibido: {data.get('token', 'N/A')[:50]}...")
                print_info(f"Redirect: {data.get('redirect', 'N/A')}")
                
                # Verificar que el redirect sea correcto
                if data.get('redirect') == usuario['dashboard_esperado']:
                    print_success(f"Redirect correcto: {data.get('redirect')}")
                else:
                    print_warning(f"Redirect diferente al esperado")
                    print_warning(f"  Esperado: {usuario['dashboard_esperado']}")
                    print_warning(f"  Recibido: {data.get('redirect')}")
                
                # Probar acceso al dashboard
                token = data.get('token')
                if token:
                    test_dashboard_access(usuario, token)
                
                return True
            else:
                print_error(f"Login falló: {data.get('message', 'Sin mensaje')}")
                return False
        else:
            print_error(f"Error HTTP {response.status_code}")
            try:
                error_data = response.json()
                print_error(f"Mensaje: {error_data.get('message', 'Sin mensaje')}")
            except:
                print_error(f"Respuesta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print_error(f"Excepción: {str(e)}")
        return False

def test_dashboard_access(usuario, token):
    """Probar acceso al dashboard con el token"""
    print_info(f"\nProbando acceso al dashboard...")
    
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(
            f"{BASE_URL}{usuario['dashboard_esperado']}",
            headers=headers,
            allow_redirects=False
        )
        
        if response.status_code == 200:
            print_success(f"Dashboard accesible (200 OK)")
            print_info(f"Tamaño respuesta: {len(response.text)} bytes")
        elif response.status_code == 302:
            print_warning(f"Redirect detectado: {response.headers.get('Location', 'N/A')}")
        else:
            print_error(f"Error accediendo al dashboard: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error probando dashboard: {str(e)}")

def main():
    print("\n" + "="*70)
    print("🔍 TEST COMPLETO DEL SISTEMA - CREDENCIALES test123")
    print("="*70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    print("="*70)
    
    # Verificar que el servidor esté corriendo
    print_info("\nVerificando servidor...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print_success(f"Servidor activo (Status: {response.status_code})")
    except Exception as e:
        print_error(f"Servidor no responde: {str(e)}")
        print_error("Asegúrate de que la aplicación esté corriendo")
        return
    
    # Probar cada usuario
    resultados = []
    for usuario in USUARIOS_TEST:
        resultado = test_login(usuario)
        resultados.append({
            "nombre": usuario["nombre"],
            "rol": usuario["rol"],
            "exitoso": resultado
        })
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*70)
    
    exitosos = sum(1 for r in resultados if r["exitoso"])
    fallidos = len(resultados) - exitosos
    
    for resultado in resultados:
        if resultado["exitoso"]:
            print_success(f"{resultado['nombre']} ({resultado['rol']})")
        else:
            print_error(f"{resultado['nombre']} ({resultado['rol']})")
    
    print("\n" + "="*70)
    print(f"Total: {len(resultados)} usuarios probados")
    print_success(f"Exitosos: {exitosos}")
    if fallidos > 0:
        print_error(f"Fallidos: {fallidos}")
    print("="*70)
    
    if exitosos == len(resultados):
        print_success("\n🎉 ¡TODOS LOS TESTS PASARON!")
    else:
        print_warning(f"\n⚠️  {fallidos} test(s) fallaron")

if __name__ == '__main__':
    main()
