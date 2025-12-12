"""
Rutas de autenticación para testigos por cédula
"""
from flask import Blueprint, request, jsonify
from backend.services.auth_testigo_service import AuthTestigoService
from backend.utils.exceptions import BaseAPIException
from backend.utils.jwt_utils import create_token_response
from backend.utils.logging_config import get_logger

logger = get_logger(__name__)

auth_testigo_bp = Blueprint('auth_testigo', __name__)


@auth_testigo_bp.route('/login-cedula', methods=['POST'])
def login_cedula():
    """
    Login de testigo usando solo cédula
    
    Body:
        cedula: Número de cédula del testigo
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        cedula = data.get('cedula')
        
        if not cedula:
            return jsonify({
                'success': False,
                'error': 'Número de cédula es requerido'
            }), 400
        
        # Autenticar testigo
        user, access_token, refresh_token = AuthTestigoService.login_por_cedula(cedula)
        
        return jsonify(create_token_response(user, access_token, refresh_token)), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Error en login de testigo: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_testigo_bp.route('/verificar-cedula', methods=['POST'])
def verificar_cedula():
    """
    Verificar si una cédula está disponible
    
    Body:
        cedula: Número de cédula a verificar
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        cedula = data.get('cedula')
        
        if not cedula:
            return jsonify({
                'success': False,
                'error': 'Número de cédula es requerido'
            }), 400
        
        disponible = AuthTestigoService.verificar_cedula_disponible(cedula)
        
        return jsonify({
            'success': True,
            'data': {
                'disponible': disponible,
                'cedula': cedula
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error verificando cédula: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500