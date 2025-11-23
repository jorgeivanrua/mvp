"""
Script para probar las correcciones del dashboard de testigo
"""
import os
import sys

def print_header(text):
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def check_file(filepath, description):
    """Verificar que un archivo existe"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {description}")
        print(f"   Ubicación: {filepath}")
        print(f"   Tamaño: {size} bytes")
        return True
    else:
        print(f"❌ {description} NO ENCONTRADO")
        print(f"   Esperado en: {filepath}")
        return False

def main():
    print_header("VERIFICACIÓN DE CORRECCIONES DEL DASHBOARD DE TESTIGO")
    
    all_ok = True
    
    # Verificar archivos creados
    print("1. ARCHIVOS DE CORRECCIÓN")
    print("-" * 80)
    
    files_to_check = [
        ('frontend/static/js/testigo-dashboard-fix.js', 'Archivo de parche JavaScript'),
        ('CORRECCION_ERRORES_TESTIGO.md', 'Documentación de errores'),
        ('RESUMEN_CORRECCIONES_TESTIGO.md', 'Resumen de correcciones')
    ]
    
    for filepath, description in files_to_check:
        if not check_file(filepath, description):
            all_ok = False
        print()
    
    # Verificar que el HTML incluye el parche
    print("\n2. VERIFICACIÓN DEL HTML")
    print("-" * 80)
    
    html_path = 'frontend/templates/testigo/dashboard.html'
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'testigo-dashboard-fix.js' in content:
            print("✅ El HTML incluye el archivo de parche")
            print("   Línea encontrada: testigo-dashboard-fix.js")
        else:
            print("❌ El HTML NO incluye el archivo de parche")
            print("   Debes agregar la línea en {% block extra_js %}")
            all_ok = False
    else:
        print(f"❌ Archivo HTML no encontrado: {html_path}")
        all_ok = False
    
    # Verificar contenido del parche
    print("\n3. VERIFICACIÓN DEL CONTENIDO DEL PARCHE")
    print("-" * 80)
    
    patch_path = 'frontend/static/js/testigo-dashboard-fix.js'
    if os.path.exists(patch_path):
        with open(patch_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ('window.showCreateForm', 'Sobrescritura de showCreateForm'),
            ('window.habilitarBotonNuevoFormulario', 'Sobrescritura de habilitarBotonNuevoFormulario'),
            ('window.formularios', 'Inicialización de variable formularios'),
            ('console.log', 'Logs de debugging')
        ]
        
        for check_str, description in checks:
            if check_str in content:
                print(f"✅ {description}")
            else:
                print(f"⚠️  {description} no encontrado")
    
    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)
    
    if all_ok:
        print("\n✅ TODAS LAS CORRECCIONES ESTÁN EN SU LUGAR")
        print("\nPróximos pasos:")
        print("1. Reinicia el servidor: python run.py")
        print("2. Accede como testigo: testigo_01_1 / testigo123")
        print("3. Abre la consola del navegador (F12)")
        print("4. Verifica que no haya errores rojos")
        print("5. Prueba el flujo completo:")
        print("   - Seleccionar mesa")
        print("   - Verificar presencia")
        print("   - Abrir nuevo formulario")
    else:
        print("\n⚠️  FALTAN ALGUNOS ARCHIVOS O CONFIGURACIONES")
        print("\nRevisa los items marcados con ❌ arriba")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
