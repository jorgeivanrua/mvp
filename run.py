"""
Script para ejecutar la aplicación
"""
import os
from backend.app import create_app
from backend.database import db

# Obtener configuración del entorno
config_name = os.getenv('FLASK_ENV', 'development')

# Crear aplicación
app = create_app(config_name)

# Inicializar BD si está vacía (solo en producción)
if config_name == 'production':
    with app.app_context():
        from backend.models.locations import Departamento
        
        # Crear tablas si no existen
        db.create_all()
        
        # Verificar si hay datos
        departamentos_count = Departamento.query.count()
        
        if departamentos_count == 0:
            print("⚠️  Base de datos vacía. Inicializando con datos de prueba...")
            try:
                import sys
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                from backend.scripts.load_complete_test_data import load_complete_test_data
                load_complete_test_data()
                print("✅ Base de datos inicializada correctamente")
            except Exception as e:
                print(f"❌ Error inicializando BD: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"✅ Base de datos OK ({departamentos_count} departamentos)")

if __name__ == '__main__':
    # Obtener puerto del entorno o usar 5000 por defecto
    port = int(os.getenv('PORT', 5000))
    
    # Ejecutar en modo desarrollo
    print(f">> Iniciando aplicacion en modo {config_name}")
    print(f">> Servidor corriendo en http://0.0.0.0:{port}")
    print(f">> Base de datos: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )
