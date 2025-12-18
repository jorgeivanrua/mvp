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
        # Verificar si ya hay datos
        config = DepartamentoConfig.query.filter_by(
            departamento_codigo='26'
        ).first()
        
        if config and config.total_usuarios_creados > 0:
            return jsonify({
                'success': True,
                'message': f'Sistema ya inicializado con {config.total_usuarios_creados} usuarios',
                'departamento': config.departamento_nombre
            })
        
        # Solo permitir en producción (Render)
        if not os.environ.get('RENDER'):
            return jsonify({
                'success': False,
                'message': 'Inicialización solo disponible en producción'
            }), 403
        
        # Cargar Quindío
        from scripts.cargar_departamento_completo import CargadorDepartamentoCompleto
        
        cargador = CargadorDepartamentoCompleto()
        resultado = cargador.cargar_departamento_completo(
            departamento_codigo='26',
            es_principal=True,
            forzar=True
        )
        
        if resultado.get('exitoso'):
            return jsonify({
                'success': True,
                'message': 'Sistema inicializado exitosamente',
                'estadisticas': resultado['estadisticas']
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Error inicializando: {resultado.get("motivo")}'
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
        # Contar departamentos configurados
        departamentos = DepartamentoConfig.query.count()
        
        # Verificar Quindío específicamente
        quindio = DepartamentoConfig.query.filter_by(
            departamento_codigo='26'
        ).first()
        
        status = {
            'initialized': departamentos > 0,
            'departamentos_count': departamentos,
            'quindio_loaded': quindio is not None,
            'environment': 'production' if os.environ.get('RENDER') else 'development'
        }
        
        if quindio:
            status['quindio_users'] = quindio.total_usuarios_creados
            status['quindio_locations'] = quindio.total_ubicaciones
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'initialized': False
        }), 500

@init_bp.route('/init', methods=['GET'])
def init_page():
    """Página de inicialización del sistema"""
    from flask import render_template
    return render_template('init_system.html')