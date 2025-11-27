"""
Rutas de Ubicaciones (DIVIPOLA) - Accesible para todos los roles
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from backend.database import db
from backend.models.location import Location

locations_bp = Blueprint('locations', __name__, url_prefix='/api/locations')


@locations_bp.route('/departamentos', methods=['GET'])
@jwt_required()
def get_departamentos():
    """
    Obtener departamento de Caquetá únicamente
    Accesible para todos los roles autenticados
    """
    try:
        # Solo retornar Caquetá (código 44)
        departamento = db.session.query(Location).filter(
            Location.tipo == 'departamento',
            Location.departamento_codigo == '44'
        ).first()
        
        if departamento:
            return jsonify({
                'success': True,
                'data': [{
                    'departamento_codigo': departamento.departamento_codigo,
                    'departamento_nombre': departamento.departamento_nombre
                }]
            })
        else:
            return jsonify({
                'success': True,
                'data': []
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@locations_bp.route('/municipios/<departamento_codigo>', methods=['GET'])
@jwt_required()
def get_municipios(departamento_codigo):
    """
    Obtener municipios de Caquetá
    Accesible para todos los roles autenticados
    """
    try:
        # Solo permitir consultas para Caquetá
        if departamento_codigo != '44':
            return jsonify({
                'success': True,
                'data': []
            })
        
        municipios = db.session.query(Location).filter(
            Location.tipo == 'municipio',
            Location.departamento_codigo == '44'
        ).order_by(Location.municipio_nombre).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'municipio_codigo': muni.municipio_codigo,
                'municipio_nombre': muni.municipio_nombre
            } for muni in municipios]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@locations_bp.route('/zonas/<municipio_codigo>', methods=['GET'])
@jwt_required()
def get_zonas(municipio_codigo):
    """
    Obtener zonas de un municipio de Caquetá
    Accesible para todos los roles autenticados
    """
    try:
        zonas = db.session.query(Location).filter(
            Location.tipo == 'zona',
            Location.departamento_codigo == '44',
            Location.municipio_codigo == municipio_codigo
        ).order_by(Location.zona_codigo).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'zona_codigo': zona.zona_codigo,
                'zona_nombre': f"Zona {zona.zona_codigo[-2:]}"
            } for zona in zonas]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@locations_bp.route('/puestos/<zona_codigo>', methods=['GET'])
@jwt_required()
def get_puestos(zona_codigo):
    """
    Obtener puestos de una zona de Caquetá
    Accesible para todos los roles autenticados
    """
    try:
        puestos = db.session.query(Location).filter(
            Location.tipo == 'puesto',
            Location.departamento_codigo == '44',
            Location.zona_codigo == zona_codigo
        ).order_by(Location.puesto_nombre).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'puesto_codigo': puesto.puesto_codigo,
                'puesto_nombre': puesto.puesto_nombre
            } for puesto in puestos]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@locations_bp.route('/mesas/<puesto_codigo>', methods=['GET'])
@jwt_required()
def get_mesas(puesto_codigo):
    """
    Obtener mesas de un puesto de Caquetá
    Accesible para todos los roles autenticados
    """
    try:
        mesas = db.session.query(Location).filter(
            Location.tipo == 'mesa',
            Location.departamento_codigo == '44',
            Location.puesto_codigo == puesto_codigo
        ).order_by(Location.mesa_codigo).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'mesa_codigo': mesa.mesa_codigo,
                'mesa_nombre': mesa.mesa_nombre
            } for mesa in mesas]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@locations_bp.route('/partidos', methods=['GET'])
@jwt_required()
def get_partidos():
    """
    Obtener todos los partidos activos
    Accesible para todos los roles autenticados
    """
    try:
        from backend.models.configuracion_electoral import Partido
        
        partidos = Partido.query.filter_by(activo=True).order_by(Partido.nombre).all()
        
        return jsonify({
            'success': True,
            'data': [partido.to_dict() for partido in partidos]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@locations_bp.route('/tipos-eleccion', methods=['GET'])
@jwt_required()
def get_tipos_eleccion():
    """
    Obtener todos los tipos de elección activos
    Accesible para todos los roles autenticados
    """
    try:
        from backend.models.configuracion_electoral import TipoEleccion
        
        tipos = TipoEleccion.query.filter_by(activo=True).order_by(TipoEleccion.nombre).all()
        
        return jsonify({
            'success': True,
            'data': [tipo.to_dict() for tipo in tipos]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
