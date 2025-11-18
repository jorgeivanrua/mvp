#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDITORÍA PROFUNDA DEL SISTEMA ELECTORAL
Identifica todos los errores, inconsistencias y problemas
"""
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import json
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

errores = []
advertencias = []
info = []

def error(categoria, mensaje, archivo=None):
    errores.append({
        'categoria': categoria,
        'mensaje': mensaje,
        'archivo': archivo,
        'severidad': 'ERROR'
    })
    print(f"{Colors.RED}✗ ERROR [{categoria}]: {mensaje}{Colors.END}")
    if archivo:
        print(f"  Archivo: {archivo}")

def advertencia(categoria, mensaje, archivo=None):
    advertencias.append({
        'categoria': categoria,
        'mensaje': mensaje,
        'archivo': archivo,
        'severidad': 'WARNING'
    })
    print(f"{Colors.YELLOW}⚠ WARNING [{categoria}]: {mensaje}{Colors.END}")
    if archivo:
        print(f"  Archivo: {archivo}")

def info_msg(categoria, mensaje):
    info.append({
        'categoria': categoria,
        'mensaje': mensaje,
        'severidad': 'INFO'
    })
    print(f"{Colors.BLUE}ℹ INFO [{categoria}]: {mensaje}{Colors.END}")

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

print_header("AUDITORÍA PROFUNDA DEL SISTEMA ELECTORAL")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# 1. VERIFICAR ESTRUCTURA DE BASE DE DATOS
# ============================================================================

print_header("1. VERIFICACIÓN DE BASE DE DATOS")

try:
    from backend.database import db
    from backend.app import create_app
    from backend.models.user import User
    from backend.models.location import Location
    from backend.models.configuracion_electoral import TipoEleccion, Partido, Candidato
    from backend.models.formulario_e14 import FormularioE14
    from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
    
    app = create_app()
    app.app_context().push()
    
    # Verificar tablas
    print("Verificando tablas...")
    
    # Usuarios
    total_users = User.query.count()
    if total_users == 0:
        error("BD", "No hay usuarios en el sistema")
    else:
        info_msg("BD", f"Usuarios: {total_users}")
    
    # Ubicaciones
    departamentos = Location.query.filter_by(tipo='departamento').count()
    municipios = Location.query.filter_by(tipo='municipio').count()
    puestos = Location.query.filter_by(tipo='puesto').count()
    mesas = Location.query.filter_by(tipo='mesa').count()
    
    if departamentos == 0:
        error("BD", "No hay departamentos configurados")
    if municipios == 0:
        error("BD", "No hay municipios configurados")
    if puestos == 0:
        error("BD", "No hay puestos de votación configurados")
    if mesas == 0:
        error("BD", "No hay mesas configuradas")
    
    info_msg("BD", f"Ubicaciones: {departamentos} depts, {municipios} muns, {puestos} puestos, {mesas} mesas")
    
    # Configuración electoral
    tipos_eleccion = TipoEleccion.query.count()
    partidos = Partido.query.count()
    candidatos = Candidato.query.count()
    
    if tipos_eleccion == 0:
        error("BD", "No hay tipos de elección configurados")
    if partidos == 0:
        error("BD", "No hay partidos políticos configurados")
    if candidatos == 0:
        advertencia("BD", "No hay candidatos configurados")
    
    info_msg("BD", f"Electoral: {tipos_eleccion} tipos, {partidos} partidos, {candidatos} candidatos")
    
    # Formularios
    formularios = FormularioE14.query.count()
    info_msg("BD", f"Formularios E-14: {formularios}")
    
    # Incidentes y delitos
    incidentes = IncidenteElectoral.query.count()
    delitos = DelitoElectoral.query.count()
    info_msg("BD", f"Incidentes: {incidentes}, Delitos: {delitos}")
    
except Exception as e:
    error("BD", f"Error conectando a la base de datos: {str(e)}")

# ============================================================================
# 2. VERIFICAR INTEGRIDAD DE DATOS
# ============================================================================

print_header("2. INTEGRIDAD DE DATOS")

try:
    # Usuarios sin ubicación (excepto super_admin)
    users_sin_ubicacion = User.query.filter(
        User.ubicacion_id == None,
        User.rol != 'super_admin'
    ).all()
    
    if users_sin_ubicacion:
        for user in users_sin_ubicacion:
            error("INTEGRIDAD", f"Usuario sin ubicación: {user.nombre} ({user.rol})")
    
    # Usuarios con ubicación inválida
    users = User.query.filter(User.ubicacion_id != None).all()
    for user in users:
        ubicacion = Location.query.get(user.ubicacion_id)
        if not ubicacion:
            error("INTEGRIDAD", f"Usuario con ubicación inválida: {user.nombre} (ID: {user.ubicacion_id})")
    
    # Candidatos sin partido
    candidatos_sin_partido = Candidato.query.filter(
        Candidato.partido_id == None,
        Candidato.es_independiente == False
    ).all()
    
    if candidatos_sin_partido:
        for cand in candidatos_sin_partido:
            error("INTEGRIDAD", f"Candidato sin partido: {cand.nombre_completo}")
    
    # Candidatos sin tipo de elección
    candidatos_sin_tipo = Candidato.query.filter(Candidato.tipo_eleccion_id == None).all()
    if candidatos_sin_tipo:
        for cand in candidatos_sin_tipo:
            error("INTEGRIDAD", f"Candidato sin tipo de elección: {cand.nombre_completo}")
    
    # Mesas sin puesto padre
    mesas_huerfanas = Location.query.filter(
        Location.tipo == 'mesa',
        Location.parent_id == None
    ).all()
    
    if mesas_huerfanas:
        for mesa in mesas_huerfanas:
            advertencia("INTEGRIDAD", f"Mesa sin puesto padre: {mesa.nombre_completo}")
    
    info_msg("INTEGRIDAD", "Verificación de integridad completada")
    
except Exception as e:
    error("INTEGRIDAD", f"Error verificando integridad: {str(e)}")

# ============================================================================
# 3. VERIFICAR MODELOS
# ============================================================================

print_header("3. VERIFICACIÓN DE MODELOS")

try:
    # Verificar que los modelos tengan los métodos necesarios
    modelos = [
        (User, ['set_password', 'check_password', 'to_dict']),
        (Location, ['to_dict']),
        (TipoEleccion, ['to_dict']),
        (Partido, ['to_dict']),
        (Candidato, ['to_dict']),
        (FormularioE14, ['to_dict']),
        (IncidenteElectoral, ['to_dict']),
        (DelitoElectoral, ['to_dict'])
    ]
    
    for modelo, metodos in modelos:
        for metodo in metodos:
            if not hasattr(modelo, metodo):
                error("MODELO", f"{modelo.__name__} no tiene método {metodo}")
            else:
                info_msg("MODELO", f"{modelo.__name__}.{metodo} ✓")
    
except Exception as e:
    error("MODELO", f"Error verificando modelos: {str(e)}")

# ============================================================================
# 4. VERIFICAR ENDPOINTS
# ============================================================================

print_header("4. VERIFICACIÓN DE ENDPOINTS")

try:
    import requests
    
    BASE_URL = "http://localhost:5000"
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
        info_msg("ENDPOINT", "Servidor Flask está corriendo")
    except:
        error("ENDPOINT", "Servidor Flask no está corriendo")
        print("  Ejecuta: python backend/app.py")
    
    # Endpoints públicos
    endpoints_publicos = [
        ("GET", "/"),
        ("POST", "/api/auth/login"),
    ]
    
    for metodo, endpoint in endpoints_publicos:
        try:
            if metodo == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=2)
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", json={}, timeout=2)
            
            if response.status_code < 500:
                info_msg("ENDPOINT", f"{metodo} {endpoint} responde")
            else:
                error("ENDPOINT", f"{metodo} {endpoint} error 500")
        except Exception as e:
            error("ENDPOINT", f"{metodo} {endpoint} no responde: {str(e)}")
    
except Exception as e:
    advertencia("ENDPOINT", f"No se pudieron verificar endpoints: {str(e)}")

# ============================================================================
# 5. VERIFICAR ARCHIVOS CRÍTICOS
# ============================================================================

print_header("5. VERIFICACIÓN DE ARCHIVOS")

archivos_criticos = [
    "backend/app.py",
    "backend/database.py",
    "backend/models/user.py",
    "backend/models/location.py",
    "backend/models/configuracion_electoral.py",
    "backend/models/formulario_e14.py",
    "backend/models/incidentes_delitos.py",
    "backend/routes/auth.py",
    "backend/routes/testigo.py",
    "backend/routes/formularios_e14.py",
    "backend/routes/incidentes_delitos.py",
    "backend/services/auth_service.py",
    "backend/utils/decorators.py",
    "backend/utils/jwt_utils.py",
    "requirements.txt",
    ".env"
]

for archivo in archivos_criticos:
    if os.path.exists(archivo):
        info_msg("ARCHIVO", f"{archivo} ✓")
    else:
        if archivo == ".env":
            advertencia("ARCHIVO", f"{archivo} no existe (puede ser normal en desarrollo)")
        else:
            error("ARCHIVO", f"{archivo} no existe", archivo)

# ============================================================================
# 6. VERIFICAR CONFIGURACIÓN
# ============================================================================

print_header("6. VERIFICACIÓN DE CONFIGURACIÓN")

try:
    # Verificar variables de entorno críticas
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    vars_criticas = [
        'SECRET_KEY',
        'JWT_SECRET_KEY',
        'DATABASE_URL'
    ]
    
    for var in vars_criticas:
        valor = os.getenv(var)
        if not valor:
            advertencia("CONFIG", f"Variable de entorno {var} no está configurada")
        elif var.endswith('SECRET_KEY') and len(valor) < 32:
            advertencia("CONFIG", f"{var} es muy corta (< 32 caracteres)")
        else:
            info_msg("CONFIG", f"{var} configurada ✓")
    
except Exception as e:
    advertencia("CONFIG", f"Error verificando configuración: {str(e)}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print_header("RESUMEN DE AUDITORÍA")

print(f"\n{Colors.BOLD}Resultados:{Colors.END}")
print(f"{Colors.RED}Errores: {len(errores)}{Colors.END}")
print(f"{Colors.YELLOW}Advertencias: {len(advertencias)}{Colors.END}")
print(f"{Colors.BLUE}Info: {len(info)}{Colors.END}")

if errores:
    print(f"\n{Colors.BOLD}{Colors.RED}ERRORES CRÍTICOS:{Colors.END}")
    categorias = {}
    for e in errores:
        cat = e['categoria']
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(e)
    
    for cat, items in categorias.items():
        print(f"\n{Colors.BOLD}[{cat}] - {len(items)} errores:{Colors.END}")
        for item in items:
            print(f"  • {item['mensaje']}")
            if item.get('archivo'):
                print(f"    Archivo: {item['archivo']}")

if advertencias:
    print(f"\n{Colors.BOLD}{Colors.YELLOW}ADVERTENCIAS:{Colors.END}")
    categorias = {}
    for w in advertencias:
        cat = w['categoria']
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(w)
    
    for cat, items in categorias.items():
        print(f"\n{Colors.BOLD}[{cat}] - {len(items)} advertencias:{Colors.END}")
        for item in items:
            print(f"  • {item['mensaje']}")

# Guardar reporte
reporte = {
    'fecha': datetime.now().isoformat(),
    'errores': errores,
    'advertencias': advertencias,
    'info': info,
    'resumen': {
        'total_errores': len(errores),
        'total_advertencias': len(advertencias),
        'total_info': len(info)
    }
}

with open('REPORTE_AUDITORIA.json', 'w', encoding='utf-8') as f:
    json.dump(reporte, f, indent=2, ensure_ascii=False)

print(f"\n{Colors.GREEN}Reporte guardado en: REPORTE_AUDITORIA.json{Colors.END}")

# Estado final
if len(errores) == 0:
    print(f"\n{Colors.BOLD}{Colors.GREEN}✓ SISTEMA SIN ERRORES CRÍTICOS{Colors.END}")
elif len(errores) < 5:
    print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠ SISTEMA CON ERRORES MENORES{Colors.END}")
else:
    print(f"\n{Colors.BOLD}{Colors.RED}✗ SISTEMA CON ERRORES CRÍTICOS{Colors.END}")

print(f"\n{Colors.BOLD}Auditoría completada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}\n")
