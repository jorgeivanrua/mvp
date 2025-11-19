"""
Rutas de herramientas administrativas
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.database import db
import os

admin_tools_bp = Blueprint('admin_tools', __name__, url_prefix='/api/admin')


@admin_tools_bp.route('/reset-database', methods=['POST'])
@jwt_required()
def reset_database():
    """
    Borrar la base de datos para forzar reinicialización
    Solo super_admin puede ejecutar esto
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'Solo super_admin puede resetear la base de datos'
            }), 403
        
        # Cerrar todas las conexiones
        db.session.remove()
        db.engine.dispose()
        
        # Borrar el archivo de base de datos
        db_path = 'instance/electoral.db'
        if os.path.exists(db_path):
            os.remove(db_path)
            return jsonify({
                'success': True,
                'message': 'Base de datos borrada. La aplicación se reiniciará automáticamente.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Archivo de base de datos no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_tools_bp.route('/fix-passwords', methods=['POST'])
@jwt_required()
def fix_passwords():
    """
    Actualizar todas las contraseñas a texto plano sin borrar la BD
    Solo super_admin puede ejecutar esto
    """
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user or current_user.rol != 'super_admin':
            return jsonify({
                'success': False,
                'error': 'Solo super_admin puede actualizar contraseñas'
            }), 403
        
        # Mapeo de contraseñas por rol
        PASSWORDS = {
            'super_admin': 'SuperAdmin123!',
            'admin_departamental': 'AdminDept123!',
            'admin_municipal': 'AdminMuni123!',
            'coordinador_departamental': 'CoordDept123!',
            'coordinador_municipal': 'CoordMuni123!',
            'auditor_electoral': 'Auditor123!',
            'coordinador_puesto': 'CoordPuesto123!',
            'testigo_electoral': 'Testigo123!'
        }
        
        users = User.query.all()
        updated = 0
        
        for user in users:
            password = PASSWORDS.get(user.rol, 'test123')
            # Actualizar directamente sin usar set_password para asegurar texto plano
            user.password_hash = password
            updated += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{updated} contraseñas actualizadas a texto plano',
            'passwords': PASSWORDS
        }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
