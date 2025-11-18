#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Revisión exhaustiva del rol Testigo Electoral
Prueba todos los endpoints, flujos y funcionalidades
"""
import requests
import json
import sys
from typing import Dict, Tuple

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:5000"

class RevisionTestigo:
    def __init__(self):
        self.token = None
        self.user_data = None
        self.ubicacion_data = None
        self.problemas = []
        self.exitos = []
    
    def log_exito(self, mensaje):
        """Registra un éxito"""
        self.exitos.append(mensaje)
        print(f"  ✓ {mensaje}")
    
    def log_problema(self, mensaje, severidad="MEDIA"):
        """Registra un problema"""
        self.problemas.append({"mensaje": mensaje, "severidad": severidad})
        icon = "🔴" if severidad == "CRÍTICA" else "🟠" if severidad == "ALTA" else "🟡"
        print(f"  {icon} {mensaje}")
    
    def test_login(self):
        """Prueba el login del testigo"""
        print("\n" + "="*80)
        print("1. PRUEBA DE LOGIN")
        print("="*80)
        
        login_data = {
            "rol": "testigo_electoral",
            "departamento_codigo": "44",
            "municipio_codigo": "01",
            "zona_codigo": "01",
            "puesto_codigo": "01",
            "password": "test123"
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.token = data.get('data', {}).get('access_token')
                    self.user_data = data.get('data', {}).get('user', {})
                    self.ubicacion_data = data.get('data', {}).get('ubicacion', {})
                    
                    self.log_exito(f"Login exitoso - Usuario: {self.user_data.get('nombre')}")
                    self.log_exito(f"Token obtenido: {self.token[:20]}...")
                    self.log_exito(f"Ubicación: {self.ubicacion_data.get('nombre_completo', 'N/A')}")
                    return True
                else:
                    self.log_problema(f"Login falló: {data.get('error')}", "CRÍTICA")
                    return False
            else:
                self.log_problema(f"Login HTTP {response.status_code}", "CRÍTICA")
                return False
        except Exception as e:
            self.log_problema(f"Error en login: {str(e)}", "CRÍTICA")
            return False
    
    def test_endpoint_info(self):
        """Prueba GET /api/testigo/info"""
        print("\n" + "="*80)
        print("2. PRUEBA DE ENDPOINT /info")
        print("="*80)
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{BASE_URL}/api/testigo/info",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    info = data.get('data', {})
                    user = info.get('user', {})
                    ubicacion = info.get('ubicacion', {})
                    
                    self.log_exito("Endpoint /info responde correctamente")
                    self.log_exito(f"Usuario ID: {user.get('id')}")
                    self.log_exito(f"Nombre: {user.get('nombre')}")
                    self.log_exito(f"Rol: {user.get('rol')}")
                    self.log_exito(f"Presencia verificada: {user.get('presencia_verificada')}")
                    
                    if ubicacion:
                        self.log_exito(f"Ubicación: {ubicacion.get('nombre_completo')}")
                        self.log_exito(f"Tipo: {ubicacion.get('tipo')}")
                    else:
                        self.log_problema("No hay datos de ubicación", "ALTA")
                    
                    return True
                else:
                    self.log_problema(f"Error en respuesta: {data.get('error')}", "ALTA")
                    return False
            else:
                self.log_problema(f"HTTP {response.status_code}: {response.text[:100]}", "ALTA")
                return False
        except Exception as e:
            self.log_problema(f"Error: {str(e)}", "ALTA")
            return False
    
    def test_endpoint_mesa(self):
        """Prueba GET /api/testigo/mesa"""
        print("\n" + "="*80)
        print("3. PRUEBA DE ENDPOINT /mesa")
        print("="*80)
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{BASE_URL}/api/testigo/mesa",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    mesa_data = data.get('data', {})
                    puesto = mesa_data.get('puesto', {})
                    mesas = mesa_data.get('mesas', [])
                    
                    self.log_exito("Endpoint /mesa responde correctamente")
                    self.log_exito(f"Puesto: {puesto.get('nombre_completo')}")
                    self.log_exito(f"Total de mesas: {len(mesas)}")
                    
                    if mesas:
                        for i, mesa in enumerate(mesas[:3], 1):
                            self.log_exito(f"  Mesa {i}: {mesa.get('nombre_completo')} - {mesa.get('total_votantes_registrados')} votantes")
                        if len(mesas) > 3:
                            self.log_exito(f"  ... y {len(mesas) - 3} mesas más")
                    else:
                        self.log_problema("No hay mesas asignadas", "MEDIA")
                    
                    return True
                else:
                    self.log_problema(f"Error en respuesta: {data.get('error')}", "ALTA")
                    return False
            else:
                self.log_problema(f"HTTP {response.status_code}: {response.text[:100]}", "ALTA")
                return False
        except Exception as e:
            self.log_problema(f"Error: {str(e)}", "ALTA")
            return False
    
    def test_endpoint_tipos_eleccion(self):
        """Prueba GET /api/testigo/tipos-eleccion"""
        print("\n" + "="*80)
        print("4. PRUEBA DE ENDPOINT /tipos-eleccion")
        print("="*80)
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{BASE_URL}/api/testigo/tipos-eleccion",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    tipos = data.get('data', [])
                    
                    self.log_exito("Endpoint /tipos-eleccion responde correctamente")
                    self.log_exito(f"Total de tipos de elección: {len(tipos)}")
                    
                    if tipos:
                        for i, tipo in enumerate(tipos[:5], 1):
                            self.log_exito(f"  {i}. {tipo.get('nombre')} ({tipo.get('codigo')})")
                        if len(tipos) > 5:
                            self.log_exito(f"  ... y {len(tipos) - 5} más")
                    else:
                        self.log_problema("No hay tipos de elección configurados", "ALTA")
                    
                    return True
                else:
                    self.log_problema(f"Error en respuesta: {data.get('error')}", "ALTA")
                    return False
            else:
                self.log_problema(f"HTTP {response.status_code}: {response.text[:100]}", "ALTA")
                return False
        except Exception as e:
            self.log_problema(f"Error: {str(e)}", "ALTA")
            return False
    
    def test_endpoint_partidos(self):
        """Prueba GET /api/testigo/partidos"""
        print("\n" + "="*80)
        print("5. PRUEBA DE ENDPOINT /partidos")
        print("="*80)
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{BASE_URL}/api/testigo/partidos",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    partidos = data.get('data', [])
                    
                    self.log_exito("Endpoint /partidos responde correctamente")
                    self.log_exito(f"Total de partidos: {len(partidos)}")
                    
                    if partidos:
                        for i, partido in enumerate(partidos[:5], 1):
                            nombre = partido.get('nombre')
                            nombre_corto = partido.get('nombre_corto')
                            color = partido.get('color', 'N/A')
                            self.log_exito(f"  {i}. {nombre} ({nombre_corto}) - Color: {color}")
                        if len(partidos) > 5:
                            self.log_exito(f"  ... y {len(partidos) - 5} más")
                    else:
                        self.log_problema("No hay partidos configurados", "ALTA")
                    
                    return True
                else:
                    self.log_problema(f"Error en respuesta: {data.get('error')}", "ALTA")
                    return False
            else:
                self.log_problema(f"HTTP {response.status_code}: {response.text[:100]}", "ALTA")
                return False
        except Exception as e:
            self.log_problema(f"Error: {str(e)}", "ALTA")
            return False
    
    def test_endpoint_profile(self):
        """Prueba GET /api/auth/profile"""
        print("\n" + "="*80)
        print("6. PRUEBA DE ENDPOINT /auth/profile")
        print("="*80)
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{BASE_URL}/api/auth/profile",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    profile = data.get('data', {})
                    user = profile.get('user', {})
                    ubicacion = profile.get('ubicacion', {})
                    
                    self.log_exito("Endpoint /auth/profile responde correctamente")
                    self.log_exito(f"Usuario: {user.get('nombre')}")
                    self.log_exito(f"Rol: {user.get('rol')}")
                    
                    if ubicacion:
                        self.log_exito(f"Ubicación: {ubicacion.get('nombre_completo')}")
                    
                    return True
                else:
                    self.log_problema(f"Error en respuesta: {data.get('error')}", "MEDIA")
                    return False
            else:
                self.log_problema(f"HTTP {response.status_code}", "MEDIA")
                return False
        except Exception as e:
            self.log_problema(f"Error: {str(e)}", "MEDIA")
            return False
    
    def test_verificar_presencia(self):
        """Prueba POST /api/auth/verificar-presencia"""
        print("\n" + "="*80)
        print("7. PRUEBA DE VERIFICAR PRESENCIA")
        print("="*80)
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                f"{BASE_URL}/api/auth/verificar-presencia",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    presencia = data.get('data', {})
                    
                    self.log_exito("Verificación de presencia exitosa")
                    self.log_exito(f"Presencia verificada: {presencia.get('presencia_verificada')}")
                    self.log_exito(f"Verificada en: {presencia.get('presencia_verificada_at')}")
                    
                    if presencia.get('coordinador_notificado'):
                        self.log_exito("Coordinador notificado")
                    
                    return True
                else:
                    self.log_problema(f"Error: {data.get('error')}", "MEDIA")
                    return False
            else:
                self.log_problema(f"HTTP {response.status_code}", "MEDIA")
                return False
        except Exception as e:
            self.log_problema(f"Error: {str(e)}", "MEDIA")
            return False
    
    def test_locations_mesas(self):
        """Prueba GET /api/locations/mesas"""
        print("\n" + "="*80)
        print("8. PRUEBA DE ENDPOINT /locations/mesas")
        print("="*80)
        
        if not self.ubicacion_data:
            self.log_problema("No hay datos de ubicación para probar", "MEDIA")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            params = {
                "departamento_codigo": self.ubicacion_data.get('departamento_codigo'),
                "municipio_codigo": self.ubicacion_data.get('municipio_codigo'),
                "zona_codigo": self.ubicacion_data.get('zona_codigo'),
                "puesto_codigo": self.ubicacion_data.get('puesto_codigo')
            }
            
            response = requests.get(
                f"{BASE_URL}/api/locations/mesas",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    mesas = data.get('data', [])
                    
                    self.log_exito("Endpoint /locations/mesas responde correctamente")
                    self.log_exito(f"Total de mesas: {len(mesas)}")
                    
                    if mesas:
                        for i, mesa in enumerate(mesas[:3], 1):
                            self.log_exito(f"  Mesa {i}: {mesa.get('nombre_completo')}")
                    
                    return True
                else:
                    self.log_problema(f"Error: {data.get('error')}", "MEDIA")
                    return False
            else:
                self.log_problema(f"HTTP {response.status_code}", "MEDIA")
                return False
        except Exception as e:
            self.log_problema(f"Error: {str(e)}", "MEDIA")
            return False
    
    def generar_reporte(self):
        """Genera reporte final"""
        print("\n" + "="*80)
        print("REPORTE FINAL - ROL TESTIGO ELECTORAL")
        print("="*80)
        
        total_pruebas = len(self.exitos) + len(self.problemas)
        exitos_count = len(self.exitos)
        problemas_count = len(self.problemas)
        
        print(f"\nTotal de pruebas: {total_pruebas}")
        print(f"Exitosas: {exitos_count}")
        print(f"Con problemas: {problemas_count}")
        print(f"Tasa de éxito: {(exitos_count / total_pruebas * 100):.1f}%")
        
        if self.problemas:
            print(f"\n🔴 PROBLEMAS ENCONTRADOS ({len(self.problemas)}):")
            
            criticos = [p for p in self.problemas if p['severidad'] == 'CRÍTICA']
            altos = [p for p in self.problemas if p['severidad'] == 'ALTA']
            medios = [p for p in self.problemas if p['severidad'] == 'MEDIA']
            
            if criticos:
                print(f"\n  CRÍTICOS ({len(criticos)}):")
                for p in criticos:
                    print(f"    🔴 {p['mensaje']}")
            
            if altos:
                print(f"\n  ALTOS ({len(altos)}):")
                for p in altos:
                    print(f"    🟠 {p['mensaje']}")
            
            if medios:
                print(f"\n  MEDIOS ({len(medios)}):")
                for p in medios:
                    print(f"    🟡 {p['mensaje']}")
        else:
            print("\n✅ ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        
        # Guardar reporte
        reporte = {
            "total_pruebas": total_pruebas,
            "exitos": exitos_count,
            "problemas": problemas_count,
            "tasa_exito": (exitos_count / total_pruebas * 100) if total_pruebas > 0 else 0,
            "detalles_exitos": self.exitos,
            "detalles_problemas": self.problemas
        }
        
        with open("revision_testigo_reporte.json", "w", encoding="utf-8") as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Reporte guardado en: revision_testigo_reporte.json")
    
    def ejecutar(self):
        """Ejecuta revisión completa"""
        print("="*80)
        print("REVISIÓN EXHAUSTIVA - ROL TESTIGO ELECTORAL")
        print("="*80)
        print(f"Base URL: {BASE_URL}")
        
        # Ejecutar pruebas
        if not self.test_login():
            print("\n❌ Login falló - No se pueden ejecutar más pruebas")
            self.generar_reporte()
            return
        
        self.test_endpoint_info()
        self.test_endpoint_mesa()
        self.test_endpoint_tipos_eleccion()
        self.test_endpoint_partidos()
        self.test_endpoint_profile()
        self.test_verificar_presencia()
        self.test_locations_mesas()
        
        self.generar_reporte()

if __name__ == "__main__":
    revision = RevisionTestigo()
    revision.ejecutar()
