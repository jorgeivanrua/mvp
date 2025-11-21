"""
Rutas del Super Admin
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.utils.decorators import role_required

super_admin_bp = Blueprint('super_admin', __name__, url_prefix='/api/super-admin')


@super_admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_stats():
    """
    Obtener estadísticas globales del sistema
    """
    try:
        from backend.database import db
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.location import Location
        
        # Contar usuarios activos
        total_usuarios = User.query.filter_by(activo=True).count()
        
        # Contar puestos y mesas
        total_puestos = Location.query.filter_by(tipo='puesto').count()
        total_mesas = Location.query.filter_by(tipo='mesa').count()
        
        # Contar formularios
        total_formularios = FormularioE14.query.count()
        formularios_pendientes = FormularioE14.query.filter_by(estado='pendiente').count()
        formularios_validados = FormularioE14.query.filter_by(estado='validado').count()
        
        # Calcular porcentaje
        porcentaje_validados = (formularios_validados / total_formularios * 100) if total_formularios > 0 else 0
        
        return jsonify({
            'success': True,
            'data': {
                'totalUsuarios': total_usuarios,
                'usuariosChange': 0,  # TODO: Calcular cambio del día
                'totalPuestos': total_puestos,
                'totalMesas': total_mesas,
                'totalFormularios': total_formularios,
                'formulariosPendientes': formularios_pendientes,
                'totalValidados': formularios_validados,
                'porcentajeValidados': round(porcentaje_validados, 2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_all_users():
    """
    Obtener todos los usuarios del sistema
    """
    try:
        users = User.query.all()
        
        users_data = []
        for user in users:
            user_dict = {
                'id': user.id,
                'nombre': user.nombre,
                'rol': user.rol,
                'activo': user.activo,
                'ubicacion_id': user.ubicacion_id,
                'ubicacion_nombre': None,
                'ultimo_acceso': user.last_login.isoformat() if user.last_login else None,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
            
            # Obtener nombre de ubicación
            if user.ubicacion_id:
                ubicacion = Location.query.get(user.ubicacion_id)
                if ubicacion:
                    user_dict['ubicacion_nombre'] = ubicacion.nombre_completo
            
            users_data.append(user_dict)
        
        return jsonify({
            'success': True,
            'data': users_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/users', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def create_user():
    """
    Crear un nuevo usuario
    """
    try:
        from backend.database import db
        
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['nombre', 'password', 'rol']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido: {field}'
                }), 400
        
        # Verificar que el nombre no exista
        existing_user = User.query.filter_by(nombre=data['nombre']).first()
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'Ya existe un usuario con ese nombre'
            }), 400
        
        # Crear usuario
        user = User(
            nombre=data['nombre'],
            rol=data['rol'],
            ubicacion_id=data.get('ubicacion_id'),
            activo=data.get('activo', True)
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario creado exitosamente',
            'data': user.to_dict()
        }), 201
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def update_user(user_id):
    """
    Actualizar un usuario
    """
    try:
        from backend.database import db
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos permitidos
        if 'nombre' in data:
            user.nombre = data['nombre']
        if 'rol' in data:
            user.rol = data['rol']
        if 'ubicacion_id' in data:
            user.ubicacion_id = data['ubicacion_id']
        if 'activo' in data:
            user.activo = data['activo']
        if 'password' in data:
            user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario actualizado exitosamente',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/users/<int:user_id>/reset-password', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def reset_user_password(user_id):
    """
    Resetear contraseña de un usuario
    """
    try:
        from backend.database import db
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        data = request.get_json()
        new_password = data.get('password')
        
        if not new_password:
            return jsonify({
                'success': False,
                'error': 'Se requiere una nueva contraseña'
            }), 400
        
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Contraseña reseteada exitosamente'
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/system-health', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_system_health():
    """
    Obtener estado de salud del sistema
    """
    try:
        from backend.database import db
        import psutil
        import time
        
        # Verificar conexión a BD
        try:
            db.session.execute('SELECT 1')
            db_status = 'healthy'
        except:
            db_status = 'unhealthy'
        
        # Métricas del sistema
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        return jsonify({
            'success': True,
            'data': {
                'status': 'healthy' if db_status == 'healthy' and cpu_percent < 80 else 'warning',
                'database': db_status,
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_mb': memory.available / (1024 * 1024),
                'timestamp': time.time()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@super_admin_bp.route('/upload/users', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def upload_users():
    """
    Cargar usuarios masivamente desde archivo Excel
    
    Formato esperado del Excel:
    - nombre: Nombre del usuario
    - password: Contraseña
    - rol: Rol del usuario (testigo, coordinador_puesto, etc.)
    - ubicacion_codigo: Código de la ubicación (opcional)
    """
    try:
        from backend.database import db
        import pandas as pd
        from io import BytesIO
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nombre de archivo vacío'
            }), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({
                'success': False,
                'error': 'El archivo debe ser Excel (.xlsx o .xls)'
            }), 400
        
        # Leer Excel
        df = pd.read_excel(BytesIO(file.read()))
        
        # Validar columnas requeridas
        required_columns = ['nombre', 'password', 'rol']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'success': False,
                'error': f'Faltan columnas requeridas: {", ".join(missing_columns)}'
            }), 400
        
        # Procesar usuarios
        created_users = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Verificar si el usuario ya existe
                existing_user = User.query.filter_by(nombre=row['nombre']).first()
                if existing_user:
                    errors.append(f"Fila {index + 2}: Usuario '{row['nombre']}' ya existe")
                    continue
                
                # Buscar ubicación si se proporciona código
                ubicacion_id = None
                if 'ubicacion_codigo' in row and pd.notna(row['ubicacion_codigo']):
                    from backend.models.location import Location
                    ubicacion = Location.query.filter_by(codigo=str(row['ubicacion_codigo'])).first()
                    if ubicacion:
                        ubicacion_id = ubicacion.id
                    else:
                        errors.append(f"Fila {index + 2}: Ubicación con código '{row['ubicacion_codigo']}' no encontrada")
                
                # Crear usuario
                user = User(
                    nombre=row['nombre'],
                    rol=row['rol'],
                    ubicacion_id=ubicacion_id,
                    activo=True
                )
                user.set_password(row['password'])
                
                db.session.add(user)
                created_users.append(row['nombre'])
                
            except Exception as e:
                errors.append(f"Fila {index + 2}: {str(e)}")
        
        # Commit si hay usuarios creados
        if created_users:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(created_users)} usuarios creados exitosamente',
            'data': {
                'created': created_users,
                'errors': errors,
                'total_processed': len(df),
                'total_created': len(created_users),
                'total_errors': len(errors)
            }
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error procesando archivo: {str(e)}'
        }), 500


@super_admin_bp.route('/upload/locations', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def upload_locations():
    """
    Cargar DIVIPOLA (ubicaciones) masivamente desde archivo Excel
    
    Formato esperado del Excel:
    - codigo: Código de la ubicación
    - nombre: Nombre de la ubicación
    - tipo: Tipo (departamento, municipio, puesto, mesa)
    - departamento_codigo: Código del departamento padre (opcional)
    - municipio_codigo: Código del municipio padre (opcional)
    - puesto_codigo: Código del puesto padre (opcional)
    """
    try:
        from backend.database import db
        from backend.models.location import Location
        import pandas as pd
        from io import BytesIO
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nombre de archivo vacío'
            }), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({
                'success': False,
                'error': 'El archivo debe ser Excel (.xlsx o .xls)'
            }), 400
        
        # Leer Excel
        df = pd.read_excel(BytesIO(file.read()))
        
        # Validar columnas requeridas
        required_columns = ['codigo', 'nombre', 'tipo']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'success': False,
                'error': f'Faltan columnas requeridas: {", ".join(missing_columns)}'
            }), 400
        
        # Procesar ubicaciones
        created_locations = []
        errors = []
        
        # Ordenar por tipo para crear jerarquía correctamente
        tipo_order = {'departamento': 0, 'municipio': 1, 'puesto': 2, 'mesa': 3}
        df['tipo_order'] = df['tipo'].map(tipo_order)
        df = df.sort_values('tipo_order')
        
        for index, row in df.iterrows():
            try:
                # Verificar si la ubicación ya existe
                existing_location = Location.query.filter_by(codigo=str(row['codigo'])).first()
                if existing_location:
                    errors.append(f"Fila {index + 2}: Ubicación con código '{row['codigo']}' ya existe")
                    continue
                
                # Buscar padre según tipo
                departamento_id = None
                municipio_id = None
                puesto_id = None
                
                if row['tipo'] == 'municipio' and 'departamento_codigo' in row and pd.notna(row['departamento_codigo']):
                    padre = Location.query.filter_by(codigo=str(row['departamento_codigo'])).first()
                    if padre:
                        departamento_id = padre.id
                
                if row['tipo'] == 'puesto' and 'municipio_codigo' in row and pd.notna(row['municipio_codigo']):
                    padre = Location.query.filter_by(codigo=str(row['municipio_codigo'])).first()
                    if padre:
                        municipio_id = padre.id
                        departamento_id = padre.departamento_id
                
                if row['tipo'] == 'mesa' and 'puesto_codigo' in row and pd.notna(row['puesto_codigo']):
                    padre = Location.query.filter_by(codigo=str(row['puesto_codigo'])).first()
                    if padre:
                        puesto_id = padre.id
                        municipio_id = padre.municipio_id
                        departamento_id = padre.departamento_id
                
                # Crear ubicación
                location = Location(
                    codigo=str(row['codigo']),
                    nombre=row['nombre'],
                    tipo=row['tipo'],
                    departamento_id=departamento_id,
                    municipio_id=municipio_id,
                    puesto_id=puesto_id
                )
                
                db.session.add(location)
                created_locations.append(row['nombre'])
                
            except Exception as e:
                errors.append(f"Fila {index + 2}: {str(e)}")
        
        # Commit si hay ubicaciones creadas
        if created_locations:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(created_locations)} ubicaciones creadas exitosamente',
            'data': {
                'created': created_locations,
                'errors': errors,
                'total_processed': len(df),
                'total_created': len(created_locations),
                'total_errors': len(errors)
            }
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error procesando archivo: {str(e)}'
        }), 500


@super_admin_bp.route('/upload/partidos', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def upload_partidos():
    """
    Cargar partidos políticos masivamente desde archivo Excel
    
    Formato esperado del Excel:
    - codigo: Código del partido (opcional, se genera automático)
    - nombre: Nombre del partido
    - nombre_corto: Nombre corto del partido
    - color: Color en formato hexadecimal (ej: #FF0000)
    - logo_url: URL del logo (opcional)
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import Partido
        import pandas as pd
        from io import BytesIO
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nombre de archivo vacío'
            }), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({
                'success': False,
                'error': 'El archivo debe ser Excel (.xlsx o .xls)'
            }), 400
        
        # Leer Excel
        df = pd.read_excel(BytesIO(file.read()))
        
        # Validar columnas requeridas
        required_columns = ['nombre', 'nombre_corto', 'color']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'success': False,
                'error': f'Faltan columnas requeridas: {", ".join(missing_columns)}'
            }), 400
        
        # Procesar partidos
        created_partidos = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Verificar si el partido ya existe
                existing_partido = Partido.query.filter_by(nombre=row['nombre']).first()
                if existing_partido:
                    errors.append(f"Fila {index + 2}: Partido '{row['nombre']}' ya existe")
                    continue
                
                # Generar código si no existe
                codigo = row.get('codigo') if 'codigo' in row and pd.notna(row.get('codigo')) else row['nombre'].upper().replace(' ', '_')
                
                # Crear partido
                partido = Partido(
                    codigo=codigo,
                    nombre=row['nombre'],
                    nombre_corto=row['nombre_corto'],
                    color=row['color'],
                    logo_url=row.get('logo_url') if 'logo_url' in row and pd.notna(row.get('logo_url')) else None,
                    activo=row.get('activo', True) if 'activo' in row else True
                )
                
                db.session.add(partido)
                created_partidos.append(row['nombre'])
                
            except Exception as e:
                errors.append(f"Fila {index + 2}: {str(e)}")
        
        # Commit si hay partidos creados
        if created_partidos:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(created_partidos)} partidos creados exitosamente',
            'data': {
                'created': created_partidos,
                'errors': errors,
                'total_processed': len(df),
                'total_created': len(created_partidos),
                'total_errors': len(errors)
            }
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error procesando archivo: {str(e)}'
        }), 500


