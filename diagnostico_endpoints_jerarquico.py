#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico usando sistema jerárquico de ubicaciones
"""
import requests
import json
import sys
from typing import Dict, List, Tuple

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:5000"

# Usuarios con ubicación jerárquica
USUARIOS_JERARQUICOS = {
    "super_admin": {
        "rol": "super_admin",
        "password": "test123",
        "descripcion": "Super Admin"
    },
    "admin_departamental": {
        "rol": "admin_departamental",
        "departamento_codigo": "44",
        "password": "test123",
        "descripcion": "Admin Departamental CAQUETA"
    },
    "admin_municipal": {
        "rol": "admin_municipal",
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "password": "test123",
        "descripcion": "Admin Municipal FLORENCIA"
    },
    "coordinador_departamental": {
        "rol": "coordinador_departamental",
        "departamento_codigo": "44",
        "password": "test123",
        "descripcion": "Coordinador Departamental CAQUETA"
    },
    "coordinador_municipal": {
        "rol": "coordinador_municipal",
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "password": "test123",
        "descripcion": "Coordinador Municipal FLORENCIA"
    },
    "coordinador_puesto": {
        "rol": "coordinador_puesto",
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "zona_codigo": "01",
        "puesto_codigo": "01",
        "password": "test123",
        "descripcion": "Coordinador Puesto 01"
    },
    "testigo_electoral": {
        "rol": "testigo_electoral",
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "zona_codigo": "01",
        "puesto_codigo": "01",
        "password": "test123",
        "descripcion": "Testigo Electoral Puesto 01"
    },
    "auditor_electoral": {
        "rol": "auditor_electoral",
        "departamento_codigo": "44",
        "password": "test123",
        "descripcion": "Auditor Electoral CAQUETA"
    }
}

# Endpoints críticos por rol
ENDPOINTS_POR_ROL = {
    "super_admin": [
        ("GET", "/api/super-admin/stats"),
        ("GET", "/api/super-admin/usuarios"),
        ("GET", "/api/super-admin/ubicaciones"),
    ],
    "admin_departamental": [
        ("GET", "/api/admin/stats"),
        ("GET", "/api/admin/usuarios"),
    ],
    "admin_municipal": [
        ("GET", "/api/admin-municipal/stats"),
    ],
    "coordinador_departamental": [
        ("GET", "/api/coordinador-departamental/stats"),
    ],
    "coordinador_municipal": [
        ("GET", "/api/coordinador-municipal/stats"),
        ("GET", "/api/coordinador-municipal/puestos"),
    ],
    "coordinador_puesto": [
        ("GET", "/api/coordinador-puesto/stats"),
        ("GET", "/api/coordinador-puesto/mesas"),
        ("GET", "/api/coordinador-puesto/incidentes"),
    ],
    "testigo_electoral": [
        ("GET", "/api/testigo/info"),
        ("GET", "/api/testigo/mesa"),
    ],
    "auditor_electoral": [
        ("GET", "/api/auditor/stats"),
    ]
}

class DiagnosticoJerarquico:
    def __init__(self):
        self.resultados = {}
        self.tokens = {}
    
    def login(self, rol: str, credenciales: Dict) -> Tuple[bool, str, Dict]:
        """Intenta hacer login con ubicación jerárquica"""
        try:
            # Preparar datos de login
            login_data = {
                "rol": credenciales["rol"],
                "password": credenciales["password"]
            }
            
            # Agregar códigos de ubicación si existen
            for key in ["departamento_codigo", "municipio_codigo", "zona_codigo", "puesto_codigo"]:
                if key in credenciales:
                    login_data[key] = credenciales[key]
            
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    token = data.get('data', {}).get('access_token')
                    user_data = data.get('data', {}).get('user', {})
                    self.tokens[rol] = token
                    return True, "OK Login exitoso", user_data
                else:
                    return False, f"X Login fallo: {data.get('error', 'Error desconocido')}", {}
            else:
                error_msg = response.text[:200]
                return False, f"X Login fallo ({response.status_code}): {error_msg}", {}
        except Exception as e:
            return False, f"X Error: {str(e)[:100]}", {}
    
    def probar_endpoint(self, rol: str, metodo: str, endpoint: str) -> Tuple[bool, str]:
        """Prueba un endpoint específico"""
        token = self.tokens.get(rol)
        if not token:
            return False, "Sin token"
        
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            if metodo == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
            else:
                return False, f"Metodo {metodo} no soportado"
            
            if response.status_code == 200:
                return True, "OK"
            elif response.status_code == 404:
                return False, "404 Not Found"
            elif response.status_code == 403:
                return False, "403 Forbidden"
            elif response.status_code == 401:
                return False, "401 Unauthorized"
            else:
                return False, f"{response.status_code}"
        except Exception as e:
            return False, f"Error: {str(e)[:30]}"
    
    def diagnosticar_rol(self, rol: str):
        """Diagnostica todos los endpoints de un rol"""
        print(f"\n{'='*80}")
        print(f"ROL: {rol.upper().replace('_', ' ')}")
        print(f"{'='*80}")
        
        credenciales = USUARIOS_JERARQUICOS.get(rol)
        if not credenciales:
            print(f"X No hay credenciales configuradas")
            return
        
        print(f"\n1. LOGIN - {credenciales['descripcion']}")
        
        # Mostrar datos de ubicación
        ubicacion_info = []
        if 'departamento_codigo' in credenciales:
            ubicacion_info.append(f"Depto: {credenciales['departamento_codigo']}")
        if 'municipio_codigo' in credenciales:
            ubicacion_info.append(f"Mun: {credenciales['municipio_codigo']}")
        if 'zona_codigo' in credenciales:
            ubicacion_info.append(f"Zona: {credenciales['zona_codigo']}")
        if 'puesto_codigo' in credenciales:
            ubicacion_info.append(f"Puesto: {credenciales['puesto_codigo']}")
        
        if ubicacion_info:
            print(f"   Ubicacion: {' | '.join(ubicacion_info)}")
        
        exito, mensaje, user_data = self.login(rol, credenciales)
        print(f"   {mensaje}")
        
        if exito and user_data:
            print(f"   Usuario: {user_data.get('nombre', 'N/A')}")
            print(f"   ID: {user_data.get('id', 'N/A')}")
        
        if not exito:
            print(f"   ! No se puede continuar sin login exitoso")
            self.resultados[rol] = {"login": False, "endpoints": {}}
            return
        
        # Probar endpoints
        print(f"\n2. ENDPOINTS")
        endpoints = ENDPOINTS_POR_ROL.get(rol, [])
        
        if not endpoints:
            print(f"   ! No hay endpoints configurados")
            self.resultados[rol] = {"login": True, "endpoints": {}}
            return
        
        resultados_endpoints = {}
        for metodo, endpoint in endpoints:
            exito_ep, mensaje_ep = self.probar_endpoint(rol, metodo, endpoint)
            status_icon = "OK" if exito_ep else "X"
            print(f"   [{status_icon}] {metodo:4} {endpoint:45} {mensaje_ep}")
            resultados_endpoints[endpoint] = {"exito": exito_ep, "mensaje": mensaje_ep}
        
        self.resultados[rol] = {"login": True, "endpoints": resultados_endpoints}
    
    def generar_resumen(self):
        """Genera resumen de resultados"""
        print(f"\n{'='*80}")
        print("RESUMEN GENERAL")
        print(f"{'='*80}\n")
        
        total_roles = len(self.resultados)
        roles_login_ok = sum(1 for r in self.resultados.values() if r.get("login"))
        
        total_endpoints = 0
        endpoints_ok = 0
        problemas = []
        
        for rol, resultado in self.resultados.items():
            if not resultado.get("login"):
                problemas.append(f"X {rol}: Login fallo")
                continue
            
            for endpoint, info in resultado.get("endpoints", {}).items():
                total_endpoints += 1
                if info["exito"]:
                    endpoints_ok += 1
                else:
                    problemas.append(f"X {rol} -> {endpoint}: {info['mensaje']}")
        
        print(f"Roles probados: {total_roles}")
        print(f"Roles con login OK: {roles_login_ok}/{total_roles}")
        print(f"Endpoints probados: {total_endpoints}")
        print(f"Endpoints funcionando: {endpoints_ok}/{total_endpoints}")
        
        if problemas:
            print(f"\n! PROBLEMAS ENCONTRADOS ({len(problemas)}):")
            for problema in problemas[:15]:
                print(f"  {problema}")
            if len(problemas) > 15:
                print(f"  ... y {len(problemas) - 15} mas")
        else:
            print(f"\nOK Todos los endpoints funcionan correctamente!")
        
        # Guardar resultados
        with open("diagnostico_jerarquico_resultado.json", "w", encoding="utf-8") as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        print(f"\nResultados guardados en: diagnostico_jerarquico_resultado.json")
    
    def ejecutar(self):
        """Ejecuta diagnóstico completo"""
        print("="*80)
        print("DIAGNOSTICO COMPLETO - SISTEMA JERARQUICO")
        print("="*80)
        print(f"Base URL: {BASE_URL}")
        print(f"Roles a probar: {len(USUARIOS_JERARQUICOS)}")
        
        for rol in USUARIOS_JERARQUICOS.keys():
            self.diagnosticar_rol(rol)
        
        self.generar_resumen()

if __name__ == "__main__":
    diagnostico = DiagnosticoJerarquico()
    diagnostico.ejecutar()
