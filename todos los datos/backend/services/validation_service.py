"""
Servicio de validación de formularios E-14
"""
from typing import Dict, List, Tuple

class ValidationResult:
    """Resultado de validación"""
    def __init__(self, is_valid: bool, errors: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
    
    def add_error(self, error: str):
        self.is_valid = False
        self.errors.append(error)

class ValidationService:
    """Servicio para validar datos de formularios E-14"""
    
    @staticmethod
    def validate_e14_data(form_data: Dict, mesa) -> ValidationResult:
        """
        Validar datos del formulario E-14
        
        Validaciones:
        1. Total votos <= Votantes registrados
        2. Suma de votos = Total votos
        3. Todos los campos numéricos >= 0
        """
        result = ValidationResult(is_valid=True)
        
        # Extraer datos
        total_votos = form_data.get('total_votos', 0)
        votos_partido_1 = form_data.get('votos_partido_1', 0)
        votos_partido_2 = form_data.get('votos_partido_2', 0)
        votos_partido_3 = form_data.get('votos_partido_3', 0)
        votos_nulos = form_data.get('votos_nulos', 0)
        votos_no_marcados = form_data.get('votos_no_marcados', 0)
        
        # Validación 1: Campos numéricos no negativos
        campos_numericos = {
            'total_votos': total_votos,
            'votos_partido_1': votos_partido_1,
            'votos_partido_2': votos_partido_2,
            'votos_partido_3': votos_partido_3,
            'votos_nulos': votos_nulos,
            'votos_no_marcados': votos_no_marcados
        }
        
        for campo, valor in campos_numericos.items():
            if valor < 0:
                result.add_error(f"{campo} no puede ser negativo")
        
        # Validación 2: Total votos <= Votantes registrados
        if mesa and total_votos > mesa.total_votantes_registrados:
            result.add_error(
                f"Total de votos ({total_votos}) excede votantes registrados "
                f"({mesa.total_votantes_registrados})"
            )
        
        # Validación 3: Suma de votos = Total votos
        suma_votos = (votos_partido_1 + votos_partido_2 + votos_partido_3 + 
                     votos_nulos + votos_no_marcados)
        
        if suma_votos != total_votos:
            result.add_error(
                f"La suma de votos ({suma_votos}) no coincide con el total "
                f"de votos ({total_votos})"
            )
        
        return result
    
    @staticmethod
    def validate_e14_uniqueness(mesa_id: int, form_id: int = None) -> Tuple[bool, str]:
        """
        Validar que no exista otro E-14 aprobado para la misma mesa
        
        Args:
            mesa_id: ID de la mesa
            form_id: ID del formulario actual (para excluir en actualizaciones)
        
        Returns:
            Tuple (es_valido, mensaje_error)
        """
        from app.models.form_e14 import FormE14
        from app.models.enums import FormStatus
        
        query = FormE14.query.filter_by(
            mesa_id=mesa_id,
            estado=FormStatus.APROBADO
        )
        
        if form_id:
            query = query.filter(FormE14.id != form_id)
        
        existing_form = query.first()
        
        if existing_form:
            return False, f"Ya existe un formulario E-14 aprobado para esta mesa (ID: {existing_form.id})"
        
        return True, ""
    
    @staticmethod
    def validate_form_transition(current_status, new_status, user_role) -> Tuple[bool, str]:
        """
        Validar transición de estado del formulario
        
        Transiciones válidas:
        - BORRADOR → ENVIADO (testigo)
        - ENVIADO → APROBADO (coordinador)
        - ENVIADO → RECHAZADO (coordinador)
        - RECHAZADO → ENVIADO (testigo, después de correcciones)
        """
        from app.models.enums import FormStatus, UserRole
        
        valid_transitions = {
            FormStatus.BORRADOR: {
                FormStatus.ENVIADO: [UserRole.TESTIGO_ELECTORAL]
            },
            FormStatus.ENVIADO: {
                FormStatus.APROBADO: [UserRole.COORDINADOR_PUESTO, UserRole.SISTEMAS],
                FormStatus.RECHAZADO: [UserRole.COORDINADOR_PUESTO, UserRole.SISTEMAS]
            },
            FormStatus.RECHAZADO: {
                FormStatus.ENVIADO: [UserRole.TESTIGO_ELECTORAL]
            }
        }
        
        if current_status not in valid_transitions:
            return False, f"No se puede cambiar el estado desde {current_status.value}"
        
        if new_status not in valid_transitions[current_status]:
            return False, f"Transición inválida: {current_status.value} → {new_status.value}"
        
        allowed_roles = valid_transitions[current_status][new_status]
        if user_role not in allowed_roles:
            return False, f"Rol {user_role.value} no autorizado para esta transición"
        
        return True, ""
