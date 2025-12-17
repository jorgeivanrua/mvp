#!/usr/bin/env python3
"""
Script para verificar la estructura de las tablas
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app import create_app
from backend.database import db

def verificar_tablas():
    """Verificar estructura de tablas"""
    
    app = create_app()
    with app.app_context():
        try:
            # Verificar si la tabla seguimiento_reportes existe
            result = db.session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='seguimiento_reportes'")
            tabla_existe = result.fetchone() is not None
            print(f'Tabla seguimiento_reportes existe: {tabla_existe}')
            
            # Verificar estructura de incidentes_delitos_fotos
            result = db.session.execute('PRAGMA table_info(incidentes_delitos_fotos)')
            columnas = result.fetchall()
            print(f'Columnas en incidentes_delitos_fotos:')
            for col in columnas:
                print(f'  - {col[1]} ({col[2]})')
                
            # Verificar todas las tablas disponibles
            result = db.session.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = result.fetchall()
            print(f'\nTablas disponibles:')
            for tabla in tablas:
                print(f'  - {tabla[0]}')
                
        except Exception as e:
            print(f'Error verificando tablas: {e}')

if __name__ == '__main__':
    verificar_tablas()