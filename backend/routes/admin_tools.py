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
