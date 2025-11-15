"""
Rutas administrativas para gestión remota
⚠️ SOLO PARA DESARROLLO - Deshabilitar en producción
"""
from flask import Blueprint, jsonify, request
import json
import os
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.models.configuracion_electoral import Campana, TipoEleccion, Partido

admin_tools_bp = Blueprint('admin_tools', __name__)

# Clave secreta para proteger endpoints (cambiar en producción)
SECRET_KEY = "temp_admin_key_2024"

def verify_admin_key():
    """Verificar clave de administrador"""
    key = request.headers.get('X-Admin-Key') or request.args.get('admin_key')
    return key == SECRET_KEY

@admin_tools_bp.route('/export-data', methods=['GET'])
def export_data():
    """
    Exportar todos los datos a JSON
    Uso: GET /api/admin-tools/export-data?admin_key=temp_admin_key_2024
    """
    if not verify_admin_key():
        return jsonify({
            'success': False,
            'error': 'Clave de administrador inválida'
        }), 403
    
    try:
        data = {
            'locations': [],
            'users': [],
            'campanas': [],
            'tipos_eleccion': [],
            'partidos': []
        }
        
        # Exportar ubicaciones
        locations = Location.query.all()
        for loc in locations:
            data['locations'].append({
                'departamento_codigo': loc.departamento_codigo,
                'municipio_codigo': loc.municipio_codigo,
                'zona_codigo': loc.zona_codigo,
                'puesto_codigo': loc.puesto_codigo,
                'mesa_codigo': loc.mesa_codigo,
                'departamento_nombre': loc.departamento_nombre,
                'municipio_nombre': loc.municipio_nombre,
                'puesto_nombre': loc.puesto_nombre,
                'mesa_nombre': loc.mesa_nombre,
                'nombre_completo': loc.nombre_completo,
                'tipo': loc.tipo,
                'total_votantes_registrados': loc.total_votantes_registrados,
                'mujeres': loc.mujeres,
                'hombres': loc.hombres,
                'comuna': loc.comuna,
                'direccion': loc.direccion,
                'latitud': loc.latitud,
                'longitud': loc.longitud,
                'activo': loc.activo
            })
        
        # Exportar usuarios (sin contraseñas)
        users = User.query.all()
        for user in users:
            ubicacion_info = None
            if user.ubicacion_id:
                loc = Location.query.get(user.ubicacion_id)
                if loc:
                    ubicacion_info = {
                        'departamento_codigo': loc.departamento_codigo,
                        'municipio_codigo': loc.municipio_codigo,
                        'zona_codigo': loc.zona_codigo,
                        'puesto_codigo': loc.puesto_codigo,
                        'mesa_codigo': loc.mesa_codigo,
                        'tipo': loc.tipo
                    }
            
            data['users'].append({
                'nombre': user.nombre,
                'rol': user.rol,
                'ubicacion_info': ubicacion_info,
                'activo': user.activo
            })
        
        # Exportar campañas
        campanas = Campana.query.all()
        for campana in campanas:
            data['campanas'].append({
                'codigo': campana.codigo,
                'nombre': campana.nombre,
                'descripcion': campana.descripcion,
                'fecha_inicio': campana.fecha_inicio.isoformat() if campana.fecha_inicio else None,
                'fecha_fin': campana.fecha_fin.isoformat() if campana.fecha_fin else None,
                'color_primario': campana.color_primario,
                'color_secundario': campana.color_secundario,
                'es_partido_completo': campana.es_partido_completo,
                'activa': campana.activa
            })
        
        # Exportar tipos de elección
        tipos = TipoEleccion.query.all()
        for tipo in tipos:
            data['tipos_eleccion'].append({
                'codigo': tipo.codigo,
                'nombre': tipo.nombre,
                'es_uninominal': getattr(tipo, 'es_uninominal', False),
                'permite_lista_cerrada': getattr(tipo, 'permite_lista_cerrada', False),
                'permite_lista_abierta': getattr(tipo, 'permite_lista_abierta', False),
                'permite_voto_preferente': getattr(tipo, 'permite_voto_preferente', False),
                'activo': tipo.activo
            })
        
        # Exportar partidos
        partidos = Partido.query.all()
        for partido in partidos:
            data['partidos'].append({
                'codigo': partido.codigo,
                'nombre': partido.nombre,
                'nombre_corto': partido.nombre_corto,
                'color': partido.color,
                'activo': partido.activo
            })
        
        return jsonify({
            'success': True,
            'data': data,
            'summary': {
                'locations': len(data['locations']),
                'users': len(data['users']),
                'campanas': len(data['campanas']),
                'tipos_eleccion': len(data['tipos_eleccion']),
                'partidos': len(data['partidos'])
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_tools_bp.route('/reset-passwords', methods=['POST'])
def reset_passwords():
    """
    Resetear todas las contraseñas a test123
    Uso: POST /api/admin-tools/reset-passwords?admin_key=temp_admin_key_2024
    """
    if not verify_admin_key():
        return jsonify({
            'success': False,
            'error': 'Clave de administrador inválida'
        }), 403
    
    try:
        users = User.query.all()
        
        if not users:
            return jsonify({
                'success': False,
                'error': 'No se encontraron usuarios'
            }), 404
        
        count = 0
        for user in users:
            user.set_password('test123')
            count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{count} contraseñas reseteadas a test123',
            'users_updated': count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_tools_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Obtener estadísticas de la base de datos
    Uso: GET /api/admin-tools/stats?admin_key=temp_admin_key_2024
    """
    if not verify_admin_key():
        return jsonify({
            'success': False,
            'error': 'Clave de administrador inválida'
        }), 403
    
    try:
        stats = {
            'locations': {
                'total': Location.query.count(),
                'departamentos': Location.query.filter_by(tipo='departamento').count(),
                'municipios': Location.query.filter_by(tipo='municipio').count(),
                'puestos': Location.query.filter_by(tipo='puesto').count(),
                'mesas': Location.query.filter_by(tipo='mesa').count()
            },
            'users': {
                'total': User.query.count(),
                'activos': User.query.filter_by(activo=True).count(),
                'por_rol': {}
            },
            'campanas': Campana.query.count(),
            'tipos_eleccion': TipoEleccion.query.count(),
            'partidos': Partido.query.count()
        }
        
        # Contar usuarios por rol
        roles = ['super_admin', 'auditor_electoral', 'coordinador_departamental', 
                'coordinador_municipal', 'coordinador_puesto', 'testigo_electoral']
        for rol in roles:
            stats['users']['por_rol'][rol] = User.query.filter_by(rol=rol).count()
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
