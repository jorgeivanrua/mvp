"""
Rutas para gestión de testigos registrados
Nuevo sistema según requerimientos de Registraduría
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.testigo_service import TestigoService
from backend.models.user import User
from backend.models.location import Location
from backend.utils.exceptions import BaseAPIException
from backend.utils.decorators import role_required
from backend.utils.logging_config import get_logger

logger = get_logger(__name__)

testigos_bp = Blueprint('testigos_registrados', __name__)


@testigos_bp.route('/validar-cedula', methods=['POST'])
def validar_testigo_cedula():
    """
    Validar testigo por cédula (endpoint público para coordinadores)
    
    Body:
        cedula: Número de cédula del testigo
        nombre: Nombre del testigo (opcional, para verificación)
        mesa_id: ID de la mesa donde se valida (opcional)
        puesto_codigo: Código del puesto (opcional)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        cedula = data.get('cedula')
        nombre = data.get('nombre', '')
        mesa_id = data.get('mesa_id')
        puesto_codigo = data.get('puesto_codigo')
        
        if not cedula:
            return jsonify({
                'success': False,
                'error': 'Número de cédula es requerido'
            }), 400
        
        # Validar testigo
        resultado = TestigoService.validar_testigo_por_cedula(
            cedula, nombre, mesa_id, puesto_codigo
        )
        
        return jsonify({
            'success': True,
            'data': resultado,
            'message': resultado['mensaje']
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Error validando testigo: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigos_bp.route('/login-cedula-simple', methods=['POST'])
def login_testigo_cedula_simple():
    """
    Login simplificado de testigo usando solo cédula
    
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
        
        # Validar testigo usando el servicio simplificado
        resultado = TestigoService.validar_testigo_simple_por_cedula(cedula)
        
        # Obtener usuario del sistema
        usuario = User.query.get(resultado['testigo']['user_id'])
        
        if not usuario:
            return jsonify({
                'success': False,
                'error': 'Error creando usuario del sistema'
            }), 500
        
        # Generar tokens
        from backend.utils.jwt_utils import generate_tokens, create_token_response
        access_token, refresh_token = generate_tokens(usuario)
        
        # Actualizar último acceso
        from datetime import datetime
        usuario.ultimo_acceso = datetime.utcnow()
        from backend.database import db
        db.session.commit()
        
        return jsonify(create_token_response(usuario, access_token, refresh_token)), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Error en login de testigo: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigos_bp.route('/login-cedula', methods=['POST'])
def login_testigo_cedula():
    """
    Login de testigo usando cédula (versión completa con validaciones)
    
    Body:
        cedula: Número de cédula del testigo
        nombre: Nombre del testigo (para verificación)
        puesto_codigo: Código del puesto donde se encuentra
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        cedula = data.get('cedula')
        nombre = data.get('nombre', '')
        puesto_codigo = data.get('puesto_codigo')
        
        if not cedula or not puesto_codigo:
            return jsonify({
                'success': False,
                'error': 'Cédula y código de puesto son requeridos'
            }), 400
        
        # Validar testigo (esto también lo crea si no existe)
        resultado = TestigoService.validar_testigo_por_cedula(
            cedula, nombre, None, puesto_codigo
        )
        
        # Obtener usuario del sistema
        usuario = User.query.get(resultado['testigo']['user_id'])
        
        if not usuario:
            return jsonify({
                'success': False,
                'error': 'Error creando usuario del sistema'
            }), 500
        
        # Generar tokens
        from backend.utils.jwt_utils import generate_tokens, create_token_response
        access_token, refresh_token = generate_tokens(usuario)
        
        # Actualizar último acceso
        from datetime import datetime
        usuario.ultimo_acceso = datetime.utcnow()
        from backend.database import db
        db.session.commit()
        
        return jsonify(create_token_response(usuario, access_token, refresh_token)), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Error en login de testigo: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigos_bp.route('/municipio/<departamento_codigo>/<municipio_codigo>', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal', 'coordinador_puesto', 'admin_municipal', 'super_admin'])
def obtener_testigos_municipio(departamento_codigo, municipio_codigo):
    """
    Obtener testigos registrados de un municipio
    """
    try:
        testigos = TestigoService.obtener_testigos_municipio(departamento_codigo, municipio_codigo)
        
        return jsonify({
            'success': True,
            'data': {
                'testigos': testigos,
                'total': len(testigos)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo testigos del municipio: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigos_bp.route('/puesto/<puesto_codigo>/validados', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto', 'coordinador_municipal', 'admin_municipal', 'super_admin'])
def obtener_testigos_validados_puesto(puesto_codigo):
    """
    Obtener testigos validados en un puesto específico
    """
    try:
        testigos = TestigoService.obtener_testigos_validados_puesto(puesto_codigo)
        
        return jsonify({
            'success': True,
            'data': {
                'testigos': testigos,
                'total': len(testigos)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo testigos validados del puesto: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigos_bp.route('/registrar', methods=['POST'])
@jwt_required()
@role_required(['coordinador_municipal', 'admin_municipal', 'super_admin'])
def registrar_testigo():
    """
    Registrar un nuevo testigo por parte de un partido
    
    Body:
        cedula: Número de cédula
        nombre_completo: Nombre completo del testigo
        partido_id: ID del partido político
        departamento_codigo: Código del departamento
        municipio_codigo: Código del municipio
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        campos_requeridos = ['cedula', 'nombre_completo', 'partido_id', 'departamento_codigo', 'municipio_codigo']
        for campo in campos_requeridos:
            if not data.get(campo):
                return jsonify({
                    'success': False,
                    'error': f'El campo {campo} es requerido'
                }), 400
        
        # Obtener usuario actual
        user_id = get_jwt_identity()
        usuario_actual = User.query.get(int(user_id))
        
        # Registrar testigo
        testigo = TestigoService.registrar_testigo_partido(
            cedula=data['cedula'],
            nombre_completo=data['nombre_completo'],
            partido_id=data['partido_id'],
            departamento_codigo=data['departamento_codigo'],
            municipio_codigo=data['municipio_codigo'],
            registrado_por=usuario_actual.nombre if usuario_actual else None
        )
        
        return jsonify({
            'success': True,
            'data': testigo.to_dict(),
            'message': 'Testigo registrado exitosamente'
        }), 201
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Error registrando testigo: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigos_bp.route('/estadisticas', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal', 'coordinador_puesto', 'admin_municipal', 'super_admin', 'monitoreo'])
def obtener_estadisticas():
    """
    Obtener estadísticas de validación de testigos
    """
    try:
        estadisticas = TestigoService.obtener_estadisticas_validacion()
        
        return jsonify({
            'success': True,
            'data': estadisticas
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigos_bp.route('/buscar-cedula/<cedula>', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal', 'coordinador_puesto', 'admin_municipal', 'super_admin'])
def buscar_testigo_por_cedula(cedula):
    """
    Buscar testigo por cédula (sin validar)
    """
    try:
        from backend.models.testigo_registrado import TestigoRegistrado
        
        # Limpiar cédula
        cedula_limpia = ''.join(filter(str.isdigit, str(cedula)))
        
        if not cedula_limpia:
            return jsonify({
                'success': False,
                'error': 'Número de cédula inválido'
            }), 400
        
        testigo = TestigoRegistrado.query.filter_by(
            cedula=cedula_limpia,
            activo=True
        ).first()
        
        if not testigo:
            return jsonify({
                'success': False,
                'error': 'Testigo no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': testigo.to_dict(include_sensitive=True)
        }), 200
        
    except Exception as e:
        logger.error(f"Error buscando testigo: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500