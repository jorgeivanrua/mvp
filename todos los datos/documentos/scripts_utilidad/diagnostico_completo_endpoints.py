#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico completo de endpoints por rol
Prueba todos los endpoints críticos para cada tipo de usuario
"""
import requests
import json
import sys
from typing import Dict, List, Tuple

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:5000"

# Usuarios de prueba por rol (nombres reales de la BD)
USUARIOS_TEST = {
    "super_admin": {"username": "Super Admin", "password": "test123", "rol": "super_admin"},
    "admin_departamental": {"username": "Admin Departamental Caquetá", "password": "test123", "rol": "admin_departamental"},
    "admin_municipal": {"username": "Admin Municipal Florencia", "password": "test123", "rol": "admin_municipal"},
    "coordinador_departamental": {"username": "Coordinador Departamental Caquetá", "password": "test123", "rol": "coordinador_departamental"},
    "coordinador_municipal": {"username": "Coordinador Municipal Florencia", "password": "test123", "rol": "coordinador_municipal"},
    "coordinador_puesto": {"username": "Coordinador Puesto 01", "password": "test123", "rol": "coordinador_puesto"},
    "testigo_electoral": {"username": "Testigo Electoral Puesto 01", "password": "test123", "rol": "testigo_electoral"},
    "auditor_electoral": {"username": "Auditor Electoral Caquetá", "password": "test123", "rol": "auditor_electoral"}
}

# Endpoints críticos por rol
ENDPOINTS_POR_ROL = {
    "super_admin": [
        ("GET", "/api/super-admin/stats"),
        ("GET", "/api/super-admin/usuarios"),
        ("GET", "/api/super-admin/ubicaciones"),
        ("GET", "/api/super-admin/partidos"),
        ("GET", "/api/super-admin/tipos-eleccion"),
    ],
    "admin_departamental": [
        ("GET", "/api/admin/stats"),
        ("GET", "/api/admin/usuarios"),
        ("GET", "/api/admin/ubicaciones"),
        ("GET", "/api/resultados/departamento"),
    ],
    "admin_municipal": [
        ("GET", "/api/admin-municipal/stats"),
        ("GET", "/api/admin-municipal/zonas"),
        ("GET", "/api/admin-municipal/puestos"),
    ],
    "coordinador_departamental": [
        ("GET", "/api/coordinador-departamental/stats"),
        ("GET", "/api/coordinador-departamental/municipios"),
        ("GET", "/api/coordinador-departamental/resumen"),
    ],
    "coordinador_municipal": [
        ("GET", "/api/coordinador-municipal/stats"),
        ("GET", "/api/coordinador-municipal/zonas"),
        ("GET", "/api/coordinador-municipal/puestos"),
        ("GET", "/api/coordinador-municipal/mesas"),
    ],
    "coordinador_puesto": [
        ("GET", "/api/coordinador-puesto/stats"),
        ("GET", "/api/coordinador-puesto/mesas"),
        ("GET", "/api/coordinador-puesto/testigos"),
        ("GET", "/api/coordinador-puesto/incidentes"),
    ],
    "testigo_electoral": [
        ("GET", "/api/testigo/info"),
        ("GET", "/api/testigo/mesa"),
        ("GET", "/api/testigo/tipos-eleccion"),
        ("GET", "/api/testigo/partidos"),
    ],
    "auditor_electoral": [
        ("GET", "/api/auditor/stats"),
        ("GET", "/api/auditor/inconsistencias"),
        ("GET", "/api/auditor/reportes"),
    ]
}

class DiagnosticoEndpoints:
    def __init__(self):
        self.resultados = {}
        self.tokens = {}
    
    def login(self, rol: str, credenciales: Dict) -> Tuple[bool, str]:
        """Intenta hacer login y obtener token"""
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json=credenciales,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token')
                self.tokens[rol] = token
                return True, f"✓ Login exitoso"
            else:
                return False, f"✗ Login falló: {response.status_code} - {response.text[:100]}"
        except Exception as e:
            return False, f"✗ Error en login: {str(e)}"
    
    def probar_endpoint(self, rol: str, metodo: str, endpoint: str) -> Tuple[bool, str, Dict]:
        """Prueba un endpoint específico"""
        token = self.tokens.get(rol)
        if not token:
            return False, "Sin token", {}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            if metodo == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
            elif metodo == "POST":
                response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json={}, timeout=10)
            else:
                return False, f"Método {metodo} no soportado", {}
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return True, f"✓ OK ({len(str(data))} bytes)", data
                except:
                    return True, f"✓ OK (respuesta no-JSON)", {}
            elif response.status_code == 404:
                return False, "✗ 404 Not Found", {}
            elif response.status_code == 403:
                return False, "✗ 403 Forbidden", {}
            elif response.status_code == 401:
                return False, "✗ 401 Unauthorized", {}
            else:
                return False, f"✗ {response.status_code}: {response.text[:100]}", {}
        except requests.exceptions.Timeout:
            return False, "✗ Timeout", {}
        except Exception as e:
            return False, f"✗ Error: {str(e)[:50]}", {}
    
    def diagnosticar_rol(self, rol: str):
        """Diagnostica todos los endpoints de un rol"""
        print(f"\n{'='*80}")
        print(f"ROL: {rol.upper().replace('_', ' ')}")
        print(f"{'='*80}")
        
        # Login
        credenciales = USUARIOS_TEST.get(rol)
        if not credenciales:
            print(f"✗ No hay credenciales configuradas para {rol}")
            return
        
        print(f"\n1. LOGIN ({credenciales['username']})")
        exito, mensaje = self.login(rol, credenciales)
        print(f"   {mensaje}")
        
        if not exito:
            print(f"   ⚠ No se puede continuar sin login exitoso")
            return
        
        # Probar endpoints
        print(f"\n2. ENDPOINTS")
        endpoints = ENDPOINTS_POR_ROL.get(rol, [])
        
        if not endpoints:
            print(f"   ⚠ No hay endpoints configurados para probar")
            return
        
        resultados_rol = {
            "login": exito,
            "endpoints": {}
        }
        
        for metodo, endpoint in endpoints:
            exito_ep, mensaje_ep, data = self.probar_endpoint(rol, metodo, endpoint)
            print(f"   {metodo:4} {endpoint:50} {mensaje_ep}")
            
            resultados_rol["endpoints"][endpoint] = {
                "exito": exito_ep,
                "mensaje": mensaje_ep,
                "tiene_datos": bool(data)
            }
        
        self.resultados[rol] = resultados_rol
    
    def generar_resumen(self):
        """Genera resumen de resultados"""
        print(f"\n{'='*80}")
        print("RESUMEN GENERAL")
        print(f"{'='*80}\n")
        
        total_roles = len(self.resultados)
        roles_ok = 0
        total_endpoints = 0
        endpoints_ok = 0
        
        problemas = []
        
        for rol, resultado in self.resultados.items():
            if not resultado.get("login"):
                problemas.append(f"❌ {rol}: Login falló")
                continue
            
            roles_ok += 1
            endpoints = resultado.get("endpoints", {})
            
            for endpoint, info in endpoints.items():
                total_endpoints += 1
                if info["exito"]:
                    endpoints_ok += 1
                else:
                    problemas.append(f"❌ {rol} -> {endpoint}: {info['mensaje']}")
        
        print(f"Roles probados: {total_roles}")
        print(f"Roles con login OK: {roles_ok}/{total_roles}")
        print(f"Endpoints probados: {total_endpoints}")
        print(f"Endpoints funcionando: {endpoints_ok}/{total_endpoints}")
        
        if problemas:
            print(f"\n⚠ PROBLEMAS ENCONTRADOS ({len(problemas)}):")
            for problema in problemas[:20]:  # Mostrar máximo 20
                print(f"  {problema}")
            if len(problemas) > 20:
                print(f"  ... y {len(problemas) - 20} más")
        else:
            print(f"\n✓ ¡Todos los endpoints funcionan correctamente!")
        
        # Guardar resultados detallados
        with open("diagnostico_endpoints_resultado.json", "w", encoding="utf-8") as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Resultados detallados guardados en: diagnostico_endpoints_resultado.json")
    
    def ejecutar(self):
        """Ejecuta diagnóstico completo"""
        print("="*80)
        print("DIAGNÓSTICO COMPLETO DE ENDPOINTS POR ROL")
        print("="*80)
        print(f"Base URL: {BASE_URL}")
        print(f"Roles a probar: {len(USUARIOS_TEST)}")
        
        for rol in USUARIOS_TEST.keys():
            self.diagnosticar_rol(rol)
        
        self.generar_resumen()

if __name__ == "__main__":
    diagnostico = DiagnosticoEndpoints()
    diagnostico.ejecutar()
