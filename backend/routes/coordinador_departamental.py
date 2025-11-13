"""
Rutas para el coordinador departamental
"""
from flask import Blueprint, render_template, jsonify, request, send_file
from backend.utils.decorators import login_required, role_required
from backend.services.departamental_service import DepartamentalService
from backend.services.discrepancia_service import DiscrepanciaService
from backend.services.reporte_departamental_service import ReporteDepartamentalService
from backend.models.user import User
from backend.models.location import Location
from backend.database import db
from datetime import datetime

bp = Blueprint('coordinador_departamental', __name__, url_prefix='/coordinador/departamental')


@bp.route('/')
@login_required
@role_required(['coordinador_departamental', 'super_admin'])
def dashboard(current_user):
    """Dashboard principal del coordinador departamental"""
    return render_template('coordinador/departamental.html', user=current_user)


@bp.route('/api/municipios')
@login_required
@role_required(['coordinador_departamental', 'super_admin'])
def obtener_municipios(current_user):
    """
    Obtener lista de municipios del departamento con estadísticas
    Query params:
        - estado: filtro por estado (completo, incompleto, con_discrepancias)
    """
    try:
        # Obtener departamento del coordinador
        if current_user.rol == 'super_admin':
            # Super admin puede ver cualquier departamento
            departamento_id = request.args.get('departamento_id', type=int)
            if not departamento_id:
                return jsonify({'error': 'Se requiere departamento_id para super_admin'}), 400
        else:
            departamento_id = current_user.ubicacion_id
        
        if not departamento_id:
            return jsonify({'error': 'Usuario sin departamento asignado'}), 400
        
        # Obtener filtros
        filtros = {}
        if request.args.get('estado'):
            filtros['estado'] = request.args.get('estado')
        
        # Obtener municipios
        resultado = DepartamentalService.obtener_municipios_departamento(departamento_id, filtros)
        
        if not resultado:
            return jsonify({'error': 'No se pudieron obtener los municipios'}), 404
        
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/consolidado')
@login_required
@role_required(['coordinador_departamental', 'super_admin'])
def obtener_consolidado(current_user):
    """
    Obtener consolidado departamental
    Query params:
        - tipo_eleccion_id: ID del tipo de elección (opcional)
    """
    try:
        # Obtener departamento del coordinador
        if current_user.rol == 'super_admin':
            departamento_id = request.args.get('departamento_id', type=int)
            if not departamento_id:
                return jsonify({'error': 'Se requiere departamento_id para super_admin'}), 400
        else:
            departamento_id = current_user.ubicacion_id
        
        if not departamento_id:
            return jsonify({'error': 'Usuario sin departamento asignado'}), 400
        
        tipo_eleccion_id = request.args.get('tipo_eleccion_id', type=int)
        
        # Calcular consolidado
        consolidado = DepartamentalService.calcular_consolidado_departamental(
            departamento_id, 
            tipo_eleccion_id
        )
        
        if not consolidado:
            return jsonify({'error': 'No se pudo calcular el consolidado'}), 404
        
        return jsonify(consolidado), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/municipio/<int:municipio_id>')
@login_required
@role_required(['coordinador_departamental', 'super_admin'])
def obtener_municipio_detallado(current_user, municipio_id):
    """Obtener información detallada de un municipio"""
    try:
        # Obtener información del municipio
        municipio_info = DepartamentalService.obtener_municipio_detallado(
            municipio_id, 
            current_user.id
        )
        
        if not municipio_info:
            return jsonify({'error': 'Municipio no encontrado o sin permisos'}), 404
        
        return jsonify(municipio_info), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/discrepancias')
