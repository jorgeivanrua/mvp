"""
Revisión Completa del Sistema Electoral
Verifica endpoints, dashboards y genera reporte
"""
import requests
import json
from datetime import datetime

BASE_URL = 'http://127.0.0.1:5000'

class SistemaRevisor:
    def __init__(self):
        self.resultados = {
            'endpoints': {'ok': 0, 'fail': 0, 'detalles': []},
            'dashboards': {'ok': 0, 'fail': 0, 'detalles': []},
            'funcionalidades': {'ok': 0, 'fail': 0, 'detalles': []}
        }
        self.token = None
    
    def print_header(self, titulo):
        print("\n" + "="*80)
        print(titulo.center(80))
        print("="*80)
    
    def login(self):
        """Obtener token de autenticación"""
        try:
            response = requests.post(f'{BASE_URL}/api/auth/login', json={
                'rol': 'super_admin',
                'password': 'admin123'
            })
            
            if response.status_code == 200:
                self.token = response.json()['data']['access_token']
                print("✅ Login exitoso")
                return True
            else:
                print(f"❌ Login fallido: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error en login: {e}")
            return False
    
    def verificar_endpoint(self, method, path, requiere_auth=False, data=None):
        """Verificar un endpoint específico"""
        try:
            headers = {}
            if requiere_auth and self.token:
                headers['Authorization'] = f'Bearer {self.token}'
            
            if method == 'GET':
                response = requests.get(f'{BASE_URL}{path}', headers=headers)
            elif method == 'POST':
                headers['Content-Type'] = 'application/json'
                response = requests.post(f'{BASE_URL}{path}', json=data, headers=headers)
            
            success = response.status_code < 400
            
            resultado = {
                'endpoint': f'{method} {path}',
                'status': response.status_code,
                'success': success
            }
            
            if success:
                self.resultados['endpoints']['ok'] += 1
                print(f"✅ {method} {path} → {response.status_code}")
            else:
                self.resultados['endpoints']['fail'] += 1
                print(f"❌ {method} {path} → {response.status_code}")
            
            self.resultados['endpoints']['detalles'].append(resultado)
            return success
            
        except Exception as e:
            self.resultados['endpoints']['fail'] += 1
            print(f"❌ {method} {path} → Error: {e}")
            return False
    
    def verificar_dashboard(self, path, nombre):
        """Verificar que un dashboard carga"""
        try:
            response = requests.get(f'{BASE_URL}{path}')
            success = response.status_code == 200
            
            resultado = {
                'dashboard': nombre,
                'path': path,
                'status': response.status_code,
                'success': success
            }
            
            if success:
                # Verificar que contiene elementos básicos
                html = response.text
                tiene_bootstrap = 'bootstrap' in html.lower()
                tiene_contenido = len(html) > 1000
                
                if tiene_bootstrap and tiene_contenido:
                    self.resultados['dashboards']['ok'] += 1
                    print(f"✅ {nombre} ({path}) → OK")
                else:
                    self.resultados['dashboards']['fail'] += 1
                    print(f"⚠️  {nombre} ({path}) → Carga pero puede tener problemas")
            else:
                self.resultados['dashboards']['fail'] += 1
                print(f"❌ {nombre} ({path}) → {response.status_code}")
            
            self.resultados['dashboards']['detalles'].append(resultado)
            return success
            
        except Exception as e:
            self.resultados['dashboards']['fail'] += 1
            print(f"❌ {nombre} ({path}) → Error: {e}")
            return False
    
    def verificar_funcionalidad(self, nombre, funcion):
        """Verificar una funcionalidad específica"""
        try:
            resultado = funcion()
            
            if resultado:
                self.resultados['funcionalidades']['ok'] += 1
                print(f"✅ {nombre}")
            else:
                self.resultados['funcionalidades']['fail'] += 1
                print(f"❌ {nombre}")
            
            self.resultados['funcionalidades']['detalles'].append({
                'funcionalidad': nombre,
                'success': resultado
            })
            
            return resultado
        except Exception as e:
            self.resultados['funcionalidades']['fail'] += 1
            print(f"❌ {nombre} → Error: {e}")
            return False
    
    def revisar_endpoints_publicos(self):
        """Revisar endpoints públicos (sin autenticación)"""
        self.print_header("ENDPOINTS PÚBLICOS")
        
        self.verificar_endpoint('GET', '/api/locations/departamentos')
        self.verificar_endpoint('GET', '/api/locations/municipios')
        self.verificar_endpoint('GET', '/api/locations/municipios?departamento_codigo=44')
        self.verificar_endpoint('GET', '/api/locations/zonas')
        self.verificar_endpoint('GET', '/api/locations/zonas?municipio_codigo=01')
        self.verificar_endpoint('GET', '/api/locations/puestos')
        self.verificar_endpoint('GET', '/api/locations/puestos?zona_codigo=01')
    
    def revisar_endpoints_autenticados(self):
        """Revisar endpoints que requieren autenticación"""
        self.print_header("ENDPOINTS AUTENTICADOS")
        
        self.verificar_endpoint('GET', '/api/gestion-usuarios/departamentos', requiere_auth=True)
        self.verificar_endpoint('GET', '/api/gestion-usuarios/municipios', requiere_auth=True)
        self.verificar_endpoint('GET', '/api/gestion-usuarios/puestos', requiere_auth=True)
        self.verificar_endpoint('GET', '/api/locations/mesas?puesto_codigo=01', requiere_auth=True)
    
    def revisar_dashboards(self):
        """Revisar todos los dashboards"""
        self.print_header("DASHBOARDS")
        
        self.verificar_dashboard('/', 'Página Principal')
        self.verificar_dashboard('/auth/login', 'Login')
        self.verificar_dashboard('/testigo/dashboard', 'Dashboard Testigo')
        self.verificar_dashboard('/coordinador/puesto', 'Dashboard Coordinador Puesto')
        self.verificar_dashboard('/coordinador/municipal', 'Dashboard Coordinador Municipal')
        self.verificar_dashboard('/coordinador/departamental', 'Dashboard Coordinador Departamental')
        self.verificar_dashboard('/admin/dashboard', 'Dashboard Admin')
        self.verificar_dashboard('/admin/super-admin', 'Dashboard Super Admin')
        self.verificar_dashboard('/admin/gestion-usuarios', 'Gestión de Usuarios')
        self.verificar_dashboard('/auditor/dashboard', 'Dashboard Auditor')
    
    def revisar_funcionalidades(self):
        """Revisar funcionalidades clave"""
        self.print_header("FUNCIONALIDADES")
        
        # Verificar que hay datos DIVIPOLA
        def check_divipola():
            r = requests.get(f'{BASE_URL}/api/locations/departamentos')
            return r.status_code == 200 and len(r.json()['data']) > 0
        
        self.verificar_funcionalidad('Datos DIVIPOLA cargados', check_divipola)
        
        # Verificar que hay puestos
        def check_puestos():
            r = requests.get(f'{BASE_URL}/api/locations/puestos')
            return r.status_code == 200 and len(r.json()['data']) > 0
        
        self.verificar_funcionalidad('Puestos de votación disponibles', check_puestos)
        
        # Verificar archivos JavaScript
        def check_js_files():
            files = [
                '/static/js/api-client.js',
                '/static/js/utils.js',
                '/static/js/login-fixed.js'
            ]
            for file in files:
                r = requests.get(f'{BASE_URL}{file}')
                if r.status_code != 200:
                    return False
            return True
        
        self.verificar_funcionalidad('Archivos JavaScript disponibles', check_js_files)
    
    def generar_reporte(self):
        """Generar reporte final"""
        self.print_header("REPORTE FINAL")
        
        total_endpoints = self.resultados['endpoints']['ok'] + self.resultados['endpoints']['fail']
        total_dashboards = self.resultados['dashboards']['ok'] + self.resultados['dashboards']['fail']
        total_funcionalidades = self.resultados['funcionalidades']['ok'] + self.resultados['funcionalidades']['fail']
        
        print(f"\n📊 ENDPOINTS:")
        print(f"   Total: {total_endpoints}")
        print(f"   ✅ OK: {self.resultados['endpoints']['ok']}")
        print(f"   ❌ Fail: {self.resultados['endpoints']['fail']}")
        print(f"   📈 Éxito: {(self.resultados['endpoints']['ok']/total_endpoints*100):.1f}%")
        
        print(f"\n📊 DASHBOARDS:")
        print(f"   Total: {total_dashboards}")
        print(f"   ✅ OK: {self.resultados['dashboards']['ok']}")
        print(f"   ❌ Fail: {self.resultados['dashboards']['fail']}")
        print(f"   📈 Éxito: {(self.resultados['dashboards']['ok']/total_dashboards*100):.1f}%")
        
        print(f"\n📊 FUNCIONALIDADES:")
        print(f"   Total: {total_funcionalidades}")
        print(f"   ✅ OK: {self.resultados['funcionalidades']['ok']}")
        print(f"   ❌ Fail: {self.resultados['funcionalidades']['fail']}")
        print(f"   📈 Éxito: {(self.resultados['funcionalidades']['ok']/total_funcionalidades*100):.1f}%")
        
        total_ok = (self.resultados['endpoints']['ok'] + 
                   self.resultados['dashboards']['ok'] + 
                   self.resultados['funcionalidades']['ok'])
        total_all = total_endpoints + total_dashboards + total_funcionalidades
        
        print(f"\n🎯 RESULTADO GLOBAL:")
        print(f"   Total pruebas: {total_all}")
        print(f"   ✅ Exitosas: {total_ok}")
        print(f"   📈 Porcentaje: {(total_ok/total_all*100):.1f}%")
        
        if (total_ok/total_all) >= 0.9:
            print(f"\n🎉 SISTEMA EN EXCELENTE ESTADO")
        elif (total_ok/total_all) >= 0.7:
            print(f"\n✅ SISTEMA FUNCIONAL CON MEJORAS MENORES")
        else:
            print(f"\n⚠️  SISTEMA REQUIERE ATENCIÓN")
        
        # Guardar reporte en archivo
        with open('REPORTE_REVISION_SISTEMA.txt', 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("REPORTE DE REVISIÓN DEL SISTEMA ELECTORAL\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"ENDPOINTS: {self.resultados['endpoints']['ok']}/{total_endpoints} OK\n")
            for detalle in self.resultados['endpoints']['detalles']:
                status = "✅" if detalle['success'] else "❌"
                f.write(f"  {status} {detalle['endpoint']} → {detalle['status']}\n")
            
            f.write(f"\nDASHBOARDS: {self.resultados['dashboards']['ok']}/{total_dashboards} OK\n")
            for detalle in self.resultados['dashboards']['detalles']:
                status = "✅" if detalle['success'] else "❌"
                f.write(f"  {status} {detalle['dashboard']} ({detalle['path']}) → {detalle['status']}\n")
            
            f.write(f"\nFUNCIONALIDADES: {self.resultados['funcionalidades']['ok']}/{total_funcionalidades} OK\n")
            for detalle in self.resultados['funcionalidades']['detalles']:
                status = "✅" if detalle['success'] else "❌"
                f.write(f"  {status} {detalle['funcionalidad']}\n")
            
            f.write(f"\nRESULTADO GLOBAL: {(total_ok/total_all*100):.1f}% ({total_ok}/{total_all})\n")
        
        print(f"\n📄 Reporte guardado en: REPORTE_REVISION_SISTEMA.txt")
    
    def ejecutar_revision_completa(self):
        """Ejecutar revisión completa del sistema"""
        self.print_header("REVISIÓN COMPLETA DEL SISTEMA ELECTORAL")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"URL Base: {BASE_URL}")
        
        # Login
        self.print_header("AUTENTICACIÓN")
        if not self.login():
            print("\n❌ No se pudo autenticar. Algunas pruebas no se ejecutarán.")
        
        # Revisar componentes
        self.revisar_endpoints_publicos()
        self.revisar_endpoints_autenticados()
        self.revisar_dashboards()
        self.revisar_funcionalidades()
        
        # Generar reporte
        self.generar_reporte()

if __name__ == '__main__':
    revisor = SistemaRevisor()
    revisor.ejecutar_revision_completa()
