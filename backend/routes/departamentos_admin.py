"""
Rutas para administración de departamentos
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.departamento_service import DepartamentoService
from backend.models.user import User
from backend.utils.exceptions import BaseAPIException

departamentos_admin_bp = Blueprint('departamentos_admin', __name__)


@departamentos_admin_bp.route('/departamentos/disponibles', methods=['GET'])
@jwt_required()
def listar_departamentos_disponibles():
    """Listar departamentos disponibles en DIVIPOLA"""
    try:
        # Verificar permisos de super admin
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'Acceso denegado. Solo super administradores pueden gestionar departamentos.'
            }), 403
        
        departamentos = DepartamentoService.listar_departamentos_disponibles()
        
        return jsonify({
            'success': True,
            'data': departamentos
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@departamentos_admin_bp.route('/departamentos/estado', methods=['GET'])
@jwt_required()
def obtener_estado_departamentos():
    """Obtener estado de departamentos configurados"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'Acceso denegado'
            }), 403
        
        estado = DepartamentoService.obtener_estado_departamentos()
        
        return jsonify({
            'success': True,
            'data': estado
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@departamentos_admin_bp.route('/departamentos/habilitar', methods=['POST'])
@jwt_required()
def habilitar_departamento():
    """
    Habilitar un departamento y cargar sus datos
    
    Body:
        departamento_codigo: Código del departamento (ej: '26')
        es_principal: Si debe ser el departamento principal (opcional)
        auto_cargar: Si debe cargar automáticamente datos (opcional, default: true)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'Acceso denegado'
            }), 403
        
        data = request.get_json()
        if not data or 'departamento_codigo' not in data:
            return jsonify({
                'success': False,
                'error': 'departamento_codigo es requerido'
            }), 400
        
        departamento_codigo = data['departamento_codigo']
        es_principal = data.get('es_principal', False)
        auto_cargar = data.get('auto_cargar', True)
        
        resultado = DepartamentoService.habilitar_departamento(
            departamento_codigo=departamento_codigo,
            es_principal=es_principal,
            auto_cargar=auto_cargar
        )
        
        return jsonify({
            'success': True,
            'message': f'Departamento {departamento_codigo} habilitado exitosamente',
            'data': resultado
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@departamentos_admin_bp.route('/departamentos/deshabilitar', methods=['POST'])
@jwt_required()
def deshabilitar_departamento():
    """
    Deshabilitar un departamento
    
    Body:
        departamento_codigo: Código del departamento
        desactivar_usuarios: Si debe desactivar usuarios (opcional, default: true)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'Acceso denegado'
            }), 403
        
        data = request.get_json()
        if not data or 'departamento_codigo' not in data:
            return jsonify({
                'success': False,
                'error': 'departamento_codigo es requerido'
            }), 400
        
        departamento_codigo = data['departamento_codigo']
        desactivar_usuarios = data.get('desactivar_usuarios', True)
        
        resultado = DepartamentoService.deshabilitar_departamento(
            departamento_codigo=departamento_codigo,
            desactivar_usuarios=desactivar_usuarios
        )
        
        return jsonify({
            'success': True,
            'message': f'Departamento {departamento_codigo} deshabilitado exitosamente',
            'data': resultado
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@departamentos_admin_bp.route('/departamentos/cargar-datos', methods=['POST'])
@jwt_required()
def cargar_datos_departamento():
    """
    Cargar/recargar datos de un departamento específico
    
    Body:
        departamento_codigo: Código del departamento
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'Acceso denegado'
            }), 403
        
        data = request.get_json()
        if not data or 'departamento_codigo' not in data:
            return jsonify({
                'success': False,
                'error': 'departamento_codigo es requerido'
            }), 400
        
        departamento_codigo = data['departamento_codigo']
        
        resultado = DepartamentoService.cargar_datos_departamento(departamento_codigo)
        
        return jsonify({
            'success': True,
            'message': f'Datos del departamento {departamento_codigo} cargados exitosamente',
            'data': resultado
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except FileNotFoundError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@departamentos_admin_bp.route('/departamentos/principal', methods=['POST'])
@jwt_required()
def marcar_departamento_principal():
    """
    Marcar un departamento como principal
    
    Body:
        departamento_codigo: Código del departamento
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'Acceso denegado'
            }), 403
        
        data = request.get_json()
        if not data or 'departamento_codigo' not in data:
            return jsonify({
                'success': False,
                'error': 'departamento_codigo es requerido'
            }), 400
        
        departamento_codigo = data['departamento_codigo']
        
        # Habilitar como principal
        resultado = DepartamentoService.habilitar_departamento(
            departamento_codigo=departamento_codigo,
            es_principal=True,
            auto_cargar=True
        )
        
        return jsonify({
            'success': True,
            'message': f'Departamento {departamento_codigo} marcado como principal',
            'data': resultado
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500