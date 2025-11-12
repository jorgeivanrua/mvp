"""
Servicio de gestión de formularios E-14
"""
from datetime import datetime
from typing import Dict, Optional
from app import db
from app.models.form_e14 import FormE14, FormE14History
from app.models.location import Location
from app.models.enums import FormStatus
from .validation_service import ValidationService

class E14Service:
    """Servicio para gestionar formularios E-14"""
    
    @staticmethod
    def create_form(data: Dict, testigo_id: int) -> Dict:
        """
        Crear nuevo formulario E-14
        
        Args:
            data: Datos del formulario
            testigo_id: ID del testigo que crea el formulario
        
        Returns:
            Dict con success, form y message
        """
        try:
            # Obtener mesa
            mesa = Location.get_by_id(data['mesa_id'])
            if not mesa:
                return {'success': False, 'message': 'Mesa no encontrada'}
            
            # Validar datos
            validation = ValidationService.validate_e14_data(data, mesa)
            if not validation.is_valid:
                return {
                    'success': False,
                    'message': 'Datos inválidos',
                    'errors': validation.errors
                }
            
            # Crear formulario
            form = FormE14(
                mesa_id=data['mesa_id'],
                testigo_id=testigo_id,
                total_votos=data['total_votos'],
                votos_partido_1=data.get('votos_partido_1', 0),
                votos_partido_2=data.get('votos_partido_2', 0),
                votos_partido_3=data.get('votos_partido_3', 0),
                votos_nulos=data.get('votos_nulos', 0),
                votos_no_marcados=data.get('votos_no_marcados', 0),
                observaciones=data.get('observaciones', ''),
                estado=FormStatus.BORRADOR
            )
            
            form.save()
            
            # Registrar en historial
            history = FormE14History(
                form_id=form.id,
                usuario_id=testigo_id,
                accion='crear',
                estado_nuevo=FormStatus.BORRADOR.value
            )
            history.save()
            
            return {
                'success': True,
                'form': form.to_dict(),
                'message': 'Formulario E-14 creado exitosamente'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error al crear formulario: {str(e)}'
            }
    
    @staticmethod
    def update_form(form_id: int, data: Dict, user_id: int) -> Dict:
        """Actualizar formulario E-14 (solo en estado borrador)"""
        try:
            form = FormE14.get_by_id(form_id)
            if not form:
                return {'success': False, 'message': 'Formulario no encontrado'}
            
            # Solo se puede editar en estado borrador
            if form.estado != FormStatus.BORRADOR:
                return {
                    'success': False,
                    'message': 'Solo se pueden editar formularios en borrador'
                }
            
            # Obtener mesa para validación
            mesa = Location.get_by_id(form.mesa_id)
            
            # Validar datos
            validation = ValidationService.validate_e14_data(data, mesa)
            if not validation.is_valid:
                return {
                    'success': False,
                    'message': 'Datos inválidos',
                    'errors': validation.errors
                }
            
            # Actualizar campos
            form.total_votos = data['total_votos']
            form.votos_partido_1 = data.get('votos_partido_1', 0)
            form.votos_partido_2 = data.get('votos_partido_2', 0)
            form.votos_partido_3 = data.get('votos_partido_3', 0)
            form.votos_nulos = data.get('votos_nulos', 0)
            form.votos_no_marcados = data.get('votos_no_marcados', 0)
            form.observaciones = data.get('observaciones', '')
            
            form.save()
            
            # Registrar en historial
            history = FormE14History(
                form_id=form.id,
                usuario_id=user_id,
                accion='actualizar',
                estado_anterior=FormStatus.BORRADOR.value,
                estado_nuevo=FormStatus.BORRADOR.value
            )
            history.save()
            
            return {
                'success': True,
                'form': form.to_dict(),
                'message': 'Formulario actualizado exitosamente'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error al actualizar formulario: {str(e)}'
            }
    
    @staticmethod
    def submit_form(form_id: int, user_id: int) -> Dict:
        """Enviar formulario para aprobación"""
        try:
            form = FormE14.get_by_id(form_id)
            if not form:
                return {'success': False, 'message': 'Formulario no encontrado'}
            
            # Validar transición de estado
            from app.models.user import User
            user = User.get_by_id(user_id)
            
            is_valid, error_msg = ValidationService.validate_form_transition(
                form.estado, FormStatus.ENVIADO, user.rol
            )
            
            if not is_valid:
                return {'success': False, 'message': error_msg}
            
            # Validar que tenga foto
            if not form.foto_url:
                return {
                    'success': False,
                    'message': 'Debe adjuntar foto del formulario físico'
                }
            
            # Cambiar estado
            estado_anterior = form.estado
            form.estado = FormStatus.ENVIADO
            form.save()
            
            # Registrar en historial
            history = FormE14History(
                form_id=form.id,
                usuario_id=user_id,
                accion='enviar',
                estado_anterior=estado_anterior.value,
                estado_nuevo=FormStatus.ENVIADO.value
            )
            history.save()
            
            return {
                'success': True,
                'form': form.to_dict(),
                'message': 'Formulario enviado para aprobación'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error al enviar formulario: {str(e)}'
            }
    
    @staticmethod
    def approve_form(form_id: int, coordinador_id: int, observaciones: str = '') -> Dict:
        """Aprobar formulario E-14"""
        try:
            form = FormE14.get_by_id(form_id)
            if not form:
                return {'success': False, 'message': 'Formulario no encontrado'}
            
            # Validar transición de estado
            from app.models.user import User
            coordinador = User.get_by_id(coordinador_id)
            
            is_valid, error_msg = ValidationService.validate_form_transition(
                form.estado, FormStatus.APROBADO, coordinador.rol
            )
            
            if not is_valid:
                return {'success': False, 'message': error_msg}
            
            # Validar unicidad (no puede haber otro E-14 aprobado para la misma mesa)
            is_unique, error_msg = ValidationService.validate_e14_uniqueness(
                form.mesa_id, form.id
            )
            
            if not is_unique:
                return {'success': False, 'message': error_msg}
            
            # Aprobar formulario
            estado_anterior = form.estado
            form.estado = FormStatus.APROBADO
            form.aprobado_por = coordinador_id
            form.aprobado_en = datetime.utcnow()
            if observaciones:
                form.observaciones = observaciones
            
            form.save()
            
            # Registrar en historial
            history = FormE14History(
                form_id=form.id,
                usuario_id=coordinador_id,
                accion='aprobar',
                estado_anterior=estado_anterior.value,
                estado_nuevo=FormStatus.APROBADO.value,
                justificacion=observaciones
            )
            history.save()
            
            return {
                'success': True,
                'form': form.to_dict(),
                'message': 'Formulario aprobado exitosamente'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error al aprobar formulario: {str(e)}'
            }
    
    @staticmethod
    def reject_form(form_id: int, coordinador_id: int, justificacion: str) -> Dict:
        """Rechazar formulario E-14"""
        try:
            if not justificacion or not justificacion.strip():
                return {
                    'success': False,
                    'message': 'La justificación es obligatoria para rechazar'
                }
            
            form = FormE14.get_by_id(form_id)
            if not form:
                return {'success': False, 'message': 'Formulario no encontrado'}
            
            # Validar transición de estado
            from app.models.user import User
            coordinador = User.get_by_id(coordinador_id)
            
            is_valid, error_msg = ValidationService.validate_form_transition(
                form.estado, FormStatus.RECHAZADO, coordinador.rol
            )
            
            if not is_valid:
                return {'success': False, 'message': error_msg}
            
            # Rechazar formulario
            estado_anterior = form.estado
            form.estado = FormStatus.RECHAZADO
            form.observaciones = justificacion
            form.save()
            
            # Registrar en historial
            history = FormE14History(
                form_id=form.id,
                usuario_id=coordinador_id,
                accion='rechazar',
                estado_anterior=estado_anterior.value,
                estado_nuevo=FormStatus.RECHAZADO.value,
                justificacion=justificacion
            )
            history.save()
            
            return {
                'success': True,
                'form': form.to_dict(),
                'message': 'Formulario rechazado'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error al rechazar formulario: {str(e)}'
            }
    
    @staticmethod
    def get_form_history(form_id: int) -> list:
        """Obtener historial de cambios de un formulario"""
        history = FormE14History.query.filter_by(form_id=form_id)\
            .order_by(FormE14History.timestamp.desc())\
            .all()
        
        return [h.to_dict() for h in history]
