"""
Rutas para manejo de fotos de formularios E-14
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.formulario_fotos_service import FormularioFotosService
from backend.utils.decorators import role_required
from backend.utils.exceptions import ValidationException, NotFoundException

formulario_fotos_bp = Blueprint('formulario_fotos', __name__, url_prefix='/api/formulario-fotos')


@formulario_fotos_bp.route('/subir/<int:formulario_id>', methods=['POST'])
@jwt_required()
@role_required(['testigo_electoral', 'coordinador_puesto', 'coordinador_municipal'])
def subir_foto(formulario_id):
    """
    Subir una foto para un formulario E-14
    """
    try:
        user_id = get_jwt_identity()
        
        # Obtener archivo
        if 'foto' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se encontró archivo de foto'
            }), 400
        
        file = request.files['foto']
        descripcion = request.form.get('descripcion', '')
        
        resultado = FormularioFotosService.subir_foto(
            formulario_id=formulario_id,
            file=file,
            descripcion=descripcion,
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


@formulario_fotos_bp.route('/formulario/<int:formulario_id>', methods=['GET'])
@jwt_required()
def obtener_fotos(formulario_id):
    """
    Obtener todas las fotos de un formulario
    """
    try:
        fotos = FormularioFotosService.obtener_fotos(formulario_id)
        
        return jsonify({
            'success': True,
            'fotos': fotos,
            'total': len(fotos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener fotos: {str(e)}'
        }), 500


@formulario_fotos_bp.route('/eliminar/<int:foto_id>', methods=['DELETE'])
@jwt_required()
@role_required(['testigo_electoral', 'coordinador_puesto', 'coordinador_municipal'])
def eliminar_foto(foto_id):
    """
    Eliminar una foto
    """
    try:
        user_id = get_jwt_identity()
        
        resultado = FormularioFotosService.eliminar_foto(
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


@formulario_fotos_bp.route('/validar/<int:foto_id>', methods=['POST'])
@jwt_required()
@role_required(['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental'])
def validar_foto(foto_id):
    """
    Validar o rechazar una foto
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        validada = data.get('validada', True)
        comentario = data.get('comentario', '')
        
        resultado = FormularioFotosService.validar_foto(
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


@formulario_fotos_bp.route('/principal/<int:foto_id>', methods=['POST'])
@jwt_required()
@role_required(['testigo_electoral', 'coordinador_puesto', 'coordinador_municipal'])
def establecer_principal(foto_id):
    """
    Establecer una foto como principal
    """
    try:
        user_id = get_jwt_identity()
        
        resultado = FormularioFotosService.establecer_principal(
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


@formulario_fotos_bp.route('/reordenar/<int:formulario_id>', methods=['POST'])
@jwt_required()
@role_required(['testigo_electoral', 'coordinador_puesto', 'coordinador_municipal'])
def reordenar_fotos(formulario_id):
    """
    Reordenar fotos de un formulario
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        orden_fotos = data.get('orden_fotos', [])
        
        if not orden_fotos:
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar el orden de las fotos'
            }), 400
        
        resultado = FormularioFotosService.reordenar_fotos(
            formulario_id=formulario_id,
            orden_fotos=orden_fotos,
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


@formulario_fotos_bp.route('/info/<int:formulario_id>', methods=['GET'])
@jwt_required()
def obtener_info_formulario(formulario_id):
    """
    Obtener información básica del formulario para la página de fotos
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        
        formulario = FormularioE14.query.get(formulario_id)
        if not formulario:
            return jsonify({
                'success': False,
                'error': 'Formulario no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'formulario': formulario.to_dict(include_fotos=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener información: {str(e)}'
        }), 500


@formulario_fotos_bp.route('/validacion-masiva/<int:formulario_id>', methods=['POST'])
@jwt_required()
@role_required(['coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental'])
def validacion_masiva(formulario_id):
    """
    Validar o rechazar todas las fotos de un formulario
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        validada = data.get('validada', True)
        comentario = data.get('comentario', '')
        
        # Obtener todas las fotos del formulario
        fotos = FormularioFotosService.obtener_fotos(formulario_id)
        
        resultados = []
        for foto in fotos:
            try:
                resultado = FormularioFotosService.validar_foto(
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