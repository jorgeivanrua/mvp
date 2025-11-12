# Routes package
from backend.routes.auth import auth_bp
from backend.routes.frontend import frontend_bp
from backend.routes.locations import locations_bp
from backend.routes.configuracion import configuracion_bp
from backend.routes.formularios_e14 import formularios_bp

__all__ = [
    'auth_bp',
    'frontend_bp',
    'locations_bp',
    'configuracion_bp',
    'formularios_bp'
]
