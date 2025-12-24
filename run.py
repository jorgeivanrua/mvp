"""
Script para ejecutar la aplicación
"""
import os
from backend.app import create_app, socketio

# Obtener configuración del entorno
config_name = os.getenv('FLASK_ENV', 'development')

# Crear aplicación
app = create_app(config_name)

# En producción, verificar si la BD necesita inicializarse
if config_name == 'production':
    with app.app_context():
        from backend.database import db
        from backend.models.location import Location
        import os
        
        # Crear tablas si no existen
        db.create_all()
        
        # Verificar si hay datos
        try:
            departamentos_count = Location.query.filter_by(tipo='departamento').count()
            
            if departamentos_count == 0:
                print("⚠️  BD vacía. Ejecutando scripts de inicialización...")
                import subprocess
                import sys
                
                scripts = [
                    'scripts/init_db.py',
                    'scripts/load_divipola.py',
                    'scripts/create_fixed_users.py',
                    'scripts/init_configuracion_electoral.py'
                ]
                
                for script in scripts:
                    if os.path.exists(script):
                        print(f"Ejecutando {script}...")
                        subprocess.run([sys.executable, script])
                
                print("✅ BD inicializada")
            else:
                print(f"✅ BD OK ({departamentos_count} departamentos)")
            
            # Las migraciones ahora se manejan con Flask-Migrate (Alembic)
            # Para aplicar migraciones: flask db upgrade
            # Para crear nueva migración: flask db migrate -m "descripción"
        except Exception as e:
            print(f"⚠️  Error verificando BD: {e}")

if __name__ == '__main__':
    # Obtener puerto del entorno o usar 5000 por defecto
    port = int(os.getenv('PORT', 5000))
    host = '0.0.0.0'
    
    # Ejecutar en modo desarrollo
    print(f">> Iniciando aplicacion en modo {config_name}")
    print(f">> Servidor corriendo en http://localhost:{port}")
    print(f">> Base de datos: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f">> Accede a: http://localhost:{port}")
    
    try:
        app.run(
            host=host,
            port=port,
            debug=app.config['DEBUG'],
            use_reloader=False
        )
    except Exception as e:
        print(f"Error al iniciar servidor: {e}")
