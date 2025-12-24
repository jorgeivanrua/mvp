"""
Sistema de métricas y monitoreo de rendimiento
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.database import db
from backend.models.user import User
from backend.models.formulario_e14 import FormularioE14
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
from datetime import datetime, timedelta
import psutil
import os

metrics_bp = Blueprint('metrics', __name__)


@metrics_bp.route('/api/system/metrics', methods=['GET'])
@jwt_required()
def get_system_metrics():
    """
    Obtener métricas del sistema (solo para administradores)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol not in ['super_admin', 'monitoreo']:
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        # Métricas de sistema
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('.')
        
        # Métricas de base de datos
        total_users = User.query.count()
        active_users = User.query.filter_by(activo=True).count()
        total_formularios = FormularioE14.query.count()
        formularios_hoy = FormularioE14.query.filter(
            FormularioE14.created_at >= datetime.utcnow().date()
        ).count()
        
        # Métricas de incidentes
        incidentes_hoy = IncidenteElectoral.query.filter(
            IncidenteElectoral.fecha_reporte >= datetime.utcnow().date()
        ).count()
        
        delitos_hoy = DelitoElectoral.query.filter(
            DelitoElectoral.fecha_reporte >= datetime.utcnow().date()
        ).count()
        
        # Usuarios por rol
        usuarios_por_rol = db.session.query(
            User.rol, 
            db.func.count(User.id)
        ).group_by(User.rol).all()
        
        metrics = {
            'timestamp': datetime.utcnow().isoformat(),
            'system': {
                'cpu_percent': cpu_percent,
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100
                }
            },
            'database': {
                'total_users': total_users,
                'active_users': active_users,
                'total_formularios': total_formularios,
                'formularios_hoy': formularios_hoy,
                'incidentes_hoy': incidentes_hoy,
                'delitos_hoy': delitos_hoy
            },
            'users_by_role': {rol: count for rol, count in usuarios_por_rol}
        }
        
        return jsonify({
            'success': True,
            'data': metrics
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@metrics_bp.route('/api/system/activity', methods=['GET'])
@jwt_required()
def get_activity_metrics():
    """
    Obtener métricas de actividad reciente
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol not in ['super_admin', 'monitoreo']:
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        # Actividad de los últimos 7 días
        fecha_inicio = datetime.utcnow() - timedelta(days=7)
        
        # Formularios por día
        formularios_por_dia = db.session.query(
            db.func.date(FormularioE14.created_at).label('fecha'),
            db.func.count(FormularioE14.id).label('count')
        ).filter(
            FormularioE14.created_at >= fecha_inicio
        ).group_by(
            db.func.date(FormularioE14.created_at)
        ).all()
        
        # Usuarios activos por día (último acceso)
        usuarios_activos_por_dia = db.session.query(
            db.func.date(User.ultimo_acceso).label('fecha'),
            db.func.count(User.id).label('count')
        ).filter(
            User.ultimo_acceso >= fecha_inicio
        ).group_by(
            db.func.date(User.ultimo_acceso)
        ).all()
        
        activity = {
            'timestamp': datetime.utcnow().isoformat(),
            'period': '7_days',
            'formularios_por_dia': [
                {
                    'fecha': str(fecha),
                    'count': count
                } for fecha, count in formularios_por_dia
            ],
            'usuarios_activos_por_dia': [
                {
                    'fecha': str(fecha),
                    'count': count
                } for fecha, count in usuarios_activos_por_dia
            ]
        }
        
        return jsonify({
            'success': True,
            'data': activity
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500