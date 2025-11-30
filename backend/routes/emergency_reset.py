"""
Endpoint de emergencia para resetear contraseñas
SOLO PARA USO EN DESARROLLO O EMERGENCIAS
"""
from flask import Blueprint, jsonify, request
from backend.database import db
from backend.models.user import User
from werkzeug.security import generate_password_hash
import os

emergency_bp = Blueprint('emergency', __name__)

# Clave secreta para proteger el endpoint
EMERGENCY_KEY = os.getenv('EMERGENCY_RESET_KEY', 'reset_passwords_2024_emergency')

@emergency_bp.route('/emergency-reset-passwords', methods=['POST'])
def emergency_reset_passwords():
    """
    Endpoint de emergencia para resetear contraseñas
    
    Uso:
    POST /api/emergency/emergency-reset-passwords
    Body: { "emergency_key": "tu_clave_secreta" }
    """
    try:
        data = request.get_json()
        
        # Verificar clave de emergencia
        if not data or data.get('emergency_key') != EMERGENCY_KEY:
            return jsonify({
                'success': False,
                'error': 'Clave de emergencia inválida'
            }), 403
        
        # Contraseñas por defecto
        passwords = {
            'super_admin': 'admin123',
            'monitoreo': 'test123',
            'coordinador_departamental': 'test123',
            'coordinador_municipal': 'test123',
            'coordinador_puesto': 'test123',
            'auditor_electoral': 'test123'
        }
        
        usuarios_actualizados = []
        usuarios_no_encontrados = []
        
        # Actualizar cada usuario
        for rol, password in passwords.items():
            usuario = User.query.filter_by(rol=rol).first()
            
            if usuario:
                usuario.password_hash = generate_password_hash(password)
                usuario.activo = True
                usuario.intentos_fallidos = 0
                usuario.bloqueado_hasta = None
                
                usuarios_actualizados.append({
                    'id': usuario.id,
                    'nombre': usuario.nombre,
                    'rol': rol,
                    'password': password
                })
            else:
                usuarios_no_encontrados.append(rol)
        
        # Guardar cambios
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Contraseñas reseteadas exitosamente',
            'usuarios_actualizados': usuarios_actualizados,
            'usuarios_no_encontrados': usuarios_no_encontrados,
            'total_actualizados': len(usuarios_actualizados)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@emergency_bp.route('/emergency-create-users', methods=['POST'])
def emergency_create_users():
    """
    Endpoint de emergencia para crear usuarios básicos si no existen
    
    Uso:
    POST /api/emergency/emergency-create-users
    Body: { "emergency_key": "tu_clave_secreta" }
    """
    try:
        data = request.get_json()
        
        # Verificar clave de emergencia
        if not data or data.get('emergency_key') != EMERGENCY_KEY:
            return jsonify({
                'success': False,
                'error': 'Clave de emergencia inválida'
            }), 403
        
        # Definir usuarios básicos
        usuarios_basicos = [
            {
                'nombre': 'Super Admin',
                'password': 'admin123',
                'rol': 'super_admin',
                'activo': True
            },
            {
                'nombre': 'Monitoreo',
                'password': 'test123',
                'rol': 'monitoreo',
                'activo': True
            },
            {
                'nombre': 'Coordinador Departamental',
                'password': 'test123',
                'rol': 'coordinador_departamental',
                'activo': True
            },
            {
                'nombre': 'Coordinador Municipal',
                'password': 'test123',
                'rol': 'coordinador_municipal',
                'activo': True
            },
            {
                'nombre': 'Coordinador Puesto',
                'password': 'test123',
                'rol': 'coordinador_puesto',
                'activo': True
            },
            {
                'nombre': 'Auditor Electoral',
                'password': 'test123',
                'rol': 'auditor_electoral',
                'activo': True
            }
        ]
        
        usuarios_creados = []
        usuarios_existentes = []
        
        for usuario_data in usuarios_basicos:
            # Buscar usuario por rol
            usuario = User.query.filter_by(
                rol=usuario_data['rol'],
                nombre=usuario_data['nombre']
            ).first()
            
            if usuario:
                usuarios_existentes.append({
                    'id': usuario.id,
                    'nombre': usuario.nombre,
                    'rol': usuario.rol
                })
            else:
                # Crear nuevo usuario
                usuario = User(
                    nombre=usuario_data['nombre'],
                    password_hash=generate_password_hash(usuario_data['password']),
                    rol=usuario_data['rol'],
                    activo=usuario_data['activo']
                )
                db.session.add(usuario)
                usuarios_creados.append({
                    'nombre': usuario_data['nombre'],
                    'rol': usuario_data['rol'],
                    'password': usuario_data['password']
                })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuarios procesados exitosamente',
            'usuarios_creados': usuarios_creados,
            'usuarios_existentes': usuarios_existentes,
            'total_creados': len(usuarios_creados),
            'total_existentes': len(usuarios_existentes)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@emergency_bp.route('/emergency-unlock-users', methods=['POST'])
def emergency_unlock_users():
    """
    Endpoint de emergencia para desbloquear todos los usuarios
    
    Uso:
    POST /api/emergency/emergency-unlock-users
    Body: { "emergency_key": "tu_clave_secreta" }
    """
    try:
        data = request.get_json()
        
        # Verificar clave de emergencia
        if not data or data.get('emergency_key') != EMERGENCY_KEY:
            return jsonify({
                'success': False,
                'error': 'Clave de emergencia inválida'
            }), 403
        
        usuarios = User.query.all()
        usuarios_desbloqueados = []
        
        for usuario in usuarios:
            if usuario.bloqueado_hasta or usuario.intentos_fallidos > 0:
                usuario.intentos_fallidos = 0
                usuario.bloqueado_hasta = None
                usuarios_desbloqueados.append({
                    'id': usuario.id,
                    'nombre': usuario.nombre,
                    'rol': usuario.rol
                })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuarios desbloqueados exitosamente',
            'usuarios_desbloqueados': usuarios_desbloqueados,
            'total': len(usuarios_desbloqueados)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@emergency_bp.route('/emergency-list-users', methods=['POST'])
def emergency_list_users():
    """
    Endpoint de emergencia para listar todos los usuarios
    
    Uso:
    POST /api/emergency/emergency-list-users
    Body: { "emergency_key": "tu_clave_secreta" }
    """
    try:
        data = request.get_json()
        
        # Verificar clave de emergencia
        if not data or data.get('emergency_key') != EMERGENCY_KEY:
            return jsonify({
                'success': False,
                'error': 'Clave de emergencia inválida'
            }), 403
        
        usuarios = User.query.all()
        
        usuarios_data = []
        for usuario in usuarios:
            usuarios_data.append({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'rol': usuario.rol,
                'activo': usuario.activo,
                'intentos_fallidos': usuario.intentos_fallidos,
                'bloqueado': usuario.bloqueado_hasta is not None,
                'ultimo_acceso': usuario.ultimo_acceso.isoformat() if usuario.ultimo_acceso else None
            })
        
        return jsonify({
            'success': True,
            'total_usuarios': len(usuarios),
            'usuarios': usuarios_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
