"""
Rutas para Auditor Electoral
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14
from backend.database import db

auditor_bp = Blueprint('auditor', __name__)


@auditor_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Estadísticas de auditoría"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'auditor_electoral':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Obtener formularios del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        # Analizar formularios
        formularios_completados = sum(1 for f in formularios if f.estado == 'completado')
        formularios_pendientes = sum(1 for f in formularios if f.estado == 'pendiente')
        formularios_en_revision = sum(1 for f in formularios if f.estado == 'en_revision')
        
        # TODO: Implementar detección de inconsistencias
        inconsistencias_detectadas = 0
        
        stats = {
            'total_formularios': len(formularios),
            'formularios_completados': formularios_completados,
            'formularios_pendientes': formularios_pendientes,
            'formularios_en_revision': formularios_en_revision,
            'inconsistencias_detectadas': inconsistencias_detectadas,
            'porcentaje_auditado': (formularios_completados / len(formularios) * 100) if formularios else 0,
            'departamento': {
                'id': departamento.id,
                'nombre': departamento.nombre_completo,
                'codigo': departamento.departamento_codigo
            }
        }
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auditor_bp.route('/inconsistencias', methods=['GET'])
@jwt_required()
def get_inconsistencias():
    """Obtener inconsistencias detectadas"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'auditor_electoral':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        # TODO: Implementar lógica de detección de inconsistencias
        # Por ahora retornamos lista vacía
        inconsistencias_data = []
        
        return jsonify({
            'success': True,
            'data': inconsistencias_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auditor_bp.route('/reportes', methods=['GET'])
@jwt_required()
def get_reportes():
    """Obtener reportes de auditoría"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'auditor_electoral':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Obtener formularios del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).order_by(FormularioE14.updated_at.desc()).limit(100).all() if mesa_ids else []
        
        reportes_data = []
        for formulario in formularios:
            mesa = Location.query.get(formulario.mesa_id)
            testigo = User.query.get(formulario.testigo_id)
            
            reportes_data.append({
                'id': formulario.id,
                'mesa_id': formulario.mesa_id,
                'mesa_nombre': mesa.nombre_completo if mesa else None,
                'testigo_id': formulario.testigo_id,
                'testigo_nombre': testigo.nombre if testigo else None,
                'estado': formulario.estado,
                'created_at': formulario.created_at.isoformat() if formulario.created_at else None,
                'updated_at': formulario.updated_at.isoformat() if formulario.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': reportes_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auditor_bp.route('/formularios', methods=['GET'])
@jwt_required()
def get_formularios():
    """Obtener formularios para auditar"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'auditor_electoral':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        departamento = Location.query.get(user.ubicacion_id)
        
        # Filtrar por estado si se proporciona
        estado = request.args.get('estado')
        
        # Obtener formularios del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        query = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ) if mesa_ids else FormularioE14.query.filter(False)
        
        if estado:
            query = query.filter_by(estado=estado)
        
        formularios = query.order_by(FormularioE14.updated_at.desc()).all()
        
        formularios_data = []
        for formulario in formularios:
            mesa = Location.query.get(formulario.mesa_id)
            testigo = User.query.get(formulario.testigo_id)
            
            formularios_data.append({
                'id': formulario.id,
                'mesa_id': formulario.mesa_id,
                'mesa_nombre': mesa.nombre_completo if mesa else None,
                'testigo_id': formulario.testigo_id,
                'testigo_nombre': testigo.nombre if testigo else None,
                'estado': formulario.estado,
                'created_at': formulario.created_at.isoformat() if formulario.created_at else None,
                'updated_at': formulario.updated_at.isoformat() if formulario.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': formularios_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
