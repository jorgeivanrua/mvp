#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Revisión completa de todos los roles del sistema
Prueba login y endpoints críticos para cada rol
"""
import requests
import json
import sys
from typing import Dict, List, Tuple

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:5000"

# Configuración de roles con sus endpoints críticos
ROLES_CONFIG = {
    "super_admin": {
        "login": {
            "rol": "super_admin",
            "password": "test123"
        },
        "endpoints": [
            ("GET", "/api/super-admin/stats", "Estadísticas generales"),
            ("GET", "/api/super-admin/usuarios", "Lista de usuarios"),
            ("GET", "/api/super-admin/ubicaciones", "Lista de ubicaciones"),
            ("GET", "/api/super-admin/partidos", "Lista de partidos"),
            ("GET", "/api/super-admin/tipos-eleccion", "Tipos de elección"),
        ]
    },
    "admin_departamental": {
        "login": {
            "rol": "admin_departamental",
            "departamento_codigo": "44",
            "password": "test123"
        },
        "endpoints": [
            ("GET", "/api/admin/stats", "Estadísticas departamentales"),
            ("GET", "/api/admin/usuarios", "Usuarios del departamento"),
            ("GET", "/api/admin/ubicaciones", "Ubicaciones del departamento"),
        ]
    },
    "admin_municipal": {
        "login": {
            "rol": "admin_municipal",
            "departamento_codigo": "44",
            "municipio_codigo": "01",
            "password": "test123"
        },
        "endpoints": [
            ("GET", "/api/admin-municipal/stats", "Estadísticas municipales"),
            ("GET", "/api/admin-municipal/zonas", "Zonas del municipio"),
            ("GET", "/api/admin-municipal/puestos", "Puestos del municipio"),
        ]
    },
    "coordinador_departamental": {
        "login": {
            "rol": "coordinador_departamental",
            "departamento_codigo": "44",
            "password": "test123"
        },
        "endpoints": [
            ("GET", "/api/coordinador-departamental/stats", "Estadísticas departamentales"),
            ("GET", "/api/coordinador-departamental/municipios", "Municipios del departamento"),
            ("GET", "/api/coordinador-departamental/resumen", "Resumen departamental"),
        ]
    },
    "coordinador_municipal": {
        "login": {
            "rol": "coordinador_municipal",
            "departamento_codigo": "44",
            "municipio_codigo": "01",
            "password": "test123"
        },
        "endpoints": [
            ("GET", "/api/coordinador-municipal/stats", "Estadísticas municipales"),
            ("GET", "/api/coordinador-municipal/zonas", "Zonas del municipio"),
            ("GET", "/api/coordinador-municipal/puestos", "Puestos del municipio"),
            ("GET", "/api/coordinador-municipal/mesas", "Mesas del municipio"),
        ]
    },
    "coordinador_puesto": {
        "login": {
            "rol": "coordinador_puesto",
            "departamento_codigo": "44",
            "municipio_codigo": "01",
            "zona_codigo": "01",
            "puesto_codigo": "01",
            "password": "test123"
        },
        "endpoints": [
            ("GET", "/api/coordinador-puesto/stats", "Estadísticas del puesto"),
            ("GET", "/api/coordinador-puesto/mesas", "Mesas del puesto"),
            ("GET", "/api/coordinador-puesto/testigos", "Testigos del puesto"),
            ("GET", "/api/coordinador-puesto/incidentes", "Incidentes del puesto"),
        ]
    },
    "testigo_electoral": {
        "login": {
            "rol": "testigo_electoral",
            "departamento_codigo": "44",
            "municipio_codigo": "01",
            "zona_codigo": "01",
            "puesto_codigo": "01",
            "password": "test123"
        },
        "endpoints": [
            ("GET", "/api/testigo/info", "Información del testigo"),
            ("GET", "/api/testigo/mesa", "Mesa asignada"),
            ("GET", "/api/testigo/tipos-eleccion", "Tipos de elección"),
            ("GET", "/api/testigo/partidos", "Partidos políticos"),
        ]
    },
    "auditor_electoral": {
        "login": {
            "rol": "auditor_electoral",
            "departamento_codigo": "44",
            "password": "test123"
        },
        "endpoints": [
            ("GET", "/api/auditor/stats", "Estadísticas de auditoría"),
            ("GET", "/api/auditor/inconsistencias", "Inconsistencias detectadas"),
            ("GET", "/api/auditor/reportes", "Reportes de auditoría"),
        ]
    }
}

class RevisionCompleta:
    def __init__(self):
        self.resultados = {}
        self.problemas = []
        self.tareas_pendientes = []
    
    def login(self, rol: str, credenciales: Dict) -> Tuple[bool, str, str]:
        """Intenta hacer login"""
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json=credenciales,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    token = data.get('data', {}).get('access_token')
                    user_name = data.get('data', {}).get('user', {}).get('nombre', 'N/A')
                    return True, user_name, token
                else:
                    error = data.get('error', 'Error desconocido')
                    self.problemas.append(f"Login {rol}: {error}")
                    return False, error, None
            else:
                error = f"HTTP {response.status_code}"
                self.problemas.append(f"Login {rol}: {error}")
                return False, error, None
        except Exception as e:
            error = str(e)[:100]
            self.problemas.append(f"Login {rol}: {error}")
            return False, error, None
    
    def probar_endpoint(self, token: str, metodo: str, endpoint: str) -> Tuple[bool, str]:
        """Prueba un endpoint"""
        if not token:
            return False, "Sin token"
        
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            if metodo == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
            elif metodo == "POST":
                response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json={}, timeout=10)
            else:
                return False, f"Método {metodo} no soportado"
            
            if response.status_code == 200:
                return True, "OK"
            elif response.status_code == 404:
                return False, "404 Not Found"
            elif response.status_code == 403:
                return False, "403 Forbidden"
            elif response.status_code == 401:
                return False, "401 Unauthorized"
            elif response.status_code == 500:
                return False, "500 Internal Error"
            else:
                return False, f"{response.status_code}"
        except Exception as e:
            return False, f"Error: {str(e)[:30]}"
    
    def revisar_rol(self, rol: str, config: Dict):
        """Revisa un rol completo"""
        print(f"\n{'='*80}")
        print(f"ROL: {rol.upper().replace('_', ' ')}")
        print(f"{'='*80}")
        
        # Login
        print(f"\n1. LOGIN")
        login_data = config['login']
        exito_login, user_name, token = self.login(rol, login_data)
        
        if exito_login:
            print(f"   ✓ OK - Usuario: {user_name}")
        else:
            print(f"   ✗ FALLO - {user_name}")
            self.tareas_pendientes.append({
                "prioridad": "ALTA",
                "rol": rol,
                "tipo": "LOGIN",
                "descripcion": f"Corregir login para {rol}: {user_name}"
            })
            self.resultados[rol] = {"login": False, "endpoints": {}}
            return
        
        # Endpoints
        print(f"\n2. ENDPOINTS")
        endpoints_ok = 0
        endpoints_total = len(config['endpoints'])
        endpoints_resultado = {}
        
        for metodo, endpoint, descripcion in config['endpoints']:
            exito, mensaje = self.probar_endpoint(token, metodo, endpoint)
            status = "✓" if exito else "✗"
            print(f"   [{status}] {metodo:4} {endpoint:50} {mensaje}")
            
            endpoints_resultado[endpoint] = {
                "exito": exito,
                "mensaje": mensaje,
                "descripcion": descripcion
            }
            
            if exito:
                endpoints_ok += 1
            else:
                # Agregar tarea pendiente
                if mensaje == "404 Not Found":
                    self.tareas_pendientes.append({
                        "prioridad": "ALTA",
                        "rol": rol,
                        "tipo": "ENDPOINT_FALTANTE",
                        "endpoint": endpoint,
                        "metodo": metodo,
                        "descripcion": f"Implementar {metodo} {endpoint} - {descripcion}"
                    })
                elif mensaje == "500 Internal Error":
                    self.tareas_pendientes.append({
                        "prioridad": "CRÍTICA",
                        "rol": rol,
                        "tipo": "ENDPOINT_ERROR",
                        "endpoint": endpoint,
                        "metodo": metodo,
                        "descripcion": f"Corregir error 500 en {metodo} {endpoint} - {descripcion}"
                    })
                else:
                    self.tareas_pendientes.append({
                        "prioridad": "MEDIA",
                        "rol": rol,
                        "tipo": "ENDPOINT_PROBLEMA",
                        "endpoint": endpoint,
                        "metodo": metodo,
                        "descripcion": f"Revisar {metodo} {endpoint} - {mensaje}"
                    })
        
        print(f"\n   Resumen: {endpoints_ok}/{endpoints_total} endpoints funcionando")
        
        self.resultados[rol] = {
            "login": True,
            "user_name": user_name,
            "endpoints": endpoints_resultado,
            "endpoints_ok": endpoints_ok,
            "endpoints_total": endpoints_total
        }
    
    def generar_resumen(self):
        """Genera resumen final"""
        print(f"\n{'='*80}")
        print("RESUMEN GENERAL")
        print(f"{'='*80}\n")
        
        total_roles = len(self.resultados)
        roles_login_ok = sum(1 for r in self.resultados.values() if r.get("login"))
        total_endpoints = sum(r.get("endpoints_total", 0) for r in self.resultados.values())
        endpoints_ok = sum(r.get("endpoints_ok", 0) for r in self.resultados.values())
        
        print(f"Roles probados: {total_roles}")
        print(f"Roles con login OK: {roles_login_ok}/{total_roles}")
        print(f"Endpoints probados: {total_endpoints}")
        print(f"Endpoints funcionando: {endpoints_ok}/{total_endpoints}")
        if total_endpoints > 0:
            print(f"Tasa de éxito: {(endpoints_ok/total_endpoints*100):.1f}%")
        else:
            print(f"Tasa de éxito: N/A (sin endpoints probados)")
        
        # Guardar resultados
        with open("revision_completa_resultado.json", "w", encoding="utf-8") as f:
            json.dump({
                "resultados": self.resultados,
                "tareas_pendientes": self.tareas_pendientes,
                "problemas": self.problemas
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Resultados guardados en: revision_completa_resultado.json")
    
    def generar_tareas_pendientes(self):
        """Genera documento de tareas pendientes"""
        print(f"\n{'='*80}")
        print("TAREAS PENDIENTES")
        print(f"{'='*80}\n")
        
        if not self.tareas_pendientes:
            print("✓ No hay tareas pendientes - Todo funciona correctamente!")
            return
        
        # Agrupar por prioridad
        criticas = [t for t in self.tareas_pendientes if t["prioridad"] == "CRÍTICA"]
        altas = [t for t in self.tareas_pendientes if t["prioridad"] == "ALTA"]
        medias = [t for t in self.tareas_pendientes if t["prioridad"] == "MEDIA"]
        
        print(f"Total de tareas: {len(self.tareas_pendientes)}")
        print(f"  - CRÍTICAS: {len(criticas)}")
        print(f"  - ALTAS: {len(altas)}")
        print(f"  - MEDIAS: {len(medias)}")
        
        # Mostrar tareas críticas
        if criticas:
            print(f"\n🔴 TAREAS CRÍTICAS ({len(criticas)}):")
            for i, tarea in enumerate(criticas, 1):
                print(f"  {i}. [{tarea['rol']}] {tarea['descripcion']}")
        
        # Mostrar tareas altas (máximo 10)
        if altas:
            print(f"\n🟠 TAREAS ALTAS ({len(altas)}):")
            for i, tarea in enumerate(altas[:10], 1):
                print(f"  {i}. [{tarea['rol']}] {tarea['descripcion']}")
            if len(altas) > 10:
                print(f"  ... y {len(altas) - 10} más")
        
        # Crear documento markdown
        self.crear_documento_tareas()
    
    def crear_documento_tareas(self):
        """Crea documento markdown con tareas pendientes"""
        with open("TAREAS_PENDIENTES_ROLES.md", "w", encoding="utf-8") as f:
            f.write("# Tareas Pendientes - Revisión Completa de Roles\n\n")
            f.write(f"**Fecha**: 2025-11-15\n\n")
            f.write(f"**Total de tareas**: {len(self.tareas_pendientes)}\n\n")
            
            # Agrupar por prioridad
            for prioridad in ["CRÍTICA", "ALTA", "MEDIA"]:
                tareas = [t for t in self.tareas_pendientes if t["prioridad"] == prioridad]
                if not tareas:
                    continue
                
                emoji = "🔴" if prioridad == "CRÍTICA" else "🟠" if prioridad == "ALTA" else "🟡"
                f.write(f"\n## {emoji} Prioridad {prioridad} ({len(tareas)} tareas)\n\n")
                
                # Agrupar por rol
                roles = {}
                for tarea in tareas:
                    rol = tarea['rol']
                    if rol not in roles:
                        roles[rol] = []
                    roles[rol].append(tarea)
                
                for rol, tareas_rol in roles.items():
                    f.write(f"\n### {rol.replace('_', ' ').title()}\n\n")
                    for i, tarea in enumerate(tareas_rol, 1):
                        f.write(f"{i}. **[{tarea['tipo']}]** {tarea['descripcion']}\n")
                        if 'endpoint' in tarea:
                            f.write(f"   - Endpoint: `{tarea['metodo']} {tarea['endpoint']}`\n")
                    f.write("\n")
        
        print(f"\n✓ Documento de tareas guardado en: TAREAS_PENDIENTES_ROLES.md")
    
    def ejecutar(self):
        """Ejecuta revisión completa"""
        print("="*80)
        print("REVISIÓN COMPLETA DE TODOS LOS ROLES")
        print("="*80)
        print(f"Base URL: {BASE_URL}")
        print(f"Roles a revisar: {len(ROLES_CONFIG)}")
        
        for rol, config in ROLES_CONFIG.items():
            self.revisar_rol(rol, config)
        
        self.generar_resumen()
        self.generar_tareas_pendientes()

if __name__ == "__main__":
    revision = RevisionCompleta()
    revision.ejecutar()
