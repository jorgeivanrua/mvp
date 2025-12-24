"""
Sistema de seguimiento y análisis de errores
"""
import logging
import json
import os
from datetime import datetime
from functools import wraps
from flask import request, g
from flask_jwt_extended import get_jwt_identity

# Configurar logger específico para errores
error_logger = logging.getLogger('error_tracker')
error_handler = logging.FileHandler('logs/errors.log')
error_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)


def track_errors(f):
    """
    Decorador para rastrear errores en endpoints
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # Obtener información del contexto
            error_info = {
                'timestamp': datetime.utcnow().isoformat(),
                'endpoint': request.endpoint,
                'method': request.method,
                'url': request.url,
                'ip': request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
                'user_agent': request.headers.get('User-Agent'),
                'error_type': type(e).__name__,
                'error_message': str(e),
                'function': f.__name__
            }
            
            # Agregar información del usuario si está autenticado
            try:
                user_id = get_jwt_identity()
                if user_id:
                    error_info['user_id'] = user_id
            except:
                pass
            
            # Agregar datos de la petición (sin información sensible)
            if request.is_json:
                try:
                    data = request.get_json()
                    # Filtrar información sensible
                    filtered_data = filter_sensitive_data(data)
                    error_info['request_data'] = filtered_data
                except:
                    pass
            
            # Log del error
            error_logger.error(json.dumps(error_info, indent=2))
            
            # Re-lanzar la excepción para que sea manejada normalmente
            raise e
    
    return decorated_function


def filter_sensitive_data(data):
    """
    Filtrar información sensible de los datos de la petición
    """
    if not isinstance(data, dict):
        return data
    
    sensitive_keys = ['password', 'token', 'secret', 'key', 'cedula']
    filtered = {}
    
    for key, value in data.items():
        if any(sensitive_key in key.lower() for sensitive_key in sensitive_keys):
            filtered[key] = '[FILTERED]'
        elif isinstance(value, dict):
            filtered[key] = filter_sensitive_data(value)
        else:
            filtered[key] = value
    
    return filtered


def get_error_stats():
    """
    Obtener estadísticas de errores (para el dashboard de admin)
    """
    try:
        if not os.path.exists('logs/errors.log'):
            return {'total_errors': 0, 'recent_errors': []}
        
        with open('logs/errors.log', 'r') as f:
            lines = f.readlines()
        
        # Contar errores totales
        total_errors = len([line for line in lines if 'ERROR' in line])
        
        # Obtener errores recientes (últimas 10 líneas)
        recent_lines = lines[-20:]  # Más líneas porque cada error puede ser multi-línea
        recent_errors = []
        
        for line in recent_lines:
            if 'ERROR' in line:
                try:
                    # Extraer el JSON del error
                    json_start = line.find('{')
                    if json_start != -1:
                        json_str = line[json_start:]
                        error_data = json.loads(json_str)
                        recent_errors.append(error_data)
                except:
                    # Si no se puede parsear el JSON, agregar la línea como texto
                    recent_errors.append({'raw_error': line.strip()})
        
        return {
            'total_errors': total_errors,
            'recent_errors': recent_errors[-10:]  # Solo los 10 más recientes
        }
    
    except Exception as e:
        return {'error': f'Could not read error stats: {str(e)}'}


def clear_old_errors(days=30):
    """
    Limpiar errores antiguos del log
    """
    try:
        if not os.path.exists('logs/errors.log'):
            return
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        with open('logs/errors.log', 'r') as f:
            lines = f.readlines()
        
        # Filtrar líneas que son más recientes que la fecha de corte
        filtered_lines = []
        for line in lines:
            try:
                # Extraer timestamp de la línea
                timestamp_str = line.split(' - ')[0]
                line_date = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                if line_date > cutoff_date:
                    filtered_lines.append(line)
            except:
                # Si no se puede parsear la fecha, mantener la línea
                filtered_lines.append(line)
        
        # Escribir las líneas filtradas de vuelta al archivo
        with open('logs/errors.log', 'w') as f:
            f.writelines(filtered_lines)
    
    except Exception as e:
        error_logger.error(f'Error cleaning old errors: {str(e)}')