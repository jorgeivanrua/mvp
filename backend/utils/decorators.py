"""
Decoradores de autenticación y autorización
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt


def token_required(fn):
    """
    Decorador que requiere un token JWT válido
    
    Usage:
        @token_required
        def protected_route():
            pass
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Token inválido o expirado'
            }), 401
    return wrapper


def role_required(*allowed_roles):
    """
    Decorador que requiere un rol específico
    
    Args:
        *allowed_roles: Roles permitidos
        
    Usage:
        @role_required('admin', 'coordinador_puesto')
        def admin_route():
            pass
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                user_role = claims.get('rol')
                
                if user_role not in allowed_roles:
                    return jsonify({
                        'success': False,
                        'error': 'No tiene permisos para acceder a este recurso'
                    }), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': 'Token inválido o expirado'
                }), 401
        return wrapper
    return decorator


def location_access_required(fn):
    """
    Decorador que verifica acceso a ubicación específica
    
    Usage:
        @location_access_required
        def location_route(location_id):
            pass
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('rol')
            user_location_id = claims.get('ubicacion_id')
            
            # Super admin tiene acceso a todo
            if user_role == 'super_admin':
                return fn(*args, **kwargs)
            
            # Obtener location_id del request
            location_id = kwargs.get('location_id') or args[0] if args else None
            
            if not location_id:
                return jsonify({
                    'success': False,
                    'error': 'ID de ubicación no proporcionado'
                }), 400
            
            # Verificar acceso según rol y jerarquía
            # TODO: Implementar lógica de verificación jerárquica
            # Por ahora, verificar que tenga acceso a la ubicación
            
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Error verificando permisos de ubicación'
            }), 403
    return wrapper


def get_current_user_id():
    """
    Obtener ID del usuario actual desde el token JWT
    
    Returns:
        int: ID del usuario o None
    """
    try:
        return get_jwt_identity()
    except:
        return None


def get_current_user_claims():
    """
    Obtener claims del usuario actual desde el token JWT
    
    Returns:
        dict: Claims del usuario o {}
    """
    try:
        return get_jwt()
    except:
        return {}
