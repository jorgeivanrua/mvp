"""Rutas para incidentes y delitos electorales"""

from flask import Blueprint, request, jsonify
from backend.utils.decorators import token_required
from backend.services.incidentes_delitos_service import IncidentesDelitosService
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral

incidentes_delitos_bp = Blueprint('incidentes_delitos', __name__)


@incidentes_delitos_bp.route('/api/incidentes', methods=['POST'])
@token_required
def crear_incidente(current_user):
    """Crear un nuevo incidente electoral"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('tipo_incidente'):
            return jsonify({'error': 'Tipo de incidente es requerido'}), 400
        if not data.get('titulo'):
            return jsonify({'error': 'Título es requerido'}), 400
        if not data.get('descripcion'):
            return jsonify({'error': 'Descripción es requerida'}), 400
        
        incidente = IncidentesDelitosService.crear_incidente(data, current_user.id)
        
        return jsonify({
            'message': 'Incidente creado exitosamente',
            'incidente': incidente.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/incidentes', methods=['GET'])
@token_required
def obtener_incidentes(current_user):
    """Obtener incidentes según permisos del usuario"""
    try:
        # Obtener filtros de query params
        filtros = {}
        if request.args.get('estado'):
            filtros['estado'] = request.args.get('estado')
        if request.args.get('severidad'):
            filtros['severidad'] = request.args.get('severidad')
        if request.args.get('tipo_incidente'):
            filtros['tipo_incidente'] = request.args.get('tipo_incidente')
        if request.args.get('fecha_desde'):
            filtros['fecha_desde'] = request.args.get('fecha_desde')
        if request.args.get('fecha_hasta'):
            filtros['fecha_hasta'] = request.args.get('fecha_hasta')
        
        incidentes = IncidentesDelitosService.obtener_incidentes(
            filtros=filtros,
            usuario_id=current_user.id,
            rol_usuario=current_user.rol
        )
        
        return jsonify({'incidentes': incidentes}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/incidentes/<int:incidente_id>', methods=['GET'])
@token_required
def obtener_incidente(current_user, incidente_id):
    """Obtener detalle de un incidente"""
    try:
        incidente = IncidenteElectoral.query.get(incidente_id)
        if not incidente:
            return jsonify({'error': 'Incidente no encontrado'}), 404
        
        # Verificar permisos
        if current_user.rol == 'testigo_electoral' and incidente.reportado_por_id != current_user.id:
            return jsonify({'error': 'No tiene permisos para ver este incidente'}), 403
        
        # Obtener seguimiento
        seguimiento = IncidentesDelitosService.obtener_seguimiento('incidente', incidente_id)
        
        return jsonify({
            'incidente': incidente.to_dict(),
            'seguimiento': seguimiento
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/incidentes/<int:incidente_id>/estado', methods=['PUT'])
@token_required
def actualizar_estado_incidente(current_user, incidente_id):
    """Actualizar estado de un incidente"""
    try:
        # Solo coordinadores y superiores pueden cambiar estado
        if current_user.rol not in ['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor_electoral', 'super_admin']:
            return jsonify({'error': 'No tiene permisos para actualizar incidentes'}), 403
        
        data = request.get_json()
        nuevo_estado = data.get('estado')
        comentario = data.get('comentario')
        
        if not nuevo_estado:
            return jsonify({'error': 'Estado es requerido'}), 400
        
        incidente = IncidentesDelitosService.actualizar_estado_incidente(
            incidente_id, nuevo_estado, current_user.id, comentario
        )
        
        return jsonify({
            'message': 'Estado actualizado exitosamente',
            'incidente': incidente.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/delitos', methods=['POST'])
@token_required
def crear_delito(current_user):
    """Crear un nuevo delito electoral"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('tipo_delito'):
            return jsonify({'error': 'Tipo de delito es requerido'}), 400
        if not data.get('titulo'):
            return jsonify({'error': 'Título es requerido'}), 400
        if not data.get('descripcion'):
            return jsonify({'error': 'Descripción es requerida'}), 400
        
        delito = IncidentesDelitosService.crear_delito(data, current_user.id)
        
        return jsonify({
            'message': 'Delito creado exitosamente',
            'delito': delito.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/delitos', methods=['GET'])
@token_required
def obtener_delitos(current_user):
    """Obtener delitos según permisos del usuario"""
    try:
        # Obtener filtros de query params
        filtros = {}
        if request.args.get('estado'):
            filtros['estado'] = request.args.get('estado')
        if request.args.get('gravedad'):
            filtros['gravedad'] = request.args.get('gravedad')
        if request.args.get('tipo_delito'):
            filtros['tipo_delito'] = request.args.get('tipo_delito')
        if request.args.get('fecha_desde'):
            filtros['fecha_desde'] = request.args.get('fecha_desde')
        if request.args.get('fecha_hasta'):
            filtros['fecha_hasta'] = request.args.get('fecha_hasta')
        
        delitos = IncidentesDelitosService.obtener_delitos(
            filtros=filtros,
            usuario_id=current_user.id,
            rol_usuario=current_user.rol
        )
        
        return jsonify({'delitos': delitos}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/delitos/<int:delito_id>', methods=['GET'])
@token_required
def obtener_delito(current_user, delito_id):
    """Obtener detalle de un delito"""
    try:
        delito = DelitoElectoral.query.get(delito_id)
        if not delito:
            return jsonify({'error': 'Delito no encontrado'}), 404
        
        # Verificar permisos
        if current_user.rol == 'testigo_electoral' and delito.reportado_por_id != current_user.id:
            return jsonify({'error': 'No tiene permisos para ver este delito'}), 403
        
        # Obtener seguimiento
        seguimiento = IncidentesDelitosService.obtener_seguimiento('delito', delito_id)
        
        return jsonify({
            'delito': delito.to_dict(),
            'seguimiento': seguimiento
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/delitos/<int:delito_id>/estado', methods=['PUT'])
@token_required
def actualizar_estado_delito(current_user, delito_id):
    """Actualizar estado de un delito"""
    try:
        # Solo coordinadores y superiores pueden cambiar estado
        if current_user.rol not in ['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor_electoral', 'super_admin']:
            return jsonify({'error': 'No tiene permisos para actualizar delitos'}), 403
        
        data = request.get_json()
        nuevo_estado = data.get('estado')
        comentario = data.get('comentario')
        
        if not nuevo_estado:
            return jsonify({'error': 'Estado es requerido'}), 400
        
        delito = IncidentesDelitosService.actualizar_estado_delito(
            delito_id, nuevo_estado, current_user.id, comentario
        )
        
        return jsonify({
            'message': 'Estado actualizado exitosamente',
            'delito': delito.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/delitos/<int:delito_id>/denunciar', methods=['POST'])
@token_required
def denunciar_delito(current_user, delito_id):
    """Denunciar formalmente un delito"""
    try:
        # Solo auditores y super_admin pueden denunciar formalmente
        if current_user.rol not in ['auditor_electoral', 'super_admin']:
            return jsonify({'error': 'No tiene permisos para denunciar formalmente'}), 403
        
        data = request.get_json()
        numero_denuncia = data.get('numero_denuncia')
        autoridad_competente = data.get('autoridad_competente')
        
        if not numero_denuncia or not autoridad_competente:
            return jsonify({'error': 'Número de denuncia y autoridad competente son requeridos'}), 400
        
        delito = IncidentesDelitosService.denunciar_formalmente(
            delito_id, current_user.id, numero_denuncia, autoridad_competente
        )
        
        return jsonify({
            'message': 'Delito denunciado formalmente',
            'delito': delito.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/reportes/estadisticas', methods=['GET'])
@token_required
def obtener_estadisticas(current_user):
    """Obtener estadísticas de incidentes y delitos"""
    try:
        estadisticas = IncidentesDelitosService.obtener_estadisticas(
            usuario_id=current_user.id,
            rol_usuario=current_user.rol
        )
        
        return jsonify(estadisticas), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/notificaciones', methods=['GET'])
@token_required
def obtener_notificaciones(current_user):
    """Obtener notificaciones del usuario"""
    try:
        solo_no_leidas = request.args.get('solo_no_leidas', 'false').lower() == 'true'
        
        notificaciones = IncidentesDelitosService.obtener_notificaciones(
            current_user.id, solo_no_leidas
        )
        
        return jsonify({'notificaciones': notificaciones}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/notificaciones/<int:notificacion_id>/leer', methods=['PUT'])
@token_required
def marcar_notificacion_leida(current_user, notificacion_id):
    """Marcar notificación como leída"""
    try:
        IncidentesDelitosService.marcar_notificacion_leida(notificacion_id)
        
        return jsonify({'message': 'Notificación marcada como leída'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@incidentes_delitos_bp.route('/api/incidentes/tipos', methods=['GET'])
@token_required
def obtener_tipos_incidentes(current_user):
    """Obtener tipos de incidentes disponibles"""
    return jsonify({'tipos': IncidenteElectoral.TIPOS_INCIDENTE}), 200


@incidentes_delitos_bp.route('/api/delitos/tipos', methods=['GET'])
@token_required
def obtener_tipos_delitos(current_user):
    """Obtener tipos de delitos disponibles"""
    return jsonify({'tipos': DelitoElectoral.TIPOS_DELITO}), 200
