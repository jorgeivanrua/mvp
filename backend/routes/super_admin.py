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
