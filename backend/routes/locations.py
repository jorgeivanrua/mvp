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


def _auto_load_divipola():
    """
    Cargar datos de DIVIPOLA automáticamente si la BD está vacía
    """
    import os
    import csv
    
    try:
        # Verificar si ya hay datos
        total_locations = Location.query.count()
        if total_locations > 0:
            print(f"[AUTO-LOAD] BD ya tiene {total_locations} ubicaciones, omitiendo carga")
            return True
        
        print("[AUTO-LOAD] BD vacía, cargando DIVIPOLA automáticamente...")
        
        # Buscar archivo CSV
        csv_paths = ['divipola.csv', 'todos los datos/divipola.csv', 'data/divipola.csv']
        csv_path = None
        for path in csv_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if not csv_path:
            print("[AUTO-LOAD] ERROR: No se encontró divipola.csv")
            return False
        
        print(f"[AUTO-LOAD] Cargando desde: {csv_path}")
        
        # Cargar datos
        locations_added = 0
        departamentos = {}
        municipios = {}
        zonas = {}
        puestos = {}
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                dd = row['dd'].strip().zfill(2)
                
                # SOLO CAQUETÁ
                if dd != '44':
                    continue
                
                mm = row['mm'].strip().zfill(2)
                zz = row['zz'].strip().zfill(2)
                pp = row['pp'].strip().zfill(2)
                mesa = row['mesa'].strip().zfill(2)
                
                departamento_nombre = row['departamento'].strip()
                municipio_nombre = row['municipio'].strip()
                puesto_nombre = row['puesto'].strip()
                mesa_nombre = row['mesa_nombre'].strip()
                
                depto_codigo = dd
                muni_codigo = f"{dd}{mm}"
                zona_codigo = f"{dd}{mm}{zz}"
                puesto_codigo = f"{dd}{mm}{zz}{pp}"
                mesa_codigo = f"{dd}{mm}{zz}{pp}{mesa}"
                
                # Departamento
                if dd not in departamentos:
                    dept = Location(
                        departamento_codigo=depto_codigo,
                        departamento_nombre=departamento_nombre,
                        nombre_completo=departamento_nombre,
                        tipo='departamento',
                        activo=True
                    )
                    db.session.add(dept)
                    db.session.flush()
                    departamentos[dd] = dept.id
                    locations_added += 1
                
                # Municipio
                if muni_codigo not in municipios:
                    muni = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        departamento_nombre=departamento_nombre,
                        municipio_nombre=municipio_nombre,
                        nombre_completo=f"{departamento_nombre} - {municipio_nombre}",
                        tipo='municipio',
                        parent_id=departamentos[dd],
                        activo=True
                    )
                    db.session.add(muni)
                    db.session.flush()
                    municipios[muni_codigo] = muni.id
                    locations_added += 1
                
                # Zona
                if zona_codigo not in zonas:
                    zona = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        zona_codigo=zona_codigo,
                        departamento_nombre=departamento_nombre,
                        municipio_nombre=municipio_nombre,
                        nombre_completo=f"{departamento_nombre} - {municipio_nombre} - Zona {zz}",
                        tipo='zona',
                        parent_id=municipios[muni_codigo],
                        activo=True
                    )
                    db.session.add(zona)
                    db.session.flush()
                    zonas[zona_codigo] = zona.id
                    locations_added += 1
                
                # Puesto
                if puesto_codigo not in puestos:
                    puesto = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        zona_codigo=zona_codigo,
                        puesto_codigo=puesto_codigo,
                        departamento_nombre=departamento_nombre,
                        municipio_nombre=municipio_nombre,
                        puesto_nombre=puesto_nombre,
                        nombre_completo=f"{departamento_nombre} - {municipio_nombre} - Zona {zz} - {puesto_nombre}",
                        tipo='puesto',
                        direccion=row.get('direccion', '').strip() or None,
                        comuna=row.get('comuna', '').strip() or None,
                        latitud=float(row['LATITUD']) if row.get('LATITUD', '').strip() else None,
                        longitud=float(row['LONGITUD']) if row.get('LONGITUD', '').strip() else None,
                        parent_id=zonas[zona_codigo],
                        activo=True
                    )
                    db.session.add(puesto)
                    db.session.flush()
                    puestos[puesto_codigo] = puesto.id
                    locations_added += 1
                
                # Mesa
                mesa_location = Location(
                    departamento_codigo=depto_codigo,
                    municipio_codigo=muni_codigo,
                    zona_codigo=zona_codigo,
                    puesto_codigo=puesto_codigo,
                    mesa_codigo=mesa_codigo,
                    departamento_nombre=departamento_nombre,
                    municipio_nombre=municipio_nombre,
                    puesto_nombre=puesto_nombre,
                    mesa_nombre=mesa_nombre,
                    nombre_completo=f"{departamento_nombre} - {municipio_nombre} - Zona {zz} - {puesto_nombre} - Mesa {mesa}",
                    tipo='mesa',
                    total_votantes_registrados=int(row.get('total_mesa', 0) or 0),
                    mujeres=int(row.get('mujeres_mesa', 0) or 0),
                    hombres=int(row.get('hombres_mesa', 0) or 0),
                    direccion=row.get('direccion', '').strip() or None,
                    comuna=row.get('comuna', '').strip() or None,
                    latitud=float(row['LATITUD']) if row.get('LATITUD', '').strip() else None,
                    longitud=float(row['LONGITUD']) if row.get('LONGITUD', '').strip() else None,
                    parent_id=puestos[puesto_codigo],
                    activo=True
                )
                db.session.add(mesa_location)
                locations_added += 1
                
                if locations_added % 100 == 0:
                    db.session.commit()
        
        db.session.commit()
        
        print(f"[AUTO-LOAD] ✅ Carga completada: {locations_added} ubicaciones")
        print(f"[AUTO-LOAD]   - Departamentos: {len(departamentos)}")
        print(f"[AUTO-LOAD]   - Municipios: {len(municipios)}")
        print(f"[AUTO-LOAD]   - Zonas: {len(zonas)}")
        print(f"[AUTO-LOAD]   - Puestos: {len(puestos)}")
        
        return True
        
    except Exception as e:
        import traceback
        print(f"[AUTO-LOAD] ❌ Error: {str(e)}")
        print(f"[AUTO-LOAD] Traceback: {traceback.format_exc()}")
        db.session.rollback()
        return False


