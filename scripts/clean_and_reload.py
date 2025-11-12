"""
Script para limpiar ubicaciones y recargar solo Caquetá
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.location import Location

app = create_app('development')

with app.app_context():
    print("\n>> Limpiando todas las ubicaciones...")
    try:
        count = Location.query.count()
        Location.query.delete()
        db.session.commit()
        print(f"   {count} ubicaciones eliminadas")
    except Exception as e:
        print(f"   Error: {e}")
        db.session.rollback()
    
    print("\n>> Verificando...")
    remaining = Location.query.count()
    print(f"   Ubicaciones restantes: {remaining}")
    
    if remaining == 0:
        print("\n>> Listo para recargar datos de Caqueta")
        print("   Ejecuta: .venv\\Scripts\\python.exe scripts\\load_divipola.py")
