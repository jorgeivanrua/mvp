"""
Rutas para el coordinador municipal
"""
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.services.municipal_service import MunicipalService
from backend.services.discrepancia_service import DiscrepanciaService
from backend.services.e24_service import E24Service
from backend.services.consolidado_service import ConsolidadoService
from backend.models.coordinador_municipal import Notificacion, AuditLog
from backend.database import db
from backend.utils.exceptions import BaseAPIException, ValidationException, NotFoundException
from backend.utils.decorators import role_required
import csv
import io
from datetime import datetime

coordinador_municipal_bp = Blueprint('coordinador_municipal', __name__, url_prefix='/api/coordinador-municipal')


@coordinador_municipal_bp.route('/puestos', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_puestos():
    """
    Obtener lista de puestos del municipio con estadísticas
    
    Query params:
        estado: Filtrar por estado (completo, incompleto, con_discrepancias)
        zona: Filtrar por zona
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        # Obtener filtros
        filtros = {}
        if request.args.get('estado'):
            filtros['estado'] = request.args.get('estado')
        if request.args.get('zona'):
            filtros['zona'] = request.args.get('zona')
        
        # Obtener puestos
        resultado = MunicipalService.obtener_puestos_municipio(ubicacion.id, filtros)
        
        if not resultado:
            raise NotFoundException('No se pudieron obtener los puestos del municipio')
        
        # Registrar en audit log
        audit_log = AuditLog(
            user_id=int(user_id),
            accion='visualizar_puestos',
            recurso='municipio',
            recurso_id=ubicacion.id,
            detalles={'filtros': filtros},
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': resultado
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/consolidado', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_consolidado():
    """
    Obtener consolidado municipal
    
    Query params:
        tipo_eleccion_id: ID del tipo de elección (opcional)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        tipo_eleccion_id = request.args.get('tipo_eleccion_id', type=int)
        
        # Calcular consolidado
        consolidado = ConsolidadoService.calcular_consolidado_municipal(
            ubicacion.id,
            tipo_eleccion_id=tipo_eleccion_id
        )
        
        if not consolidado:
            raise NotFoundException('No se pudo calcular el consolidado municipal')
        
        return jsonify({
            'success': True,
            'data': consolidado
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/puesto/<int:puesto_id>', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_puesto_detallado(puesto_id):
    """
    Obtener detalles completos de un puesto
    
    Path params:
        puesto_id: ID del puesto
    """
    try:
        user_id = get_jwt_identity()
        
        # Obtener detalles del puesto
        puesto_detallado = MunicipalService.obtener_puesto_detallado(puesto_id, int(user_id))
        
        if not puesto_detallado:
            raise NotFoundException('Puesto no encontrado o sin permisos para acceder')
        
        # Registrar en audit log
        audit_log = AuditLog(
            user_id=int(user_id),
            accion='visualizar_puesto_detallado',
            recurso='puesto',
            recurso_id=puesto_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': puesto_detallado
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/discrepancias', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_discrepancias():
    """
    Obtener puestos con discrepancias o anomalías
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        # Detectar discrepancias
        discrepancias = DiscrepanciaService.detectar_discrepancias_municipio(ubicacion.id)
        
        return jsonify({
            'success': True,
            'data': discrepancias
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@coordinador_municipal_bp.route('/e24-municipal', methods=['POST'])
@jwt_required()
@role_required(['coordinador_municipal'])
def generar_e24_municipal():
    """
    Generar formulario E-24 Municipal
    
    Body:
        tipo_eleccion_id: ID del tipo de elección
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        data = request.get_json()
        if not data or 'tipo_eleccion_id' not in data:
            raise ValidationException('El tipo_eleccion_id es obligatorio')
        
        tipo_eleccion_id = data['tipo_eleccion_id']
        
        # Generar E-24
        e24_municipal = E24Service.generar_e24_municipal(
            ubicacion.id,
            tipo_eleccion_id,
            int(user_id)
        )
        
        # Registrar en audit log
        audit_log = AuditLog(
            user_id=int(user_id),
            accion='generar_e24_municipal',
            recurso='e24_municipal',
            recurso_id=e24_municipal.id,
            detalles={'tipo_eleccion_id': tipo_eleccion_id},
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Formulario E-24 Municipal generado exitosamente',
            'data': e24_municipal.to_dict(include_votos=True)
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/comparacion', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def comparar_puestos():
    """
    Comparar múltiples puestos
    
    Query params:
        puesto_ids: IDs de puestos separados por coma (ej: 1,2,3)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        # Obtener IDs de puestos
        puesto_ids_str = request.args.get('puesto_ids', '')
        if not puesto_ids_str:
            raise ValidationException('Se requiere al menos 2 puestos para comparar')
        
        try:
            puesto_ids = [int(pid) for pid in puesto_ids_str.split(',')]
        except ValueError:
            raise ValidationException('IDs de puestos inválidos')
        
        if len(puesto_ids) < 2:
            raise ValidationException('Se requiere al menos 2 puestos para comparar')
        
        if len(puesto_ids) > 5:
            raise ValidationException('Máximo 5 puestos para comparar')
        
        # Comparar puestos
        comparacion = MunicipalService.comparar_puestos(puesto_ids)
        
        if not comparacion:
            raise NotFoundException('No se pudieron comparar los puestos')
        
        return jsonify({
            'success': True,
            'data': comparacion
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/estadisticas', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_estadisticas():
    """
    Obtener estadísticas detalladas del municipio
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        # Obtener puestos y consolidado
        resultado_puestos = MunicipalService.obtener_puestos_municipio(ubicacion.id)
        consolidado = ConsolidadoService.calcular_consolidado_municipal(ubicacion.id)
        
        if not resultado_puestos or not consolidado:
            raise NotFoundException('No se pudieron obtener las estadísticas')
        
        # Calcular estadísticas adicionales
        puestos = resultado_puestos.get('puestos', [])
        
        # Tiempo promedio de validación (simulado por ahora)
        tiempo_promedio_validacion = 0
        
        # Tasa de rechazo por puesto
        tasa_rechazo_por_puesto = []
        for puesto in puestos:
            stats = MunicipalService.calcular_estadisticas_puesto(puesto['id'])
            if stats:
                formularios = stats.get('formularios', {})
                total = formularios.get('total', 0)
                rechazados = formularios.get('rechazados', 0)
                tasa = (rechazados / total * 100) if total > 0 else 0
                
                tasa_rechazo_por_puesto.append({
                    'puesto_id': puesto['id'],
                    'puesto_nombre': puesto['nombre'],
                    'tasa_rechazo': round(tasa, 2)
                })
        
        estadisticas = {
            'resumen_general': resultado_puestos.get('estadisticas', {}),
            'consolidado': consolidado.get('resumen', {}),
            'tiempo_promedio_validacion': tiempo_promedio_validacion,
            'tasa_rechazo_por_puesto': tasa_rechazo_por_puesto
        }
        
        return jsonify({
            'success': True,
            'data': estadisticas
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/notificar', methods=['POST'])
@jwt_required()
@role_required(['coordinador_municipal'])
def enviar_notificacion():
    """
    Enviar notificación a coordinadores de puesto
    
    Body:
        puesto_ids: Lista de IDs de puestos
        mensaje: Mensaje a enviar
        prioridad: Prioridad (baja, normal, alta, urgente)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        data = request.get_json()
        if not data:
            raise ValidationException('No se proporcionaron datos')
        
        puesto_ids = data.get('puesto_ids', [])
        mensaje = data.get('mensaje', '').strip()
        prioridad = data.get('prioridad', 'normal')
        
        if not mensaje:
            raise ValidationException('El mensaje es obligatorio')
        
        if not puesto_ids:
            raise ValidationException('Debe seleccionar al menos un puesto')
        
        if prioridad not in ['baja', 'normal', 'alta', 'urgente']:
            prioridad = 'normal'
        
        # Obtener coordinadores de los puestos
        coordinadores = User.query.filter(
            User.ubicacion_id.in_(puesto_ids),
            User.rol == 'coordinador_puesto'
        ).all()
        
        if not coordinadores:
            raise NotFoundException('No se encontraron coordinadores para los puestos seleccionados')
        
        # Crear notificaciones
        notificaciones_creadas = []
        for coordinador in coordinadores:
            notificacion = Notificacion(
                remitente_id=int(user_id),
                destinatario_id=coordinador.id,
                mensaje=mensaje,
                prioridad=prioridad
            )
            db.session.add(notificacion)
            notificaciones_creadas.append(coordinador.nombre)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Notificación enviada a {len(notificaciones_creadas)} coordinador(es)',
            'data': {
                'destinatarios': notificaciones_creadas
            }
        }), 201
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/exportar', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def exportar_datos():
    """
    Exportar datos consolidados
    
    Query params:
        formato: Formato de exportación (csv, xlsx)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        formato = request.args.get('formato', 'csv').lower()
        
        if formato not in ['csv', 'xlsx']:
            raise ValidationException('Formato no soportado. Use csv o xlsx')
        
        # Obtener consolidado
        consolidado = ConsolidadoService.calcular_consolidado_municipal(ubicacion.id)
        
        if not consolidado:
            raise NotFoundException('No hay datos para exportar')
        
        # Generar CSV
        if formato == 'csv':
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Encabezados
            writer.writerow(['Municipio', ubicacion.municipio_nombre or ubicacion.nombre_completo])
            writer.writerow(['Código', ubicacion.municipio_codigo])
            writer.writerow(['Fecha de Generación', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow(['Coordinador', user.nombre])
            writer.writerow([])
            
            # Resumen
            resumen = consolidado.get('resumen', {})
            writer.writerow(['RESUMEN DE VOTACIÓN'])
            writer.writerow(['Total Votantes Registrados', resumen.get('total_votantes_registrados', 0)])
            writer.writerow(['Total Votos', resumen.get('total_votos', 0)])
            writer.writerow(['Votos Válidos', resumen.get('votos_validos', 0)])
            writer.writerow(['Votos Nulos', resumen.get('votos_nulos', 0)])
            writer.writerow(['Votos en Blanco', resumen.get('votos_blanco', 0)])
            writer.writerow(['Participación %', resumen.get('participacion_porcentaje', 0)])
            writer.writerow([])
            
            # Votos por partido
            writer.writerow(['VOTOS POR PARTIDO'])
            writer.writerow(['Partido', 'Votos', 'Porcentaje'])
            
            votos_por_partido = consolidado.get('votos_por_partido', [])
            for vp in votos_por_partido:
                writer.writerow([
                    vp['partido_nombre'],
                    vp['total_votos'],
                    f"{vp['porcentaje']:.2f}%"
                ])
            
            # Registrar en audit log
            audit_log = AuditLog(
                user_id=int(user_id),
                accion='exportar_datos',
                recurso='municipio',
                recurso_id=ubicacion.id,
                detalles={'formato': formato},
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            db.session.add(audit_log)
            db.session.commit()
            
            # Preparar respuesta
            output.seek(0)
            filename = f'consolidado_municipal_{ubicacion.municipio_codigo}_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.csv'
            
            return output.getvalue(), 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': f'attachment; filename={filename}'
            }
        
        else:
            # XLSX no implementado por ahora
            raise ValidationException('Formato XLSX no implementado aún')
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@coordinador_municipal_bp.route('/e24-puestos', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_e24_puestos():
    """
    Obtener lista de E-24s de Puesto del municipio
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        # Obtener todos los puestos del municipio
        puestos = Location.query.filter_by(
            municipio_codigo=ubicacion.municipio_codigo,
            tipo='puesto'
        ).all()
        
        puesto_ids = [p.id for p in puestos]
        
        # Obtener E-24s de estos puestos
        from backend.models.coordinador_municipal import FormularioE24Puesto
        
        e24_puestos = FormularioE24Puesto.query.filter(
            FormularioE24Puesto.puesto_id.in_(puesto_ids)
        ).order_by(FormularioE24Puesto.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [e24.to_dict(include_votos=True) for e24 in e24_puestos]
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@coordinador_municipal_bp.route('/consolidado-por-zona', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_consolidado_por_zona():
    """
    Obtener consolidado municipal agrupado por zona
    
    Query params:
        tipo_eleccion_id: ID del tipo de elección (opcional)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        tipo_eleccion_id = request.args.get('tipo_eleccion_id', type=int)
        
        # Obtener todas las zonas del municipio
        zonas = db.session.query(Location.zona_codigo, Location.zona_nombre).filter(
            Location.municipio_codigo == ubicacion.municipio_codigo,
            Location.tipo == 'puesto',
            Location.zona_codigo.isnot(None)
        ).distinct().all()
        
        consolidados_por_zona = []
        
        for zona_codigo, zona_nombre in zonas:
            # Obtener puestos de esta zona
            puestos_zona = Location.query.filter_by(
                municipio_codigo=ubicacion.municipio_codigo,
                zona_codigo=zona_codigo,
                tipo='puesto'
            ).all()
            
            # Calcular consolidado de la zona
            total_votos_zona = 0
            votos_por_partido_zona = {}
            total_puestos = len(puestos_zona)
            puestos_completos = 0
            
            for puesto in puestos_zona:
                consolidado_puesto = ConsolidadoService.calcular_consolidado_puesto(puesto.id, tipo_eleccion_id)
                
                if consolidado_puesto:
                    resumen = consolidado_puesto.get('resumen', {})
                    total_votos_zona += resumen.get('total_votos', 0)
                    
                    # Sumar votos por partido
                    for vp in consolidado_puesto.get('votos_por_partido', []):
                        partido_id = vp['partido_id']
                        if partido_id not in votos_por_partido_zona:
                            votos_por_partido_zona[partido_id] = {
                                'partido_id': partido_id,
                                'partido_nombre': vp['partido_nombre'],
                                'partido_nombre_corto': vp['partido_nombre_corto'],
                                'partido_color': vp['partido_color'],
                                'total_votos': 0
                            }
                        votos_por_partido_zona[partido_id]['total_votos'] += vp['total_votos']
                    
                    # Verificar si el puesto está completo
                    if consolidado_puesto.get('puesto', {}).get('mesas_validadas', 0) == consolidado_puesto.get('puesto', {}).get('total_mesas', 0):
                        puestos_completos += 1
            
            # Calcular porcentajes
            votos_por_partido_lista = list(votos_por_partido_zona.values())
            for vp in votos_por_partido_lista:
                vp['porcentaje'] = (vp['total_votos'] / total_votos_zona * 100) if total_votos_zona > 0 else 0
            
            # Ordenar por votos
            votos_por_partido_lista.sort(key=lambda x: x['total_votos'], reverse=True)
            
            consolidados_por_zona.append({
                'zona_codigo': zona_codigo,
                'zona_nombre': zona_nombre or f'Zona {zona_codigo}',
                'total_puestos': total_puestos,
                'puestos_completos': puestos_completos,
                'porcentaje_avance': (puestos_completos / total_puestos * 100) if total_puestos > 0 else 0,
                'total_votos': total_votos_zona,
                'votos_por_partido': votos_por_partido_lista
            })
        
        # Ordenar por zona_codigo
        consolidados_por_zona.sort(key=lambda x: x['zona_codigo'])
        
        return jsonify({
            'success': True,
            'data': consolidados_por_zona
        }), 200
        
    except BaseAPIException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
