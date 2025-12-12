"""
Servicio de autenticación para testigos por cédula
"""
from datetime import datetime
from backend.database import db
from backend.models.user import User
from backend.utils.exceptions import AuthenticationException, ValidationException
from backend.utils.jwt_utils import generate_tokens
from backend.utils.logging_config import get_logger

logger = get_logger(__name__)


class AuthTestigoService:
    """Servicio para autenticación de testigos por cédula"""
    
    @staticmethod
    def login_por_cedula(cedula):
        """
        Autenticar testigo usando solo cédula (contraseña fija: test123)
        
        Args:
            cedula: Número de cédula del testigo
            
        Returns:
            tuple: (user, access_token, refresh_token)
        """
        # Limpiar cédula (solo números)
        cedula_limpia = ''.join(filter(str.isdigit, str(cedula)))
        
        if not cedula_limpia:
            raise ValidationException({'cedula': ['Número de cédula inválido']})
        
        if len(cedula_limpia) < 6 or len(cedula_limpia) > 12:
            raise ValidationException({'cedula': ['Número de cédula debe tener entre 6 y 12 dígitos']})
        
        logger.info(f"Autenticando testigo con cédula: {cedula_limpia}")
        
        # Buscar testigo por cédula
        user = User.query.filter_by(
            cedula=cedula_limpia,
            rol='testigo_electoral',
            activo=True
        ).first()
        
        if not user:
            raise AuthenticationException("Testigo no encontrado. Verifique que su cédula esté registrada en el sistema.")
        
        # Verificar contraseña fija (test123)
        if not user.check_password('test123'):
            raise AuthenticationException("Error de autenticación. Contacte al administrador.")
        
        # Verificar si está bloqueado
        if user.bloqueado_hasta and user.bloqueado_hasta > datetime.utcnow():
            tiempo_restante = (user.bloqueado_hasta - datetime.utcnow()).seconds // 60
            raise AuthenticationException(
                f"Cuenta bloqueada. Intente en {tiempo_restante} minutos"
            )
        
        # Reset intentos fallidos y actualizar último acceso
        user.intentos_fallidos = 0
        user.bloqueado_hasta = None
        user.ultimo_acceso = datetime.utcnow()
        db.session.commit()
        
        # Generar tokens
        access_token, refresh_token = generate_tokens(user)
        
        logger.info(f"Login exitoso para testigo: {user.nombre} (cédula: {cedula_limpia})")
        
        return user, access_token, refresh_token
    
    @staticmethod
    def verificar_cedula_disponible(cedula, user_id=None):
        """
        Verificar si una cédula está disponible
        
        Args:
            cedula: Número de cédula a verificar
            user_id: ID del usuario actual (para excluir en ediciones)
            
        Returns:
            bool: True si está disponible
        """
        cedula_limpia = ''.join(filter(str.isdigit, str(cedula)))
        
        if not cedula_limpia:
            return False
        
        query = User.query.filter_by(cedula=cedula_limpia)
        
        if user_id:
            query = query.filter(User.id != user_id)
        
        return query.first() is None
    
    @staticmethod
    def asignar_cedula_testigo(user_id, cedula):
        """
        Asignar cédula a un testigo existente
        
        Args:
            user_id: ID del usuario testigo
            cedula: Número de cédula a asignar
        """
        cedula_limpia = ''.join(filter(str.isdigit, str(cedula)))
        
        if not cedula_limpia or len(cedula_limpia) < 6:
            raise ValidationException({'cedula': ['Número de cédula inválido']})
        
        # Verificar que esté disponible
        if not AuthTestigoService.verificar_cedula_disponible(cedula_limpia, user_id):
            raise ValidationException({'cedula': ['Esta cédula ya está registrada por otro testigo']})
        
        # Obtener usuario
        user = User.query.get(user_id)
        if not user or user.rol != 'testigo_electoral':
            raise ValidationException({'user': ['Usuario testigo no encontrado']})
        
        # Asignar cédula
        user.cedula = cedula_limpia
        db.session.commit()
        
        logger.info(f"Cédula {cedula_limpia} asignada al testigo {user.nombre}")
        
        return user