@super_admin_bp.route('/upload/candidatos', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def upload_candidatos():
    """
    Cargar candidatos masivamente desde archivo Excel
    
    Formato esperado del Excel:
    - codigo: Código del candidato (opcional, se genera automático)
    - nombre_completo: Nombre completo del candidato
    - partido_nombre: Nombre del partido
    - tipo_eleccion_nombre: Nombre del tipo de elección
    - numero_lista: Número de lista (opcional)
    - es_independiente: True/False (opcional, default False)
    - es_cabeza_lista: True/False (opcional, default False)
    - foto_url: URL de la foto (opcional)
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import Candidato, Partido, TipoEleccion
        import pandas as pd
        from io import BytesIO
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nombre de archivo vacío'
            }), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({
                'success': False,
                'error': 'El archivo debe ser Excel (.xlsx o .xls)'
            }), 400
        
        # Leer Excel
        df = pd.read_excel(BytesIO(file.read()))
        
        # Validar columnas requeridas
        required_columns = ['nombre_completo', 'partido_nombre', 'tipo_eleccion_nombre']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'success': False,
                'error': f'Faltan columnas requeridas: {", ".join(missing_columns)}'
            }), 400
        
        # Procesar candidatos
        created_candidatos = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Buscar partido
                partido = Partido.query.filter_by(nombre=row['partido_nombre']).first()
                if not partido:
                    errors.append(f"Fila {index + 2}: Partido '{row['partido_nombre']}' no encontrado")
                    continue
                
                # Buscar tipo de elección
                tipo_eleccion = TipoEleccion.query.filter_by(nombre=row['tipo_eleccion_nombre']).first()
                if not tipo_eleccion:
                    errors.append(f"Fila {index + 2}: Tipo de elección '{row['tipo_eleccion_nombre']}' no encontrado")
                    continue
                
                # Generar código si no existe
                if 'codigo' in row and pd.notna(row.get('codigo')):
                    codigo = row['codigo']
                else:
                    codigo = f"{tipo_eleccion.codigo}_{partido.codigo}_{index+1}"
                
                # Verificar si el candidato ya existe
                existing_candidato = Candidato.query.filter_by(codigo=codigo).first()
                
                if existing_candidato:
                    errors.append(f"Fila {index + 2}: Candidato con código '{codigo}' ya existe")
                    continue
                
                # Crear candidato
                candidato = Candidato(
                    codigo=codigo,
                    nombre_completo=row['nombre_completo'],
                    partido_id=partido.id,
                    tipo_eleccion_id=tipo_eleccion.id,
                    numero_lista=row.get('numero_lista') if 'numero_lista' in row and pd.notna(row.get('numero_lista')) else None,
                    es_independiente=row.get('es_independiente', False) if 'es_independiente' in row else False,
                    es_cabeza_lista=row.get('es_cabeza_lista', False) if 'es_cabeza_lista' in row else False,
                    foto_url=row.get('foto_url') if 'foto_url' in row and pd.notna(row.get('foto_url')) else None,
                    activo=row.get('activo', True) if 'activo' in row else True
                )
                
                db.session.add(candidato)
                created_candidatos.append(row['nombre_completo'])
                
            except Exception as e:
                errors.append(f"Fila {index + 2}: {str(e)}")
        
        # Commit si hay candidatos creados
        if created_candidatos:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(created_candidatos)} candidatos creados exitosamente',
            'data': {
                'created': created_candidatos,
                'errors': errors,
                'total_processed': len(df),
                'total_created': len(created_candidatos),
                'total_errors': len(errors)
            }
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error procesando archivo: {str(e)}'
        }), 500



@super_admin_bp.route('/tipos-eleccion', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_tipos_eleccion():
    """
    Obtener todos los tipos de elección
    """
    try:
        from backend.models.configuracion_electoral import TipoEleccion
        
        tipos = TipoEleccion.query.all()
        
        return jsonify({
            'success': True,
            'data': [tipo.to_dict() for tipo in tipos]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/tipos-eleccion', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def create_tipo_eleccion():
    """
    Crear un nuevo tipo de elección
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import TipoEleccion
        
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        # Verificar que no exista
        existing = TipoEleccion.query.filter_by(nombre=data['nombre']).first()
        if existing:
            return jsonify({
                'success': False,
                'error': 'Ya existe un tipo de elección con ese nombre'
            }), 400
        
        # Generar código automático
        codigo = data.get('codigo', data['nombre'].upper().replace(' ', '_'))
        
        tipo = TipoEleccion(
            codigo=codigo,
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            es_uninominal=data.get('es_uninominal', False),
            permite_lista_cerrada=data.get('permite_lista_cerrada', not data.get('es_uninominal', False)),
            permite_lista_abierta=data.get('permite_lista_abierta', False),
            permite_coaliciones=data.get('permite_coaliciones', False),
            activo=data.get('activo', True)
        )
        
        db.session.add(tipo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tipo de elección creado exitosamente',
            'data': tipo.to_dict()
        }), 201
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/tipos-eleccion/<int:tipo_id>', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def update_tipo_eleccion(tipo_id):
    """
    Actualizar un tipo de elección (habilitar/deshabilitar)
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import TipoEleccion
        
        tipo = TipoEleccion.query.get(tipo_id)
        if not tipo:
            return jsonify({
                'success': False,
                'error': 'Tipo de elección no encontrado'
            }), 404
        
        data = request.get_json()
        
        if 'nombre' in data:
            tipo.nombre = data['nombre']
        if 'descripcion' in data:
            tipo.descripcion = data['descripcion']
        if 'es_uninominal' in data:
            tipo.es_uninominal = data['es_uninominal']
        if 'permite_lista_cerrada' in data:
            tipo.permite_lista_cerrada = data['permite_lista_cerrada']
        if 'permite_lista_abierta' in data:
            tipo.permite_lista_abierta = data['permite_lista_abierta']
        if 'permite_coaliciones' in data:
            tipo.permite_coaliciones = data['permite_coaliciones']
        if 'activo' in data:
            tipo.activo = data['activo']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tipo de elección actualizado exitosamente',
            'data': tipo.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/partidos/<int:partido_id>/toggle', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def toggle_partido(partido_id):
    """
    Habilitar/deshabilitar un partido para recolección de datos
    """
    try:
        from backend.database import db
        from backend.models.partido import Partido
        
        partido = Partido.query.get(partido_id)
        if not partido:
            return jsonify({
                'success': False,
                'error': 'Partido no encontrado'
            }), 404
        
        data = request.get_json()
        partido.activo = data.get('activo', not partido.activo)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Partido {"habilitado" if partido.activo else "deshabilitado"} exitosamente',
            'data': partido.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/candidatos/<int:candidato_id>/toggle', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def toggle_candidato(candidato_id):
    """
    Habilitar/deshabilitar un candidato para recolección de datos
    """
    try:
        from backend.database import db
        from backend.models.candidato import Candidato
        
        candidato = Candidato.query.get(candidato_id)
        if not candidato:
            return jsonify({
                'success': False,
                'error': 'Candidato no encontrado'
            }), 404
        
        data = request.get_json()
        candidato.activo = data.get('activo', not candidato.activo)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Candidato {"habilitado" if candidato.activo else "deshabilitado"} exitosamente',
            'data': candidato.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/download/template/<template_type>', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def download_template(template_type):
    """
    Descargar plantilla Excel con datos de ejemplo
    
    Tipos: users, locations, partidos, candidatos, tipos_eleccion
    """
    try:
        import pandas as pd
        from io import BytesIO
        from flask import send_file
        
        templates = {
            'users': {
                'data': {
                    'nombre': ['Juan Perez', 'Maria Garcia', 'Carlos Lopez', 'Ana Martinez', 'Pedro Rodriguez'],
                    'password': ['password123', 'password456', 'password789', 'password101', 'password202'],
                    'rol': ['testigo', 'coordinador_puesto', 'coordinador_municipal', 'coordinador_departamental', 'auditor'],
                    'ubicacion_codigo': ['001001001001', '001001001', '001001', '001', '']
                },
                'filename': 'plantilla_usuarios.xlsx'
            },
            'locations': {
                'data': {
                    'codigo': ['001', '001001', '001001001', '001001001001', '001001001002'],
                    'nombre': ['Departamento Ejemplo', 'Municipio Ejemplo', 'Puesto Electoral 1', 'Mesa 1', 'Mesa 2'],
                    'tipo': ['departamento', 'municipio', 'puesto', 'mesa', 'mesa'],
                    'departamento_codigo': ['', '001', '001', '001', '001'],
                    'municipio_codigo': ['', '', '001001', '001001', '001001'],
                    'puesto_codigo': ['', '', '', '001001001', '001001001']
                },
                'filename': 'plantilla_divipola.xlsx'
            },
            'partidos': {
                'data': {
                    'nombre': ['Partido Liberal', 'Partido Conservador', 'Partido Verde', 'Partido de la U', 'Polo Democrático'],
                    'sigla': ['PL', 'PC', 'PV', 'PU', 'PD'],
                    'color': ['#FF0000', '#0000FF', '#00FF00', '#FFFF00', '#FF00FF'],
                    'numero_lista': [1, 2, 3, 4, 5]
                },
                'filename': 'plantilla_partidos.xlsx'
            },
            'candidatos': {
                'data': {
                    'nombre': ['Juan Perez', 'Maria Garcia', 'Carlos Lopez', 'Ana Martinez', 'Pedro Rodriguez'],
                    'partido_nombre': ['Partido Liberal', 'Partido Conservador', 'Partido Verde', 'Partido de la U', 'Polo Democrático'],
                    'tipo_eleccion_nombre': ['Presidente', 'Senado', 'Cámara', 'Gobernador', 'Alcalde'],
                    'numero_lista': [1, 2, 3, 4, 5]
                },
                'filename': 'plantilla_candidatos.xlsx'
            },
            'tipos_eleccion': {
                'data': {
                    'nombre': ['Presidente', 'Senado', 'Cámara', 'Gobernador', 'Alcalde', 'Concejo', 'JAL'],
                    'es_uninominal': [True, False, False, True, True, False, False]
                },
                'filename': 'plantilla_tipos_eleccion.xlsx'
            }
        }
        
        if template_type not in templates:
            return jsonify({
                'success': False,
                'error': 'Tipo de plantilla no válido'
            }), 400
        
        template = templates[template_type]
        df = pd.DataFrame(template['data'])
        
        # Crear archivo Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Datos')
            
            # Ajustar ancho de columnas
            worksheet = writer.sheets['Datos']
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = max_length
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=template['filename']
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



# ============================================
# GESTIÓN DE CAMPAÑAS
# ============================================

@super_admin_bp.route('/campanas', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_campanas():
    """
    Obtener todas las campañas
    """
    try:
        from backend.models.configuracion_electoral import Campana
        
        campanas = Campana.query.order_by(Campana.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [campana.to_dict() for campana in campanas]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/campanas', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def create_campana():
    """
    Crear una nueva campaña
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import Campana
        
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not data or 'nombre' not in data:
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        # Generar código automático
        codigo = data.get('codigo', data['nombre'].upper().replace(' ', '_'))
        
        # Verificar que no exista
        existing = Campana.query.filter_by(codigo=codigo).first()
        if existing:
            return jsonify({
                'success': False,
                'error': 'Ya existe una campaña con ese código'
            }), 400
        
        campana = Campana(
            codigo=codigo,
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            fecha_inicio=data.get('fecha_inicio'),
            fecha_fin=data.get('fecha_fin'),
            color_primario=data.get('color_primario', '#1e3c72'),
            color_secundario=data.get('color_secundario', '#2a5298'),
            logo_url=data.get('logo_url'),
            es_candidato_unico=data.get('es_candidato_unico', False),
            es_partido_completo=data.get('es_partido_completo', False),
            activa=False,  # No activar automáticamente
            created_by=int(user_id)
        )
        
        db.session.add(campana)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Campaña creada exitosamente',
            'data': campana.to_dict()
        }), 201
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/campanas/<int:campana_id>/activar', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def activar_campana(campana_id):
    """
    Activar una campaña (desactiva las demás)
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import Campana
        
        campana = Campana.query.get(campana_id)
        if not campana:
            return jsonify({
                'success': False,
                'error': 'Campaña no encontrada'
            }), 404
        
        # Desactivar todas las campañas
        Campana.query.update({'activa': False})
        
        # Activar la seleccionada
        campana.activa = True
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Campaña "{campana.nombre}" activada exitosamente',
            'data': campana.to_dict()
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/campanas/<int:campana_id>/reset', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def reset_campana(campana_id):
    """
    Resetear datos de una campaña (eliminar formularios, incidentes, delitos)
    PELIGROSO: Requiere confirmación
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import Campana
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import Incidente, Delito
        
        data = request.get_json()
        confirmacion = data.get('confirmacion', '')
        
        if confirmacion != 'CONFIRMAR_RESET':
            return jsonify({
                'success': False,
                'error': 'Se requiere confirmación explícita'
            }), 400
        
        campana = Campana.query.get(campana_id)
        if not campana:
            return jsonify({
                'success': False,
                'error': 'Campaña no encontrada'
            }), 404
        
        # Contar registros antes de eliminar
        formularios_count = FormularioE14.query.filter_by(campana_id=campana_id).count()
        incidentes_count = Incidente.query.filter_by(campana_id=campana_id).count()
        delitos_count = Delito.query.filter_by(campana_id=campana_id).count()
        
        # Eliminar datos de la campaña
        FormularioE14.query.filter_by(campana_id=campana_id).delete()
        Incidente.query.filter_by(campana_id=campana_id).delete()
        Delito.query.filter_by(campana_id=campana_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Campaña "{campana.nombre}" reseteada exitosamente',
            'data': {
                'formularios_eliminados': formularios_count,
                'incidentes_eliminados': incidentes_count,
                'delitos_eliminados': delitos_count
            }
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/campanas/<int:campana_id>', methods=['DELETE'])
@jwt_required()
@role_required(['super_admin'])
def delete_campana(campana_id):
    """
    Eliminar una campaña completa (incluyendo todos sus datos)
    PELIGROSO: Requiere confirmación
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import Campana
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import Incidente, Delito
        
        data = request.get_json()
        confirmacion = data.get('confirmacion', '')
        
        if confirmacion != 'CONFIRMAR_ELIMINACION':
            return jsonify({
                'success': False,
                'error': 'Se requiere confirmación explícita'
            }), 400
        
        campana = Campana.query.get(campana_id)
        if not campana:
            return jsonify({
                'success': False,
                'error': 'Campaña no encontrada'
            }), 404
        
        if campana.activa:
            return jsonify({
                'success': False,
                'error': 'No se puede eliminar la campaña activa'
            }), 400
        
        # Eliminar todos los datos asociados
        FormularioE14.query.filter_by(campana_id=campana_id).delete()
        Incidente.query.filter_by(campana_id=campana_id).delete()
        Delito.query.filter_by(campana_id=campana_id).delete()
        
        # Eliminar la campaña
        db.session.delete(campana)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Campaña "{campana.nombre}" eliminada exitosamente'
        }), 200
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================
# GESTIÓN DE TEMAS
# ============================================

@super_admin_bp.route('/temas', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_temas():
    """
    Obtener todos los temas configurados
    """
    try:
        from backend.models.configuracion_electoral import ConfiguracionTema
        
        temas = ConfiguracionTema.query.filter_by(activo=True).all()
        
        return jsonify({
            'success': True,
            'data': [tema.to_dict() for tema in temas]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/temas', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def create_tema():
    """
    Crear una nueva configuración de tema
    """
    try:
        from backend.database import db
        from backend.models.configuracion_electoral import ConfiguracionTema
        
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({
                'success': False,
                'error': 'El nombre es requerido'
            }), 400
        
        tema = ConfiguracionTema(
            nombre=data['nombre'],
            aplica_a_rol=data.get('aplica_a_rol'),
            aplica_a_tipo_eleccion_id=data.get('aplica_a_tipo_eleccion_id'),
            campana_id=data.get('campana_id'),
            color_primario=data.get('color_primario', '#1e3c72'),
            color_secundario=data.get('color_secundario', '#2a5298'),
            color_acento=data.get('color_acento', '#28a745'),
            color_fondo=data.get('color_fondo', '#f8f9fa'),
            color_texto=data.get('color_texto', '#212529'),
            logo_url=data.get('logo_url'),
            favicon_url=data.get('favicon_url'),
            activo=True
        )
        
        db.session.add(tema)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tema creado exitosamente',
            'data': tema.to_dict()
        }), 201
        
    except Exception as e:
        from backend.database import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



# ============================================
# TESTING Y AUDITORÍA
# ============================================

@super_admin_bp.route('/test/load-data', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def load_test_data_endpoint():
    """
    Cargar datos de prueba en el sistema
    """
    try:
        import subprocess
        import sys
        
        # Ejecutar script de carga de datos
        result = subprocess.run(
            [sys.executable, 'backend/scripts/load_test_data.py'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Datos de prueba cargados exitosamente',
                'output': result.stdout
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Error al cargar datos de prueba',
                'output': result.stderr
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/test/audit', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def system_audit():
    """
    Auditoría completa del sistema
    Verifica que todas las funcionalidades estén operativas
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        from backend.models.incidentes_delitos import Incidente, Delito
        
        audit_results = {
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'success',
            'checks': []
        }
        
        # Check 1: Base de datos
        try:
            db.session.execute('SELECT 1')
            audit_results['checks'].append({
                'name': 'Database Connection',
                'status': 'pass',
                'message': 'Conexión a base de datos OK'
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Database Connection',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Check 2: Usuarios
        try:
            total_users = User.query.count()
            users_by_role = db.session.query(
                User.rol, db.func.count(User.id)
            ).group_by(User.rol).all()
            
            audit_results['checks'].append({
                'name': 'Users',
                'status': 'pass',
                'message': f'Total: {total_users} usuarios',
                'details': {role: count for role, count in users_by_role}
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Users',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Check 3: Ubicaciones
        try:
            locations_by_type = db.session.query(
                Location.tipo, db.func.count(Location.id)
            ).group_by(Location.tipo).all()
            
            audit_results['checks'].append({
                'name': 'Locations',
                'status': 'pass',
                'message': 'Ubicaciones configuradas',
                'details': {tipo: count for tipo, count in locations_by_type}
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Locations',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Check 4: Configuración Electoral
        try:
            from backend.models.configuracion_electoral import TipoEleccion, Partido, Candidato
            
            tipos_count = TipoEleccion.query.filter_by(activo=True).count()
            partidos_count = Partido.query.filter_by(activo=True).count()
            candidatos_count = Candidato.query.filter_by(activo=True).count()
            
            audit_results['checks'].append({
                'name': 'Electoral Configuration',
                'status': 'pass',
                'message': 'Configuración electoral OK',
                'details': {
                    'tipos_eleccion': tipos_count,
                    'partidos': partidos_count,
                    'candidatos': candidatos_count
                }
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Electoral Configuration',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Check 5: Formularios
        try:
            formularios_count = FormularioE14.query.count()
            formularios_by_estado = db.session.query(
                FormularioE14.estado, db.func.count(FormularioE14.id)
            ).group_by(FormularioE14.estado).all()
            
            audit_results['checks'].append({
                'name': 'Formularios E-14',
                'status': 'pass',
                'message': f'Total: {formularios_count} formularios',
                'details': {estado: count for estado, count in formularios_by_estado}
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Formularios E-14',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Check 6: Incidentes y Delitos
        try:
            incidentes_count = Incidente.query.count()
            delitos_count = Delito.query.count()
            
            audit_results['checks'].append({
                'name': 'Incidents & Crimes',
                'status': 'pass',
                'message': 'Sistema de incidentes OK',
                'details': {
                    'incidentes': incidentes_count,
                    'delitos': delitos_count
                }
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Incidents & Crimes',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Check 7: Campañas
        try:
            from backend.models.configuracion_electoral import Campana
            
            campanas_count = Campana.query.count()
            campana_activa = Campana.query.filter_by(activa=True).first()
            
            audit_results['checks'].append({
                'name': 'Campaigns',
                'status': 'pass',
                'message': f'Total: {campanas_count} campañas',
                'details': {
                    'total': campanas_count,
                    'activa': campana_activa.nombre if campana_activa else 'Ninguna'
                }
            })
        except Exception as e:
            audit_results['checks'].append({
                'name': 'Campaigns',
                'status': 'fail',
                'message': f'Error: {str(e)}'
            })
        
        # Determinar estado general
        failed_checks = [c for c in audit_results['checks'] if c['status'] == 'fail']
        if failed_checks:
            audit_results['status'] = 'warning'
            audit_results['message'] = f'{len(failed_checks)} checks fallidos'
        else:
            audit_results['message'] = 'Todos los checks pasaron exitosamente'
        
        return jsonify({
            'success': True,
            'data': audit_results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/monitoreo-departamental', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_monitoreo_departamental():
    """
    Obtener datos de monitoreo por departamento para gráficos
    """
    try:
        from backend.models.formulario_e14 import FormularioE14
        
        # Obtener todos los departamentos
        departamentos = Location.query.filter_by(tipo='departamento', activo=True).all()
        
        monitoreo_data = []
        
        for depto in departamentos:
            # Obtener todas las mesas del departamento
            mesas = Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=depto.departamento_codigo,
                activo=True
            ).all()
            
            mesa_ids = [m.id for m in mesas]
            
            # Obtener formularios
            formularios = FormularioE14.query.filter(
                FormularioE14.mesa_id.in_(mesa_ids)
            ).all() if mesa_ids else []
            
            validados = sum(1 for f in formularios if f.estado == 'validado')
            pendientes = sum(1 for f in formularios if f.estado == 'pendiente')
            rechazados = sum(1 for f in formularios if f.estado == 'rechazado')
            
            porcentaje_avance = round((validados / len(mesas) * 100), 2) if mesas else 0
            
            monitoreo_data.append({
                'departamento': depto.departamento_nombre,
                'codigo': depto.departamento_codigo,
                'total_mesas': len(mesas),
                'total_formularios': len(formularios),
                'validados': validados,
                'pendientes': pendientes,
                'rechazados': rechazados,
                'sin_reporte': len(mesas) - len(formularios),
                'porcentaje_avance': porcentaje_avance
            })
        
        # Ordenar por porcentaje de avance descendente
        monitoreo_data.sort(key=lambda x: x['porcentaje_avance'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': monitoreo_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/audit-logs', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_audit_logs():
    """
    Obtener logs de auditoría del sistema
    """
    try:
        # Intentar obtener logs de la tabla AuditLog si existe
        try:
            from backend.models.coordinador_municipal import AuditLog
            
            limit = request.args.get('limit', 100, type=int)
            
            logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(limit).all()
            
            logs_data = []
            for log in logs:
                user = User.query.get(log.user_id)
                logs_data.append({
                    'id': log.id,
                    'user_id': log.user_id,
                    'user_nombre': user.nombre if user else 'Usuario eliminado',
                    'accion': log.accion,
                    'recurso': log.recurso,
                    'recurso_id': log.recurso_id,
                    'detalles': log.detalles,
                    'ip_address': log.ip_address,
                    'user_agent': log.user_agent,
                    'created_at': log.created_at.isoformat() if log.created_at else None
                })
            
            return jsonify({
                'success': True,
                'data': logs_data
            }), 200
            
        except ImportError:
            # Si no existe el modelo, devolver mensaje
            return jsonify({
                'success': True,
                'data': [],
                'message': 'Sistema de auditoría no configurado'
            }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@super_admin_bp.route('/incidentes-delitos', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_incidentes_delitos_admin():
    """
    Obtener todos los incidentes y delitos del sistema con información completa
    """
    try:
        from backend.models.incidentes_delitos import Incidente, Delito
        
        # Obtener incidentes
        incidentes = Incidente.query.order_by(Incidente.fecha_reporte.desc()).limit(50).all()
        
        incidentes_data = []
        for inc in incidentes:
            reportante = User.query.get(inc.reportado_por)
            mesa = Location.query.get(inc.mesa_id) if inc.mesa_id else None
            
            # Obtener ubicación completa
            ubicacion_completa = 'N/A'
            if mesa:
                puesto = Location.query.filter_by(
                    tipo='puesto',
                    departamento_codigo=mesa.departamento_codigo,
                    municipio_codigo=mesa.municipio_codigo,
                    zona_codigo=mesa.zona_codigo,
                    puesto_codigo=mesa.puesto_codigo
                ).first()
                
                municipio = Location.query.filter_by(
                    tipo='municipio',
                    departamento_codigo=mesa.departamento_codigo,
                    municipio_codigo=mesa.municipio_codigo
                ).first()
                
                departamento = Location.query.filter_by(
                    tipo='departamento',
                    departamento_codigo=mesa.departamento_codigo
                ).first()
                
                ubicacion_completa = f"{departamento.departamento_nombre if departamento else 'N/A'} > {municipio.municipio_nombre if municipio else 'N/A'} > {puesto.puesto_nombre if puesto else 'N/A'} > Mesa {mesa.mesa_codigo}"
            
            incidentes_data.append({
                'id': inc.id,
                'tipo': 'incidente',
                'titulo': inc.titulo,
                'descripcion': inc.descripcion,
                'tipo_incidente': inc.tipo_incidente,
                'severidad': inc.severidad,
                'estado': inc.estado,
                'reportado_por': reportante.nombre if reportante else 'Usuario eliminado',
                'reportado_por_rol': reportante.rol if reportante else 'N/A',
                'ubicacion': ubicacion_completa,
                'mesa_codigo': mesa.mesa_codigo if mesa else 'N/A',
                'fecha_reporte': inc.fecha_reporte.isoformat() if inc.fecha_reporte else None,
                'notas_resolucion': inc.notas_resolucion
            })
        
        # Obtener delitos
        delitos = Delito.query.order_by(Delito.fecha_reporte.desc()).limit(50).all()
        
        delitos_data = []
        for delito in delitos:
            reportante = User.query.get(delito.reportado_por)
            mesa = Location.query.get(delito.mesa_id) if delito.mesa_id else None
            
            # Obtener ubicación completa
            ubicacion_completa = 'N/A'
            if mesa:
                puesto = Location.query.filter_by(
                    tipo='puesto',
                    departamento_codigo=mesa.departamento_codigo,
                    municipio_codigo=mesa.municipio_codigo,
                    zona_codigo=mesa.zona_codigo,
                    puesto_codigo=mesa.puesto_codigo
                ).first()
                
                municipio = Location.query.filter_by(
                    tipo='municipio',
                    departamento_codigo=mesa.departamento_codigo,
                    municipio_codigo=mesa.municipio_codigo
                ).first()
                
                departamento = Location.query.filter_by(
                    tipo='departamento',
                    departamento_codigo=mesa.departamento_codigo
                ).first()
                
                ubicacion_completa = f"{departamento.departamento_nombre if departamento else 'N/A'} > {municipio.municipio_nombre if municipio else 'N/A'} > {puesto.puesto_nombre if puesto else 'N/A'} > Mesa {mesa.mesa_codigo}"
            
            delitos_data.append({
                'id': delito.id,
                'tipo': 'delito',
                'titulo': delito.titulo,
                'descripcion': delito.descripcion,
                'tipo_delito': delito.tipo_delito,
                'gravedad': delito.gravedad,
                'estado': delito.estado,
                'reportado_por': reportante.nombre if reportante else 'Usuario eliminado',
                'reportado_por_rol': reportante.rol if reportante else 'N/A',
                'ubicacion': ubicacion_completa,
                'mesa_codigo': mesa.mesa_codigo if mesa else 'N/A',
                'fecha_reporte': delito.fecha_reporte.isoformat() if delito.fecha_reporte else None,
                'denunciado_formalmente': delito.denunciado_formalmente,
                'resultado_investigacion': delito.resultado_investigacion
            })
        
        return jsonify({
            'success': True,
            'data': {
                'incidentes': incidentes_data,
                'delitos': delitos_data,
                'total_incidentes': len(incidentes_data),
                'total_delitos': len(delitos_data)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
