"""
Servicio para gestión de reportes de participación
"""
from backend.database import db
from backend.models.reporte_participacion import ReporteParticipacion
from backend.models.location import Location
from backend.models.user import User
from backend.utils.exceptions import ValidationException, NotFoundException
from datetime import datetime, time
from sqlalchemy import func, and_


class ReporteParticipacionService:
    """Servicio para operaciones de reportes de participación"""
    
    @staticmethod
    def crear_reporte(data, testigo_id):
        """
        Crear un nuevo reporte de participación
        
        Args:
            data: Diccionario con datos del reporte
            testigo_id: ID del testigo que crea el reporte
            
        Returns:
            ReporteParticipacion: Reporte creado
        """
        # Validar datos requeridos
        required_fields = ['mesa_id', 'hora_reporte', 'personas_votadas']
        
        for field in required_fields:
            if field not in data:
                raise ValidationException({field: [f'El campo {field} es requerido']})
        
        # Validar que la mesa existe
        mesa = Location.query.get(data['mesa_id'])
        if not mesa or mesa.tipo != 'mesa':
            raise ValidationException({'mesa_id': ['Mesa no encontrada']})
        
        # Validar que el testigo tiene acceso a esta mesa
        testigo = User.query.get(testigo_id)
        if not testigo:
            raise ValidationException({'testigo_id': ['Testigo no encontrado']})
        
        # Parsear hora del reporte
        if isinstance(data['hora_reporte'], str):
            try:
                hora_reporte = datetime.fromisoformat(data['hora_reporte'].replace('Z', '+00:00'))
            except ValueError:
                raise ValidationException({'hora_reporte': ['Formato de fecha inválido']})
        else:
            hora_reporte = data['hora_reporte']
        
        # Validar que la hora está en horario de votación (8am - 4pm)
        hora_del_dia = hora_reporte.time()
        if not (time(8, 0) <= hora_del_dia <= time(16, 0)):
            raise ValidationException({
                'hora_reporte': ['La hora del reporte debe estar entre 8:00 AM y 4:00 PM']
            })
        
        # Validar que no sea futura
        if hora_reporte > datetime.utcnow():
            raise ValidationException({
                'hora_reporte': ['La hora del reporte no puede ser futura']
            })
        
        # ⭐ NUEVA VALIDACIÓN: Ventana de tiempo de 30 minutos
        # Los reportes solo se pueden enviar dentro de una ventana de 30 minutos después de la hora
        # Ejemplo: Reporte de 9am solo se puede enviar entre 9:00am y 9:30am
        hora_actual = datetime.utcnow()
        hora_redondeada_objetivo = hora_reporte.replace(minute=0, second=0, microsecond=0)
        
        # Calcular la ventana de tiempo permitida
        inicio_ventana = hora_redondeada_objetivo
        fin_ventana = hora_redondeada_objetivo.replace(minute=30)
        
        # Validar que la hora actual esté dentro de la ventana
        if not (inicio_ventana <= hora_actual <= fin_ventana):
            hora_objetivo_str = hora_redondeada_objetivo.strftime('%I:%M %p')
            inicio_str = inicio_ventana.strftime('%I:%M %p')
            fin_str = fin_ventana.strftime('%I:%M %p')
            
            raise ValidationException({
                'hora_reporte': [
                    f'El reporte de {hora_objetivo_str} solo se puede enviar entre {inicio_str} y {fin_str}. '
                    f'Por favor espere hasta la ventana de tiempo correspondiente.'
                ]
            })
        
        # Validar personas votadas
        personas_votadas = int(data['personas_votadas'])
        if personas_votadas < 0:
            raise ValidationException({
                'personas_votadas': ['El número de personas votadas no puede ser negativo']
            })
        
        votantes_registrados = mesa.total_votantes_registrados or 0
        if votantes_registrados > 0 and personas_votadas > votantes_registrados:
            raise ValidationException({
                'personas_votadas': [
                    f'El número de personas votadas ({personas_votadas}) no puede exceder '
                    f'los votantes registrados ({votantes_registrados})'
                ]
            })
        
        # ⭐ REPORTES INDEPENDIENTES POR HORA
        # Cada reporte es una "fotografía" del flujo en esa hora específica
        # Validar que el número de personas sea razonable para una hora
        if personas_votadas > 500:  # Límite razonable por hora
            raise ValidationException({
                'personas_votadas': [
                    f'El número de personas votadas en una hora ({personas_votadas}) parece muy alto. '
                    f'Verifique que esté reportando solo las personas que votaron en esta hora específica.'
                ]
            })
        
        # Validar que no exceda los votantes registrados de la mesa (por hora)
        if votantes_registrados > 0 and personas_votadas > votantes_registrados:
            raise ValidationException({
                'personas_votadas': [
                    f'El número de personas votadas en una hora ({personas_votadas}) no puede exceder '
                    f'los votantes registrados de la mesa ({votantes_registrados}).'
                ]
            })
        
        # Verificar que no exista ya un reporte para esta hora
        # Redondear a la hora más cercana para evitar duplicados
        hora_redondeada = hora_reporte.replace(minute=0, second=0, microsecond=0)
        reporte_existente = ReporteParticipacion.query.filter_by(
            mesa_id=data['mesa_id'],
            hora_reporte=hora_redondeada
        ).first()
        
        if reporte_existente:
            raise ValidationException({
                'hora_reporte': [
                    f'Ya existe un reporte para esta mesa a las {hora_redondeada.strftime("%H:00")}. '
                    f'Solo se permite un reporte por hora.'
                ]
            })
        
        # Calcular porcentaje de participación para esta hora específica
        # Cada reporte es independiente - muestra el flujo de esa hora
        porcentaje_participacion = 0
        if votantes_registrados > 0:
            porcentaje_participacion = (personas_votadas / votantes_registrados) * 100
        
        # Crear reporte
        reporte = ReporteParticipacion(
            mesa_id=data['mesa_id'],
            testigo_id=testigo_id,
            hora_reporte=hora_redondeada,
            personas_votadas=personas_votadas,
            porcentaje_participacion=porcentaje_participacion,
            observaciones=data.get('observaciones', '')
        )
        
        db.session.add(reporte)
        db.session.commit()
        
        return reporte
    
    @staticmethod
    def obtener_reportes_mesa(mesa_id):
        """
        Obtener todos los reportes de una mesa
        
        Args:
            mesa_id: ID de la mesa
            
        Returns:
            dict: Diccionario con reportes y estadísticas
        """
        mesa = Location.query.get(mesa_id)
        if not mesa or mesa.tipo != 'mesa':
            raise NotFoundException('Mesa no encontrada')
        
        reportes = ReporteParticipacion.query.filter_by(
            mesa_id=mesa_id
        ).order_by(ReporteParticipacion.hora_reporte.asc()).all()
        
        ultimo_reporte = reportes[-1] if reportes else None
        
        return {
            'mesa': {
                'id': mesa.id,
                'codigo': mesa.mesa_codigo,
                'nombre': mesa.mesa_nombre,
                'votantes_registrados': mesa.total_votantes_registrados or 0
            },
            'reportes': [r.to_dict() for r in reportes],
            'ultimo_reporte': ultimo_reporte.to_dict() if ultimo_reporte else None,
            'total_reportes': len(reportes)
        }
    
    @staticmethod
    def obtener_participacion_puesto(puesto_id, hora_especifica=None):
        """
        Obtener participación de todas las mesas de un puesto
        
        Args:
            puesto_id: ID del puesto
            hora_especifica: Hora específica para filtrar reportes (opcional)
            
        Returns:
            dict: Diccionario con participación del puesto
        """
        puesto = Location.query.get(puesto_id)
        if not puesto or puesto.tipo != 'puesto':
            raise NotFoundException('Puesto no encontrado')
        
        # Obtener todas las mesas del puesto
        mesas = Location.query.filter_by(
            puesto_codigo=puesto.puesto_codigo,
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            tipo='mesa',
            activo=True
        ).all()
        
        total_votantes = sum(m.total_votantes_registrados or 0 for m in mesas)
        
        # Obtener reportes por hora o histórico completo
        mesas_data = []
        total_personas_votadas = 0
        mesas_reportadas = 0
        ultima_hora_reporte = None
        
        for mesa in mesas:
            if hora_especifica:
                # Obtener reporte de hora específica
                reporte = ReporteParticipacion.query.filter_by(
                    mesa_id=mesa.id,
                    hora_reporte=hora_especifica
                ).first()
                
                personas_mesa = reporte.personas_votadas if reporte else 0
                ultimo_reporte = reporte
            else:
                # Obtener histórico completo (suma de todos los reportes independientes)
                reportes = ReporteParticipacion.query.filter_by(mesa_id=mesa.id).all()
                personas_mesa = sum(r.personas_votadas for r in reportes)
                
                ultimo_reporte = ReporteParticipacion.query.filter_by(
                    mesa_id=mesa.id
                ).order_by(ReporteParticipacion.hora_reporte.desc()).first()
            
            if ultimo_reporte:
                mesas_reportadas += 1
                total_personas_votadas += personas_mesa
                
                if not ultima_hora_reporte or ultimo_reporte.hora_reporte > ultima_hora_reporte:
                    ultima_hora_reporte = ultimo_reporte.hora_reporte
            
            mesas_data.append({
                'mesa_id': mesa.id,
                'mesa_codigo': mesa.mesa_codigo,
                'votantes_registrados': mesa.total_votantes_registrados or 0,
                'personas_votadas': personas_mesa,
                'ultimo_reporte': ultimo_reporte.to_dict() if ultimo_reporte else None,
                'tendencia': ReporteParticipacionService._calcular_tendencia(mesa.id) if ultimo_reporte else 'sin_datos'
            })
        
        porcentaje_participacion = 0
        if total_votantes > 0:
            porcentaje_participacion = (total_personas_votadas / total_votantes) * 100
        
        return {
            'puesto': {
                'id': puesto.id,
                'nombre': puesto.puesto_nombre,
                'total_mesas': len(mesas),
                'total_votantes': total_votantes
            },
            'resumen': {
                'total_personas_votadas': total_personas_votadas,
                'porcentaje_participacion': round(porcentaje_participacion, 2),
                'mesas_reportadas': mesas_reportadas,
                'ultimo_reporte': ultima_hora_reporte.isoformat() if ultima_hora_reporte else None,
                'hora_especifica': hora_especifica.isoformat() if hora_especifica else None
            },
            'mesas': mesas_data
        }
    
    @staticmethod
    def obtener_flujo_por_hora(puesto_id=None, municipio_id=None, zona_id=None):
        """
        Obtener flujo de votación por hora para análisis de tendencias
        
        Args:
            puesto_id: ID del puesto (opcional)
            municipio_id: ID del municipio (opcional) 
            zona_id: ID de la zona (opcional)
            
        Returns:
            dict: Flujo por hora agregado
        """
        from datetime import datetime, time
        from sqlalchemy import func
        
        # Construir filtros según el nivel
        if puesto_id:
            puesto = Location.query.get(puesto_id)
            if not puesto:
                raise NotFoundException('Puesto no encontrado')
            
            mesas = Location.query.filter_by(
                puesto_codigo=puesto.puesto_codigo,
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                tipo='mesa',
                activo=True
            ).all()
        elif zona_id:
            zona = Location.query.get(zona_id)
            if not zona:
                raise NotFoundException('Zona no encontrada')
            
            mesas = Location.query.filter_by(
                zona_codigo=zona.zona_codigo,
                departamento_codigo=zona.departamento_codigo,
                municipio_codigo=zona.municipio_codigo,
                tipo='mesa',
                activo=True
            ).all()
        elif municipio_id:
            municipio = Location.query.get(municipio_id)
            if not municipio:
                raise NotFoundException('Municipio no encontrado')
            
            mesas = Location.query.filter_by(
                municipio_codigo=municipio.municipio_codigo,
                departamento_codigo=municipio.departamento_codigo,
                tipo='mesa',
                activo=True
            ).all()
        else:
            raise ValidationException({'filtro': ['Debe especificar puesto_id, zona_id o municipio_id']})
        
        mesa_ids = [m.id for m in mesas]
        
        # Obtener reportes agrupados por hora
        reportes_por_hora = db.session.query(
            ReporteParticipacion.hora_reporte,
            func.sum(ReporteParticipacion.personas_votadas).label('total_personas')
        ).filter(
            ReporteParticipacion.mesa_id.in_(mesa_ids)
        ).group_by(
            ReporteParticipacion.hora_reporte
        ).order_by(
            ReporteParticipacion.hora_reporte
        ).all()
        
        # Formatear datos para gráficos
        flujo_data = []
        for hora, total in reportes_por_hora:
            flujo_data.append({
                'hora': hora.strftime('%H:00'),
                'hora_completa': hora.isoformat(),
                'personas_votadas': total,
                'porcentaje_hora': 0  # Se puede calcular si se conoce el total esperado
            })
        
        return {
            'flujo_por_hora': flujo_data,
            'total_mesas': len(mesas),
            'total_reportes': len(reportes_por_hora),
            'resumen': {
                'hora_pico': max(flujo_data, key=lambda x: x['personas_votadas']) if flujo_data else None,
                'total_personas': sum(item['personas_votadas'] for item in flujo_data),
                'promedio_por_hora': sum(item['personas_votadas'] for item in flujo_data) / len(flujo_data) if flujo_data else 0
            }
        }
    
    @staticmethod
    def obtener_total_historico_mesa(mesa_id):
        """
        Obtener el total histórico de una mesa (suma de todos los reportes independientes)
        
        Args:
            mesa_id: ID de la mesa
            
        Returns:
            int: Total histórico de personas que han votado
        """
        reportes = ReporteParticipacion.query.filter_by(mesa_id=mesa_id).all()
        return sum(r.personas_votadas for r in reportes)
    
    @staticmethod
    def _calcular_tendencia(mesa_id):
        """
        Calcular tendencia de participación de una mesa basada en reportes incrementales
        
        Args:
            mesa_id: ID de la mesa
            
        Returns:
            str: 'normal', 'lenta', 'rapida', 'estancada'
        """
        reportes = ReporteParticipacion.query.filter_by(
            mesa_id=mesa_id
        ).order_by(ReporteParticipacion.hora_reporte.desc()).limit(2).all()
        
        if len(reportes) < 2:
            return 'normal'
        
        ultimo = reportes[0]
        penultimo = reportes[1]
        
        # Comparar los incrementos por hora (no acumulados)
        incremento_ultimo = ultimo.personas_votadas
        incremento_penultimo = penultimo.personas_votadas
        
        if incremento_ultimo == 0:
            return 'estancada'
        elif incremento_ultimo < 20:
            return 'lenta'
        elif incremento_ultimo > 100:
            return 'rapida'
        else:
            return 'normal'
