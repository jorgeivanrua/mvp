"""
Script para verificar que todo está listo para deploy en Render
"""
import os
import sys

def check_file_exists(filepath, required=True):
    """Verificar si un archivo existe"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {filepath}")
    return exists

def check_executable(filepath):
    """Verificar si un archivo es ejecutable (en sistemas Unix)"""
    if os.name == 'nt':  # Windows
        print(f"ℹ️  {filepath} - Permisos de ejecución se configurarán en Render")
        return True
    else:
        is_exec = os.access(filepath, os.X_OK)
        status = "✅" if is_exec else "❌"
        print(f"{status} {filepath} - {'Ejecutable' if is_exec else 'No ejecutable'}")
        return is_exec

def main():
    print("🔍 Verificando preparación para deploy en Render...\n")
    
    all_good = True
    
    # Archivos requeridos
    print("📄 Archivos de configuración:")
    all_good &= check_file_exists("render.yaml")
    all_good &= check_file_exists("build.sh")
    all_good &= check_file_exists("requirements.txt")
    all_good &= check_file_exists("run.py")
    all_good &= check_file_exists("backend/config.py")
    
    print("\n📄 Scripts de inicialización:")
    all_good &= check_file_exists("scripts/init_db.py")
    all_good &= check_file_exists("scripts/load_divipola.py")
    all_good &= check_file_exists("scripts/create_test_users.py")
    all_good &= check_file_exists("scripts/init_configuracion_electoral.py")
    all_good &= check_file_exists("scripts/create_formularios_e14_tables.py")
    
    print("\n📊 Archivos de datos:")
    csv_found = False
    csv_locations = [
        "todos los datos/divipola.csv",
        "divipola.csv",
        "data/divipola.csv"
    ]
    for location in csv_locations:
        if check_file_exists(location, required=False):
            csv_found = True
            break
    
    if not csv_found:
        print("❌ No se encontró divipola.csv en ninguna ubicación")
        print("   Ubicaciones buscadas:")
        for loc in csv_locations:
            print(f"   - {loc}")
        all_good = False
    
    print("\n🔧 Permisos de ejecución:")
    check_executable("build.sh")
    
    print("\n📚 Documentación:")
    check_file_exists("DEPLOY_RENDER.md", required=False)
    check_file_exists("CAMBIOS_PARA_DEPLOY.md", required=False)
    check_file_exists("README.md", required=False)
    
    print("\n" + "="*60)
    if all_good:
        print("✅ TODO LISTO PARA DEPLOY")
        print("\nPróximos pasos:")
        print("1. git add .")
        print("2. git commit -m 'Preparado para deploy en Render'")
        print("3. git push")
        print("4. Ve a https://render.com y conecta tu repositorio")
        print("\n📖 Lee DEPLOY_RENDER.md para instrucciones detalladas")
    else:
        print("❌ HAY PROBLEMAS QUE RESOLVER")
        print("\nRevisa los archivos marcados con ❌ arriba")
        print("📖 Consulta DEPLOY_RENDER.md para más información")
    print("="*60)
    
    return 0 if all_good else 1

if __name__ == '__main__':
    sys.exit(main())
