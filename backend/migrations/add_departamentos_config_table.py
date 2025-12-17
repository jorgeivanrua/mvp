"""
Migración para crear tabla de configuración de departamentos
"""
import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.database import db
from backend.models.departamento_config import DepartamentoConfig

def run_migration():
    """Ejecutar migración para crear tabla departamentos_config"""
    print("=" * 60)
    print("MIGRACIÓN: Crear tabla departamentos_config")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Crear tabla si no existe
            db.create_all()
            
            print("✅ Tabla departamentos_config creada exitosamente")
            
            # Verificar que la tabla existe
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'departamentos_config' in tables:
                print("✅ Tabla verificada en la base de datos")
                
                # Mostrar estructura de la tabla
                columns = inspector.get_columns('departamentos_config')
                print("\n📋 Estructura de la tabla:")
                for col in columns:
                    print(f"   • {col['name']}: {col['type']}")
                
                print(f"\n📊 Total de columnas: {len(columns)}")
            else:
                print("❌ Error: Tabla no encontrada después de la creación")
                return False
            
            print("\n" + "=" * 60)
            print("MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print("=" * 60)
            return True
            
        except Exception as e:
            print(f"❌ Error en la migración: {str(e)}")
            return False

if __name__ == '__main__':
    success = run_migration()
    sys.exit(0 if success else 1)