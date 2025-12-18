#!/usr/bin/env python3
"""
Script de inicialización para Render usando backup de BD
Restaura la base de datos completa desde un archivo de backup
"""
import sys
import os
import glob

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

def encontrar_backup_mas_reciente():
    """Encontrar el archivo de backup más reciente"""
    backup_patterns = [
        'data/backup_electoral_*.sql',
        'backup_electoral_*.sql',
        'data/electoral_backup.sql',
        'electoral_backup.sql'
    ]
    
    backup_files = []
    for pattern in backup_patterns:
        backup_files.extend(glob.glob(pattern))
    
    if not backup_files:
        return None
    
    # Ordenar por fecha de modificación (más reciente primero)
    backup_files.sort(key=os.path.getmtime, reverse=True)
    return backup_files[0]

def verificar_estado():
    """Verificar si ya hay datos cargados"""
    try:
        from backend.app import create_app
        from backend.models.user import User
        from backend.models.location import Location
        
        app = create_app()
        with app.app_context():
            usuarios = User.query.count()
            ubicaciones = Location.query.count()
            
            print(f"📊 Estado actual: {usuarios} usuarios, {ubicaciones} ubicaciones")
            
            if usuarios > 2 and ubicaciones > 0:
                print("✅ Sistema ya inicializado")
                return True
            return False
    except Exception as e:
        print(f"⚠️  Error verificando estado: {e}")
        return False

def main():
    """Inicialización usando backup"""
    print("🚀 Inicialización de Render usando backup de BD...")
    print("=" * 60)
    
    # Verificar estado actual
    if verificar_estado():
        print("ℹ️  No se requiere inicialización")
        return
    
    # Buscar archivo de backup
    backup_file = encontrar_backup_mas_reciente()
    
    if not backup_file:
        print("❌ No se encontró archivo de backup")
        print("💡 Archivos buscados:")
        print("   - data/backup_electoral_*.sql")
        print("   - backup_electoral_*.sql")
        print("   - data/electoral_backup.sql")
        print("   - electoral_backup.sql")
        print("\n💡 Crea un backup con: python scripts/backup_database.py")
        sys.exit(1)
    
    print(f"📁 Usando backup: {backup_file}")
    
    # Ejecutar restauración
    try:
        import subprocess
        
        result = subprocess.run([
            sys.executable, 'scripts/restore_database.py', backup_file
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Restauración completada exitosamente")
            print(result.stdout)
            
            # Verificar resultado
            if verificar_estado():
                print("\n🎉 ¡Sistema inicializado correctamente desde backup!")
            else:
                print("\n⚠️  Restauración completada pero faltan datos")
        else:
            print("❌ Error en la restauración")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error ejecutando restauración: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()