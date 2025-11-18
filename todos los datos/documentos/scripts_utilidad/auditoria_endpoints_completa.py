#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditoría completa de endpoints - Revisa todos los endpoints existentes
"""
import os
import re
import json
from pathlib import Path

# Endpoints esperados por rol según diseño del sistema
ENDPOINTS_ESPERADOS = {
    "super_admin": {
        "prefix": "/api/super-admin",
        "endpoints": [
            ("GET", "/stats", "Estadísticas generales del sistema"),
            ("GET", "/usuarios", "Lista de todos los usuarios"),
            ("GET", "/ubicaciones", "Lista de todas las ubicaciones"),
            ("GET", "/partidos", "Lista de partidos políticos"),
            ("GET", "/tipos-eleccion", "Tipos de elección configurados"),
            ("POST", "/usuarios", "Crear nuevo usuario"),
            ("PUT", "/usuarios/<id>", "Actualizar usuario"),
            ("DELETE", "/usuarios/<id>", "Eliminar usuario"),
        ]
    },
    "admin_departamental": {
        "prefix": "/api/admin",
        "endpoints": [
            ("GET", "/stats", "Estadísticas del departamento"),
            ("GET", "/usuarios", "Usuarios del departamento"),
            ("GET", "/ubicaciones", "Ubicaciones del departamento"),
            ("GET", "/formularios", "Formularios del departamento"),
        ]
    },
    "admin_municipal": {
        "prefix": "/api/admin-municipal",
        "endpoints": [
            ("GET", "/stats", "Estadísticas del municipio"),
            ("GET", "/zonas", "Zonas del municipio"),
            ("GET", "/puestos", "Puestos del municipio"),
            ("GET", "/mesas", "Mesas del municipio"),
        ]
    },
    "coordinador_departamental": {
        "prefix": "/api/coordinador-departamental",
        "endpoints": [
            ("GET", "/stats", "Estadísticas departamentales"),
            ("GET", "/municipios", "Municipios del departamento"),
            ("GET", "/resumen", "Resumen de avance departamental"),
        ]
    },
    "coordinador_municipal": {
        "prefix": "/api/coordinador-municipal",
        "endpoints": [
            ("GET", "/stats", "Estadísticas municipales"),
            ("GET", "/zonas", "Zonas del municipio"),
            ("GET", "/puestos", "Puestos del municipio"),
            ("GET", "/mesas", "Mesas del municipio"),
            ("GET", "/formularios", "Formularios del municipio"),
        ]
    },
    "coordinador_puesto": {
        "prefix": "/api/coordinador-puesto",
        "endpoints": [
            ("GET", "/stats", "Estadísticas del puesto"),
            ("GET", "/mesas", "Mesas del puesto"),
            ("GET", "/testigos", "Testigos del puesto"),
            ("GET", "/incidentes", "Incidentes del puesto"),
            ("GET", "/formularios", "Formularios del puesto"),
        ]
    },
    "testigo_electoral": {
        "prefix": "/api/testigo",
        "endpoints": [
            ("GET", "/info", "Información del testigo"),
            ("GET", "/mesa", "Mesa asignada"),
            ("GET", "/tipos-eleccion", "Tipos de elección"),
            ("GET", "/partidos", "Partidos políticos"),
            ("GET", "/formularios", "Formularios del testigo"),
            ("POST", "/formularios", "Crear formulario"),
        ]
    },
    "auditor_electoral": {
        "prefix": "/api/auditor",
        "endpoints": [
            ("GET", "/stats", "Estadísticas de auditoría"),
            ("GET", "/inconsistencias", "Inconsistencias detectadas"),
            ("GET", "/reportes", "Reportes de auditoría"),
            ("GET", "/formularios", "Formularios para auditar"),
        ]
    }
}

def extraer_endpoints_de_archivo(filepath):
    """Extrae endpoints de un archivo de rutas"""
    endpoints = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar decoradores @bp.route
        pattern = r"@\w+_bp\.route\(['\"]([^'\"]+)['\"](?:,\s*methods=\[([^\]]+)\])?\)"
        matches = re.finditer(pattern, content)
        
        for match in matches:
            path = match.group(1)
            methods_str = match.group(2)
            
            if methods_str:
                methods = [m.strip().strip("'\"") for m in methods_str.split(',')]
            else:
                methods = ['GET']
            
            for method in methods:
                endpoints.append((method, path))
    
    except Exception as e:
        print(f"Error leyendo {filepath}: {e}")
    
    return endpoints

def analizar_blueprints():
    """Analiza todos los blueprints existentes"""
    routes_dir = Path("backend/routes")
    blueprints_encontrados = {}
    
    for filepath in routes_dir.glob("*.py"):
        if filepath.name == "__init__.py":
            continue
        
        filename = filepath.stem
        endpoints = extraer_endpoints_de_archivo(filepath)
        
        if endpoints:
            blueprints_encontrados[filename] = {
                "archivo": str(filepath),
                "endpoints": endpoints
            }
    
    return blueprints_encontrados

def generar_reporte():
    """Genera reporte completo de auditoría"""
    print("="*80)
    print("AUDITORÍA COMPLETA DE ENDPOINTS")
    print("="*80)
    
    blueprints = analizar_blueprints()
    
    print(f"\nBlueprints encontrados: {len(blueprints)}")
    for nombre, info in blueprints.items():
        print(f"  - {nombre}: {len(info['endpoints'])} endpoints")
    
    # Analizar por rol
    print(f"\n{'='*80}")
    print("ANÁLISIS POR ROL")
    print(f"{'='*80}")
    
    problemas = []
    endpoints_ok = 0
    endpoints_faltantes = 0
    
    for rol, config in ENDPOINTS_ESPERADOS.items():
        print(f"\n{rol.upper().replace('_', ' ')}")
        print(f"{'-'*80}")
        
        # Buscar blueprint correspondiente
        blueprint_name = None
        if rol == "super_admin":
            blueprint_name = "super_admin"
        elif rol == "admin_departamental":
            blueprint_name = "admin"
        elif rol == "admin_municipal":
            blueprint_name = "admin_municipal"
        elif rol == "coordinador_departamental":
            blueprint_name = "coordinador_departamental"
        elif rol == "coordinador_municipal":
            blueprint_name = "coordinador_municipal"
        elif rol == "coordinador_puesto":
            blueprint_name = "coordinador_puesto"
        elif rol == "testigo_electoral":
            blueprint_name = "testigo"
        elif rol == "auditor_electoral":
            blueprint_name = "auditor"
        
        if blueprint_name and blueprint_name in blueprints:
            endpoints_existentes = blueprints[blueprint_name]['endpoints']
            print(f"Blueprint: {blueprint_name}.py ✓")
            print(f"Endpoints encontrados: {len(endpoints_existentes)}")
        else:
            print(f"Blueprint: {blueprint_name}.py ✗ NO EXISTE")
            endpoints_existentes = []
            problemas.append({
                "tipo": "BLUEPRINT_FALTANTE",
                "rol": rol,
                "blueprint": blueprint_name,
                "descripcion": f"Crear archivo backend/routes/{blueprint_name}.py"
            })
        
        # Verificar cada endpoint esperado
        print(f"\nEndpoints esperados:")
        for metodo, path, descripcion in config['endpoints']:
            full_path = config['prefix'] + path
            encontrado = any(
                e[0] == metodo and (e[1] == path or e[1] == full_path)
                for e in endpoints_existentes
            )
            
            if encontrado:
                print(f"  ✓ {metodo:4} {full_path:50} {descripcion}")
                endpoints_ok += 1
            else:
                print(f"  ✗ {metodo:4} {full_path:50} {descripcion}")
                endpoints_faltantes += 1
                problemas.append({
                    "tipo": "ENDPOINT_FALTANTE",
                    "rol": rol,
                    "metodo": metodo,
                    "path": full_path,
                    "descripcion": descripcion
                })
    
    # Resumen
    print(f"\n{'='*80}")
    print("RESUMEN")
    print(f"{'='*80}")
    print(f"Endpoints funcionando: {endpoints_ok}")
    print(f"Endpoints faltantes: {endpoints_faltantes}")
    print(f"Total problemas: {len(problemas)}")
    
    # Generar lista de correcciones
    generar_lista_correcciones(problemas)
    
    # Guardar JSON
    with open("auditoria_endpoints.json", "w", encoding="utf-8") as f:
        json.dump({
            "blueprints": blueprints,
            "problemas": problemas,
            "resumen": {
                "endpoints_ok": endpoints_ok,
                "endpoints_faltantes": endpoints_faltantes,
                "total_problemas": len(problemas)
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Auditoría guardada en: auditoria_endpoints.json")

def generar_lista_correcciones(problemas):
    """Genera documento markdown con lista de correcciones"""
    with open("LISTA_CORRECCIONES_ENDPOINTS.md", "w", encoding="utf-8") as f:
        f.write("# Lista de Correcciones de Endpoints\n\n")
        f.write(f"**Fecha**: 2025-11-15\n")
        f.write(f"**Total de correcciones**: {len(problemas)}\n\n")
        
        # Agrupar por tipo
        blueprints_faltantes = [p for p in problemas if p["tipo"] == "BLUEPRINT_FALTANTE"]
        endpoints_faltantes = [p for p in problemas if p["tipo"] == "ENDPOINT_FALTANTE"]
        
        if blueprints_faltantes:
            f.write(f"## 🔴 Blueprints Faltantes ({len(blueprints_faltantes)})\n\n")
            for p in blueprints_faltantes:
                f.write(f"### {p['rol'].replace('_', ' ').title()}\n")
                f.write(f"- **Archivo**: `backend/routes/{p['blueprint']}.py`\n")
                f.write(f"- **Acción**: {p['descripcion']}\n\n")
        
        if endpoints_faltantes:
            f.write(f"## 🟠 Endpoints Faltantes ({len(endpoints_faltantes)})\n\n")
            
            # Agrupar por rol
            por_rol = {}
            for p in endpoints_faltantes:
                rol = p['rol']
                if rol not in por_rol:
                    por_rol[rol] = []
                por_rol[rol].append(p)
            
            for rol, endpoints in por_rol.items():
                f.write(f"### {rol.replace('_', ' ').title()} ({len(endpoints)} endpoints)\n\n")
                for p in endpoints:
                    f.write(f"- [ ] `{p['metodo']} {p['path']}` - {p['descripcion']}\n")
                f.write("\n")
    
    print(f"✓ Lista de correcciones guardada en: LISTA_CORRECCIONES_ENDPOINTS.md")

if __name__ == "__main__":
    generar_reporte()
