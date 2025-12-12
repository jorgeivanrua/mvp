"""
Rutas para servir componentes HTML dinámicamente
"""

from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.formulario_e14 import FormularioE14
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
from backend.models.user import User
from backend.database import db

components_bp = Blueprint('components', __name__)

@components_bp.route('/api/components/formulario-fotos', methods=['POST'])
@jwt_required()
def get_formulario_fotos_component():
    """Obtener el componente HTML para fotos de formularios E-14"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        formulario_id = data.get('formulario_id')
        es_coordinador = data.get('es_coordinador', False)
        es_solo_lectura = data.get('es_solo_lectura', False)
        
        if not formulario_id:
            return jsonify({'error': 'ID de formulario requerido'}), 400
        
        # Verificar que el formulario existe y el usuario tiene acceso
        formulario = FormularioE14.query.get(formulario_id)
        if not formulario:
            return jsonify({'error': 'Formulario no encontrado'}), 404
        
        # Verificar permisos
        if not es_coordinador and formulario.testigo_id != current_user.id:
            return jsonify({'error': 'Sin permisos para acceder a este formulario'}), 403
        
        # Renderizar el componente
        html = render_template('components/formulario-fotos.html',
                             formulario_id=formulario_id,
                             es_coordinador=es_coordinador,
                             es_solo_lectura=es_solo_lectura)
        
        return html, 200, {'Content-Type': 'text/html'}
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@components_bp.route('/api/components/incidentes-delitos-fotos', methods=['POST'])
@jwt_required()
def get_incidentes_delitos_fotos_component():
    """Obtener el componente HTML para evidencias fotográficas de incidentes/delitos"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        tipo_reporte = data.get('tipo_reporte')  # 'incidente' o 'delito'
        reporte_id = data.get('reporte_id')
        es_coordinador = data.get('es_coordinador', False)
        es_solo_lectura = data.get('es_solo_lectura', False)
        
        if not tipo_reporte or not reporte_id:
            return jsonify({'error': 'Tipo de reporte e ID requeridos'}), 400
        
        if tipo_reporte not in ['incidente', 'delito']:
            return jsonify({'error': 'Tipo de reporte inválido'}), 400
        
        # Verificar que el reporte existe y el usuario tiene acceso
        if tipo_reporte == 'incidente':
            reporte = IncidenteElectoral.query.get(reporte_id)
        else:  # delito
            reporte = DelitoElectoral.query.get(reporte_id)
            
        if not reporte:
            return jsonify({'error': 'Reporte no encontrado'}), 404
        
        # Verificar permisos
        if not es_coordinador and reporte.testigo_id != current_user.id:
            return jsonify({'error': 'Sin permisos para acceder a este reporte'}), 403
        
        # Renderizar el componente
        html = render_template('components/incidentes-delitos-fotos.html',
                             tipo_reporte=tipo_reporte,
                             reporte_id=reporte_id,
                             es_coordinador=es_coordinador,
                             es_solo_lectura=es_solo_lectura)
        
        return html, 200, {'Content-Type': 'text/html'}
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500