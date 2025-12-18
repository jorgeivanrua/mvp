"""
Rutas para inicialización del sistema en producción
"""
from flask import Blueprint, jsonify, request
from backend.database import db
from backend.models.departamento_config import DepartamentoConfig
import os

init_bp = Blueprint('init', __name__)

@init_bp.route('/init-system', methods=['POST'])
def init_system():
    """
    Endpoint para inicializar el sistema en producción
    Carga Quindío automáticamente si no hay datos
    """
    try:
        # Verificar si ya hay datos básicos
        from backend.models.user import User
        from backend.models.location import Location
        
        usuarios_count = 0
        ubicaciones_quindio = 0
        
        try:
            usuarios_count = User.query.count()
            ubicaciones_quindio = Location.query.filter_by(
                departamento_codigo='26'
            ).count()
        except:
            pass
        
        # Si ya hay datos de Quindío, no reinicializar
        if usuarios_count > 2 and ubicaciones_quindio > 0:
            return jsonify({
                'success': True,
                'message': f'Sistema ya inicializado con {usuarios_count} usuarios y {ubicaciones_quindio} ubicaciones de Quindío',
                'already_initialized': True
            })
        
        # Ejecutar script de inicialización simple
        import subprocess
        import sys
        
        # Ejecutar el script de inicialización con backup
        result = subprocess.run([
            sys.executable, 'init_render_backup.py'
        ], capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Sistema inicializado exitosamente',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Error en inicialización: {result.stderr}',
                'output': result.stdout
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'message': 'Timeout en inicialización - proceso tomó más de 5 minutos'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@init_bp.route('/system-status', methods=['GET'])
def system_status():
    """Verificar estado del sistema"""
    try:
        # Verificar si las tablas existen
        from backend.models.user import User
        from backend.models.location import Location
        
        # Contar usuarios y ubicaciones básicos
        try:
            usuarios_count = User.query.count()
            ubicaciones_count = Location.query.count()
        except:
            usuarios_count = 0
            ubicaciones_count = 0
        
        # Intentar verificar departamentos configurados
        departamentos_count = 0
        quindio_users = 0
        quindio_locations = 0
        quindio_loaded = False
        
        try:
            departamentos_count = DepartamentoConfig.query.count()
            quindio = DepartamentoConfig.query.filter_by(
                departamento_codigo='26'
            ).first()
            
            if quindio:
                quindio_loaded = True
                quindio_users = quindio.total_usuarios_creados
                quindio_locations = quindio.total_ubicaciones
        except:
            # Si no existe la tabla, verificar por ubicaciones de Quindío
            try:
                quindio_locations = Location.query.filter_by(
                    departamento_codigo='26'
                ).count()
                quindio_loaded = quindio_locations > 0
            except:
                pass
        
        status = {
            'initialized': usuarios_count > 2,  # Más que solo super admin
            'departamentos_count': departamentos_count,
            'quindio_loaded': quindio_loaded,
            'usuarios_count': usuarios_count,
            'ubicaciones_count': ubicaciones_count,
            'quindio_users': quindio_users,
            'quindio_locations': quindio_locations,
            'environment': 'production' if os.environ.get('RENDER') else 'development'
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'initialized': False,
            'usuarios_count': 0,
            'ubicaciones_count': 0
        }), 200  # Cambiar a 200 para evitar errores en frontend

@init_bp.route('/init', methods=['GET'])
def init_page():
    """Página de inicialización del sistema"""
    from flask import render_template
    return render_template('init_system.html')