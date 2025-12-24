"""
Sistema básico de rate limiting para proteger la API
"""
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
import json
import os

# Almacenamiento en memoria para rate limiting (en producción usar Redis)
rate_limit_storage = {}

def rate_limit(max_requests=100, window_minutes=15):
    """
    Decorador para limitar la tasa de peticiones por IP
    
    Args:
        max_requests: Número máximo de peticiones permitidas
        window_minutes: Ventana de tiempo en minutos
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Obtener IP del cliente
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            if not client_ip:
                client_ip = 'unknown'
            
            # Crear clave única para esta IP y endpoint
            key = f"{client_ip}:{request.endpoint}"
            current_time = datetime.utcnow()
            
            # Limpiar entradas expiradas
            cleanup_expired_entries()
            
            # Verificar si existe entrada para esta IP
            if key in rate_limit_storage:
                entry = rate_limit_storage[key]
                window_start = datetime.fromisoformat(entry['window_start'])
                
                # Si estamos en la misma ventana de tiempo
                if current_time - window_start < timedelta(minutes=window_minutes):
                    if entry['count'] >= max_requests:
                        return jsonify({
                            'success': False,
                            'error': 'Rate limit exceeded',
                            'retry_after': int((window_start + timedelta(minutes=window_minutes) - current_time).total_seconds())
                        }), 429
                    
                    # Incrementar contador
                    rate_limit_storage[key]['count'] += 1
                else:
                    # Nueva ventana de tiempo
                    rate_limit_storage[key] = {
                        'count': 1,
                        'window_start': current_time.isoformat()
                    }
            else:
                # Primera petición de esta IP
                rate_limit_storage[key] = {
                    'count': 1,
                    'window_start': current_time.isoformat()
                }
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def cleanup_expired_entries():
    """Limpiar entradas expiradas del almacenamiento"""
    current_time = datetime.utcnow()
    expired_keys = []
    
    for key, entry in rate_limit_storage.items():
        window_start = datetime.fromisoformat(entry['window_start'])
        if current_time - window_start > timedelta(hours=1):  # Limpiar después de 1 hora
            expired_keys.append(key)
    
    for key in expired_keys:
        del rate_limit_storage[key]


def get_rate_limit_status():
    """Obtener estado actual del rate limiting (para debugging)"""
    cleanup_expired_entries()
    return {
        'active_entries': len(rate_limit_storage),
        'entries': rate_limit_storage
    }