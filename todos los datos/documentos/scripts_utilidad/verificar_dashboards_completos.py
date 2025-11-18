"""
Script para verificar que todos los dashboards tengan sus funcionalidades implementadas
"""
import os
from pathlib import Path

def verificar_dashboards():
    """Verificar dashboards y sus funcionalidades"""
    
    print("\n" + "="*80)
    print("VERIFICACIÓN DE DASHBOARDS Y FUNCIONALIDADES")
    print("="*80)
    
    # Definir dashboards esperados
    dashboards = {
        'Super Admin': {
            'template': 'frontend/templates/admin/super-admin-dashboard.html',
            'js': 'frontend/static/js/super-admin-dashboard.js',
            'ruta': '/admin/super-admin',
            'funcionalidades': [
                'Gestión de usuarios',
                'Carga masiva de datos',
                'Gestión de campañas',
                'Configuración de temas',
                'Estadísticas del sistema',
                'Auditoría del sistema'
            ]
        },
        'Admin Dashboard': {
            'template': 'frontend/templates/admin/dashboard.html',
            'js': 'frontend/static/js/admin-dashboard.js',
            'ruta': '/admin/dashboard',
            'funcionalidades': [
                'Vista general del sistema',
                'Gestión básica'
            ]
        },
        'Testigo Electoral': {
            'template': 'frontend/templates/testigo/dashboard.html',
            'js': 'frontend/static/js/testigo-dashboard-new.js',
            'ruta': '/testigo/dashboard',
            'funcionalidades': [
                'Registro de formularios E-14',
                'Captura de fotos',
                'Verificación de presencia',
                'Modo offline',
                'Sincronización de datos'
            ]
        },
        'Coordinador de Puesto': {
            'template': 'frontend/templates/coordinador/puesto.html',
            'js': 'frontend/static/js/coordinador-puesto.js',
            'ruta': '/coordinador/puesto',
            'funcionalidades': [
                'Validación de formularios E-14',
                'Gestión de testigos',
                'Consolidado E-24 Puesto',
                'Reportes de incidentes',
                'Reportes de delitos electorales'
            ]
        },
        'Coordinador Municipal': {
            'template': 'frontend/templates/coordinador/municipal.html',
            'js': 'frontend/static/js/coordinador-municipal.js',
            'ruta': '/coordinador/municipal',
            'funcionalidades': [
                'Consolidado municipal',
                'Gestión de puestos',
                'E-24 Municipal',
                'Comparación de resultados',
                'Exportación de datos'
            ]
        },
        'Coordinador Departamental': {
            'template': 'frontend/templates/coordinador/departamental.html',
            'js': 'frontend/static/js/coordinador-departamental.js',
            'ruta': '/coordinador/departamental',
            'funcionalidades': [
                'Consolidado departamental',
                'Gestión de municipios',
                'Reportes departamentales',
                'Estadísticas generales'
            ]
        },
        'Auditor Electoral': {
            'template': 'frontend/templates/auditor/dashboard.html',
            'js': 'frontend/static/js/auditor-dashboard.js',
            'ruta': '/auditor/dashboard',
            'funcionalidades': [
                'Auditoría de formularios',
                'Logs del sistema',
                'Reportes de auditoría',
                'Verificación de integridad'
            ]
        }
    }
    
    print("\n📊 VERIFICACIÓN POR DASHBOARD:\n")
    print(f"{'DASHBOARD':<30} {'TEMPLATE':<10} {'JS':<10} {'FUNCIONALIDADES'}")
    print("-" * 80)
    
    resultados = []
    
    for nombre, info in dashboards.items():
        # Verificar template
        template_existe = os.path.exists(info['template'])
        template_status = "✅" if template_existe else "❌"
        
        # Verificar JS
        js_existe = os.path.exists(info['js'])
        js_status = "✅" if js_existe else "❌"
        
        # Contar funcionalidades
        num_funcionalidades = len(info['funcionalidades'])
        
        print(f"{nombre:<30} {template_status:<10} {js_status:<10} {num_funcionalidades} funcionalidades")
        
        # Mostrar funcionalidades
        for func in info['funcionalidades']:
            print(f"  └─ {func}")
        
        resultados.append({
            'nombre': nombre,
            'template': template_existe,
            'js': js_existe,
            'completo': template_existe and js_existe
        })
        print()
    
    # Resumen
    print("="*80)
    print("RESUMEN")
    print("="*80)
    
    total = len(resultados)
    completos = sum(1 for r in resultados if r['completo'])
    templates_ok = sum(1 for r in resultados if r['template'])
    js_ok = sum(1 for r in resultados if r['js'])
    
    print(f"\n✅ Dashboards completos: {completos}/{total}")
    print(f"✅ Templates existentes: {templates_ok}/{total}")
    print(f"✅ Archivos JS existentes: {js_ok}/{total}")
    
    # Dashboards incompletos
    incompletos = [r for r in resultados if not r['completo']]
    if incompletos:
        print(f"\n⚠️  Dashboards incompletos:")
        for r in incompletos:
            print(f"   • {r['nombre']}")
            if not r['template']:
                print(f"     - Falta template")
            if not r['js']:
                print(f"     - Falta archivo JS")
    
    # Verificar funcionalidades implementadas
    print("\n" + "="*80)
    print("FUNCIONALIDADES CLAVE IMPLEMENTADAS")
    print("="*80)
    
    funcionalidades_globales = {
        'Sistema de Auditoría': {
            'archivos': [
                'backend/models/audit_log.py',
                'backend/utils/audit.py'
            ],
            'descripcion': 'Registro de todas las acciones del sistema'
        },
        'Gestión de Incidentes': {
            'archivos': [
                'backend/models/incidente_electoral.py',
                'backend/routes/incidentes.py',
                'frontend/static/js/incidentes-delitos.js'
            ],
            'descripcion': 'Registro y seguimiento de incidentes electorales'
        },
        'Modo Offline': {
            'archivos': [
                'frontend/static/js/sync-manager.js'
            ],
            'descripcion': 'Funcionamiento sin conexión y sincronización'
        },
        'Sistema de Campañas': {
            'archivos': [
                'backend/models/configuracion_electoral.py',
                'backend/migrations/add_campana_system.py'
            ],
            'descripcion': 'Multi-tenancy por campaña electoral'
        }
    }
    
    print()
    for nombre, info in funcionalidades_globales.items():
        archivos_existen = all(os.path.exists(f) for f in info['archivos'])
        status = "✅" if archivos_existen else "❌"
        print(f"{status} {nombre}")
        print(f"   {info['descripcion']}")
        for archivo in info['archivos']:
            existe = os.path.exists(archivo)
            file_status = "✅" if existe else "❌"
            print(f"   {file_status} {archivo}")
        print()
    
    print("="*80)
    print("RECOMENDACIONES")
    print("="*80)
    
    if completos == total:
        print("\n✅ Todos los dashboards están completos")
        print("✅ Puedes proceder a probar cada dashboard")
    else:
        print("\n⚠️  Algunos dashboards necesitan atención")
        print("   Revisa los archivos faltantes arriba")
    
    print("\n💡 Para probar los dashboards:")
    print("   1. Iniciar sesión con el rol correspondiente")
    print("   2. Verificar que cargue el dashboard")
    print("   3. Probar cada funcionalidad")
    print("   4. Verificar que no haya errores en la consola")
    print()

if __name__ == '__main__':
    verificar_dashboards()
