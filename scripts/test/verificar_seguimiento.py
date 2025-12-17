#!/usr/bin/env python3
"""
Script para verificar la estructura de la tabla seguimiento_reportes
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app import create_app
from backend.database import db

def verificar_seguimiento():
    """Verificar estructura de tabla seguimiento_reportes"""
    
    app = create_app()
    with app.app_context():
        try:
            # Verificar estructura de seguimiento_reportes
            result = db.session.execute('PRAGMA table_info(seguimiento_reportes)')
            columnas = result.fetchall()
            print(f'Columnas en seguimiento_reportes:')
            for col in columnas:
                print(f'  - {col[1]} ({col[2]})')
                
            # Contar registros
            result = db.session.execute('SELECT COUNT(*) FROM seguimiento_reportes')
            count = result.fetchone()[0]
            print(f'\nTotal de registros: {count}')
            
            # Ver algunos registros de ejemplo
            if count > 0:
                result = db.session.execute('SELECT * FROM seguimiento_reportes LIMIT 3')
                registros = result.fetchall()
                print(f'\nPrimeros 3 registros:')
                for i, registro in enumerate(registros):
                    print(f'  Registro {i+1}: {registro}')
                
        except Exception as e:
            print(f'Error verificando seguimiento_reportes: {e}')

if __name__ == '__main__':
    verificar_seguimiento()