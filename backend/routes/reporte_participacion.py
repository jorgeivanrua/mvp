"""
Rutas para reportes de participación horaria (E-11)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.reporte_participacion_service import ReporteParticipacionService
from backend.models.user import User
from backend.utils.exceptions import BaseAPIException
from backend.utils.decorators import role_required

reporte_participacion_bp = Blueprint('reporte_participacion', __name__, url_prefix='/api/reporte-participacion')


@reporte_participacion_bp.route('', methods=['POST'])
@jwt_required()
@role_required(['testigo_electoral'])
def crear_reporte():
    """
    Crear un nuevo reporte de participación
    
    Body:
        mesa_id: ID de la mesa
        hora_reporte: Hora del reporte (ISO format)
        personas_votadas: Número de personas que han votado
        observaciones: Observaciones opcionales
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Crear reporte
        reporte = ReporteParticipacionService.crear_reporte(data, int(user_id))
        
        return jsonify({
            'success': True,
            'message': 'Reporte de participación creado exitosamente',
            'data': reporte.to_dict_completo()
        }), 201
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@reporte_participacion_bp.route('/mesa/<int:mesa_id>', methods=['GET'])
@jwt_required()
def obtener_reportes_mesa(mesa_id):
    """
    Obtener todos los reportes de una mesa
    
    Path params:
        mesa_id: ID de la mesa
    """
    try:
        data = ReporteParticipacionService.obtener_reportes_mesa(mesa_id)
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@reporte_participacion_bp.route('/puesto/<int:puesto_id>', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto', 'coordinador_municipal', 'monitoreo', 'super_admin'])
def obtener_participacion_puesto(puesto_id):
    """
    Obtener participación de todas las mesas de un puesto
    
    Path params:
        puesto_id: ID del puesto
    """
    try:
        data = ReporteParticipacionService.obtener_participacion_puesto(puesto_id)
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@reporte_participacion_bp.route('/mi-mesa', methods=['GET'])
@jwt_required()
@role_required(['testigo_electoral'])
def obtener_mis_reportes():
    """
    Obtener reportes de la mesa del testigo actual
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin mesa asignada'
            }), 400
        
        data = ReporteParticipacionService.obtener_reportes_mesa(user.ubicacion_id)
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
