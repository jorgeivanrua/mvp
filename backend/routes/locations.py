"""
Rutas de ubicaciones
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.location import Location

locations_bp = Blueprint('locations', __name__)


@locations_bp.route('/departamentos', methods=['GET'])
def get_departamentos():
    """Obtener lista de departamentos"""
    try:
        departamentos = Location.query.filter_by(tipo='departamento').all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': d.id,
                'codigo': d.departamento_codigo,
                'nombre': d.departamento_nombre
            } for d in departamentos]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@locations_bp.route('/municipios', methods=['GET'])
def get_municipios():
    """Obtener municipios filtrados por departamento"""
    try:
        dept_codigo = request.args.get('departamento_codigo')
        query = Location.query.filter_by(tipo='municipio')
        
        if dept_codigo:
            query = query.filter_by(departamento_codigo=dept_codigo)
        
        municipios = query.all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': m.id,
                'codigo': m.municipio_codigo,
                'nombre': m.municipio_nombre
            } for m in municipios]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@locations_bp.route('/zonas', methods=['GET'])
def get_zonas():
    """Obtener zonas filtradas"""
    try:
        muni_codigo = request.args.get('municipio_codigo')
        query = Location.query.filter_by(tipo='zona')
        
        if muni_codigo:
            query = query.filter_by(municipio_codigo=muni_codigo)
        
        zonas = query.all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': z.id,
                'codigo': z.zona_codigo,
                'nombre_completo': z.nombre_completo
            } for z in zonas]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@locations_bp.route('/puestos', methods=['GET'])
def get_puestos():
    """Obtener puestos filtrados"""
    try:
        zona_codigo = request.args.get('zona_codigo')
        query = Location.query.filter_by(tipo='puesto')
        
        if zona_codigo:
            query = query.filter_by(zona_codigo=zona_codigo)
        
        puestos = query.all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': p.id,
                'codigo': p.puesto_codigo,
                'nombre': p.puesto_nombre
            } for p in puestos]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@locations_bp.route('/mesas', methods=['GET'])
@jwt_required()
def get_mesas():
    """Obtener mesas filtradas"""
    try:
        puesto_codigo = request.args.get('puesto_codigo')
        departamento_codigo = request.args.get('departamento_codigo')
        municipio_codigo = request.args.get('municipio_codigo')
        zona_codigo = request.args.get('zona_codigo')
        
        query = Location.query.filter_by(tipo='mesa')
        
        if departamento_codigo:
            query = query.filter_by(departamento_codigo=departamento_codigo)
        if municipio_codigo:
            query = query.filter_by(municipio_codigo=municipio_codigo)
        if zona_codigo:
            query = query.filter_by(zona_codigo=zona_codigo)
        if puesto_codigo:
            query = query.filter_by(puesto_codigo=puesto_codigo)
        
        mesas = query.all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': m.id,
                'mesa_codigo': m.mesa_codigo,
                'mesa_nombre': m.mesa_nombre,
                'puesto_codigo': m.puesto_codigo,
                'puesto_nombre': m.puesto_nombre,
                'zona_codigo': m.zona_codigo,
                'municipio_codigo': m.municipio_codigo,
                'municipio_nombre': m.municipio_nombre,
                'departamento_codigo': m.departamento_codigo,
                'departamento_nombre': m.departamento_nombre,
                'nombre_completo': m.nombre_completo,
                'total_votantes_registrados': m.total_votantes_registrados,
                'hombres': m.hombres,
                'mujeres': m.mujeres,
                'direccion': m.direccion
            } for m in mesas]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
