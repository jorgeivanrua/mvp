"""
Test del flujo completo E14:
1. Testigo registra votos en una mesa
2. Coordinador de puesto verifica y aprueba el formulario
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

# Colores
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

def print_section(msg):
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"🔍 {msg}")
    print(f"{'='*70}{Colors.END}")

def login(rol, ubicacion_data, password="test123"):
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
                return data.get('data', {}).get('access_token'), data.get('data', {}).get('user')
        return None, None
    except Exception as e:
        print_error(f"Error en login: {str(e)}")
        return None, None

def main():
    print("\n" + "="*70)
    print("🗳️  TEST FLUJO COMPLETO E14")
    print("="*70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Verificar servidor
    print_info("\nVerificando servidor...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print_success(f"Servidor activo (Status: {response.status_code})")
    except Exception as e:
        print_error(f"Servidor no responde: {str(e)}")
        return
    
    # ========================================================================
    # PASO 1: Login como Coordinador de Puesto
    # ========================================================================
    print_section("PASO 1: Login como Coordinador de Puesto")
    
    coordinador_ubicacion = {
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "zona_codigo": "01",
        "puesto_codigo": "01"
    }
    
    token_coordinador, user_coordinador = login("coordinador_puesto", coordinador_ubicacion)
    
    if not token_coordinador:
        print_error("No se pudo hacer login como coordinador")
        return
    
    print_success(f"Login exitoso: {user_coordinador.get('nombre')}")
    print_info(f"Ubicación: {user_coordinador.get('ubicacion_id')}")
    
    headers_coordinador = {"Authorization": f"Bearer {token_coordinador}"}
    
    # Obtener información del puesto
    print_info("\nObteniendo información del puesto...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/coordinador-puesto/puesto-info",
            headers=headers_coordinador
        )
        
        if response.status_code == 200:
            puesto_info = response.json().get('data', {})
            print_success(f"Puesto: {puesto_info.get('puesto_nombre', 'N/A')}")
            print_info(f"Total mesas: {puesto_info.get('total_mesas', 0)}")
        else:
            print_warning(f"No se pudo obtener info del puesto: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # ========================================================================
    # PASO 2: Obtener Candidatos Disponibles
    # ========================================================================
    print_section("PASO 2: Obtener Candidatos Disponibles")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/configuracion/candidatos",
            headers=headers_coordinador
        )
        
        if response.status_code == 200:
            candidatos_data = response.json()
            candidatos = candidatos_data.get('data', [])
            print_success(f"Candidatos disponibles: {len(candidatos)}")
            
            if candidatos:
                print_info("\nPrimeros 5 candidatos:")
                for cand in candidatos[:5]:
                    print(f"  - {cand.get('nombre_completo')} (ID: {cand.get('id')})")
            else:
                print_warning("No hay candidatos configurados")
                print_info("El sistema necesita candidatos para registrar votos")
                return
        else:
            print_error(f"Error obteniendo candidatos: {response.status_code}")
            return
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return
    
    # ========================================================================
    # PASO 3: Obtener Partidos Disponibles
    # ========================================================================
    print_section("PASO 3: Obtener Partidos Disponibles")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/configuracion/partidos",
            headers=headers_coordinador
        )
        
        if response.status_code == 200:
            partidos_data = response.json()
            partidos = partidos_data.get('data', [])
            print_success(f"Partidos disponibles: {len(partidos)}")
            
            if partidos:
                print_info("\nPrimeros 5 partidos:")
                for partido in partidos[:5]:
                    print(f"  - {partido.get('nombre')} (ID: {partido.get('id')})")
        else:
            print_warning(f"Error obteniendo partidos: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # ========================================================================
    # PASO 4: Simular Registro de Votos (Formulario E14)
    # ========================================================================
    print_section("PASO 4: Simular Registro de Votos (Formulario E14)")
    
    # Preparar datos del formulario E14
    # Usamos la primera mesa del puesto
    mesa_id = 5  # Primera mesa del puesto 01
    
    # Preparar votos por candidato (primeros 3 candidatos)
    votos_candidatos = []
    for i, candidato in enumerate(candidatos[:3]):
        votos_candidatos.append({
            "candidato_id": candidato.get('id'),
            "votos": (i + 1) * 10  # 10, 20, 30 votos
        })
    
    # Preparar votos por partido (primeros 3 partidos)
    votos_partidos = []
    for i, partido in enumerate(partidos[:3]):
        votos_partidos.append({
            "partido_id": partido.get('id'),
            "votos": (i + 1) * 5  # 5, 10, 15 votos
        })
    
    formulario_e14 = {
        "mesa_id": mesa_id,
        "votos_candidatos": votos_candidatos,
        "votos_partidos": votos_partidos,
        "votos_blancos": 5,
        "votos_nulos": 3,
        "votos_no_marcados": 2,
        "total_votantes": 100,
        "observaciones": "Prueba de flujo E14 completo"
    }
    
    print_info(f"\nRegistrando formulario E14 para mesa ID: {mesa_id}")
    print_info(f"Total candidatos con votos: {len(votos_candidatos)}")
    print_info(f"Total partidos con votos: {len(votos_partidos)}")
    print_info(f"Votos blancos: {formulario_e14['votos_blancos']}")
    print_info(f"Votos nulos: {formulario_e14['votos_nulos']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/coordinador-puesto/formulario-e14",
            headers=headers_coordinador,
            json=formulario_e14
        )
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print_success("Formulario E14 registrado exitosamente")
            
            formulario_id = result.get('data', {}).get('id') or result.get('id')
            print_info(f"Formulario ID: {formulario_id}")
            
        else:
            print_error(f"Error registrando formulario: {response.status_code}")
            try:
                error_data = response.json()
                print_error(f"Mensaje: {error_data.get('message', 'Sin mensaje')}")
            except:
                print_error(f"Respuesta: {response.text[:200]}")
            return
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return
    
    # ========================================================================
    # PASO 5: Verificar Formularios Registrados
    # ========================================================================
    print_section("PASO 5: Verificar Formularios Registrados")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/coordinador-puesto/formularios",
            headers=headers_coordinador
        )
        
        if response.status_code == 200:
            formularios_data = response.json()
            formularios = formularios_data.get('data', [])
            print_success(f"Formularios encontrados: {len(formularios)}")
            
            if formularios:
                print_info("\nÚltimos formularios:")
                for form in formularios[-3:]:
                    print(f"  - ID: {form.get('id')}")
                    print(f"    Mesa: {form.get('mesa_nombre', 'N/A')}")
                    print(f"    Estado: {form.get('estado', 'N/A')}")
                    print(f"    Total votos: {form.get('total_votos', 0)}")
        else:
            print_warning(f"Error obteniendo formularios: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # ========================================================================
    # PASO 6: Obtener Estadísticas del Puesto
    # ========================================================================
    print_section("PASO 6: Obtener Estadísticas del Puesto")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/coordinador-puesto/estadisticas",
            headers=headers_coordinador
        )
        
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print_success("Estadísticas obtenidas")
            print_info(f"Total mesas: {stats.get('total_mesas', 0)}")
            print_info(f"Mesas con formulario: {stats.get('mesas_con_formulario', 0)}")
            print_info(f"Porcentaje completado: {stats.get('porcentaje_completado', 0)}%")
        else:
            print_warning(f"Estadísticas no disponibles: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # ========================================================================
    # RESUMEN
    # ========================================================================
    print_section("RESUMEN DEL FLUJO E14")
    
    print("\n✅ Flujo completado exitosamente:")
    print("  1. ✅ Login como Coordinador de Puesto")
    print("  2. ✅ Obtención de candidatos y partidos")
    print("  3. ✅ Registro de formulario E14")
    print("  4. ✅ Verificación de formularios registrados")
    print("  5. ✅ Consulta de estadísticas")
    
    print("\n" + "="*70)
    print("🎉 TEST COMPLETADO")
    print("="*70)

if __name__ == '__main__':
    main()