def _auto_create_users():
    """
    Crear usuarios automáticamente si no existen
    """
    from backend.models.user import User
    
    try:
        # Verificar si ya hay usuarios
        total_users = User.query.count()
        if total_users > 0:
            print(f"[AUTO-USERS] Ya existen {total_users} usuarios, omitiendo creación")
            return True
        
        print("[AUTO-USERS] No hay usuarios, creando usuarios básicos...")
        
        # Obtener ubicaciones necesarias
        caqueta = Location.query.filter_by(
            tipo='departamento',
            departamento_codigo='44'
        ).first()
        
        florencia = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo='44',
            municipio_codigo='4401'
        ).first()
        
        if not caqueta or not florencia:
            print("[AUTO-USERS] ERROR: No se encontraron ubicaciones necesarias")
            return False
        
        # Crear usuarios básicos
        usuarios = [
            # Super Admin - Contraseña fija admin123
            {
                'nombre': 'admin',
                'rol': 'super_admin',
                'ubicacion_id': None,
                'password': 'admin123'  # Contraseña fija para Super Admin
            },
            # Admin Departamental - Contraseña test123 (modificable)
            {
                'nombre': 'admin_caqueta',
                'rol': 'admin_departamental',
                'ubicacion_id': caqueta.id,
                'password': 'test123'
            },
            # Admin Municipal - Contraseña test123 (modificable)
            {
                'nombre': 'admin_florencia',
                'rol': 'admin_municipal',
                'ubicacion_id': florencia.id,
                'password': 'test123'
            }
        ]
        
        for user_data in usuarios:
            user = User(
                nombre=user_data['nombre'],
                rol=user_data['rol'],
                ubicacion_id=user_data['ubicacion_id'],
                activo=True
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            print(f"[AUTO-USERS] Creado: {user_data['nombre']} ({user_data['rol']})")
        
        db.session.commit()
        print(f"[AUTO-USERS] ✅ {len(usuarios)} usuarios creados")
        return True
        
    except Exception as e:
        import traceback
        print(f"[AUTO-USERS] ❌ Error: {str(e)}")
        print(f"[AUTO-USERS] Traceback: {traceback.format_exc()}")
        db.session.rollback()
        return False


def _auto_load_partidos_candidatos():
    """
    Cargar partidos y candidatos automáticamente si no existen
    """
    from backend.models.configuracion_electoral import Partido, TipoEleccion, Candidato
    
    try:
        # Verificar si ya hay partidos
        total_partidos = Partido.query.count()
        if total_partidos > 0:
            print(f"[AUTO-PARTIDOS] Ya existen {total_partidos} partidos, omitiendo carga")
            return True
        
        print("[AUTO-PARTIDOS] No hay partidos, cargando datos electorales...")
        
        # Crear tipos de elección
        tipos_eleccion = [
            {'codigo': 'SENADO', 'nombre': 'Senado de la República', 'descripcion': 'Elección para Senadores', 'activo': True},
            {'codigo': 'CAMARA', 'nombre': 'Cámara de Representantes', 'descripcion': 'Elección para Representantes', 'activo': True}
        ]
        
        tipos_creados = {}
        for tipo_data in tipos_eleccion:
            tipo = TipoEleccion(**tipo_data)
            db.session.add(tipo)
            db.session.flush()
            tipos_creados[tipo_data['codigo']] = tipo
            print(f"[AUTO-PARTIDOS] Tipo: {tipo_data['nombre']}")
        
        # Crear partidos
        partidos_data = [
            {'codigo': 'LIBERAL', 'nombre': 'Partido Liberal Colombiano', 'sigla': 'PLC', 'color': '#FF0000', 'activo': True},
            {'codigo': 'CONSERVADOR', 'nombre': 'Partido Conservador Colombiano', 'sigla': 'PCC', 'color': '#0000FF', 'activo': True},
            {'codigo': 'PACTO', 'nombre': 'Pacto Histórico', 'sigla': 'PH', 'color': '#FF1493', 'activo': True},
            {'codigo': 'CENTRO_DEM', 'nombre': 'Centro Democrático', 'sigla': 'CD', 'color': '#00BFFF', 'activo': True},
            {'codigo': 'CAMBIO_RAD', 'nombre': 'Cambio Radical', 'sigla': 'CR', 'color': '#FFD700', 'activo': True},
            {'codigo': 'VERDE', 'nombre': 'Alianza Verde', 'sigla': 'AV', 'color': '#00FF00', 'activo': True},
            {'codigo': 'VOTO_BLANCO', 'nombre': 'Voto en Blanco', 'sigla': 'BLANCO', 'color': '#FFFFFF', 'activo': True}
        ]
        
        partidos_creados = {}
        for partido_data in partidos_data:
            partido = Partido(**partido_data)
            db.session.add(partido)
            db.session.flush()
            partidos_creados[partido_data['codigo']] = partido
            print(f"[AUTO-PARTIDOS] Partido: {partido_data['sigla']}")
        
        # Crear algunos candidatos de ejemplo
        candidatos_data = [
            # Senado
            {'nombre': 'Gustavo Bolívar', 'partido': 'PACTO', 'tipo': 'SENADO', 'numero_lista': 1},
            {'nombre': 'Paloma Valencia', 'partido': 'CENTRO_DEM', 'tipo': 'SENADO', 'numero_lista': 1},
            {'nombre': 'Angélica Lozano', 'partido': 'VERDE', 'tipo': 'SENADO', 'numero_lista': 1},
            # Cámara Caquetá
            {'nombre': 'Hernán Banguero', 'partido': 'LIBERAL', 'tipo': 'CAMARA', 'numero_lista': 1, 'depto': '44'},
            {'nombre': 'Carlos Ramírez', 'partido': 'CONSERVADOR', 'tipo': 'CAMARA', 'numero_lista': 1, 'depto': '44'},
            {'nombre': 'Ana María Torres', 'partido': 'PACTO', 'tipo': 'CAMARA', 'numero_lista': 1, 'depto': '44'}
        ]
        
        for cand_data in candidatos_data:
            candidato = Candidato(
                nombre=cand_data['nombre'],
                partido_id=partidos_creados[cand_data['partido']].id,
                tipo_eleccion_id=tipos_creados[cand_data['tipo']].id,
                numero_lista=cand_data['numero_lista'],
                departamento_codigo=cand_data.get('depto'),
                activo=True
            )
            db.session.add(candidato)
        
        db.session.commit()
        print(f"[AUTO-PARTIDOS] ✅ {len(partidos_creados)} partidos y {len(candidatos_data)} candidatos creados")
        return True
        
    except Exception as e:
        import traceback
        print(f"[AUTO-PARTIDOS] ❌ Error: {str(e)}")
        print(f"[AUTO-PARTIDOS] Traceback: {traceback.format_exc()}")
        db.session.rollback()
        return False


@locations_bp.route('/departamentos', methods=['GET'])
def get_departamentos():
    """
    Obtener departamento de Caquetá únicamente
    Endpoint público (necesario para login)
    
    Returns:
        JSON con lista de departamentos (solo Caquetá)
    """
    try:
        # Verificar si hay datos, si no, cargar automáticamente
        total_locations = Location.query.count()
        if total_locations == 0:
            print("[DEPARTAMENTOS] BD vacía, intentando carga automática...")
            _auto_load_divipola()
            # Crear usuarios después de cargar ubicaciones
            _auto_create_users()
            # Cargar partidos y candidatos
            _auto_load_partidos_candidatos()
        
        # Buscar departamento de Caquetá
        departamentos = Location.query.filter_by(
            tipo='departamento',
            departamento_codigo=CAQUETA_CODE,
            activo=True
        ).all()
        
        if departamentos:
            data = [{
                'departamento_codigo': dept.departamento_codigo,
                'departamento_nombre': dept.departamento_nombre
            } for dept in departamentos]
            
            return jsonify({
                'success': True,
                'data': data
            }), 200
        else:
            # Si aún no hay datos después de intentar cargar
            total_deptos = Location.query.filter_by(tipo='departamento').count()
            
            return jsonify({
                'success': False,
                'error': 'No se encontró el departamento de Caquetá. La base de datos puede estar vacía o el archivo divipola.csv no está disponible.',
                'data': [],
                'debug': {
                    'total_departamentos': total_deptos,
                    'total_locations': Location.query.count(),
                    'buscando_codigo': CAQUETA_CODE
                }
            }), 404
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[ERROR] Error en get_departamentos: {str(e)}")
        print(f"[ERROR] Traceback: {error_trace}")
        return jsonify({
            'success': False,
            'error': f'Error al obtener departamentos: {str(e)}'
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
