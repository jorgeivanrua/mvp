#!/usr/bin/env python3
"""
Script para restaurar backup de la base de datos en Render
Ejecuta el archivo SQL de backup para recrear todos los datos
"""
import sys
import os
import sqlite3
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

def restaurar_desde_sql(backup_file):
    """Restaurar base de datos desde archivo SQL"""
    
    if not os.path.exists(backup_file):
        print(f"❌ Archivo de backup no encontrado: {backup_file}")
        return False
    
    print(f"📥 Restaurando desde: {backup_file}")
    
    try:
        from backend.app import create_app
        from backend.database import db
        
        app = create_app()
        with app.app_context():
            # Crear todas las tablas primero (por si acaso)
            db.create_all()
            
            # Leer y ejecutar el archivo SQL
            with open(backup_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Dividir en statements individuales
            statements = sql_content.split(';')
            
            print(f"📋 Ejecutando {len(statements)} statements SQL...")
            
            executed = 0
            for i, statement in enumerate(statements):
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        db.session.execute(statement)
                        executed += 1
                        
                        if executed % 100 == 0:
                            print(f"   ⏳ Ejecutados: {executed} statements...")
                            db.session.commit()
                            
                    except Exception as e:
                        if "already exists" not in str(e).lower():
                            print(f"⚠️  Warning en statement {i}: {e}")
            
            # Commit final
            db.session.commit()
            
            print(f"✅ Restauración completada: {executed} statements ejecutados")
            
            # Verificar datos restaurados
            from backend.models.user import User
            from backend.models.location import Location
            from backend.models.departamento_config import DepartamentoConfig
            
            usuarios = User.query.count()
            ubicaciones = Location.query.count()
            
            try:
                departamentos = DepartamentoConfig.query.count()
            except:
                departamentos = 0
            
            print(f"📊 Datos restaurados:")
            print(f"   👥 Usuarios: {usuarios}")
            print(f"   📍 Ubicaciones: {ubicaciones}")
            print(f"   🏛️  Departamentos: {departamentos}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error durante la restauración: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("❌ Uso: python scripts/restore_database.py <archivo_backup.sql>")
        print("💡 Ejemplo: python scripts/restore_database.py data/backup_electoral_20251217_160000.sql")
        sys.exit(1)
    
    backup_file = sys.argv[1]
    
    print("🚀 Restaurando base de datos electoral...")
    print("=" * 60)
    
    if restaurar_desde_sql(backup_file):
        print(f"\n🎉 Base de datos restaurada exitosamente!")
        print(f"💡 El sistema está listo para usar")
    else:
        print(f"\n❌ Error restaurando la base de datos")
        sys.exit(1)

if __name__ == '__main__':
    main()