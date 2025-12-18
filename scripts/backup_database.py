#!/usr/bin/env python3
"""
Script para crear backup de la base de datos SQLite
Genera un archivo SQL con todos los datos para restaurar en Render
"""
import sys
import os
import sqlite3
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

def crear_backup_sql():
    """Crear backup SQL de la base de datos"""
    
    # Buscar la base de datos
    db_paths = [
        'instance/electoral.db',
        'electoral.db',
        'backend/instance/electoral.db'
    ]
    
    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("❌ No se encontró la base de datos SQLite")
        return False
    
    print(f"📊 Creando backup desde: {db_path}")
    
    # Crear nombre del archivo de backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"data/backup_electoral_{timestamp}.sql"
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        
        # Crear el archivo SQL
        with open(backup_filename, 'w', encoding='utf-8') as f:
            # Escribir header
            f.write("-- Backup de Base de Datos Electoral\n")
            f.write(f"-- Creado: {datetime.now().isoformat()}\n")
            f.write("-- Archivo: backup_electoral.sql\n\n")
            
            f.write("-- Desactivar verificaciones de claves foráneas\n")
            f.write("PRAGMA foreign_keys=OFF;\n\n")
            
            # Obtener todas las tablas
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = cursor.fetchall()
            
            print(f"📋 Tablas encontradas: {len(tables)}")
            
            for (table_name,) in tables:
                print(f"   📄 Procesando tabla: {table_name}")
                
                # Obtener estructura de la tabla
                cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
                create_sql = cursor.fetchone()[0]
                
                f.write(f"-- Tabla: {table_name}\n")
                f.write(f"DROP TABLE IF EXISTS {table_name};\n")
                f.write(f"{create_sql};\n\n")
                
                # Obtener datos de la tabla
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()
                
                if rows:
                    # Obtener nombres de columnas
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns_info = cursor.fetchall()
                    column_names = [col[1] for col in columns_info]
                    
                    f.write(f"-- Datos de {table_name} ({len(rows)} registros)\n")
                    
                    for row in rows:
                        # Escapar valores NULL y strings
                        values = []
                        for value in row:
                            if value is None:
                                values.append('NULL')
                            elif isinstance(value, str):
                                # Escapar comillas simples
                                escaped_value = value.replace("'", "''")
                                values.append(f"'{escaped_value}'")
                            else:
                                values.append(str(value))
                        
                        columns_str = ', '.join(column_names)
                        values_str = ', '.join(values)
                        f.write(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});\n")
                    
                    f.write("\n")
            
            f.write("-- Reactivar verificaciones de claves foráneas\n")
            f.write("PRAGMA foreign_keys=ON;\n")
            f.write("\n-- Fin del backup\n")
        
        conn.close()
        
        # Verificar tamaño del archivo
        file_size = os.path.getsize(backup_filename)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"✅ Backup creado exitosamente:")
        print(f"   📁 Archivo: {backup_filename}")
        print(f"   📊 Tamaño: {file_size_mb:.2f} MB")
        print(f"   📋 Tablas: {len(tables)}")
        
        return backup_filename
        
    except Exception as e:
        print(f"❌ Error creando backup: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Creando backup de la base de datos electoral...")
    print("=" * 60)
    
    backup_file = crear_backup_sql()
    
    if backup_file:
        print(f"\n🎉 Backup completado exitosamente!")
        print(f"💡 Para restaurar en Render, usa: python scripts/restore_database.py {backup_file}")
    else:
        print(f"\n❌ Error creando el backup")
        sys.exit(1)

if __name__ == '__main__':
    main()