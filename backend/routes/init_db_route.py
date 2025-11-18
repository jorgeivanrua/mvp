"""
Ruta especial para inicializar la base de datos
Solo para uso en desarrollo/primera configuración
"""
from flask import Blueprint, jsonify
from backend.database import db
from backend.models.location import Location

init_db_bp = Blueprint('init_db', __name__)

@init_db_bp.route('/init-db-page')
def init_db_page():
    """Página HTML para inicializar la BD"""
    from flask import render_template
    return render_template('init_db.html')

@init_db_bp.route('/init-database-secret-endpoint-2024', methods=['GET', 'POST'])
def init_database():
    """
    Endpoint especial para inicializar la base de datos
    Acceder a: /init-database-secret-endpoint-2024
    """
    try:
        # Verificar si ya hay datos
        departamentos_count = Location.query.filter_by(tipo='departamento').count()
        
        if departamentos_count > 0:
            return jsonify({
                'success': True,
                'message': f'Base de datos ya tiene datos ({departamentos_count} departamentos)',
                'already_initialized': True
            }), 200
        
        # Crear tablas si no existen
        db.create_all()
        
        # Cargar datos de prueba
        print("⚠️  Inicializando base de datos con datos de prueba...")
        
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        
        from backend.scripts.load_complete_test_data import load_complete_test_data
        load_complete_test_data()
        
        # Verificar que se cargaron los datos
        departamentos_count = Location.query.filter_by(tipo='departamento').count()
        
        return jsonify({
            'success': True,
            'message': f'Base de datos inicializada correctamente con {departamentos_count} departamentos',
            'departamentos': departamentos_count
        }), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error inicializando BD: {e}")
        print(error_trace)
        
        return jsonify({
            'success': False,
            'error': str(e),
            'trace': error_trace
        }), 500
