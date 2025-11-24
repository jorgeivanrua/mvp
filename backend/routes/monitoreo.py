"""
Rutas para el rol de Monitoreo
Dashboard de monitoreo en tiempo real con geolocalización
"""
from flask import Blueprint, render_template, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.database import db
from backend.utils.decorators import role_required

monitoreo_bp = Blueprint('monitoreo', __name__, url_prefix='/monitoreo')


@monitoreo_bp.route('/dashboard')
@jwt_required()
@role_required('monitoreo')
def dashboard():
    """Dashboard principal de monitoreo"""
    return render_template('monitoreo/dashboard.html')


@monitoreo_bp.route('/api/usuarios-activos', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_usuarios_activos():
    """
    Obtener todos los usuarios activos con su última geolocalización
    """
    try:
        # Obtener todos los usuarios activos con geolocalización
        usuarios = User.query.filter(
            User.activo == True,
            User.ultima_latitud.isnot(None),
            User.ultima_longitud.isnot(None)
        ).all()
        
        usuarios_data = []
        for usuario in usuarios:
            ubicacion = None
            if usuario.ubicacion_id:
                location = Location.query.get(usuario.ubicacion_id)
                if location:
                    ubicacion = location.to_dict()
            
            usuarios_data.append({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'rol': usuario.rol,
                'latitud': usuario.ultima_latitud,
                'longitud': usuario.ultima_longitud,
                'precision': usuario.precision_geolocalizacion,
                'ultima_actualizacion': usuario.ultima_geolocalizacion_at.isoformat() if usuario.ultima_geolocalizacion_at else None,
                'ubicacion': ubicacion,
                'presencia_verificada': usuario.presencia_verificada if usuario.rol == 'testigo_electoral' else None
            })
        
        return jsonify({
            'success': True,
            'data': usuarios_data,
            'total': len(usuarios_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@monitoreo_bp.route('/api/estadisticas', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_estadisticas():
    """
    Obtener estadísticas generales del sistema
    """
    try:
        # Contar usuarios por rol
        testigos_total = User.query.filter_by(rol='testigo_electoral', activo=True).count()
        testigos_con_geo = User.query.filter(
            User.rol == 'testigo_electoral',
            User.activo == True,
            User.ultima_latitud.isnot(None)
        ).count()
        testigos_presencia = User.query.filter(
            User.rol == 'testigo_electoral',
            User.activo == True,
            User.presencia_verificada == True
        ).count()
        
        coordinadores_total = User.query.filter(
            User.rol.in_(['coordinador_departamental', 'coordinador_municipal', 'coordinador_puesto']),
            User.activo == True
        ).count()
        coordinadores_con_geo = User.query.filter(
            User.rol.in_(['coordinador_departamental', 'coordinador_municipal', 'coordinador_puesto']),
            User.activo == True,
            User.ultima_latitud.isnot(None)
        ).count()
        
        # Contar formularios
        from backend.models.formulario_e14 import FormularioE14
        formularios_total = FormularioE14.query.count()
        formularios_validados = FormularioE14.query.filter_by(estado='validado').count()
        formularios_pendientes = FormularioE14.query.filter_by(estado='pendiente').count()
        
        return jsonify({
            'success': True,
            'data': {
                'testigos': {
                    'total': testigos_total,
                    'con_geolocalizacion': testigos_con_geo,
                    'con_presencia_verificada': testigos_presencia,
                    'porcentaje_geo': round((testigos_con_geo / testigos_total * 100), 2) if testigos_total > 0 else 0
                },
                'coordinadores': {
                    'total': coordinadores_total,
                    'con_geolocalizacion': coordinadores_con_geo,
                    'porcentaje_geo': round((coordinadores_con_geo / coordinadores_total * 100), 2) if coordinadores_total > 0 else 0
                },
                'formularios': {
                    'total': formularios_total,
                    'validados': formularios_validados,
                    'pendientes': formularios_pendientes
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
