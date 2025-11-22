"""
Rutas para configuración del sistema
Permite al Super Admin personalizar la apariencia
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.configuracion_sistema import ConfiguracionSistema, FondoLogin
from backend.database import db
from backend.utils.decorators import role_required
from werkzeug.utils import secure_filename
import os
import uuid

config_sistema_bp = Blueprint('config_sistema', __name__, url_prefix='/api/config-sistema')

# Configuración de uploads
UPLOAD_FOLDER = 'frontend/static/uploads/fondos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@config_sistema_bp.route('/fondos', methods=['GET'])
def get_fondos():
    """
    Obtener todos los fondos disponibles
    Endpoint público para que el login pueda cargar el fondo activo
    """
    try:
        fondos = FondoLogin.query.order_by(FondoLogin.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [fondo.to_dict() for fondo in fondos]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_sistema_bp.route('/fondos/activo', methods=['GET'])
def get_fondo_activo():
    """
    Obtener el fondo activo actual
    Endpoint público para el login
    """
    try:
        fondo = FondoLogin.get_activo()
        
        if not fondo:
            # Retornar fondo por defecto (bandera de Colombia)
            return jsonify({
                'success': True,
                'data': {
                    'tipo': 'gradient',
                    'color1': '#FCD116',
                    'color2': '#003893',
                    'color3': '#CE1126',
                    'direccion': '180deg',
                    'overlay_color': '#FFFFFF',
                    'overlay_opacity': 0.1
                }
            }), 200
        
        return jsonify({
            'success': True,
            'data': fondo.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_sistema_bp.route('/fondos', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def crear_fondo():
    """
    Crear un nuevo fondo
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Validar tipo
        tipo = data.get('tipo')
        if tipo not in ['gradient', 'image', 'solid']:
            return jsonify({
                'success': False,
                'error': 'Tipo de fondo inválido'
            }), 400
        
        # Crear fondo
        fondo = FondoLogin(
            nombre=data.get('nombre', 'Fondo personalizado'),
            tipo=tipo,
            created_by=int(user_id)
        )
        
        # Configurar según tipo
        if tipo == 'gradient':
            fondo.color1 = data.get('color1')
            fondo.color2 = data.get('color2')
            fondo.color3 = data.get('color3')
            fondo.direccion = data.get('direccion', '180deg')
            
        elif tipo == 'image':
            fondo.imagen_url = data.get('imagen_url')
            fondo.imagen_posicion = data.get('imagen_posicion', 'center')
            fondo.imagen_tamano = data.get('imagen_tamano', 'cover')
            
        elif tipo == 'solid':
            fondo.color_solido = data.get('color_solido')
        
        # Overlay opcional
        if data.get('overlay_color'):
            fondo.overlay_color = data.get('overlay_color')
            fondo.overlay_opacity = data.get('overlay_opacity', 0.1)
        
        db.session.add(fondo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Fondo creado exitosamente',
            'data': fondo.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_sistema_bp.route('/fondos/<int:fondo_id>/activar', methods=['PUT'])
@jwt_required()
@role_required(['super_admin'])
def activar_fondo(fondo_id):
    """
    Activar un fondo (desactiva los demás)
    """
    try:
        fondo = FondoLogin.query.get(fondo_id)
        
        if not fondo:
            return jsonify({
                'success': False,
                'error': 'Fondo no encontrado'
            }), 404
        
        # Desactivar todos los fondos
        FondoLogin.query.update({'activo': False})
        
        # Activar el seleccionado
        fondo.activo = True
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Fondo activado exitosamente',
            'data': fondo.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_sistema_bp.route('/fondos/<int:fondo_id>', methods=['DELETE'])
@jwt_required()
@role_required(['super_admin'])
def eliminar_fondo(fondo_id):
    """
    Eliminar un fondo
    """
    try:
        fondo = FondoLogin.query.get(fondo_id)
        
        if not fondo:
            return jsonify({
                'success': False,
                'error': 'Fondo no encontrado'
            }), 404
        
        # No permitir eliminar el fondo activo
        if fondo.activo:
            return jsonify({
                'success': False,
                'error': 'No se puede eliminar el fondo activo. Activa otro fondo primero.'
            }), 400
        
        # Si es imagen, eliminar archivo
        if fondo.tipo == 'image' and fondo.imagen_url:
            try:
                # Extraer ruta del archivo
                filename = fondo.imagen_url.split('/')[-1]
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass  # No fallar si no se puede eliminar el archivo
        
        db.session.delete(fondo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Fondo eliminado exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_sistema_bp.route('/fondos/upload', methods=['POST'])
@jwt_required()
@role_required(['super_admin'])
def upload_fondo():
    """
    Subir imagen de fondo
    """
    try:
        user_id = get_jwt_identity()
        
        # Verificar que se envió un archivo
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se envió ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No se seleccionó ningún archivo'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Tipo de archivo no permitido. Use: png, jpg, jpeg, gif, webp'
            }), 400
        
        # Crear directorio si no existe
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Generar nombre único
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Guardar archivo
        file.save(filepath)
        
        # URL relativa para acceder al archivo
        file_url = f"/static/uploads/fondos/{filename}"
        
        # Obtener datos adicionales del form
        nombre = request.form.get('nombre', 'Fondo con imagen')
        imagen_posicion = request.form.get('imagen_posicion', 'center')
        imagen_tamano = request.form.get('imagen_tamano', 'cover')
        overlay_color = request.form.get('overlay_color')
        overlay_opacity = float(request.form.get('overlay_opacity', 0.1))
        
        # Crear fondo en la base de datos
        fondo = FondoLogin(
            nombre=nombre,
            tipo='image',
            imagen_url=file_url,
            imagen_posicion=imagen_posicion,
            imagen_tamano=imagen_tamano,
            overlay_color=overlay_color,
            overlay_opacity=overlay_opacity,
            created_by=int(user_id)
        )
        
        db.session.add(fondo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Imagen subida exitosamente',
            'data': fondo.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@config_sistema_bp.route('/fondos/predefinidos', methods=['GET'])
@jwt_required()
@role_required(['super_admin'])
def get_fondos_predefinidos():
    """
    Obtener fondos predefinidos para selección rápida
    """
    try:
        fondos_predefinidos = [
            {
                'nombre': 'Bandera de Colombia',
                'tipo': 'gradient',
                'color1': '#FCD116',
                'color2': '#003893',
                'color3': '#CE1126',
                'direccion': '180deg',
                'preview': 'linear-gradient(180deg, #FCD116 0%, #FCD116 50%, #003893 50%, #003893 75%, #CE1126 75%, #CE1126 100%)'
            },
            {
                'nombre': 'Azul Institucional',
                'tipo': 'gradient',
                'color1': '#003893',
                'color2': '#001f5c',
                'direccion': '135deg',
                'preview': 'linear-gradient(135deg, #003893 0%, #001f5c 100%)'
            },
            {
                'nombre': 'Amarillo Vibrante',
                'tipo': 'solid',
                'color_solido': '#FCD116',
                'preview': '#FCD116'
            },
            {
                'nombre': 'Rojo Patriótico',
                'tipo': 'solid',
                'color_solido': '#CE1126',
                'preview': '#CE1126'
            },
            {
                'nombre': 'Azul Oscuro',
                'tipo': 'solid',
                'color_solido': '#003893',
                'preview': '#003893'
            },
            {
                'nombre': 'Gradiente Amanecer',
                'tipo': 'gradient',
                'color1': '#FCD116',
                'color2': '#FF6B6B',
                'direccion': '45deg',
                'preview': 'linear-gradient(45deg, #FCD116 0%, #FF6B6B 100%)'
            },
            {
                'nombre': 'Gradiente Océano',
                'tipo': 'gradient',
                'color1': '#003893',
                'color2': '#00D4FF',
                'direccion': '135deg',
                'preview': 'linear-gradient(135deg, #003893 0%, #00D4FF 100%)'
            }
        ]
        
        return jsonify({
            'success': True,
            'data': fondos_predefinidos
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
