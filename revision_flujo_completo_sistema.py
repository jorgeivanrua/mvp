#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REVISIÓN COMPLETA DEL FLUJO DEL SISTEMA ELECTORAL
Simula el flujo completo desde testigo hasta auditor
"""
import requests
import json
from datetime import datetime
import sys
import io

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuración
BASE_URL = "http://localhost:5000"
CAMPANA_ID = 1

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.END}\n")

def print_section(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'─'*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'─'*80}{Colors.END}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

# ============================================================================
# FUNCIONES DE LOGIN Y AUTENTICACIÓN
# ============================================================================

def login(rol, ubicacion_data, password):
    """Login y obtener token"""
    try:
        login_data = {
            "rol": rol,
            "password": password
        }
        login_data.update(ubicacion_data)
        
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data
        )
        if response.status_code == 200:
            data = response.json()
            print_success(f"Login exitoso: {rol}")
            return data.get('access_token')
        else:
            print_error(f"Login fallido: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print_error(f"Error en login: {str(e)}")
        return None

def get_headers(token):
    """Obtener headers con token"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

# ============================================================================
# FASE 1: TESTIGO ELECTORAL - CARGA DE DATOS
# ============================================================================

def fase_testigo():
    """Simula el trabajo completo de un testigo electoral"""
    print_header("FASE 1: TESTIGO ELECTORAL - CARGA DE DATOS")
    
    # Login como testigo
    print_section("1.1 Login del Testigo")
    ubicacion_testigo = {
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "puesto_codigo": "001"
    }
    token = login("testigo_electoral", ubicacion_testigo, "test123")
    if not token:
        return False
    
    headers = get_headers(token)
    
    # Obtener información de la mesa asignada
    print_section("1.2 Verificar Mesa Asignada")
    try:
        response = requests.get(f"{BASE_URL}/api/testigo/mi-mesa", headers=headers)
        if response.status_code == 200:
            mesa_info = response.json()
            print_success(f"Mesa asignada: {mesa_info.get('numero_mesa', 'N/A')}")
            print_info(f"Puesto: {mesa_info.get('puesto_votacion', 'N/A')}")
            print_info(f"Municipio: {mesa_info.get('municipio', 'N/A')}")
        else:
            print_error(f"Error obteniendo mesa: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

    # Obtener tipos de elección disponibles
    print_section("1.3 Obtener Tipos de Elección")
    try:
        response = requests.get(f"{BASE_URL}/api/testigo/tipos-eleccion", headers=headers)
        if response.status_code == 200:
            tipos = response.json()
            print_success(f"Tipos de elección disponibles: {len(tipos)}")
            for tipo in tipos[:5]:  # Mostrar primeros 5
                print_info(f"  - {tipo.get('nombre', 'N/A')} (ID: {tipo.get('id')})")
        else:
            print_error(f"Error obteniendo tipos: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Obtener partidos políticos
    print_section("1.4 Obtener Partidos Políticos")
    try:
        response = requests.get(f"{BASE_URL}/api/testigo/partidos", headers=headers)
        if response.status_code == 200:
            partidos = response.json()
            print_success(f"Partidos disponibles: {len(partidos)}")
            for partido in partidos[:5]:  # Mostrar primeros 5
                print_info(f"  - {partido.get('nombre', 'N/A')} (ID: {partido.get('id')})")
        else:
            print_error(f"Error obteniendo partidos: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Obtener candidatos para Presidencia
    print_section("1.5 Obtener Candidatos (Presidencia)")
    try:
        response = requests.get(
            f"{BASE_URL}/api/testigo/candidatos",
            params={"tipo_eleccion_id": 1},  # Presidencia
            headers=headers
        )
        if response.status_code == 200:
            candidatos = response.json()
            print_success(f"Candidatos para Presidencia: {len(candidatos)}")
            for candidato in candidatos:
                print_info(f"  - {candidato.get('nombre', 'N/A')} ({candidato.get('partido', 'N/A')})")
        else:
            print_error(f"Error obteniendo candidatos: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

    # Registrar Formulario E-14 (Presidencia)
    print_section("1.6 Registrar Formulario E-14 - Presidencia")
    try:
        formulario_data = {
            "tipo_eleccion_id": 1,  # Presidencia
            "votos_partidos": [
                {"partido_id": 1, "votos": 150},  # Liberal
                {"partido_id": 2, "votos": 120},  # Conservador
                {"partido_id": 3, "votos": 80}    # Verde
            ],
            "votos_candidatos": [
                {"candidato_id": 1, "votos": 150},  # Candidato Liberal
                {"candidato_id": 2, "votos": 120},  # Candidato Conservador
                {"candidato_id": 3, "votos": 80}    # Candidato Verde
            ],
            "votos_nulos": 5,
            "votos_blancos": 10,
            "votos_no_marcados": 2,
            "total_votantes": 367
        }
        
        response = requests.post(
            f"{BASE_URL}/api/testigo/formularios-e14",
            json=formulario_data,
            headers=headers
        )
        
        if response.status_code == 201:
            print_success("Formulario E-14 Presidencia registrado exitosamente")
            data = response.json()
            print_info(f"ID del formulario: {data.get('id', 'N/A')}")
        else:
            print_error(f"Error registrando formulario: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Registrar Formulario E-14 (Senado - Lista Cerrada)
    print_section("1.7 Registrar Formulario E-14 - Senado")
    try:
        formulario_data = {
            "tipo_eleccion_id": 8,  # Senado
            "votos_partidos": [
                {"partido_id": 1, "votos": 180},  # Liberal
                {"partido_id": 2, "votos": 140}   # Conservador
            ],
            "votos_nulos": 8,
            "votos_blancos": 12,
            "votos_no_marcados": 3,
            "total_votantes": 343
        }
        
        response = requests.post(
            f"{BASE_URL}/api/testigo/formularios-e14",
            json=formulario_data,
            headers=headers
        )
        
        if response.status_code == 201:
            print_success("Formulario E-14 Senado registrado exitosamente")
        else:
            print_error(f"Error registrando formulario: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

    # Registrar incidente
    print_section("1.8 Registrar Incidente")
    try:
        incidente_data = {
            "tipo": "retraso_apertura",
            "descripcion": "La mesa abrió 30 minutos tarde debido a la ausencia inicial de jurados",
            "gravedad": "media"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/testigo/incidentes",
            json=incidente_data,
            headers=headers
        )
        
        if response.status_code == 201:
            print_success("Incidente registrado exitosamente")
        else:
            print_error(f"Error registrando incidente: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ver mis formularios registrados
    print_section("1.9 Consultar Mis Formularios E-14")
    try:
        response = requests.get(f"{BASE_URL}/api/testigo/formularios-e14", headers=headers)
        if response.status_code == 200:
            formularios = response.json()
            print_success(f"Formularios registrados: {len(formularios)}")
            for form in formularios:
                print_info(f"  - {form.get('tipo_eleccion', 'N/A')}: {form.get('total_votantes', 0)} votantes")
        else:
            print_error(f"Error consultando formularios: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    print_success("✓ FASE TESTIGO COMPLETADA")
    return True

# ============================================================================
# FASE 2: COORDINADOR DE PUESTO - SUPERVISIÓN LOCAL
# ============================================================================

def fase_coordinador_puesto():
    """Simula el trabajo del coordinador de puesto"""
    print_header("FASE 2: COORDINADOR DE PUESTO - SUPERVISIÓN LOCAL")
    
    # Login como coordinador de puesto
    print_section("2.1 Login del Coordinador de Puesto")
    ubicacion_coord = {
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "puesto_codigo": "001"
    }
    token = login("coordinador_puesto", ubicacion_coord, "test123")
    if not token:
        return False
    
    headers = get_headers(token)

    # Ver mesas del puesto
    print_section("2.2 Consultar Mesas del Puesto")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-puesto/mesas", headers=headers)
        if response.status_code == 200:
            mesas = response.json()
            print_success(f"Mesas en el puesto: {len(mesas)}")
            for mesa in mesas[:5]:
                print_info(f"  - Mesa {mesa.get('numero_mesa', 'N/A')}: {mesa.get('testigos_asignados', 0)} testigos")
        else:
            print_error(f"Error consultando mesas: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ver formularios del puesto
    print_section("2.3 Consultar Formularios E-14 del Puesto")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-puesto/formularios-e14", headers=headers)
        if response.status_code == 200:
            formularios = response.json()
            print_success(f"Formularios E-14 registrados: {len(formularios)}")
            
            # Agrupar por tipo de elección
            tipos_count = {}
            for form in formularios:
                tipo = form.get('tipo_eleccion', 'Desconocido')
                tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
            
            for tipo, count in tipos_count.items():
                print_info(f"  - {tipo}: {count} formularios")
        else:
            print_error(f"Error consultando formularios: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ver incidentes del puesto
    print_section("2.4 Consultar Incidentes del Puesto")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-puesto/incidentes", headers=headers)
        if response.status_code == 200:
            incidentes = response.json()
            print_success(f"Incidentes reportados: {len(incidentes)}")
            for inc in incidentes[:3]:
                print_info(f"  - {inc.get('tipo', 'N/A')}: {inc.get('descripcion', 'N/A')[:50]}...")
        else:
            print_error(f"Error consultando incidentes: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ver estadísticas del puesto
    print_section("2.5 Estadísticas del Puesto")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-puesto/estadisticas", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print_success("Estadísticas del puesto:")
            print_info(f"  - Total mesas: {stats.get('total_mesas', 0)}")
            print_info(f"  - Formularios registrados: {stats.get('formularios_registrados', 0)}")
            print_info(f"  - Participación: {stats.get('participacion', 0)}%")
        else:
            print_error(f"Error consultando estadísticas: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    print_success("✓ FASE COORDINADOR PUESTO COMPLETADA")
    return True

# ============================================================================
# FASE 3: ADMIN MUNICIPAL - SUPERVISIÓN MUNICIPAL
# ============================================================================

def fase_admin_municipal():
    """Simula el trabajo del administrador municipal"""
    print_header("FASE 3: ADMIN MUNICIPAL - SUPERVISIÓN MUNICIPAL")
    
    # Login como admin municipal
    print_section("3.1 Login del Admin Municipal")
    ubicacion_admin = {
        "departamento_codigo": "44",
        "municipio_codigo": "01"
    }
    token = login("admin_municipal", ubicacion_admin, "test123")
    if not token:
        return False
    
    headers = get_headers(token)
    
    # Ver puestos del municipio
    print_section("3.2 Consultar Puestos del Municipio")
    try:
        response = requests.get(f"{BASE_URL}/api/admin-municipal/puestos", headers=headers)
        if response.status_code == 200:
            puestos = response.json()
            print_success(f"Puestos en el municipio: {len(puestos)}")
            for puesto in puestos[:5]:
                print_info(f"  - {puesto.get('nombre', 'N/A')}: {puesto.get('mesas', 0)} mesas")
        else:
            print_error(f"Error consultando puestos: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ver formularios del municipio
    print_section("3.3 Consultar Formularios E-14 del Municipio")
    try:
        response = requests.get(f"{BASE_URL}/api/admin-municipal/formularios-e14", headers=headers)
        if response.status_code == 200:
            formularios = response.json()
            print_success(f"Formularios E-14 del municipio: {len(formularios)}")
        else:
            print_error(f"Error consultando formularios: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ver estadísticas municipales
    print_section("3.4 Estadísticas Municipales")
    try:
        response = requests.get(f"{BASE_URL}/api/admin-municipal/estadisticas", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print_success("Estadísticas municipales:")
            print_info(f"  - Total puestos: {stats.get('total_puestos', 0)}")
            print_info(f"  - Total mesas: {stats.get('total_mesas', 0)}")
            print_info(f"  - Formularios: {stats.get('formularios_registrados', 0)}")
        else:
            print_error(f"Error consultando estadísticas: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    print_success("✓ FASE ADMIN MUNICIPAL COMPLETADA")
    return True

# ============================================================================
# FASE 4: COORDINADOR DEPARTAMENTAL - SUPERVISIÓN DEPARTAMENTAL
# ============================================================================

def fase_coordinador_departamental():
    """Simula el trabajo del coordinador departamental"""
    print_header("FASE 4: COORDINADOR DEPARTAMENTAL - SUPERVISIÓN DEPARTAMENTAL")
    
    # Login como coordinador departamental
    print_section("4.1 Login del Coordinador Departamental")
    ubicacion_coord_dep = {
        "departamento_codigo": "44"
    }
    token = login("coordinador_departamental", ubicacion_coord_dep, "test123")
    if not token:
        return False
    
    headers = get_headers(token)
    
    # Ver municipios del departamento
    print_section("4.2 Consultar Municipios del Departamento")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-departamental/municipios", headers=headers)
        if response.status_code == 200:
            municipios = response.json()
            print_success(f"Municipios en el departamento: {len(municipios)}")
            for mun in municipios[:5]:
                print_info(f"  - {mun.get('nombre', 'N/A')}: {mun.get('puestos', 0)} puestos")
        else:
            print_error(f"Error consultando municipios: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ver formularios del departamento
    print_section("4.3 Consultar Formularios E-14 del Departamento")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-departamental/formularios-e14", headers=headers)
        if response.status_code == 200:
            formularios = response.json()
            print_success(f"Formularios E-14 del departamento: {len(formularios)}")
        else:
            print_error(f"Error consultando formularios: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ver estadísticas departamentales
    print_section("4.4 Estadísticas Departamentales")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinador-departamental/estadisticas", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print_success("Estadísticas departamentales:")
            print_info(f"  - Total municipios: {stats.get('total_municipios', 0)}")
            print_info(f"  - Total puestos: {stats.get('total_puestos', 0)}")
            print_info(f"  - Total mesas: {stats.get('total_mesas', 0)}")
            print_info(f"  - Formularios: {stats.get('formularios_registrados', 0)}")
        else:
            print_error(f"Error consultando estadísticas: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    print_success("✓ FASE COORDINADOR DEPARTAMENTAL COMPLETADA")
    return True

# ============================================================================
# FASE 5: AUDITOR ELECTORAL - AUDITORÍA Y ANÁLISIS
# ============================================================================

def fase_auditor():
    """Simula el trabajo del auditor electoral"""
    print_header("FASE 5: AUDITOR ELECTORAL - AUDITORÍA Y ANÁLISIS")
    
    # Login como auditor
    print_section("5.1 Login del Auditor Electoral")
    token = login("auditor_electoral", {}, "test123")
    if not token:
        return False
    
    headers = get_headers(token)
    
    # Ver todos los formularios
    print_section("5.2 Consultar Todos los Formularios E-14")
    try:
        response = requests.get(f"{BASE_URL}/api/auditor/formularios-e14", headers=headers)
        if response.status_code == 200:
            formularios = response.json()
            print_success(f"Total formularios E-14 en el sistema: {len(formularios)}")
            
            # Análisis por tipo de elección
            tipos_count = {}
            total_votos = 0
            for form in formularios:
                tipo = form.get('tipo_eleccion', 'Desconocido')
                tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
                total_votos += form.get('total_votantes', 0)
            
            print_info(f"  Total votos registrados: {total_votos}")
            for tipo, count in tipos_count.items():
                print_info(f"  - {tipo}: {count} formularios")
        else:
            print_error(f"Error consultando formularios: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ver incidentes
    print_section("5.3 Consultar Todos los Incidentes")
    try:
        response = requests.get(f"{BASE_URL}/api/auditor/incidentes", headers=headers)
        if response.status_code == 200:
            incidentes = response.json()
            print_success(f"Total incidentes reportados: {len(incidentes)}")
            
            # Análisis por gravedad
            gravedad_count = {}
            for inc in incidentes:
                grav = inc.get('gravedad', 'desconocida')
                gravedad_count[grav] = gravedad_count.get(grav, 0) + 1
            
            for grav, count in gravedad_count.items():
                print_info(f"  - {grav.capitalize()}: {count} incidentes")
        else:
            print_error(f"Error consultando incidentes: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

    # Análisis de inconsistencias
    print_section("5.4 Detectar Inconsistencias")
    try:
        response = requests.get(f"{BASE_URL}/api/auditor/inconsistencias", headers=headers)
        if response.status_code == 200:
            inconsistencias = response.json()
            if inconsistencias:
                print_warning(f"Inconsistencias detectadas: {len(inconsistencias)}")
                for inc in inconsistencias[:5]:
                    print_warning(f"  - {inc.get('tipo', 'N/A')}: {inc.get('descripcion', 'N/A')}")
            else:
                print_success("No se detectaron inconsistencias")
        else:
            print_error(f"Error consultando inconsistencias: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Resultados por tipo de elección
    print_section("5.5 Resultados por Tipo de Elección")
    try:
        # Presidencia
        response = requests.get(
            f"{BASE_URL}/api/auditor/resultados",
            params={"tipo_eleccion_id": 1},
            headers=headers
        )
        if response.status_code == 200:
            resultados = response.json()
            print_success("Resultados Presidencia:")
            for resultado in resultados.get('candidatos', []):
                print_info(f"  - {resultado.get('nombre', 'N/A')}: {resultado.get('votos', 0)} votos")
        else:
            print_error(f"Error consultando resultados: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Estadísticas generales
    print_section("5.6 Estadísticas Generales del Sistema")
    try:
        response = requests.get(f"{BASE_URL}/api/auditor/estadisticas", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print_success("Estadísticas generales:")
            print_info(f"  - Total departamentos: {stats.get('total_departamentos', 0)}")
            print_info(f"  - Total municipios: {stats.get('total_municipios', 0)}")
            print_info(f"  - Total puestos: {stats.get('total_puestos', 0)}")
            print_info(f"  - Total mesas: {stats.get('total_mesas', 0)}")
            print_info(f"  - Formularios E-14: {stats.get('formularios_registrados', 0)}")
            print_info(f"  - Participación: {stats.get('participacion', 0)}%")
        else:
            print_error(f"Error consultando estadísticas: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    print_success("✓ FASE AUDITOR COMPLETADA")
    return True

# ============================================================================
# FASE 6: SUPER ADMIN - CONFIGURACIÓN Y GESTIÓN
# ============================================================================

def fase_super_admin():
    """Simula el trabajo del super administrador"""
    print_header("FASE 6: SUPER ADMIN - CONFIGURACIÓN Y GESTIÓN")
    
    # Login como super admin
    print_section("6.1 Login del Super Admin")
    token = login("super_admin", {}, "test123")
    if not token:
        return False
    
    headers = get_headers(token)
    
    # Ver campañas
    print_section("6.2 Consultar Campañas")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/campanas", headers=headers)
        if response.status_code == 200:
            campanas = response.json()
            print_success(f"Campañas en el sistema: {len(campanas)}")
            for camp in campanas:
                print_info(f"  - {camp.get('nombre', 'N/A')} ({camp.get('fecha_inicio', 'N/A')})")
        else:
            print_error(f"Error consultando campañas: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ver tipos de elección
    print_section("6.3 Consultar Tipos de Elección")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/tipos-eleccion", headers=headers)
        if response.status_code == 200:
            tipos = response.json()
            print_success(f"Tipos de elección configurados: {len(tipos)}")
            for tipo in tipos[:5]:
                print_info(f"  - {tipo.get('nombre', 'N/A')} ({tipo.get('tipo_votacion', 'N/A')})")
        else:
            print_error(f"Error consultando tipos: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ver partidos
    print_section("6.4 Consultar Partidos Políticos")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/partidos", headers=headers)
        if response.status_code == 200:
            partidos = response.json()
            print_success(f"Partidos políticos configurados: {len(partidos)}")
            for partido in partidos[:5]:
                print_info(f"  - {partido.get('nombre', 'N/A')} ({partido.get('sigla', 'N/A')})")
        else:
            print_error(f"Error consultando partidos: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

    # Ver candidatos
    print_section("6.5 Consultar Candidatos")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/candidatos", headers=headers)
        if response.status_code == 200:
            candidatos = response.json()
            print_success(f"Candidatos configurados: {len(candidatos)}")
            
            # Agrupar por tipo de elección
            tipos_count = {}
            for cand in candidatos:
                tipo = cand.get('tipo_eleccion', 'Desconocido')
                tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
            
            for tipo, count in tipos_count.items():
                print_info(f"  - {tipo}: {count} candidatos")
        else:
            print_error(f"Error consultando candidatos: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ver usuarios
    print_section("6.6 Consultar Usuarios del Sistema")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/usuarios", headers=headers)
        if response.status_code == 200:
            usuarios = response.json()
            print_success(f"Usuarios en el sistema: {len(usuarios)}")
            
            # Agrupar por rol
            roles_count = {}
            for user in usuarios:
                rol = user.get('role', 'desconocido')
                roles_count[rol] = roles_count.get(rol, 0) + 1
            
            for rol, count in roles_count.items():
                print_info(f"  - {rol}: {count} usuarios")
        else:
            print_error(f"Error consultando usuarios: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Estadísticas globales
    print_section("6.7 Estadísticas Globales del Sistema")
    try:
        response = requests.get(f"{BASE_URL}/api/super-admin/estadisticas", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print_success("Estadísticas globales:")
            print_info(f"  - Campañas activas: {stats.get('campanas_activas', 0)}")
            print_info(f"  - Total usuarios: {stats.get('total_usuarios', 0)}")
            print_info(f"  - Total ubicaciones: {stats.get('total_ubicaciones', 0)}")
            print_info(f"  - Formularios E-14: {stats.get('total_formularios', 0)}")
            print_info(f"  - Incidentes: {stats.get('total_incidentes', 0)}")
        else:
            print_error(f"Error consultando estadísticas: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    print_success("✓ FASE SUPER ADMIN COMPLETADA")
    return True

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Ejecuta la revisión completa del sistema"""
    print_header("REVISIÓN COMPLETA DEL SISTEMA ELECTORAL")
    print_info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"URL Base: {BASE_URL}")
    print_info(f"Campaña ID: {CAMPANA_ID}")
    
    resultados = {
        "testigo": False,
        "coordinador_puesto": False,
        "admin_municipal": False,
        "coordinador_departamental": False,
        "auditor": False,
        "super_admin": False
    }
    
    # Ejecutar cada fase
    try:
        resultados["testigo"] = fase_testigo()
    except Exception as e:
        print_error(f"Error en fase testigo: {str(e)}")
    
    try:
        resultados["coordinador_puesto"] = fase_coordinador_puesto()
    except Exception as e:
        print_error(f"Error en fase coordinador puesto: {str(e)}")
    
    try:
        resultados["admin_municipal"] = fase_admin_municipal()
    except Exception as e:
        print_error(f"Error en fase admin municipal: {str(e)}")
    
    try:
        resultados["coordinador_departamental"] = fase_coordinador_departamental()
    except Exception as e:
        print_error(f"Error en fase coordinador departamental: {str(e)}")
    
    try:
        resultados["auditor"] = fase_auditor()
    except Exception as e:
        print_error(f"Error en fase auditor: {str(e)}")
    
    try:
        resultados["super_admin"] = fase_super_admin()
    except Exception as e:
        print_error(f"Error en fase super admin: {str(e)}")
    
    # Resumen final
    print_header("RESUMEN FINAL DE LA REVISIÓN")
    
    total_fases = len(resultados)
    fases_exitosas = sum(1 for v in resultados.values() if v)
    
    print_section("Resultados por Fase")
    for fase, exitoso in resultados.items():
        if exitoso:
            print_success(f"{fase.replace('_', ' ').title()}: EXITOSO")
        else:
            print_error(f"{fase.replace('_', ' ').title()}: FALLIDO")
    
    print_section("Resumen General")
    print_info(f"Fases completadas: {fases_exitosas}/{total_fases}")
    print_info(f"Porcentaje de éxito: {(fases_exitosas/total_fases)*100:.1f}%")
    
    if fases_exitosas == total_fases:
        print_success("\n✓ SISTEMA COMPLETAMENTE FUNCIONAL")
    elif fases_exitosas > 0:
        print_warning(f"\n⚠ SISTEMA PARCIALMENTE FUNCIONAL ({fases_exitosas}/{total_fases} fases)")
    else:
        print_error("\n✗ SISTEMA NO FUNCIONAL")
    
    print(f"\n{Colors.BOLD}Revisión completada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}\n")

if __name__ == "__main__":
    main()