@login_required
@role_required(['coordinador_departamental', 'super_admin'])
def obtener_discrepancias(current_user):
    """Obtener discrepancias del departamento"""
    try:
        # Obtener departamento del coordinador
        if current_user.rol == 'super_admin':
            departamento_id = request.args.get('departamento_id', type=int)
            if not departamento_id:
                return jsonify({'error': 'Se requiere departamento_id para super_admin'}), 400
        else:
            departamento_id = current_user.ubicacion_id
        
        if not departamento_id:
            return jsonify({'error': 'Usuario sin departamento asignado'}), 400
        
        # Detectar discrepancias
        discrepancias = DiscrepanciaService.detectar_discrepancias_departamento(departamento_id)
        
        return jsonify({'discrepancias': discrepancias}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/comparar-municipios', methods=['POST'])
@login_required
@role_required(['coordinador_departamental', 'super_admin'])
def comparar_municipios(current_user):
    """
    Comparar estadísticas entre municipios
    Body: { "municipio_ids": [1, 2, 3] }
    """
    try:
        data = request.get_json()
        municipio_ids = data.get('municipio_ids', [])
        
        if not municipio_ids or len(municipio_ids) < 2:
            return jsonify({'error': 'Se requieren al menos 2 municipios para comparar'}), 400
        
        # Comparar municipios
        comparacion = DepartamentalService.comparar_municipios(municipio_ids)
        
        if not comparacion:
            return jsonify({'error': 'No se pudo realizar la comparación'}), 404
        
        return jsonify(comparacion), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/reporte/validar')
@login_required
@role_required(['coordinador_departamental', 'super_admin'])
def validar_reporte(current_user):
    """Validar si se puede generar el reporte departamental"""
    try:
        # Obtener departamento del coordinador
        if current_user.rol == 'super_admin':
            departamento_id = request.args.get('departamento_id', type=int)
            if not departamento_id:
                return jsonify({'error': 'Se requiere departamento_id para super_admin'}), 400
        else:
            departamento_id = current_user.ubicacion_id
        
        if not departamento_id:
            return jsonify({'error': 'Usuario sin departamento asignado'}), 400
        
        # Validar requisitos
        cumple, errores = ReporteDepartamentalService.validar_requisitos_reporte(departamento_id)
        
        return jsonify({
            'puede_generar': cumple,
            'errores': errores
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/reporte/generar', methods=['POST'])
@login_required
@role_required(['coordinador_departamental', 'super_admin'])
def generar_reporte(current_user):
    """
    Generar reporte departamental
    Body: { "tipo_eleccion_id": 1 }
    """
    try:
        data = request.get_json()
        tipo_eleccion_id = data.get('tipo_eleccion_id')
        
        if not tipo_eleccion_id:
            return jsonify({'error': 'Se requiere tipo_eleccion_id'}), 400
        
        # Obtener departamento del coordinador
        if current_user.rol == 'super_admin':
            departamento_id = data.get('departamento_id')
            if not departamento_id:
                return jsonify({'error': 'Se requiere departamento_id para super_admin'}), 400
        else:
            departamento_id = current_user.ubicacion_id
        
        if not departamento_id:
            return jsonify({'error': 'Usuario sin departamento asignado'}), 400
        
        # Generar reporte
        reporte = ReporteDepartamentalService.generar_reporte_departamental(
            departamento_id,
            tipo_eleccion_id,
            current_user.id
        )
        
        return jsonify({
            'mensaje': 'Reporte generado exitosamente',
            'reporte': {
                'id': reporte.id,
                'version': reporte.version,
                'pdf_url': reporte.pdf_url,
                'created_at': reporte.created_at.isoformat()
            }
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/reportes')
@login_required
@role_required(['coordinador_departamental', 'super_admin'])
def listar_reportes(current_user):
    """Listar reportes generados del departamento"""
    try:
        # Obtener departamento del coordinador
        if current_user.rol == 'super_admin':
            departamento_id = request.args.get('departamento_id', type=int)
            if not departamento_id:
                return jsonify({'error': 'Se requiere departamento_id para super_admin'}), 400
        else:
            departamento_id = current_user.ubicacion_id
        
        if not departamento_id:
            return jsonify({'error': 'Usuario sin departamento asignado'}), 400
        
        # Obtener reportes
        from backend.models.coordinador_departamental import ReporteDepartamental
        reportes = ReporteDepartamental.query.filter_by(
            departamento_id=departamento_id
        ).order_by(ReporteDepartamental.created_at.desc()).all()
        
        reportes_data = []
        for reporte in reportes:
            coordinador = User.query.get(reporte.coordinador_id)
            reportes_data.append({
                'id': reporte.id,
                'version': reporte.version,
                'total_municipios': reporte.total_municipios,
                'municipios_incluidos': reporte.municipios_incluidos,
                'total_votos': reporte.total_votos,
                'pdf_url': reporte.pdf_url,
                'coordinador_nombre': coordinador.nombre if coordinador else 'Desconocido',
                'created_at': reporte.created_at.isoformat()
            })
        
        return jsonify({'reportes': reportes_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
