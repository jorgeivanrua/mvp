"""
Utilidades para manejo de JWT
"""
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta


def generate_tokens(user):
    """
    Generar tokens de acceso y renovación para un usuario
    
    Args:
        user: Objeto User
        
    Returns:
        tuple: (access_token, refresh_token)
    """
    # Claims adicionales para incluir en el token
    additional_claims = {
        'rol': user.rol,
        'ubicacion_id': user.ubicacion_id,
        'nombre': user.nombre
    }
    
    # Generar tokens (identity debe ser string)
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims
    )
    
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims=additional_claims
    )
    
    return access_token, refresh_token


def create_token_response(user, access_token, refresh_token):
    """
    Crear respuesta con tokens y datos de usuario
    
    Args:
        user: Objeto User
        access_token: Token de acceso
        refresh_token: Token de renovación
        
    Returns:
        dict: Respuesta con tokens y usuario
    """
    return {
        'success': True,
        'data': {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'nombre': user.nombre,
                'rol': user.rol,
                'ubicacion_id': user.ubicacion_id,
                'activo': user.activo
            }
        }
    }
