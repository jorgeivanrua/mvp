# Routes package
from backend.routes.auth import auth_bp
from backend.routes.frontend import frontend_bp
from backend.routes.locations import locations_bp
from backend.routes.configuracion import configuracion_bp
from backend.routes.formularios_e14 import formularios_bp
from backend.routes.coordinador_municipal import coordinador_municipal_bp
from backend.routes.super_admin import super_admin_bp
from backend.routes.public import public_bp

__all__ = [
    'auth_bp',
    'frontend_bp',
    'locations_bp',
    'configuracion_bp',
    'formularios_bp',
    'coordinador_municipal_bp',
    'super_admin_bp',
    'public_bp'
]
