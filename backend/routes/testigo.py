"""
Rutas para testigos electorales
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.configuracion_electoral import TipoEleccion, Partido
from backend.database import db

testigo_bp = Blueprint('testigo', __name__)


@testigo_bp.route('/info', methods=['GET'])
@jwt_required()
def get_testigo_info():
    """
    Obtener información del testigo actual
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        if user.rol != 'testigo_electoral':
            return jsonify({
                'success': False,
                'error': 'Solo testigos pueden acceder a este endpoint'
            }), 403
        
        # Obtener ubicación
        ubicacion = None
        if user.ubicacion_id:
            location = Location.query.get(user.ubicacion_id)
            if location:
                ubicacion = {
                    'id': location.id,
                    'nombre_completo': location.nombre_completo,
                    'tipo': location.tipo,
                    'departamento_codigo': location.departamento_codigo,
                    'municipio_codigo': location.municipio_codigo,
                    'zona_codigo': location.zona_codigo,
                    'puesto_codigo': location.puesto_codigo,
                    'puesto_nombre': location.puesto_nombre
                }
        
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'id': user.id,
                    'nombre': user.nombre,
                    'rol': user.rol,
                    'activo': user.activo,
                    'presencia_verificada': user.presencia_verificada,
                    'presencia_verificada_at': user.presencia_verificada_at.isoformat() if user.presencia_verificada_at else None,
                    'ultimo_acceso': user.ultimo_acceso.isoformat() if user.ultimo_acceso else None
                },
                'ubicacion': ubicacion
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigo_bp.route('/mesa', methods=['GET'])
@jwt_required()
def get_testigo_mesa():
    """
    Obtener información de la mesa asignada al testigo
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        if user.rol != 'testigo_electoral':
            return jsonify({
                'success': False,
                'error': 'Solo testigos pueden acceder a este endpoint'
            }), 403
        
        # El testigo está asignado a un puesto, no a una mesa específica
        # Obtener todas las mesas del puesto
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Testigo sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        if not puesto or puesto.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Ubicación inválida'
            }), 400
        
        # Obtener mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo,
            activo=True
        ).all()
        
        mesas_data = []
        for mesa in mesas:
            mesas_data.append({
                'id': mesa.id,
                'nombre_completo': mesa.nombre_completo,
                'mesa_codigo': mesa.mesa_codigo,
                'puesto_nombre': mesa.puesto_nombre,
                'total_votantes_registrados': mesa.total_votantes_registrados,
                'mujeres': mesa.mujeres,
                'hombres': mesa.hombres
            })
        
        return jsonify({
            'success': True,
            'data': {
                'puesto': {
                    'id': puesto.id,
                    'nombre_completo': puesto.nombre_completo,
                    'puesto_codigo': puesto.puesto_codigo,
                    'puesto_nombre': puesto.puesto_nombre
                },
                'mesas': mesas_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigo_bp.route('/tipos-eleccion', methods=['GET'])
@jwt_required()
def get_tipos_eleccion():
    """
    Obtener tipos de elección disponibles
    """
    try:
        tipos = TipoEleccion.query.filter_by(activo=True).order_by(TipoEleccion.orden).all()
        
        tipos_data = []
        for tipo in tipos:
            tipos_data.append({
                'id': tipo.id,
                'codigo': tipo.codigo,
                'nombre': tipo.nombre,
                'descripcion': tipo.descripcion,
                'es_uninominal': tipo.es_uninominal,
                'permite_lista_cerrada': tipo.permite_lista_cerrada,
                'permite_lista_abierta': tipo.permite_lista_abierta,
                'permite_coaliciones': tipo.permite_coaliciones
            })
        
        return jsonify({
            'success': True,
            'data': tipos_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigo_bp.route('/partidos', methods=['GET'])
@jwt_required()
def get_partidos():
    """
    Obtener partidos políticos disponibles
    """
    try:
        partidos = Partido.query.filter_by(activo=True).order_by(Partido.orden).all()
        
        partidos_data = []
        for partido in partidos:
            partidos_data.append({
                'id': partido.id,
                'codigo': partido.codigo,
                'nombre': partido.nombre,
                'nombre_corto': partido.nombre_corto,
                'color': partido.color,
                'logo_url': partido.logo_url
            })
        
        return jsonify({
            'success': True,
            'data': partidos_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@testigo_bp.route('/candidatos', methods=['GET'])
@jwt_required()
def get_candidatos():
    """
    Obtener candidatos por tipo de elección
    Query params:
        - tipo_eleccion_id: ID del tipo de elección (opcional)
    """
    try:
        from backend.models.configuracion_electoral import Candidato
        
        tipo_eleccion_id = request.args.get('tipo_eleccion_id', type=int)
        
        query = Candidato.query.filter_by(activo=True)
        
        if tipo_eleccion_id:
            query = query.filter_by(tipo_eleccion_id=tipo_eleccion_id)
        
        candidatos = query.order_by(Candidato.orden).all()
        
        candidatos_data = []
        for candidato in candidatos:
            partido = Partido.query.get(candidato.partido_id) if candidato.partido_id else None
            tipo_eleccion = TipoEleccion.query.get(candidato.tipo_eleccion_id) if candidato.tipo_eleccion_id else None
            
            candidatos_data.append({
                'id': candidato.id,
                'codigo': candidato.codigo,
                'nombre_completo': candidato.nombre_completo,
                'numero_lista': candidato.numero_lista,
                'partido_id': candidato.partido_id,
                'partido_nombre': partido.nombre if partido else None,
                'partido_nombre_corto': partido.nombre_corto if partido else None,
                'partido_color': partido.color if partido else None,
                'tipo_eleccion_id': candidato.tipo_eleccion_id,
                'tipo_eleccion_nombre': tipo_eleccion.nombre if tipo_eleccion else None,
                'foto_url': candidato.foto_url,
                'es_independiente': candidato.es_independiente,
                'es_cabeza_lista': candidato.es_cabeza_lista
            })
        
        return jsonify({
            'success': True,
            'data': candidatos_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
