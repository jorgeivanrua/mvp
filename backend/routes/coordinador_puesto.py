"""
Rutas para Coordinador de Puesto
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14
from backend.database import db

coordinador_puesto_bp = Blueprint('coordinador_puesto', __name__)


@coordinador_puesto_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Estadísticas del puesto"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        # Obtener mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo,
            activo=True
        ).all()
        
        # Obtener testigos del puesto
        testigos = User.query.filter_by(
            ubicacion_id=puesto.id,
            rol='testigo_electoral',
            activo=True
        ).all()
        
        # Obtener formularios del puesto
        mesa_ids = [m.id for m in mesas]
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        formularios_completados = sum(1 for f in formularios if f.estado == 'completado')
        
        stats = {
            'total_mesas': len(mesas),
            'total_testigos': len(testigos),
            'testigos_presentes': sum(1 for t in testigos if t.presencia_verificada),
            'total_formularios': len(formularios),
            'formularios_completados': formularios_completados,
            'formularios_pendientes': len(formularios) - formularios_completados,
            'porcentaje_avance': (formularios_completados / len(formularios) * 100) if formularios else 0,
            'puesto': {
                'id': puesto.id,
                'nombre': puesto.nombre_completo,
                'codigo': puesto.puesto_codigo
            }
        }
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/mesas', methods=['GET'])
@jwt_required()
def get_mesas():
    """Obtener mesas del puesto"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo,
            activo=True
        ).all()
        
        mesas_data = []
        for mesa in mesas:
            # Buscar formulario de la mesa
            formulario = FormularioE14.query.filter_by(mesa_id=mesa.id).first()
            
            mesas_data.append({
                'id': mesa.id,
                'nombre_completo': mesa.nombre_completo,
                'mesa_codigo': mesa.mesa_codigo,
                'total_votantes_registrados': mesa.total_votantes_registrados,
                'mujeres': mesa.mujeres,
                'hombres': mesa.hombres,
                'tiene_formulario': formulario is not None,
                'estado_formulario': formulario.estado if formulario else None
            })
        
        return jsonify({
            'success': True,
            'data': mesas_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/testigos', methods=['GET'])
@jwt_required()
def get_testigos():
    """Obtener testigos del puesto"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        testigos = User.query.filter_by(
            ubicacion_id=user.ubicacion_id,
            rol='testigo_electoral',
            activo=True
        ).all()
        
        testigos_data = []
        for testigo in testigos:
            testigos_data.append({
                'id': testigo.id,
                'nombre': testigo.nombre,
                'presencia_verificada': testigo.presencia_verificada,
                'presencia_verificada_at': testigo.presencia_verificada_at.isoformat() if testigo.presencia_verificada_at else None,
                'ultimo_acceso': testigo.ultimo_acceso.isoformat() if testigo.ultimo_acceso else None
            })
        
        return jsonify({
            'success': True,
            'data': testigos_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/incidentes', methods=['GET'])
@jwt_required()
def get_incidentes():
    """Obtener incidentes del puesto con evidencias fotográficas"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        # Importar modelos de incidentes y delitos
        from backend.models.incidentes_delitos import IncidenteElectoral, EvidenciaFotografica
        
        # Obtener incidentes del puesto
        incidentes = IncidenteElectoral.query.join(
            Location, IncidenteElectoral.mesa_id == Location.id
        ).filter(
            Location.puesto_codigo == puesto.puesto_codigo,
            Location.municipio_codigo == puesto.municipio_codigo,
            Location.departamento_codigo == puesto.departamento_codigo
        ).order_by(IncidenteElectoral.fecha_reporte.desc()).all()
        
        incidentes_data = []
        for inc in incidentes:
            # Obtener evidencias fotográficas
            evidencias = EvidenciaFotografica.query.filter_by(
                incidente_id=inc.id
            ).all()
            
            mesa = Location.query.get(inc.mesa_id)
            reportado_por = User.query.get(inc.reportado_por_id)
            
            incidentes_data.append({
                'id': inc.id,
                'titulo': inc.titulo,
                'descripcion': inc.descripcion,
                'tipo_incidente': inc.tipo_incidente,
                'tipo_incidente_label': inc.get_tipo_incidente_label(),
                'severidad': inc.severidad,
                'severidad_label': inc.get_severidad_label(),
                'estado': inc.estado,
                'estado_label': inc.get_estado_label(),
                'fecha_reporte': inc.fecha_reporte.isoformat() if inc.fecha_reporte else None,
                'ubicacion_gps': inc.ubicacion_gps,
                'notas_resolucion': inc.notas_resolucion,
                'mesa_id': inc.mesa_id,
                'mesa_codigo': mesa.mesa_codigo if mesa else None,
                'reportado_por_id': inc.reportado_por_id,
                'reportado_por_nombre': reportado_por.nombre if reportado_por else 'Desconocido',
                'evidencias': [{
                    'id': ev.id,
                    'filename': ev.filename,
                    'url': ev.url,
                    'tipo': ev.tipo,
                    'descripcion': ev.descripcion
                } for ev in evidencias]
            })
        
        return jsonify({
            'success': True,
            'data': incidentes_data,
            'total': len(incidentes_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/delitos', methods=['GET'])
@jwt_required()
def get_delitos():
    """Obtener delitos del puesto con evidencias fotográficas"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        # Importar modelos de delitos
        from backend.models.incidentes_delitos import DelitoElectoral, EvidenciaFotografica
        
        # Obtener delitos del puesto
        delitos = DelitoElectoral.query.join(
            Location, DelitoElectoral.mesa_id == Location.id
        ).filter(
            Location.puesto_codigo == puesto.puesto_codigo,
            Location.municipio_codigo == puesto.municipio_codigo,
            Location.departamento_codigo == puesto.departamento_codigo
        ).order_by(DelitoElectoral.fecha_reporte.desc()).all()
        
        delitos_data = []
        for delito in delitos:
            # Obtener evidencias fotográficas
            evidencias = EvidenciaFotografica.query.filter_by(
                delito_id=delito.id
            ).all()
            
            mesa = Location.query.get(delito.mesa_id)
            reportado_por = User.query.get(delito.reportado_por_id)
            
            delitos_data.append({
                'id': delito.id,
                'titulo': delito.titulo,
                'descripcion': delito.descripcion,
                'tipo_delito': delito.tipo_delito,
                'tipo_delito_label': delito.get_tipo_delito_label(),
                'gravedad': delito.gravedad,
                'gravedad_label': delito.get_gravedad_label(),
                'estado': delito.estado,
                'estado_label': delito.get_estado_label(),
                'fecha_reporte': delito.fecha_reporte.isoformat() if delito.fecha_reporte else None,
                'ubicacion_gps': delito.ubicacion_gps,
                'testigos_adicionales': delito.testigos_adicionales,
                'denunciado_formalmente': delito.denunciado_formalmente,
                'numero_denuncia': delito.numero_denuncia,
                'resultado_investigacion': delito.resultado_investigacion,
                'mesa_id': delito.mesa_id,
                'mesa_codigo': mesa.mesa_codigo if mesa else None,
                'reportado_por_id': delito.reportado_por_id,
                'reportado_por_nombre': reportado_por.nombre if reportado_por else 'Desconocido',
                'evidencias': [{
                    'id': ev.id,
                    'filename': ev.filename,
                    'url': ev.url,
                    'tipo': ev.tipo,
                    'descripcion': ev.descripcion
                } for ev in evidencias]
            })
        
        return jsonify({
            'success': True,
            'data': delitos_data,
            'total': len(delitos_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/formularios', methods=['GET'])
@jwt_required()
def get_formularios():
    """Obtener formularios del puesto"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        # Obtener mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo,
            activo=True
        ).all()
        
        mesa_ids = [m.id for m in mesas]
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids)
        ).all() if mesa_ids else []
        
        formularios_data = []
        for formulario in formularios:
            mesa = Location.query.get(formulario.mesa_id)
            testigo = User.query.get(formulario.testigo_id)
            
            # Obtener tipo de elección
            tipo_eleccion = None
            if formulario.tipo_eleccion_id:
                from backend.models.configuracion_electoral import TipoEleccion
                tipo_eleccion = TipoEleccion.query.get(formulario.tipo_eleccion_id)
            
            formularios_data.append({
                'id': formulario.id,
                'mesa_id': formulario.mesa_id,
                'mesa_codigo': mesa.mesa_codigo if mesa else None,
                'mesa_nombre': mesa.mesa_nombre if mesa else None,
                'testigo_id': formulario.testigo_id,
                'testigo_nombre': testigo.nombre if testigo else None,
                'tipo_eleccion_id': formulario.tipo_eleccion_id,
                'tipo_eleccion_nombre': tipo_eleccion.nombre if tipo_eleccion else None,
                'total_votos': formulario.total_votos or 0,
                'estado': formulario.estado,
                'created_at': formulario.created_at.isoformat() if formulario.created_at else None,
                'updated_at': formulario.updated_at.isoformat() if formulario.updated_at else None
            })
        
        # Calcular estadísticas
        total_formularios = len(formularios)
        pendientes = len([f for f in formularios if f.estado == 'pendiente'])
        validados = len([f for f in formularios if f.estado == 'validado'])
        rechazados = len([f for f in formularios if f.estado == 'rechazado'])
        
        # Mesas con formularios reportados
        mesas_reportadas = len(set(f.mesa_id for f in formularios))
        total_mesas = len(mesas)
        
        estadisticas = {
            'total': total_formularios,
            'pendientes': pendientes,
            'validados': validados,
            'rechazados': rechazados,
            'mesas_reportadas': mesas_reportadas,
            'total_mesas': total_mesas
        }
        
        return jsonify({
            'success': True,
            'data': {
                'formularios': formularios_data,
                'estadisticas': estadisticas
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/formularios/<int:formulario_id>', methods=['GET'])
@jwt_required()
def get_formulario(formulario_id):
    """Obtener un formulario específico"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        formulario = FormularioE14.query.get(formulario_id)
        if not formulario:
            return jsonify({
                'success': False,
                'error': 'Formulario no encontrado'
            }), 404
        
        # Verificar que el formulario pertenece al puesto del coordinador
        mesa = Location.query.get(formulario.mesa_id)
        puesto = Location.query.get(user.ubicacion_id)
        
        if not mesa or not puesto or mesa.puesto_codigo != puesto.puesto_codigo:
            return jsonify({
                'success': False,
                'error': 'No tiene permisos para ver este formulario'
            }), 403
        
        testigo = User.query.get(formulario.testigo_id)
        
        # ⭐ MEJORADO: Obtener votos por partido y candidatos
        from backend.models.formulario_e14 import VotoPartido, VotoCandidato
        from backend.models.partido_politico import PartidoPolitico as Partido
        from backend.models.candidato import Candidato
        
        # Votos por partido
        votos_partidos = []
        votos_partido_records = VotoPartido.query.filter_by(formulario_id=formulario.id).all()
        
        for vp in votos_partido_records:
            partido = Partido.query.get(vp.partido_id)
            votos_partidos.append({
                'partido_id': vp.partido_id,
                'partido_nombre': partido.nombre if partido else 'Desconocido',
                'partido_sigla': partido.sigla if partido else 'N/A',
                'partido_color': partido.color if partido else '#6c757d',
                'votos': vp.votos
            })
        
        # ⭐ NUEVO: Votos por candidatos
        votos_candidatos = []
        votos_candidato_records = VotoCandidato.query.filter_by(formulario_id=formulario.id).all()
        
        for vc in votos_candidato_records:
            candidato = Candidato.query.get(vc.candidato_id)
            if candidato:
                partido = Partido.query.get(candidato.partido_id)
                votos_candidatos.append({
                    'candidato_id': vc.candidato_id,
                    'candidato_nombre': candidato.nombre_completo,
                    'candidato_numero': candidato.numero_lista,
                    'partido_id': candidato.partido_id,
                    'partido_nombre': partido.nombre if partido else 'Desconocido',
                    'partido_sigla': partido.sigla if partido else 'N/A',
                    'partido_color': partido.color if partido else '#6c757d',
                    'votos': vc.votos
                })
        
        formulario_data = {
            'id': formulario.id,
            'mesa_id': formulario.mesa_id,
            'mesa': {
                'codigo': mesa.mesa_codigo,
                'nombre': mesa.mesa_nombre or mesa.nombre_completo
            },
            'testigo': {
                'id': testigo.id,
                'nombre': testigo.nombre,
                'cedula': testigo.cedula
            } if testigo else None,
            'tipo_eleccion_id': formulario.tipo_eleccion_id,
            'total_votantes_registrados': formulario.total_votantes_registrados,
            'total_votos': formulario.total_votos,
            'votos_validos': formulario.votos_validos,
            'votos_nulos': formulario.votos_nulos,
            'votos_blanco': formulario.votos_blanco,
            'tarjetas_no_marcadas': formulario.tarjetas_no_marcadas,
            'total_tarjetas': formulario.total_tarjetas,
            'estado': formulario.estado,
            'imagen_url': formulario.imagen_url,
            'observaciones': formulario.observaciones,
            'votos_partidos': votos_partidos,  # ⭐ Votos por partido
            'votos_candidatos': votos_candidatos,  # ⭐ NUEVO: Votos por candidatos
            'created_at': formulario.created_at.isoformat() if formulario.created_at else None,
            'updated_at': formulario.updated_at.isoformat() if formulario.updated_at else None
        }
        
        return jsonify({
            'success': True,
            'data': formulario_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/formularios/<int:formulario_id>/validar', methods=['PUT'])
@jwt_required()
def validar_formulario(formulario_id):
    """Validar un formulario"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        formulario = FormularioE14.query.get(formulario_id)
        if not formulario:
            return jsonify({
                'success': False,
                'error': 'Formulario no encontrado'
            }), 404
        
        if formulario.estado != 'pendiente':
            return jsonify({
                'success': False,
                'error': 'Solo se pueden validar formularios pendientes'
            }), 400
        
        # Verificar que el formulario pertenece al puesto del coordinador
        mesa = Location.query.get(formulario.mesa_id)
        puesto = Location.query.get(user.ubicacion_id)
        
        if not mesa or not puesto or mesa.puesto_codigo != puesto.puesto_codigo:
            return jsonify({
                'success': False,
                'error': 'No tiene permisos para validar este formulario'
            }), 403
        
        data = request.get_json()
        
        # Actualizar formulario
        formulario.estado = 'validado'
        formulario.validado_por_id = user.id
        formulario.validado_at = db.func.now()
        
        if data and 'comentario' in data:
            formulario.observaciones = data['comentario']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Formulario validado exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/formularios/<int:formulario_id>/rechazar', methods=['PUT'])
@jwt_required()
def rechazar_formulario(formulario_id):
    """Rechazar un formulario"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        formulario = FormularioE14.query.get(formulario_id)
        if not formulario:
            return jsonify({
                'success': False,
                'error': 'Formulario no encontrado'
            }), 404
        
        if formulario.estado != 'pendiente':
            return jsonify({
                'success': False,
                'error': 'Solo se pueden rechazar formularios pendientes'
            }), 400
        
        # Verificar que el formulario pertenece al puesto del coordinador
        mesa = Location.query.get(formulario.mesa_id)
        puesto = Location.query.get(user.ubicacion_id)
        
        if not mesa or not puesto or mesa.puesto_codigo != puesto.puesto_codigo:
            return jsonify({
                'success': False,
                'error': 'No tiene permisos para rechazar este formulario'
            }), 403
        
        data = request.get_json()
        
        if not data or 'motivo' not in data:
            return jsonify({
                'success': False,
                'error': 'Se requiere un motivo de rechazo'
            }), 400
        
        # Actualizar formulario
        formulario.estado = 'rechazado'
        formulario.motivo_rechazo = data['motivo']
        formulario.validado_por_id = user.id
        formulario.validado_at = db.func.now()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Formulario rechazado exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/consolidado', methods=['GET'])
@jwt_required()
def get_consolidado():
    """Obtener consolidado del puesto"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        # Obtener mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo,
            activo=True
        ).all()
        
        mesa_ids = [m.id for m in mesas]
        
        # Obtener formularios validados
        formularios = FormularioE14.query.filter(
            FormularioE14.mesa_id.in_(mesa_ids),
            FormularioE14.estado == 'validado'
        ).all() if mesa_ids else []
        
        # Calcular consolidado
        from backend.models.formulario_e14 import VotoPartido
        from backend.models.partido_politico import PartidoPolitico as Partido
        
        votos_por_partido = {}
        total_votos = 0
        total_votantes_registrados = sum(m.total_votantes_registrados or 0 for m in mesas)
        
        for formulario in formularios:
            total_votos += formulario.total_votos or 0
            
            # Sumar votos por partido
            votos_partido = VotoPartido.query.filter_by(formulario_id=formulario.id).all()
            for vp in votos_partido:
                if vp.partido_id not in votos_por_partido:
                    partido = Partido.query.get(vp.partido_id)
                    votos_por_partido[vp.partido_id] = {
                        'partido_id': vp.partido_id,
                        'partido_nombre': partido.nombre if partido else 'Desconocido',
                        'partido_nombre_corto': partido.sigla if partido else 'N/A',
                        'partido_color': partido.color if partido else '#6c757d',
                        'total_votos': 0,
                        'porcentaje': 0
                    }
                votos_por_partido[vp.partido_id]['total_votos'] += vp.votos or 0
        
        # Calcular porcentajes
        for partido_data in votos_por_partido.values():
            if total_votos > 0:
                partido_data['porcentaje'] = (partido_data['total_votos'] / total_votos) * 100
        
        # Ordenar por votos
        votos_por_partido_list = sorted(votos_por_partido.values(), key=lambda x: x['total_votos'], reverse=True)
        
        participacion_porcentaje = (total_votos / total_votantes_registrados * 100) if total_votantes_registrados > 0 else 0
        
        consolidado = {
            'resumen': {
                'total_votos': total_votos,
                'total_votantes_registrados': total_votantes_registrados,
                'participacion_porcentaje': participacion_porcentaje,
                'total_formularios': len(formularios),
                'total_mesas': len(mesas)
            },
            'votos_por_partido': votos_por_partido_list
        }
        
        return jsonify({
            'success': True,
            'data': consolidado
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/mesas-detalle', methods=['GET'])
@jwt_required()
def get_mesas_detalle():
    """Obtener mesas del puesto con detalles completos"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        # Obtener mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo,
            activo=True
        ).all()
        
        mesas_data = []
        for mesa in mesas:
            # Buscar formulario de la mesa
            formulario = FormularioE14.query.filter_by(mesa_id=mesa.id).first()
            
            # Buscar testigo asignado
            testigo = User.query.filter_by(
                ubicacion_id=mesa.id,
                rol='testigo_electoral',
                activo=True
            ).first()
            
            mesas_data.append({
                'id': mesa.id,
                'mesa_codigo': mesa.mesa_codigo,
                'mesa_nombre': mesa.mesa_nombre or mesa.nombre_completo,
                'total_votantes_registrados': mesa.total_votantes_registrados,
                'mujeres': mesa.mujeres,
                'hombres': mesa.hombres,
                'tiene_formulario': formulario is not None,
                'estado_formulario': formulario.estado if formulario else None,
                'total_votos': formulario.total_votos if formulario else 0,
                'votos_validos': formulario.votos_validos if formulario else 0,
                'votos_nulos': formulario.votos_nulos if formulario else 0,
                'votos_blanco': formulario.votos_blanco if formulario else 0,
                'testigo_id': testigo.id if testigo else None,
                'testigo_nombre': testigo.nombre if testigo else None,
                'testigo_presente': testigo.presencia_verificada if testigo else False,
                'testigo_presente_desde': testigo.presencia_verificada_at.isoformat() if testigo and testigo.presencia_verificada_at else None
            })
        
        return jsonify({
            'success': True,
            'data': mesas_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/testigos-puesto', methods=['GET'])
@jwt_required()
def get_testigos_puesto():
    """Obtener testigos del puesto con estado detallado"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        # Obtener mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo,
            activo=True
        ).all()
        
        testigos_data = []
        for mesa in mesas:
            # Buscar testigo asignado a esta mesa
            testigo = User.query.filter_by(
                ubicacion_id=mesa.id,
                rol='testigo_electoral',
                activo=True
            ).first()
            
            if testigo:
                # Buscar formulario del testigo
                formulario = FormularioE14.query.filter_by(
                    mesa_id=mesa.id,
                    testigo_id=testigo.id
                ).first()
                
                testigos_data.append({
                    'id': testigo.id,
                    'nombre': testigo.nombre,
                    'cedula': testigo.cedula,
                    'mesa_id': mesa.id,
                    'mesa_codigo': mesa.mesa_codigo,
                    'mesa_nombre': mesa.mesa_nombre or mesa.nombre_completo,
                    'presencia_verificada': testigo.presencia_verificada,
                    'presencia_verificada_at': testigo.presencia_verificada_at.isoformat() if testigo.presencia_verificada_at else None,
                    'ultimo_acceso': testigo.ultimo_acceso.isoformat() if testigo.ultimo_acceso else None,
                    'tiene_formulario': formulario is not None,
                    'estado_formulario': formulario.estado if formulario else None,
                    'formulario_id': formulario.id if formulario else None
                })
        
        return jsonify({
            'success': True,
            'data': testigos_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_puesto_bp.route('/generar-e24', methods=['POST'])
@jwt_required()
def generar_e24():
    """Generar formulario E-24 consolidado del puesto"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != 'coordinador_puesto':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        if not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        puesto = Location.query.get(user.ubicacion_id)
        
        # Por ahora retornamos un mensaje de que la funcionalidad está en desarrollo
        return jsonify({
            'success': False,
            'error': 'Funcionalidad de generación de E-24 en desarrollo'
        }), 501
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
