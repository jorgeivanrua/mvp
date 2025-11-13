"""
Rutas para gestión de formularios E-14
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.formulario_service import FormularioService
from backend.services.validacion_service import ValidacionService
from backend.services.consolidado_service import ConsolidadoService
from backend.models.user import User
from backend.models.location import Location
from backend.utils.exceptions import BaseAPIException
from backend.utils.decorators import role_required

formularios_bp = Blueprint('formularios', __name__, url_prefix='/api/formularios')


@formularios_bp.route('/puesto', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto'])
def obtener_formularios_puesto():
    """
    Obtener formularios del puesto del coordinador
    
    Query params:
        estado: Filtrar por estado (opcional)
        page: Número de página (default: 1)
        per_page: Resultados por página (default: 20)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        # Obtener ubicación del coordinador (debe ser un puesto)
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Coordinador no asignado a un puesto válido'
            }), 400
        
        # Obtener parámetros de query
        estado = request.args.get('estado')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Construir filtros
        filtros = {}
        if estado:
            filtros['estado'] = estado
        
        # Obtener formularios
        resultado = FormularioService.obtener_formularios_por_puesto(
            ubicacion.id,
            filtros=filtros,
            page=page,
            per_page=per_page
        )
        
        return jsonify({
            'success': True,
            'data': resultado
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/<int:formulario_id>', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor_electoral', 'super_admin'])
def obtener_formulario(formulario_id):
    """
    Obtener detalles completos de un formulario
    
    Path params:
        formulario_id: ID del formulario
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        # Obtener formulario con todos los detalles
        formulario_data = FormularioService.obtener_formulario_por_id(
            formulario_id,
            include_votos=True,
            include_historial=True
        )
        
        # Verificar permisos según rol
        # TODO: Implementar verificación de permisos por rol y ubicación
        
        return jsonify({
            'success': True,
            'data': formulario_data
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/<int:formulario_id>/validar', methods=['PUT'])
@jwt_required()
@role_required(['coordinador_puesto'])
def validar_formulario(formulario_id):
    """
    Validar un formulario E-14
    
    Path params:
        formulario_id: ID del formulario
        
    Body:
        cambios: Diccionario opcional con cambios a aplicar
        comentario: Comentario opcional del coordinador
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        cambios = data.get('cambios')
        comentario = data.get('comentario')
        
        # Validar formulario
        formulario = ValidacionService.validar_formulario(
            formulario_id,
            int(user_id),
            cambios=cambios,
            comentario=comentario
        )
        
        return jsonify({
            'success': True,
            'message': 'Formulario validado exitosamente',
            'data': formulario.to_dict(include_votos=True)
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/<int:formulario_id>/rechazar', methods=['PUT'])
@jwt_required()
@role_required(['coordinador_puesto'])
def rechazar_formulario(formulario_id):
    """
    Rechazar un formulario E-14
    
    Path params:
        formulario_id: ID del formulario
        
    Body:
        motivo: Motivo del rechazo (obligatorio)
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'motivo' not in data:
            return jsonify({
                'success': False,
                'error': 'El motivo de rechazo es obligatorio'
            }), 400
        
        motivo = data['motivo']
        
        # Rechazar formulario
        formulario = ValidacionService.rechazar_formulario(
            formulario_id,
            int(user_id),
            motivo
        )
        
        return jsonify({
            'success': True,
            'message': 'Formulario rechazado',
            'data': formulario.to_dict()
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/consolidado', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental'])
def obtener_consolidado():
    """
    Obtener consolidado del puesto/municipio del coordinador
    
    Query params:
        tipo_eleccion_id: ID del tipo de elección (opcional)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        ubicacion = Location.query.get(user.ubicacion_id)
        tipo_eleccion_id = request.args.get('tipo_eleccion_id', type=int)
        
        # Calcular consolidado según el tipo de ubicación
        if ubicacion.tipo == 'puesto':
            consolidado = ConsolidadoService.calcular_consolidado_puesto(
                ubicacion.id,
                tipo_eleccion_id=tipo_eleccion_id
            )
        elif ubicacion.tipo == 'municipio':
            consolidado = ConsolidadoService.calcular_consolidado_municipal(
                ubicacion.id,
                tipo_eleccion_id=tipo_eleccion_id
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Tipo de ubicación no soportado para consolidado'
            }), 400
        
        if not consolidado:
            return jsonify({
                'success': False,
                'error': 'No se pudo calcular el consolidado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': consolidado
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/mesas', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto'])
def obtener_mesas_puesto():
    """
    Obtener lista de mesas del puesto con estado de reporte
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Coordinador no asignado a un puesto válido'
            }), 400
        
        # Obtener todas las mesas del puesto
        mesas = Location.query.filter_by(
            puesto_codigo=ubicacion.puesto_codigo,
            tipo='mesa'
        ).all()
        
        # Para cada mesa, obtener información del testigo y estado del formulario
        resultado = []
        for mesa in mesas:
            # Buscar testigo asignado a esta mesa
            testigo = User.query.filter_by(
                ubicacion_id=mesa.id,
                rol='testigo'
            ).first()
            
            # Buscar formulario más reciente de esta mesa
            from backend.models.formulario_e14 import FormularioE14
            formulario = FormularioE14.query.filter_by(
                mesa_id=mesa.id
            ).order_by(FormularioE14.created_at.desc()).first()
            
            mesa_data = {
                'mesa_id': mesa.id,
                'mesa_codigo': mesa.mesa_codigo,
                'mesa_nombre': mesa.nombre_completo,
                'total_votantes_registrados': mesa.total_votantes_registrados,
                'testigo_id': testigo.id if testigo else None,
                'testigo_nombre': testigo.nombre if testigo else None,
                'testigo_presente': testigo.presencia_verificada if testigo else False,
                'testigo_presente_desde': testigo.presencia_verificada_at.isoformat() if testigo and testigo.presencia_verificada_at else None,
                'tiene_formulario': formulario is not None,
                'estado_formulario': formulario.estado if formulario else None,
                'ultima_actualizacion': formulario.updated_at.isoformat() if formulario else None,
                # Datos del formulario para E-24
                'formulario_id': formulario.id if formulario else None,
                'total_votos': formulario.total_votos if formulario and formulario.estado == 'validado' else 0,
                'votos_validos': formulario.votos_validos if formulario and formulario.estado == 'validado' else 0,
                'votos_nulos': formulario.votos_nulos if formulario and formulario.estado == 'validado' else 0,
                'votos_blanco': formulario.votos_blanco if formulario and formulario.estado == 'validado' else 0
            }
            
            resultado.append(mesa_data)
        
        return jsonify({
            'success': True,
            'data': resultado
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('', methods=['POST'])
@jwt_required()
@role_required(['testigo'])
def crear_formulario():
    """
    Crear un nuevo formulario E-14
    
    Body:
        mesa_id: ID de la mesa
        tipo_eleccion_id: ID del tipo de elección
        total_votantes_registrados: Total de votantes registrados
        total_votos: Total de votos
        votos_validos: Votos válidos
        votos_nulos: Votos nulos
        votos_blanco: Votos en blanco
        tarjetas_no_marcadas: Tarjetas no marcadas
        total_tarjetas: Total de tarjetas
        estado: Estado del formulario (borrador/pendiente)
        observaciones: Observaciones (opcional)
        votos_partidos: Lista de votos por partido
        votos_candidatos: Lista de votos por candidato
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Crear formulario
        formulario = FormularioService.crear_formulario(data, int(user_id))
        
        return jsonify({
            'success': True,
            'message': 'Formulario creado exitosamente',
            'data': formulario.to_dict(include_votos=True)
        }), 201
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@formularios_bp.route('/<int:formulario_id>', methods=['PUT'])
@jwt_required()
@role_required(['testigo', 'coordinador_puesto'])
def actualizar_formulario(formulario_id):
    """
    Actualizar un formulario E-14
    
    Path params:
        formulario_id: ID del formulario
        
    Body:
        Campos a actualizar
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Actualizar formulario
        formulario = FormularioService.actualizar_formulario(
            formulario_id,
            data,
            int(user_id)
        )
        
        return jsonify({
            'success': True,
            'message': 'Formulario actualizado exitosamente',
            'data': formulario.to_dict(include_votos=True)
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
