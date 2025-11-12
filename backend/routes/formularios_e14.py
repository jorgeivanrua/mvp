"""
Rutas API para Formularios E-14
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, time
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.database import db
from backend.models.formulario_e14 import FormularioE14, VotoPartido, VotoCandidato
from backend.models.user import User

bp = Blueprint('formularios_e14', __name__, url_prefix='/api/formularios-e14')

@bp.route('', methods=['GET'])
@jwt_required()
def get_formularios():
    """Obtener formularios E-14"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Filtros
        testigo_id = request.args.get('testigo_id', type=int)
        mesa_id = request.args.get('mesa_id', type=int)
        tipo_eleccion_id = request.args.get('tipo_eleccion_id', type=int)
        estado = request.args.get('estado')
        
        query = FormularioE14.query
        
        # Si es testigo, solo ver sus propios formularios
        if current_user.rol == 'testigo':
            query = query.filter_by(testigo_id=current_user.id)
        elif testigo_id:
            query = query.filter_by(testigo_id=testigo_id)
        
        if mesa_id:
            query = query.filter_by(mesa_id=mesa_id)
        if tipo_eleccion_id:
            query = query.filter_by(tipo_eleccion_id=tipo_eleccion_id)
        if estado:
            query = query.filter_by(estado=estado)
        
        formularios = query.order_by(FormularioE14.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [f.to_dict() for f in formularios]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener formularios: {str(e)}'
        }), 500


@bp.route('/<int:formulario_id>', methods=['GET'])
@jwt_required()
def get_formulario(formulario_id):
    """Obtener un formulario específico"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        formulario = FormularioE14.query.get(formulario_id)
        
        if not formulario:
            return jsonify({
                'success': False,
                'message': 'Formulario no encontrado'
            }), 404
        
        # Verificar permisos
        if current_user.rol == 'testigo' and formulario.testigo_id != current_user.id:
            return jsonify({
                'success': False,
                'message': 'No tienes permiso para ver este formulario'
            }), 403
        
        return jsonify({
            'success': True,
            'data': formulario.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener formulario: {str(e)}'
        }), 500


@bp.route('', methods=['POST'])
@jwt_required()
def create_formulario():
    """Crear un nuevo formulario E-14"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Solo testigos pueden crear formularios
        if current_user.rol != 'testigo':
            return jsonify({
                'success': False,
                'message': 'Solo los testigos pueden crear formularios'
            }), 403
        
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = [
            'mesa_id', 'tipo_eleccion_id', 'hora_apertura', 'hora_cierre',
            'total_votantes_registrados', 'total_votos', 'votos_validos',
            'votos_nulos', 'votos_blanco', 'tarjetas_no_marcadas', 'total_tarjetas'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Campo requerido: {field}'
                }), 400
        
        # Convertir horas
        try:
            hora_apertura = datetime.strptime(data['hora_apertura'], '%H:%M').time()
            hora_cierre = datetime.strptime(data['hora_cierre'], '%H:%M').time()
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Formato de hora inválido. Use HH:MM'
            }), 400
        
        # Crear formulario
        formulario = FormularioE14(
            testigo_id=current_user.id,
            mesa_id=data['mesa_id'],
            tipo_eleccion_id=data['tipo_eleccion_id'],
            hora_apertura=hora_apertura,
            hora_cierre=hora_cierre,
            total_votantes_registrados=data['total_votantes_registrados'],
            total_votos=data['total_votos'],
            votos_validos=data['votos_validos'],
            votos_nulos=data['votos_nulos'],
            votos_blanco=data['votos_blanco'],
            tarjetas_no_marcadas=data['tarjetas_no_marcadas'],
            total_tarjetas=data['total_tarjetas'],
            imagen_url=data.get('imagen_url'),
            observaciones=data.get('observaciones')
        )
        
        db.session.add(formulario)
        db.session.flush()  # Para obtener el ID
        
        # Agregar votos por partido
        votos_partidos = data.get('votos_partidos', [])
        for vp in votos_partidos:
            if vp.get('votos', 0) > 0:  # Solo guardar si hay votos
                voto_partido = VotoPartido(
                    formulario_id=formulario.id,
                    partido_id=vp['partido_id'],
                    votos=vp['votos']
                )
                db.session.add(voto_partido)
        
        # Agregar votos por candidato
        votos_candidatos = data.get('votos_candidatos', [])
        for vc in votos_candidatos:
            if vc.get('votos', 0) > 0:  # Solo guardar si hay votos
                voto_candidato = VotoCandidato(
                    formulario_id=formulario.id,
                    candidato_id=vc['candidato_id'],
                    votos=vc['votos']
                )
                db.session.add(voto_candidato)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Formulario E-14 creado exitosamente',
            'data': formulario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al crear formulario: {str(e)}'
        }), 500


