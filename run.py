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
    # Obtener puerto del entorno o usar 5000 por defecto
    port = int(os.getenv('PORT', 5000))
    
    # Ejecutar en modo desarrollo
    print(f"🚀 Iniciando aplicación en modo {config_name}")
    print(f"🌐 Servidor corriendo en http://0.0.0.0:{port}")
    print(f"📊 Base de datos: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )
