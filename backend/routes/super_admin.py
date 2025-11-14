"""
Rutas del Super Admin
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.decorators import role_required

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
        
        return jsonify({
            'success': True,
            'data': [user.to_dict() for user in users]
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
    - nombre: Nombre del partido
    - sigla: Sigla del partido
    - color: Color en formato hexadecimal (ej: #FF0000)
    - numero_lista: Número de lista (opcional)
    """
    try:
        from backend.database import db
        from backend.models.partido import Partido
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
        required_columns = ['nombre', 'sigla', 'color']
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
                
                # Crear partido
                partido = Partido(
                    nombre=row['nombre'],
                    sigla=row['sigla'],
                    color=row['color'],
                    numero_lista=row.get('numero_lista') if 'numero_lista' in row and pd.notna(row.get('numero_lista')) else None
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
    - nombre: Nombre del candidato
    - partido_nombre: Nombre del partido
    - tipo_eleccion_nombre: Nombre del tipo de elección
    - numero_lista: Número de lista (opcional)
    """
    try:
        from backend.database import db
        from backend.models.candidato import Candidato
        from backend.models.partido import Partido
        from backend.models.tipo_eleccion import TipoEleccion
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
        required_columns = ['nombre', 'partido_nombre', 'tipo_eleccion_nombre']
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
                
                # Verificar si el candidato ya existe
                existing_candidato = Candidato.query.filter_by(
                    nombre=row['nombre'],
                    partido_id=partido.id,
                    tipo_eleccion_id=tipo_eleccion.id
                ).first()
                
                if existing_candidato:
                    errors.append(f"Fila {index + 2}: Candidato '{row['nombre']}' ya existe para este partido y tipo de elección")
                    continue
                
                # Crear candidato
                candidato = Candidato(
                    nombre=row['nombre'],
                    partido_id=partido.id,
                    tipo_eleccion_id=tipo_eleccion.id,
                    numero_lista=row.get('numero_lista') if 'numero_lista' in row and pd.notna(row.get('numero_lista')) else None
                )
                
                db.session.add(candidato)
                created_candidatos.append(row['nombre'])
                
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
