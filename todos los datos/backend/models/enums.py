"""
Enumeraciones para el sistema electoral MVP
"""
import enum

class UserRole(enum.Enum):
    """Roles de usuario en el sistema"""
    TESTIGO_ELECTORAL = 'testigo_electoral'
    COORDINADOR_PUESTO = 'coordinador_puesto'
    SISTEMAS = 'sistemas'

class LocationType(enum.Enum):
    """Tipos de ubicación geográfica"""
    DEPARTAMENTO = 'departamento'
    MUNICIPIO = 'municipio'
    PUESTO = 'puesto'
    MESA = 'mesa'

class FormStatus(enum.Enum):
    """Estados del formulario E-14"""
    BORRADOR = 'borrador'
    ENVIADO = 'enviado'
    APROBADO = 'aprobado'
    RECHAZADO = 'rechazado'
