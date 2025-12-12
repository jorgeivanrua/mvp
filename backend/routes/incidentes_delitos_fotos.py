"""
Rutas para manejo de fotos de incidentes y delitos electorales
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.incidentes_delitos_fotos_service import IncidentesDelitosFotosService
from backend.utils.decorators import role_required
from backend.utils.exceptions import ValidationException, NotFoundException

incidentes_delitos_fotos_bp = Blueprint('incidentes_delitos_fotos', __name__, url_prefix='/api/evidencias-fotos')


@incidentes_delitos_fotos_bp.route('/subir/<tipo_reporte>/<int:reporte_id>', methods=['POST'])
@jwt_required()
@role_required(['testigo_electoral', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor_electoral'])
def subir_foto(tipo_reporte, reporte_id):
    """
    Subir una foto de evidencia para un incidente o delito
    """
    try:
        user_id = get_jwt_identity()
        
        # Validar tipo de reporte
        if tipo_reporte not in ['incidente', 'delito']:
            return jsonify({
                'success': False,
                'error': 'Tipo de reporte inválido. Use "incidente" o "delito"'
            }), 400
        
        # Obtener archivo
        if 'foto' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se encontró archivo de foto'
            }), 400
        
        file = request.files['foto']
        descripcion = request.form.get('descripcion', '')
        categoria = request.form.get('categoria', 'general')
        tipo_evidencia = request.form.get('tipo_evidencia', 'directa')
        relevancia = request.form.get('relevancia', 'media')
        
        resultado = IncidentesDelitosFotosService.subir_foto(
            tipo_reporte=tipo_reporte,
            reporte_id=reporte_id,
            file=file,
            descripcion=descripcion,
            categoria=categoria,
            tipo_evidencia=tipo_evidencia,
            relevancia=relevancia,
            usuario_id=int(user_id)
        )
        
        return jsonify(resultado), 200
        
    except ValidationException as e:
        return jsonify({
            'success': False,
            'errors': e.errors
        }), 400
    except NotFoundException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500


@incidentes_delitos_fotos_bp.route('/<tipo_reporte>/<int:reporte_id>', methods=['GET'])
@jwt_required()
def obtener_fotos(tipo_reporte, reporte_id):
    """
    Obtener todas las fotos de un incidente o delito
    """
    try:
        # Validar tipo de reporte
        if tipo_reporte not in ['incidente', 'delito']:
            return jsonify({
                'success': False,
                'error': 'Tipo de reporte inválido. Use "incidente" o "delito"'
            }), 400
        
        fotos = IncidentesDelitosFotosService.obtener_fotos(tipo_reporte, reporte_id)
        estadisticas = IncidentesDelitosFotosService.obtener_estadisticas_fotos(tipo_reporte, reporte_id)
        
        return jsonify({
            'success': True,
            'fotos': fotos,
            'estadisticas': estadisticas
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener fotos: {str(e)}'
        }), 500


@incidentes_delitos_fotos_bp.route('/eliminar/<int:foto_id>', methods=['DELETE'])
@jwt_required()
@role_required(['testigo_electoral', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor_electoral'])
def eliminar_foto(foto_id):
    """
    Eliminar una foto de evidencia
    """
    try:
        user_id = get_jwt_identity()
        
        resultado = IncidentesDelitosFotosService.eliminar_foto(
            foto_id=foto_id,
            usuario_id=int(user_id)
        )
        
        return jsonify(resultado), 200
        
    except ValidationException as e:
        return jsonify({
            'success': False,
            'errors': e.errors
        }), 400
    except NotFoundException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500


@incidentes_delitos_fotos_bp.route('/validar/<int:foto_id>', methods=['POST'])
@jwt_required()
@role_required(['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor_electoral'])
def validar_foto(foto_id):
    """
    Validar o rechazar una foto de evidencia
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        validada = data.get('validada', True)
        comentario = data.get('comentario', '')
        
        resultado = IncidentesDelitosFotosService.validar_foto(
            foto_id=foto_id,
            validada=validada,
            comentario=comentario,
            usuario_id=int(user_id)
        )
        
        return jsonify(resultado), 200
        
    except ValidationException as e:
        return jsonify({
            'success': False,
            'errors': e.errors
        }), 400
    except NotFoundException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500


