"""
WebSocket Service para notificaciones en tiempo real
"""
from flask_socketio import emit, join_room, leave_room
from flask import current_app
from backend.app import socketio
from functools import wraps
from flask_jwt_extended import decode_token
import logging

logger = logging.getLogger(__name__)

# Diccionario para rastrear usuarios conectados
# Formato: {user_id: [sid1, sid2, ...]}
connected_users = {}


def authenticated_only(f):
    """
    Decorator para requerir autenticación en eventos de SocketIO
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        # El token JWT se pasa en el handshake
        # Por ahora permitimos conexiones sin autenticación
        # TODO: Implementar autenticación JWT en SocketIO
        return f(*args, **kwargs)
    return wrapped


@socketio.on('connect')
def handle_connect():
    """
    Handler para cuando un cliente se conecta
    """
    from flask import request
    sid = request.sid
    logger.info(f'Cliente conectado: {sid}')
    
    # Emitir confirmación de conexión
    emit('connected', {'message': 'Conectado al servidor de notificaciones'})


@socketio.on('disconnect')
def handle_disconnect():
    """
    Handler para cuando un cliente se desconecta
    """
    from flask import request
    sid = request.sid
    logger.info(f'Cliente desconectado: {sid}')
    
    # Remover de usuarios conectados
    for user_id, sids in list(connected_users.items()):
        if sid in sids:
            sids.remove(sid)
            if not sids:
                del connected_users[user_id]
            logger.info(f'Usuario {user_id} desconectado (sid: {sid})')


@socketio.on('register')
def handle_register(data):
    """
    Handler para registrar un usuario conectado
    
    Args:
        data: {'user_id': int}
    """
    from flask import request
    sid = request.sid
    user_id = data.get('user_id')
    
    if not user_id:
        emit('error', {'message': 'user_id requerido'})
        return
    
    # Agregar a usuarios conectados
    if user_id not in connected_users:
        connected_users[user_id] = []
    
    if sid not in connected_users[user_id]:
        connected_users[user_id].append(sid)
    
    # Unir a room personal del usuario
    join_room(f'user_{user_id}')
    
    logger.info(f'Usuario {user_id} registrado (sid: {sid})')
    emit('registered', {'message': 'Registrado exitosamente', 'user_id': user_id})


@socketio.on('unregister')
def handle_unregister(data):
    """
    Handler para desregistrar un usuario
    
    Args:
        data: {'user_id': int}
    """
    from flask import request
    sid = request.sid
    user_id = data.get('user_id')
    
    if not user_id:
        return
    
    # Remover de usuarios conectados
    if user_id in connected_users and sid in connected_users[user_id]:
        connected_users[user_id].remove(sid)
        if not connected_users[user_id]:
            del connected_users[user_id]
    
    # Salir de room personal
    leave_room(f'user_{user_id}')
    
    logger.info(f'Usuario {user_id} desregistrado (sid: {sid})')


class WebSocketService:
    """
    Servicio para emitir notificaciones por WebSocket
    """
    
    @staticmethod
    def emit_to_user(user_id, event, data):
        """
        Emitir evento a un usuario específico
        
        Args:
            user_id: ID del usuario
            event: Nombre del evento
            data: Datos a enviar
        """
        try:
            room = f'user_{user_id}'
            socketio.emit(event, data, room=room)
            logger.info(f'Evento {event} emitido a usuario {user_id}')
            return True
        except Exception as e:
            logger.error(f'Error emitiendo a usuario {user_id}: {str(e)}')
            return False
    
    @staticmethod
    def emit_to_users(user_ids, event, data):
        """
        Emitir evento a múltiples usuarios
        
        Args:
            user_ids: Lista de IDs de usuarios
            event: Nombre del evento
            data: Datos a enviar
        """
        success_count = 0
        for user_id in user_ids:
            if WebSocketService.emit_to_user(user_id, event, data):
                success_count += 1
        
        logger.info(f'Evento {event} emitido a {success_count}/{len(user_ids)} usuarios')
        return success_count
    
    @staticmethod
    def emit_global(event, data):
        """
        Emitir evento a todos los clientes conectados
        
        Args:
            event: Nombre del evento
            data: Datos a enviar
        """
        try:
            socketio.emit(event, data, broadcast=True)
            logger.info(f'Evento {event} emitido globalmente')
            return True
        except Exception as e:
            logger.error(f'Error emitiendo globalmente: {str(e)}')
            return False
    
    @staticmethod
    def get_connected_users():
        """
        Obtener lista de usuarios conectados
        
        Returns:
            Lista de user_ids conectados
        """
        return list(connected_users.keys())
    
    @staticmethod
    def is_user_connected(user_id):
        """
        Verificar si un usuario está conectado
        
        Args:
            user_id: ID del usuario
            
        Returns:
            bool: True si está conectado
        """
        return user_id in connected_users and len(connected_users[user_id]) > 0
    
    @staticmethod
    def notify_new_incidente(incidente_data, user_ids):
        """
        Notificar sobre nuevo incidente
        
        Args:
            incidente_data: Datos del incidente
            user_ids: Lista de IDs de usuarios a notificar
        """
        data = {
            'tipo': 'nuevo_incidente',
            'incidente': incidente_data,
            'timestamp': incidente_data.get('fecha_reporte')
        }
        return WebSocketService.emit_to_users(user_ids, 'nueva_notificacion', data)
    
    @staticmethod
    def notify_new_delito(delito_data, user_ids):
        """
        Notificar sobre nuevo delito
        
        Args:
            delito_data: Datos del delito
            user_ids: Lista de IDs de usuarios a notificar
        """
        data = {
            'tipo': 'nuevo_delito',
            'delito': delito_data,
            'timestamp': delito_data.get('fecha_reporte')
        }
        return WebSocketService.emit_to_users(user_ids, 'nueva_notificacion', data)
    
    @staticmethod
    def notify_estado_cambio(reporte_data, user_ids):
        """
        Notificar sobre cambio de estado
        
        Args:
            reporte_data: Datos del reporte
            user_ids: Lista de IDs de usuarios a notificar
        """
        data = {
            'tipo': 'cambio_estado',
            'reporte': reporte_data,
            'timestamp': reporte_data.get('fecha_actualizacion')
        }
        return WebSocketService.emit_to_users(user_ids, 'nueva_notificacion', data)
    
    @staticmethod
    def notify_mapa_update():
        """
        Notificar que el mapa debe actualizarse
        """
        data = {
            'tipo': 'actualizar_mapa',
            'timestamp': None  # Se agregará en el cliente
        }
        return WebSocketService.emit_global('actualizar_mapa', data)
