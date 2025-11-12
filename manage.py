"""
Script de gestión de la aplicación
"""
import os
from flask_migrate import Migrate, init, migrate, upgrade, downgrade
from backend.app import create_app
from backend.database import db

# Crear aplicación
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Configurar Flask-Migrate
migrate_instance = Migrate(app, db)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python manage.py [comando]")
        print("Comandos disponibles:")
        print("  init     - Inicializar migraciones")
        print("  migrate  - Crear nueva migración")
        print("  upgrade  - Aplicar migraciones")
        print("  downgrade - Revertir migración")
        sys.exit(1)
    
    command = sys.argv[1]
    
    with app.app_context():
        if command == 'init':
            init()
            print("✅ Migraciones inicializadas")
        elif command == 'migrate':
            message = sys.argv[2] if len(sys.argv) > 2 else "Auto migration"
            migrate(message=message)
            print(f"✅ Migración creada: {message}")
        elif command == 'upgrade':
            upgrade()
            print("✅ Migraciones aplicadas")
        elif command == 'downgrade':
            downgrade()
            print("✅ Migración revertida")
        else:
            print(f"❌ Comando desconocido: {command}")
            sys.exit(1)
