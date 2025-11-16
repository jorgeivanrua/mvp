#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico completo de endpoints por rol - Versión 2
Usa los datos reales de la base de datos para hacer login
"""
import requests
import json
import sys
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.app import create_app

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:5000"

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
        self.app = create_app('development')
        self.usuarios_por_rol = {}
        
    def cargar_usuarios(self):
        """Carga usuarios de la base de datos"""
        with self.app.app_context():
            usuarios = User.query.filter_by(activo=True).all()
            
            for user in usuarios:
                if user.rol not in self.usuarios_por_rol:
                    self.usuarios_por_rol[user.rol] = []
                
                user_data = {
                    'id': user.id,
                    'nombre': user.nombre,
                    'rol': user.rol,
                    'password': 'test123'  # Contraseña conocida
                }
                
                # Obtener datos de ubicación
                if user.ubicacion_id:
                    location = Location.query.get(user.ubicacion_id)
                    if location:
                        user_data['ubicacion'] = {
                            'departamento_codigo': location.departamento_codigo,
                            'municipio_codigo': location.municipio_codigo,
                            'zona_codigo': location.zona_codigo,
                            'puesto_codigo': location.puesto_codigo,
                            'tipo': location.tipo
                        }
                
                self.usuarios_por_rol[user.rol].append(user_data)
    
    def construir_payload_login(self, user_data):
        """Construye el payload de login según el rol"""
        payload = {
            'rol': user_data['rol'],
            'password': user_data['password']
        }
        
        if 'ubicacion' in user_data:
            ub = user_data['ubicacion']
            if ub.get('departamento_codigo'):
                payload['departamento_codigo'] = ub['departamento_codigo']
            if ub.get('municipio_codigo'):
                payload['municipio_codigo'] = ub['municipio_codigo']
            if ub.get('zona_codigo'):
                payload['zona_codigo'] = ub['zona_codigo']
            if ub.get('puesto_codigo'):
                payload['puesto_codigo'] = ub['puesto_codigo']
        
        return payload
    
    def login(self, user_data):
        """Intenta hacer login y obtener token"""
        try:
            payload = self.construir_payload_login(user_data)
            
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token')
                if token:
                    return True, f"✓ Login exitoso", token
                else:
                    return False, f"✓ Login OK pero sin token en respuesta", None
            else:
                return False, f"✗ Login falló: {response.status_code} - {response.text[:100]}", None
        except Exception as e:
            return False, f"✗ Error en login: {str(e)[:100]}", None
    
    def probar_endpoint(self, token, metodo, endpoint):
        """Prueba un endpoint específico"""
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
    
    def diagnosticar_rol(self, rol):
        """Diagnostica todos los endpoints de un rol"""
        print(f"\n{'='*80}")
        print(f"ROL: {rol.upper().replace('_', ' ')}")
        print(f"{'='*80}")
        
        usuarios = self.usuarios_por_rol.get(rol, [])
        if not usuarios:
            print(f"⚠ No hay usuarios con rol {rol}")
            return
        
        # Usar el primer usuario del rol
        user_data = usuarios[0]
        print(f"\n1. LOGIN ({user_data['nombre']})")
        
        exito, mensaje, token = self.login(user_data)
        print(f"   {mensaje}")
        
        if not exito or not token:
            print(f"   ⚠ No se puede continuar sin login exitoso y token")
            return
        
        # Probar endpoints
        print(f"\n2. ENDPOINTS")
        endpoints = ENDPOINTS_POR_ROL.get(rol, [])
        
        if not endpoints:
            print(f"   ⚠ No hay endpoints configurados para probar")
            return
        
        resultados_rol = {
            "login": exito,
            "usuario": user_data['nombre'],
            "endpoints": {}
        }
        
        for metodo, endpoint in endpoints:
            exito_ep, mensaje_ep, data = self.probar_endpoint(token, metodo, endpoint)
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
        with open("diagnostico_endpoints_resultado_v2.json", "w", encoding="utf-8") as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Resultados detallados guardados en: diagnostico_endpoints_resultado_v2.json")
    
    def ejecutar(self):
        """Ejecuta diagnóstico completo"""
        print("="*80)
        print("DIAGNÓSTICO COMPLETO DE ENDPOINTS POR ROL - V2")
        print("="*80)
        print(f"Base URL: {BASE_URL}")
        
        print("\nCargando usuarios de la base de datos...")
        self.cargar_usuarios()
        print(f"Usuarios cargados: {sum(len(users) for users in self.usuarios_por_rol.values())}")
        print(f"Roles encontrados: {len(self.usuarios_por_rol)}")
        
        for rol in self.usuarios_por_rol.keys():
            self.diagnosticar_rol(rol)
        
        self.generar_resumen()

if __name__ == "__main__":
    diagnostico = DiagnosticoEndpoints()
    diagnostico.ejecutar()
