"""
Script para ejecutar la aplicación
"""
import os
from backend.app import create_app

# Obtener configuración del entorno
config_name = os.getenv('FLASK_ENV', 'development')

# Crear aplicación
app = create_app(config_name)

if __name__ == '__main__':
    # Ejecutar en modo desarrollo
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
