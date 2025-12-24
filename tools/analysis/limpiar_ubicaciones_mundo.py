#!/usr/bin/env python3
"""
Script para limpiar TODAS las ubicaciones y cargar SOLO Quindío
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.database import db
from backend.models.location import Location
from backend.models.user import User

def limpiar_y_cargar_quindio():
    app = create_app()
    
    with app.app_context():
        print("[*] Limpiando TODAS las ubicaciones...")
        
        # Contar ubicaciones antes
        total_antes = Location.query.count()
        print(f"    Ubicaciones en BD: {total_antes}")
        
        # Eliminar todas las ubicaciones
        Location.query.delete()
        db.session.commit()
        
        print(f"    [OK] Ubicaciones eliminadas")
        
        # Verificar que se eliminaron
        total_despues = Location.query.count()
        print(f"    Ubicaciones restantes: {total_despues}")
        
        print()
        print("[*] Ahora cargando SOLO Quindío...")
        print("    La próxima vez que accedas a la API de ubicaciones,")
        print("    se cargará SOLO Quindío (código 26) desde divipola.csv")
        print()
        print("[OK] BD limpia - lista para cargar Quindío")

if __name__ == '__main__':
    limpiar_y_cargar_quindio()