@incidentes_delitos_fotos_bp.route('/principal/<int:foto_id>', methods=['POST'])
@jwt_required()
@role_required(['testigo_electoral', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor_electoral'])
def establecer_principal(foto_id):
    """
    Establecer una foto como principal
    """
    try:
        user_id = get_jwt_identity()
        
        resultado = IncidentesDelitosFotosService.establecer_principal(
            foto_id=foto_id,
            usuario_id=int(user_id)
        )
        
        return jsonify(resultado), 200
        
    except ValidationException as e:
        return jsonify({
            'success': False,
            'errors': e.errors
        }), 400
    except NotFoundException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500


@incidentes_delitos_fotos_bp.route('/metadatos/<int:foto_id>', methods=['PUT'])
@jwt_required()
@role_required(['testigo_electoral', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor_electoral'])
def actualizar_metadatos(foto_id):
    """
    Actualizar metadatos de una foto
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        descripcion = data.get('descripcion')
        categoria = data.get('categoria')
        tipo_evidencia = data.get('tipo_evidencia')
        relevancia = data.get('relevancia')
        
        resultado = IncidentesDelitosFotosService.actualizar_metadatos(
            foto_id=foto_id,
            descripcion=descripcion,
            categoria=categoria,
            tipo_evidencia=tipo_evidencia,
            relevancia=relevancia,
            usuario_id=int(user_id)
        )
        
        return jsonify(resultado), 200
        
    except ValidationException as e:
        return jsonify({
            'success': False,
            'errors': e.errors
        }), 400
    except NotFoundException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500


@incidentes_delitos_fotos_bp.route('/info/<tipo_reporte>/<int:reporte_id>', methods=['GET'])
@jwt_required()
def obtener_info_reporte(tipo_reporte, reporte_id):
    """
    Obtener información básica del incidente o delito para la página de fotos
    """
    try:
        # Validar tipo de reporte
        if tipo_reporte not in ['incidente', 'delito']:
            return jsonify({
                'success': False,
                'error': 'Tipo de reporte inválido'
            }), 400
        
        if tipo_reporte == 'incidente':
            from backend.models.incidentes_delitos import IncidenteElectoral
            reporte = IncidenteElectoral.query.get(reporte_id)
        else:
            from backend.models.incidentes_delitos import DelitoElectoral
            reporte = DelitoElectoral.query.get(reporte_id)
        
        if not reporte:
            return jsonify({
                'success': False,
                'error': f'{tipo_reporte.title()} no encontrado'
            }), 404
        
        # Obtener estadísticas de fotos
        estadisticas = IncidentesDelitosFotosService.obtener_estadisticas_fotos(tipo_reporte, reporte_id)
        
        reporte_dict = reporte.to_dict()
        reporte_dict['estadisticas_fotos'] = estadisticas
        
        return jsonify({
            'success': True,
            'reporte': reporte_dict,
            'tipo_reporte': tipo_reporte
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener información: {str(e)}'
        }), 500


@incidentes_delitos_fotos_bp.route('/validacion-masiva/<tipo_reporte>/<int:reporte_id>', methods=['POST'])
@jwt_required()
@role_required(['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor_electoral'])
def validacion_masiva(tipo_reporte, reporte_id):
    """
    Validar o rechazar todas las fotos de un reporte
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validar tipo de reporte
        if tipo_reporte not in ['incidente', 'delito']:
            return jsonify({
                'success': False,
                'error': 'Tipo de reporte inválido'
            }), 400
        
        validada = data.get('validada', True)
        comentario = data.get('comentario', '')
        
        # Obtener todas las fotos del reporte
        fotos = IncidentesDelitosFotosService.obtener_fotos(tipo_reporte, reporte_id)
        
        resultados = []
        for foto in fotos:
            try:
                resultado = IncidentesDelitosFotosService.validar_foto(
                    foto_id=foto['id'],
                    validada=validada,
                    comentario=comentario,
                    usuario_id=int(user_id)
                )
                resultados.append({
                    'foto_id': foto['id'],
                    'success': True
                })
            except Exception as e:
                resultados.append({
                    'foto_id': foto['id'],
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'resultados': resultados,
            'message': f'Validación masiva completada: {len([r for r in resultados if r["success"]])} fotos procesadas'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error en validación masiva: {str(e)}'
        }), 500


@incidentes_delitos_fotos_bp.route('/categorias', methods=['GET'])
@jwt_required()
def obtener_categorias():
    """
    Obtener las categorías disponibles para evidencias
    """
    try:
        from backend.models.incidentes_delitos_fotos import IncidenteDelitoFoto
        
        return jsonify({
            'success': True,
            'categorias': IncidenteDelitoFoto.CATEGORIAS,
            'tipos_evidencia': IncidenteDelitoFoto.TIPOS_EVIDENCIA,
            'relevancias': IncidenteDelitoFoto.RELEVANCIAS
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener categorías: {str(e)}'
        }), 500