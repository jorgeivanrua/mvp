"""
Endpoints para geolocalización de ubicaciones (puestos, mesas, etc.)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario import FormularioE14
from backend.database import db
from backend.utils.decorators import role_required

locations_geo_bp = Blueprint('locations_geo', __name__, url_prefix='/api/locations')


@locations_geo_bp.route('/puestos-geolocalizados', methods=['GET'])
@jwt_required()
def obtener_puestos_geolocalizados():
    """
    Obtener puestos de votación con coordenadas geográficas
    Filtra según el rol y ubicación del usuario
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Construir query base
        query = Location.query.filter(
            Location.tipo == 'puesto',
            Location.activo == True,
            Location.latitud.isnot(None),
            Location.longitud.isnot(None)
        )
        
        # Filtrar según rol y ubicación
        if user.rol == 'coordinador_puesto' and user.ubicacion_id:
            # Solo su puesto
            ubicacion = Location.query.get(user.ubicacion_id)
            if ubicacion:
                query = query.filter_by(
                    puesto_codigo=ubicacion.puesto_codigo,
                    departamento_codigo=ubicacion.departamento_codigo,
                    municipio_codigo=ubicacion.municipio_codigo
                )
        
        elif user.rol == 'coordinador_municipal' and user.ubicacion_id:
            # Puestos del municipio
            ubicacion = Location.query.get(user.ubicacion_id)
            if ubicacion:
                query = query.filter_by(
                    municipio_codigo=ubicacion.municipio_codigo,
                    departamento_codigo=ubicacion.departamento_codigo
                )
        
        elif user.rol == 'coordinador_departamental' and user.ubicacion_id:
            # Puestos del departamento
            ubicacion = Location.query.get(user.ubicacion_id)
            if ubicacion:
                query = query.filter_by(
                    departamento_codigo=ubicacion.departamento_codigo
                )
        
        elif user.rol == 'testigo_electoral' and user.ubicacion_id:
            # Puesto de su mesa
            mesa = Location.query.get(user.ubicacion_id)
            if mesa and mesa.tipo == 'mesa':
                query = query.filter_by(
                    puesto_codigo=mesa.puesto_codigo,
                    departamento_codigo=mesa.departamento_codigo,
                    municipio_codigo=mesa.municipio_codigo
                )
        
        # Ejecutar query
        puestos = query.all()
        
        # Formatear respuesta con estadísticas
        puestos_data = []
        for puesto in puestos:
            # Contar mesas del puesto
            mesas = Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa',
                activo=True
            ).count()
            
            # Contar formularios del puesto
            mesa_ids = [m.id for m in Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa'
            ).all()]
            
            formularios_count = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids)
            ).count()
            
            formularios_validados = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids),
                FormularioE14.estado == 'validado'
            ).count()
            
            puestos_data.append({
                'id': puesto.id,
                'puesto_codigo': puesto.puesto_codigo,
                'puesto_nombre': puesto.puesto_nombre,
                'municipio_codigo': puesto.municipio_codigo,
                'municipio_nombre': puesto.municipio_nombre,
                'departamento_codigo': puesto.departamento_codigo,
                'departamento_nombre': puesto.departamento_nombre,
                'zona_codigo': puesto.zona_codigo,
                'zona_nombre': puesto.zona_nombre,
                'direccion': puesto.direccion,
                'latitud': float(puesto.latitud),
                'longitud': float(puesto.longitud),
                'nombre_completo': puesto.nombre_completo,
                'total_mesas': mesas,
                'total_formularios': formularios_count,
                'formularios_validados': formularios_validados,
                'porcentaje_avance': round((formularios_validados / mesas * 100) if mesas > 0 else 0, 2)
            })
        
        return jsonify({
            'success': True,
            'data': puestos_data
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error obteniendo puestos geolocalizados: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error al obtener puestos geolocalizados: {str(e)}'
        }), 500


@locations_geo_bp.route('/mesas-geolocalizadas', methods=['GET'])
@jwt_required()
def obtener_mesas_geolocalizadas():
    """
    Obtener mesas de votación con coordenadas geográficas
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Construir query base
        query = Location.query.filter(
            Location.tipo == 'mesa',
            Location.activo == True,
            Location.latitud.isnot(None),
            Location.longitud.isnot(None)
        )
        
        # Filtrar según rol
        if user.rol == 'coordinador_puesto' and user.ubicacion_id:
            ubicacion = Location.query.get(user.ubicacion_id)
            if ubicacion:
                query = query.filter_by(
                    puesto_codigo=ubicacion.puesto_codigo,
                    departamento_codigo=ubicacion.departamento_codigo,
                    municipio_codigo=ubicacion.municipio_codigo,
                    zona_codigo=ubicacion.zona_codigo
                )
        
        elif user.rol == 'coordinador_municipal' and user.ubicacion_id:
            ubicacion = Location.query.get(user.ubicacion_id)
            if ubicacion:
                query = query.filter_by(
                    municipio_codigo=ubicacion.municipio_codigo,
                    departamento_codigo=ubicacion.departamento_codigo
                )
        
        # Ejecutar query
        mesas = query.all()
        
        # Formatear respuesta
        mesas_data = []
        for mesa in mesas:
            # Obtener testigo asignado
            testigo = User.query.filter_by(
                ubicacion_id=mesa.id,
                rol='testigo_electoral',
                activo=True
            ).first()
            
            # Obtener formulario
            formulario = FormularioE14.query.filter_by(mesa_id=mesa.id).first()
            
            mesas_data.append({
                'id': mesa.id,
                'mesa_codigo': mesa.mesa_codigo,
                'puesto_codigo': mesa.puesto_codigo,
                'puesto_nombre': mesa.puesto_nombre,
                'latitud': float(mesa.latitud),
                'longitud': float(mesa.longitud),
                'nombre_completo': mesa.nombre_completo,
                'testigo_asignado': testigo.nombre if testigo else None,
                'testigo_presente': testigo.presencia_verificada if testigo else False,
                'tiene_formulario': formulario is not None,
                'estado_formulario': formulario.estado if formulario else None
            })
        
        return jsonify({
            'success': True,
            'data': mesas_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener mesas geolocalizadas: {str(e)}'
        }), 500