@bp.route('/<int:formulario_id>', methods=['PUT'])
@jwt_required()
def update_formulario(formulario_id):
    """Actualizar un formulario E-14"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        formulario = FormularioE14.query.get(formulario_id)
        
        if not formulario:
            return jsonify({
                'success': False,
                'message': 'Formulario no encontrado'
            }), 404
        
        # Verificar permisos
        if current_user.rol == 'testigo' and formulario.testigo_id != current_user.id:
            return jsonify({
                'success': False,
                'message': 'No tienes permiso para editar este formulario'
            }), 403
        
        # Solo permitir edición si está pendiente
        if formulario.estado != 'pendiente':
            return jsonify({
                'success': False,
                'message': 'No se puede editar un formulario validado o rechazado'
            }), 400
        
        data = request.get_json()
        
        # Actualizar campos básicos
        if 'hora_apertura' in data:
            formulario.hora_apertura = datetime.strptime(data['hora_apertura'], '%H:%M').time()
        if 'hora_cierre' in data:
            formulario.hora_cierre = datetime.strptime(data['hora_cierre'], '%H:%M').time()
        
        campos_actualizables = [
            'total_votantes_registrados', 'total_votos', 'votos_validos',
            'votos_nulos', 'votos_blanco', 'tarjetas_no_marcadas',
            'total_tarjetas', 'imagen_url', 'observaciones'
        ]
        
        for campo in campos_actualizables:
            if campo in data:
                setattr(formulario, campo, data[campo])
        
        # Actualizar votos por partido
        if 'votos_partidos' in data:
            # Eliminar votos anteriores
            VotoPartido.query.filter_by(formulario_id=formulario.id).delete()
            
            # Agregar nuevos votos
            for vp in data['votos_partidos']:
                if vp.get('votos', 0) > 0:
                    voto_partido = VotoPartido(
                        formulario_id=formulario.id,
                        partido_id=vp['partido_id'],
                        votos=vp['votos']
                    )
                    db.session.add(voto_partido)
        
        # Actualizar votos por candidato
        if 'votos_candidatos' in data:
            # Eliminar votos anteriores
            VotoCandidato.query.filter_by(formulario_id=formulario.id).delete()
            
            # Agregar nuevos votos
            for vc in data['votos_candidatos']:
                if vc.get('votos', 0) > 0:
                    voto_candidato = VotoCandidato(
                        formulario_id=formulario.id,
                        candidato_id=vc['candidato_id'],
                        votos=vc['votos']
                    )
                    db.session.add(voto_candidato)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Formulario actualizado exitosamente',
            'data': formulario.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al actualizar formulario: {str(e)}'
        }), 500


@bp.route('/<int:formulario_id>/validar', methods=['POST'])
@jwt_required()
def validar_formulario(formulario_id):
    """Validar o rechazar un formulario E-14"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Solo admin y coordinador pueden validar
        if current_user.rol not in ['admin', 'coordinador']:
            return jsonify({
                'success': False,
                'message': 'No tienes permiso para validar formularios'
            }), 403
        
        formulario = FormularioE14.query.get(formulario_id)
        
        if not formulario:
            return jsonify({
                'success': False,
                'message': 'Formulario no encontrado'
            }), 404
        
        data = request.get_json()
        estado = data.get('estado')  # 'validado' o 'rechazado'
        observaciones = data.get('observaciones', '')
        
        if estado not in ['validado', 'rechazado']:
            return jsonify({
                'success': False,
                'message': 'Estado inválido. Use "validado" o "rechazado"'
            }), 400
        
        formulario.estado = estado
        formulario.observaciones = observaciones
        formulario.validado_por = current_user.id
        formulario.fecha_validacion = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Formulario {estado} exitosamente',
            'data': formulario.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al validar formulario: {str(e)}'
        }), 500


@bp.route('/<int:formulario_id>', methods=['DELETE'])
@jwt_required()
def delete_formulario(formulario_id):
    """Eliminar un formulario E-14"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Solo admin puede eliminar
        if current_user.rol != 'admin':
            return jsonify({
                'success': False,
                'message': 'No tienes permiso para eliminar formularios'
            }), 403
        
        formulario = FormularioE14.query.get(formulario_id)
        
        if not formulario:
            return jsonify({
                'success': False,
                'message': 'Formulario no encontrado'
            }), 404
        
        db.session.delete(formulario)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Formulario eliminado exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al eliminar formulario: {str(e)}'
        }), 500
