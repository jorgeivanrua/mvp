"""
Rutas de Ubicaciones (DIVIPOLA) - Accesible para todos
Endpoints públicos necesarios para el proceso de login
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, jwt_required, get_jwt_identity
from functools import wraps
from backend.database import db
from backend.models.location import Location

locations_bp = Blueprint('locations', __name__)

# Constante para el código de Caquetá
CAQUETA_CODE = '44'

def validate_caqueta_code(code):
    """Validar que el código pertenece a Caquetá"""
    if not code:
        return False
    return code.startswith(CAQUETA_CODE)


@locations_bp.route('/departamentos', methods=['GET'])
def get_departamentos():
    """
    Obtener departamento de Caquetá únicamente
    Endpoint público (necesario para login)
    
    Returns:
        JSON con lista de departamentos (solo Caquetá)
    """
    try:
        # Solo retornar Caquetá (código 44)
        departamento = Location.query.filter_by(
            tipo='departamento',
            departamento_codigo=CAQUETA_CODE,
            activo=True
        ).first()
        
        if departamento:
            return jsonify({
                'success': True,
                'data': [{
                    'departamento_codigo': departamento.departamento_codigo,
                    'departamento_nombre': departamento.departamento_nombre
                }]
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el departamento de Caquetá',
                'data': []
            }), 404
            
    except Exception as e:
        print(f"Error en get_departamentos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener departamentos'
        }), 500


@locations_bp.route('/municipios/<departamento_codigo>', methods=['GET'])
def get_municipios(departamento_codigo):
    """
    Obtener municipios de Caquetá
    Endpoint público (necesario para login)
    
    Args:
        departamento_codigo: Código del departamento (debe ser 44)
        
    Returns:
        JSON con lista de municipios
    """
    try:
        # Validar que sea Caquetá
        if departamento_codigo != CAQUETA_CODE:
            return jsonify({
                'success': False,
                'error': f'Solo se permiten consultas para Caquetá (código {CAQUETA_CODE})',
                'data': []
            }), 400
        
        # Obtener municipios activos
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo=CAQUETA_CODE,
            activo=True
        ).order_by(Location.municipio_nombre).all()
        
        if not municipios:
            return jsonify({
                'success': False,
                'error': 'No se encontraron municipios',
                'data': []
            }), 404
        
        return jsonify({
            'success': True,
            'data': [{
                'municipio_codigo': muni.municipio_codigo,
                'municipio_nombre': muni.municipio_nombre
            } for muni in municipios]
        }), 200
        
    except Exception as e:
        print(f"Error en get_municipios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener municipios'
        }), 500


@locations_bp.route('/zonas/<municipio_codigo>', methods=['GET'])
def get_zonas(municipio_codigo):
    """
    Obtener zonas de un municipio de Caquetá
    Endpoint público (necesario para login)
    
    Args:
        municipio_codigo: Código del municipio (debe empezar con 44)
        
    Returns:
        JSON con lista de zonas
    """
    try:
        # Validar que pertenece a Caquetá
        if not validate_caqueta_code(municipio_codigo):
            return jsonify({
                'success': False,
                'error': 'Código de municipio inválido',
                'data': []
            }), 400
        
        # Obtener zonas activas
        zonas = Location.query.filter_by(
            tipo='zona',
            departamento_codigo=CAQUETA_CODE,
            municipio_codigo=municipio_codigo,
            activo=True
        ).order_by(Location.zona_codigo).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'zona_codigo': zona.zona_codigo,
                'zona_nombre': f"Zona {zona.zona_codigo[-2:]}"
            } for zona in zonas]
        }), 200
        
    except Exception as e:
        print(f"Error en get_zonas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener zonas'
        }), 500


@locations_bp.route('/puestos/<zona_codigo>', methods=['GET'])
def get_puestos(zona_codigo):
    """
    Obtener puestos de una zona de Caquetá
    Endpoint público (necesario para login)
    
    Args:
        zona_codigo: Código de la zona (debe empezar con 44)
        
    Returns:
        JSON con lista de puestos
    """
    try:
        # Validar que pertenece a Caquetá
        if not validate_caqueta_code(zona_codigo):
            return jsonify({
                'success': False,
                'error': 'Código de zona inválido',
                'data': []
            }), 400
        
        # Obtener puestos activos
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo=CAQUETA_CODE,
            zona_codigo=zona_codigo,
            activo=True
        ).order_by(Location.puesto_nombre).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'puesto_codigo': puesto.puesto_codigo,
                'puesto_nombre': puesto.puesto_nombre
            } for puesto in puestos]
        }), 200
        
    except Exception as e:
        print(f"Error en get_puestos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener puestos'
        }), 500


@locations_bp.route('/mesas/<puesto_codigo>', methods=['GET'])
def get_mesas(puesto_codigo):
    """
    Obtener mesas de un puesto de Caquetá
    Endpoint público (necesario para login)
    
    Args:
        puesto_codigo: Código del puesto (debe empezar con 44)
        
    Returns:
        JSON con lista de mesas
    """
    try:
        # Validar que pertenece a Caquetá
        if not validate_caqueta_code(puesto_codigo):
            return jsonify({
                'success': False,
                'error': 'Código de puesto inválido',
                'data': []
            }), 400
        
        # Obtener mesas activas
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=CAQUETA_CODE,
            puesto_codigo=puesto_codigo,
            activo=True
        ).order_by(Location.mesa_codigo).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'mesa_codigo': mesa.mesa_codigo,
                'mesa_nombre': mesa.mesa_nombre
            } for mesa in mesas]
        }), 200
        
    except Exception as e:
        print(f"Error en get_mesas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener mesas'
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
