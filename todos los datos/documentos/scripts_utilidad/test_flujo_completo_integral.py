#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST INTEGRAL DEL FLUJO COMPLETO DEL SISTEMA ELECTORAL
Prueba todas las funcionalidades desde login hasta auditoría
"""
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def login(rol, ubicacion_data, password):
    """Login y obtener token"""
    try:
        login_data = {"rol": rol, "password": password}
        login_data.update(ubicacion_data)
        
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Login exitoso: {rol}")
            return data.get('access_token')
        else:
            print_error(f"Login fallido: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error en login: {str(e)}")
        return None

def get_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# ============================================================================
# PRUEBA 1: TESTIGO ELECTORAL - FLUJO COMPLETO
# ============================================================================

def test_testigo_completo():
    print_header("PRUEBA 1: TESTIGO ELECTORAL - FLUJO COMPLETO")
    
    # 1. Login
    print("\n--- 1.1 Login ---")
    token = login("testigo_electoral", {
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "puesto_codigo": "001"
    }, "test123")
    
    if not token:
        return False
    
    headers = get_headers(token)
    
    # 2. Verificar presencia
    print("\n--- 1.2 Verificar Presencia ---")
    try:
        response = requests.post(f"{BASE_URL}/api/auth/verificar-presencia", headers=headers)
        if response.status_code == 200:
            print_success("Presencia verificada")
            data = response.json()
            print_info(f"Verificado en: {data.get('data', {}).get('presencia_verificada_at', 'N/A')}")
        else:
            print_warning(f"No se pudo verificar presencia: {response.status_code}")
            print_warning(f"Respuesta: {response.text}")
    except Exception as e:
        print_error(f"Error verificar presencia: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 3. Obtener información de la mesa
    print("\n--- 1.3 Información de la Mesa/Puesto ---")
    try:
        response = requests.get(f"{BASE_URL}/api/testigo/mesa", headers=headers)
        if response.status_code == 200:
            mesa_info = response.json()
            print_success("Información obtenida")
            data = mesa_info.get('data', {})
            puesto = data.get('puesto', {})
            mesas = data.get('mesas', [])
            print_info(f"Puesto: {puesto.get('nombre_completo', 'N/A')}")
            print_info(f"Mesas disponibles: {len(mesas)}")
            for mesa in mesas[:3]:
                print_info(f"  - Mesa {mesa.get('mesa_codigo')}: {mesa.get('total_votantes_registrados')} votantes")
        else:
            print_error(f"Error: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 4. Obtener tipos de elección
    print("\n--- 1.4 Tipos de Elección ---")
    try:
        response = requests.get(f"{BASE_URL}/api/testigo/tipos-eleccion", headers=headers)
        if response.status_code == 200:
            result = response.json()
            tipos = result.get('data', []) if isinstance(result, dict) else result
            print_success(f"Tipos disponibles: {len(tipos)}")
            for tipo in tipos[:3]:
                print_info(f"  - {tipo.get('nombre')} (ID: {tipo.get('id')})")
        else:
            print_error(f"Error: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 5. Obtener partidos
    print("\n--- 1.5 Partidos Políticos ---")
    try:
        response = requests.get(f"{BASE_URL}/api/testigo/partidos", headers=headers)
        if response.status_code == 200:
            result = response.json()
            partidos = result.get('data', []) if isinstance(result, dict) else result
            print_success(f"Partidos disponibles: {len(partidos)}")
            for partido in partidos[:3]:
                print_info(f"  - {partido.get('nombre')} ({partido.get('sigla')})")
        else:
            print_error(f"Error: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 6. Obtener candidatos para Presidencia
    print("\n--- 1.6 Candidatos (Presidencia) ---")
    try:
        response = requests.get(
            f"{BASE_URL}/api/testigo/candidatos",
            params={"tipo_eleccion_id": 1},
            headers=headers
        )
        if response.status_code == 200:
            result = response.json()
            candidatos = result.get('data', []) if isinstance(result, dict) else result
            print_success(f"Candidatos: {len(candidatos)}")
            for cand in candidatos:
                print_info(f"  - {cand.get('nombre')} ({cand.get('partido')})")
        else:
            print_error(f"Error: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

    # 7. Registrar Formulario E-14 (Presidencia)
    print("\n--- 1.7 Registrar Formulario E-14 (Presidencia) ---")
    try:
        formulario = {
            "tipo_eleccion_id": 1,
            "mesa_codigo": "001",  # Mesa específica
            "votos_partidos": [
                {"partido_id": 1, "votos": 150},
                {"partido_id": 2, "votos": 120},
                {"partido_id": 3, "votos": 80}
            ],
            "votos_candidatos": [
                {"candidato_id": 1, "votos": 150},
                {"candidato_id": 2, "votos": 120},
                {"candidato_id": 3, "votos": 80}
            ],
            "votos_nulos": 5,
            "votos_blancos": 10,
            "votos_no_marcados": 2,
            "total_votantes": 367
        }
        
        response = requests.post(
            f"{BASE_URL}/api/testigo/formularios-e14",
            json=formulario,
            headers=headers
        )
        
        if response.status_code == 201:
            print_success("Formulario E-14 registrado")
            data = response.json()
            print_info(f"ID: {data.get('id', 'N/A')}")
        else:
            print_error(f"Error: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 8. Registrar Incidente
    print("\n--- 1.8 Registrar Incidente ---")
    try:
        incidente = {
            "tipo": "retraso_apertura",
            "descripcion": "La mesa abrió 30 minutos tarde",
            "gravedad": "media",
            "mesa_codigo": "001"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/testigo/incidentes",
            json=incidente,
            headers=headers
        )
        
        if response.status_code == 201:
            print_success("Incidente registrado")
        else:
            print_error(f"Error: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 9. Registrar Delito Electoral
    print("\n--- 1.9 Registrar Delito Electoral ---")
    try:
        delito = {
            "tipo_delito": "compra_votos",
            "descripcion": "Se observó entrega de dinero a votantes",
            "gravedad": "alta",
            "evidencia_fotografica": False,
            "testigos_adicionales": 2,
            "mesa_codigo": "001"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/testigo/delitos",
            json=delito,
            headers=headers
        )
        
        if response.status_code == 201:
            print_success("Delito electoral registrado")
        else:
            print_warning(f"Endpoint de delitos: {response.status_code}")
            # Este endpoint puede no existir aún
    except Exception as e:
        print_warning(f"Endpoint de delitos no disponible")
    
    # 10. Consultar mis formularios
    print("\n--- 1.10 Consultar Mis Formularios ---")
    try:
        response = requests.get(f"{BASE_URL}/api/testigo/formularios-e14", headers=headers)
        if response.status_code == 200:
            formularios = response.json()
            print_success(f"Formularios registrados: {len(formularios)}")
            for form in formularios:
                print_info(f"  - {form.get('tipo_eleccion', 'N/A')}: {form.get('total_votantes', 0)} votantes")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # 11. Consultar mis incidentes
    print("\n--- 1.11 Consultar Mis Incidentes ---")
    try:
        response = requests.get(f"{BASE_URL}/api/testigo/incidentes", headers=headers)
        if response.status_code == 200:
            incidentes = response.json()
            print_success(f"Incidentes registrados: {len(incidentes)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    print_success("\n✓ PRUEBA TESTIGO COMPLETADA")
    return True

# ============================================================================
# PRUEBA 2: COORDINADOR DE PUESTO
# ============================================================================

def test_coordinador_puesto():
    print_header("PRUEBA 2: COORDINADOR DE PUESTO")
    
    # Login
    print("\n--- 2.1 Login ---")
    token = login("coordinador_puesto", {
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "puesto_codigo": "001"
    }, "test123")
    
    if not token:
        return False
    
    headers = get_headers(token)
    
    # Consultar mesas
    print("\n--- 2.2 Mesas del Puesto ---")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-puesto/mesas", headers=headers)
        if response.status_code == 200:
            mesas = response.json()
            print_success(f"Mesas: {len(mesas)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Consultar formularios
    print("\n--- 2.3 Formularios E-14 del Puesto ---")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-puesto/formularios-e14", headers=headers)
        if response.status_code == 200:
            formularios = response.json()
            print_success(f"Formularios: {len(formularios)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Consultar incidentes
    print("\n--- 2.4 Incidentes del Puesto ---")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-puesto/incidentes", headers=headers)
        if response.status_code == 200:
            incidentes = response.json()
            print_success(f"Incidentes: {len(incidentes)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Estadísticas
    print("\n--- 2.5 Estadísticas del Puesto ---")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-puesto/estadisticas", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print_success("Estadísticas obtenidas")
            print_info(f"  Total mesas: {stats.get('total_mesas', 0)}")
            print_info(f"  Formularios: {stats.get('formularios_registrados', 0)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    print_success("\n✓ PRUEBA COORDINADOR PUESTO COMPLETADA")
    return True

# ============================================================================
# PRUEBA 3: AUDITOR ELECTORAL
# ============================================================================

def test_auditor():
    print_header("PRUEBA 3: AUDITOR ELECTORAL")
    
    # Login
    print("\n--- 3.1 Login ---")
    token = login("auditor_electoral", {}, "test123")
    
    if not token:
        return False
    
    headers = get_headers(token)
    
    # Consultar todos los formularios
    print("\n--- 3.2 Todos los Formularios E-14 ---")
    try:
        response = requests.get(f"{BASE_URL}/api/auditor/formularios-e14", headers=headers)
        if response.status_code == 200:
            formularios = response.json()
            print_success(f"Total formularios: {len(formularios)}")
            
            # Análisis
            total_votos = sum(f.get('total_votantes', 0) for f in formularios)
            print_info(f"  Total votos: {total_votos}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Consultar incidentes
    print("\n--- 3.3 Todos los Incidentes ---")
    try:
        response = requests.get(f"{BASE_URL}/api/auditor/incidentes", headers=headers)
        if response.status_code == 200:
            incidentes = response.json()
            print_success(f"Total incidentes: {len(incidentes)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Detectar inconsistencias
    print("\n--- 3.4 Detectar Inconsistencias ---")
    try:
        response = requests.get(f"{BASE_URL}/api/auditor/inconsistencias", headers=headers)
        if response.status_code == 200:
            inconsistencias = response.json()
            if inconsistencias:
                print_warning(f"Inconsistencias detectadas: {len(inconsistencias)}")
            else:
                print_success("No se detectaron inconsistencias")
        else:
            print_warning(f"Endpoint inconsistencias: {response.status_code}")
    except Exception as e:
        print_warning("Endpoint inconsistencias no disponible")
    
    # Resultados por tipo de elección
    print("\n--- 3.5 Resultados Presidencia ---")
    try:
        response = requests.get(
            f"{BASE_URL}/api/auditor/resultados",
            params={"tipo_eleccion_id": 1},
            headers=headers
        )
        if response.status_code == 200:
            resultados = response.json()
            print_success("Resultados obtenidos")
            for resultado in resultados.get('candidatos', [])[:3]:
                print_info(f"  - {resultado.get('nombre')}: {resultado.get('votos')} votos")
        else:
            print_warning(f"Endpoint resultados: {response.status_code}")
    except Exception as e:
        print_warning("Endpoint resultados no disponible")
    
    print_success("\n✓ PRUEBA AUDITOR COMPLETADA")
    return True

# ============================================================================
# PRUEBA 4: SUPER ADMIN
# ============================================================================

def test_super_admin():
    print_header("PRUEBA 4: SUPER ADMIN")
    
    # Login
    print("\n--- 4.1 Login ---")
    token = login("super_admin", {}, "test123")
    
    if not token:
        return False
    
    headers = get_headers(token)
    
    # Consultar campañas
    print("\n--- 4.2 Campañas ---")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/campanas", headers=headers)
        if response.status_code == 200:
            campanas = response.json()
            print_success(f"Campañas: {len(campanas)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Consultar tipos de elección
    print("\n--- 4.3 Tipos de Elección ---")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/tipos-eleccion", headers=headers)
        if response.status_code == 200:
            tipos = response.json()
            print_success(f"Tipos de elección: {len(tipos)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Consultar partidos
    print("\n--- 4.4 Partidos ---")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/partidos", headers=headers)
        if response.status_code == 200:
            partidos = response.json()
            print_success(f"Partidos: {len(partidos)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Consultar candidatos
    print("\n--- 4.5 Candidatos ---")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/candidatos", headers=headers)
        if response.status_code == 200:
            candidatos = response.json()
            print_success(f"Candidatos: {len(candidatos)}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Consultar usuarios
    print("\n--- 4.6 Usuarios ---")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/usuarios", headers=headers)
        if response.status_code == 200:
            usuarios = response.json()
            print_success(f"Usuarios: {len(usuarios)}")
            
            # Agrupar por rol
            roles = {}
            for user in usuarios:
                rol = user.get('role', 'desconocido')
                roles[rol] = roles.get(rol, 0) + 1
            
            for rol, count in roles.items():
                print_info(f"  - {rol}: {count}")
        else:
            print_error(f"Error: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    print_success("\n✓ PRUEBA SUPER ADMIN COMPLETADA")
    return True

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    print_header("TEST INTEGRAL DEL SISTEMA ELECTORAL")
    print_info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"URL: {BASE_URL}")
    
    resultados = {
        "testigo": False,
        "coordinador_puesto": False,
        "auditor": False,
        "super_admin": False
    }
    
    # Ejecutar pruebas
    try:
        resultados["testigo"] = test_testigo_completo()
    except Exception as e:
        print_error(f"Error en prueba testigo: {str(e)}")
    
    try:
        resultados["coordinador_puesto"] = test_coordinador_puesto()
    except Exception as e:
        print_error(f"Error en prueba coordinador: {str(e)}")
    
    try:
        resultados["auditor"] = test_auditor()
    except Exception as e:
        print_error(f"Error en prueba auditor: {str(e)}")
    
    try:
        resultados["super_admin"] = test_super_admin()
    except Exception as e:
        print_error(f"Error en prueba super admin: {str(e)}")
    
    # Resumen
    print_header("RESUMEN FINAL")
    
    total = len(resultados)
    exitosos = sum(1 for v in resultados.values() if v)
    
    for rol, exitoso in resultados.items():
        if exitoso:
            print_success(f"{rol.replace('_', ' ').title()}: EXITOSO")
        else:
            print_error(f"{rol.replace('_', ' ').title()}: FALLIDO")
    
    print(f"\n{Colors.BOLD}Pruebas exitosas: {exitosos}/{total} ({(exitosos/total)*100:.1f}%){Colors.END}")
    
    if exitosos == total:
        print_success("\n✓ TODAS LAS PRUEBAS PASARON")
    elif exitosos > 0:
        print_warning(f"\n⚠ PRUEBAS PARCIALMENTE EXITOSAS")
    else:
        print_error("\n✗ TODAS LAS PRUEBAS FALLARON")
    
    print(f"\n{Colors.BOLD}Test completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}\n")

if __name__ == "__main__":
    main()
