"""
Script de inicialización para Render.com
Se ejecuta automáticamente en el despliegue
"""
import os
import sys
import subprocess

def print_header(text):
    """Imprimir encabezado"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def run_command(command, description):
    """Ejecutar un comando"""
    print(f">> {description}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {description} completado")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ Error en {description}")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {description}: {e}")
        return False

def main():
    """Función principal para Render"""
    print_header("RENDER.COM - INICIALIZACIÓN DEL SISTEMA")
    
    # Verificar que estamos en Render
    is_render = os.getenv('RENDER') == 'true'
    if is_render:
        print("✅ Entorno Render detectado")
    else:
        print("⚠️  No se detectó entorno Render, continuando de todos modos...")
    
    # Obtener DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print(f"✅ DATABASE_URL configurada")
        # Render usa postgres:// pero SQLAlchemy necesita postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
            os.environ['DATABASE_URL'] = database_url
            print("   Ajustado formato de URL para SQLAlchemy")
    else:
        print("⚠️  DATABASE_URL no configurada, usando SQLite local")
    
    # Configurar entorno de producción
    os.environ['FLASK_ENV'] = 'production'
    print("✅ Entorno configurado como 'production'")
    
    # PASO 1: Inicializar base de datos
    print_header("PASO 1: INICIALIZACIÓN DE BASE DE DATOS")
    if not run_command(
        f"{sys.executable} scripts/init_db.py",
        "Crear estructura de base de datos"
    ):
        print("❌ Error crítico en inicialización de BD")
        sys.exit(1)
    
    # PASO 2: Aplicar migraciones
    print_header("PASO 2: APLICACIÓN DE MIGRACIONES")
    migration_script = 'backend/migrations/apply_user_geolocation.py'
    if os.path.exists(migration_script):
        run_command(
            f"{sys.executable} {migration_script}",
            "Aplicar migración de geolocalización"
        )
    
    # PASO 3: Cargar ubicaciones (si existe el archivo)
    print_header("PASO 3: CARGA DE UBICACIONES")
    divipola_paths = [
        'todos los datos/divipola.csv',
        'divipola.csv',
        'data/divipola.csv'
    ]
    
    divipola_found = False
    for path in divipola_paths:
        if os.path.exists(path):
            print(f"✅ Archivo DIVIPOLA encontrado: {path}")
            divipola_found = True
            run_command(
                f"{sys.executable} scripts/load_divipola.py",
                "Cargar datos de ubicaciones"
            )
            break
    
    if not divipola_found:
        print("⚠️  Archivo DIVIPOLA no encontrado")
        print("   Las ubicaciones deberán cargarse manualmente después del despliegue")
    
    # PASO 4: Crear usuarios del sistema
    print_header("PASO 4: CREACIÓN DE USUARIOS")
    
    # Verificar si ya existen usuarios
    try:
        from backend.app import create_app
        from backend.database import db
        from backend.models.user import User
        
        app = create_app('production')
        with app.app_context():
            user_count = User.query.count()
            
            if user_count > 0:
                print(f"✅ Ya existen {user_count} usuarios en la base de datos")
                print("   Omitiendo creación de usuarios")
            else:
                print(">> No hay usuarios, creando usuarios del sistema...")
                run_command(
                    f"{sys.executable} scripts/create_fixed_users.py",
                    "Crear usuarios fijos"
                )
    except Exception as e:
        print(f"⚠️  Error verificando usuarios: {e}")
        print("   Intentando crear usuarios de todos modos...")
        run_command(
            f"{sys.executable} scripts/create_fixed_users.py",
            "Crear usuarios fijos"
        )
    
    # PASO 5: Configuración electoral
    print_header("PASO 5: CONFIGURACIÓN ELECTORAL")
    config_script = 'scripts/init_configuracion_electoral.py'
    if os.path.exists(config_script):
        run_command(
            f"{sys.executable} {config_script}",
            "Inicializar configuración electoral"
        )
    
    # RESUMEN
    print_header("INICIALIZACIÓN COMPLETADA")
    print("✅ El sistema está listo para funcionar en Render")
    print("\nCREDENCIALES DE ACCESO:")
    print("-" * 80)
    print("Usuario: admin")
    print("Password: admin123")
    print("-" * 80)
    print("\n⚠️  IMPORTANTE: Cambia las contraseñas después del primer acceso")
    print("=" * 80)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error en inicialización: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
