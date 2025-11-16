"""
Rutas para Coordinador Departamental
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14
from backend.database import db

bp = Blueprint('coordinador_departamental', __name__)


@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Estadísticas departamentales"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_departamental':
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
        
        # Obtener ubicaciones del departamento
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).count()
        
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).count()
        
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).count()
        
        # Obtener formularios del departamento
        mesa_ids = [m.id for m in Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()]
        
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        formularios_completados = sum(1 for f in formularios if f.estado == 'completado')
        
        stats = {
            'total_municipios': municipios,
            'total_puestos': puestos,
            'total_mesas': mesas,
            'total_formularios': len(formularios),
            'formularios_completados': formularios_completados,
            'formularios_pendientes': len(formularios) - formularios_completados,
            'porcentaje_avance': (formularios_completados / len(formularios) * 100) if formularios else 0,
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


@bp.route('/municipios', methods=['GET'])
@jwt_required()
def get_municipios():
    """Obtener municipios del departamento"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_departamental':
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
        
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()
        
        municipios_data = []
        for municipio in municipios:
            # Contar puestos y mesas del municipio
            puestos_count = Location.query.filter_by(
                tipo='puesto',
                departamento_codigo=municipio.departamento_codigo,
                municipio_codigo=municipio.municipio_codigo,
                activo=True
            ).count()
            
            mesas_count = Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=municipio.departamento_codigo,
                municipio_codigo=municipio.municipio_codigo,
                activo=True
            ).count()
            
            # Obtener formularios del municipio
            mesa_ids = [m.id for m in Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=municipio.departamento_codigo,
                municipio_codigo=municipio.municipio_codigo,
                activo=True
            ).all()]
            
            formularios = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids)
            ).all() if mesa_ids else []
            
            formularios_completados = sum(1 for f in formularios if f.estado == 'completado')
            
            municipios_data.append({
                'id': municipio.id,
                'nombre': municipio.municipio_nombre,
                'nombre_completo': municipio.nombre_completo,
                'municipio_codigo': municipio.municipio_codigo,
                'total_puestos': puestos_count,
                'total_mesas': mesas_count,
                'total_formularios': len(formularios),
                'formularios_completados': formularios_completados,
                'porcentaje_avance': (formularios_completados / len(formularios) * 100) if formularios else 0
            })
        
        return jsonify({
            'success': True,
            'data': municipios_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/resumen', methods=['GET'])
@jwt_required()
def get_resumen():
    """Resumen de avance departamental"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_departamental':
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
        
        # Obtener resumen por municipio
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=departamento.departamento_codigo,
            activo=True
        ).all()
        
        resumen_municipios = []
        total_mesas_depto = 0
        total_formularios_depto = 0
        total_completados_depto = 0
        
        for municipio in municipios:
            mesa_ids = [m.id for m in Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=municipio.departamento_codigo,
                municipio_codigo=municipio.municipio_codigo,
                activo=True
            ).all()]
            
            mesas_count = len(mesa_ids)
            formularios = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids)
            ).all() if mesa_ids else []
            
            formularios_completados = sum(1 for f in formularios if f.estado == 'completado')
            
            total_mesas_depto += mesas_count
            total_formularios_depto += len(formularios)
            total_completados_depto += formularios_completados
            
            resumen_municipios.append({
                'municipio': municipio.municipio_nombre,
                'total_mesas': mesas_count,
                'formularios_completados': formularios_completados,
                'porcentaje_avance': (formularios_completados / mesas_count * 100) if mesas_count > 0 else 0
            })
        
        resumen = {
            'departamento': departamento.nombre_completo,
            'total_municipios': len(municipios),
            'total_mesas': total_mesas_depto,
            'total_formularios': total_formularios_depto,
            'formularios_completados': total_completados_depto,
            'porcentaje_avance_general': (total_completados_depto / total_mesas_depto * 100) if total_mesas_depto > 0 else 0,
            'resumen_por_municipio': resumen_municipios
        }
        
        return jsonify({
            'success': True,
            'data': resumen
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
