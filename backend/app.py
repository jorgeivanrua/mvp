"""
Aplicación principal Flask
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from whitenoise import WhiteNoise

from backend.config import config
from backend.database import init_db
from backend.utils.jwt_callbacks import configure_jwt_callbacks

# Inicializar extensiones
jwt = JWTManager()


def create_app(config_name='default'):
    """
    Factory para crear la aplicación Flask
    
    Args:
        config_name: Nombre de la configuración a usar
        
    Returns:
        Flask app configurada
    """
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    init_db(app)
    jwt.init_app(app)
    configure_jwt_callbacks(jwt)
    CORS(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Registrar manejadores de errores
    register_error_handlers(app)
    
    # Configurar WhiteNoise para servir archivos estáticos en producción
    if not app.debug:
        app.wsgi_app = WhiteNoise(
            app.wsgi_app,
            root='frontend/static',
            prefix='static/',
            max_age=31536000 if not app.debug else 0
        )
    
    return app


def register_blueprints(app):
    """Registrar blueprints de rutas"""
    from backend.routes.auth import auth_bp
    from backend.routes.locations import locations_bp
    from backend.routes.frontend import frontend_bp
    from backend.routes.configuracion import configuracion_bp
    from backend.routes.formularios_e14 import formularios_bp
    from backend.routes.coordinador_municipal import coordinador_municipal_bp
    from backend.routes.coordinador_departamental import bp as coordinador_departamental_bp
    from backend.routes.incidentes_delitos import incidentes_delitos_bp
    from backend.routes.super_admin import super_admin_bp
    from backend.routes.testigo import testigo_bp
    from backend.routes.coordinador_puesto import coordinador_puesto_bp
    from backend.routes.admin import admin_bp
    from backend.routes.admin_municipal import admin_municipal_bp
    from backend.routes.auditor import auditor_bp
    from backend.routes.gestion_usuarios import gestion_usuarios_bp
    from backend.routes.admin_tools import admin_tools_bp
    from backend.routes.admin_data_import import admin_import_bp
    from backend.routes.verificacion_presencia import verificacion_bp
    from backend.routes.locations_geo import locations_geo_bp
    from backend.routes.configuracion_sistema import config_sistema_bp
    
    # API routes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(locations_bp, url_prefix='/api/locations')
    app.register_blueprint(locations_geo_bp)
    app.register_blueprint(config_sistema_bp)
    app.register_blueprint(configuracion_bp, url_prefix='/api/configuracion')
    app.register_blueprint(formularios_bp)
    app.register_blueprint(coordinador_municipal_bp)
    app.register_blueprint(coordinador_departamental_bp)
    app.register_blueprint(incidentes_delitos_bp)
    app.register_blueprint(super_admin_bp)
    app.register_blueprint(testigo_bp, url_prefix='/api/testigo')
    app.register_blueprint(coordinador_puesto_bp, url_prefix='/api/coordinador-puesto')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(admin_municipal_bp, url_prefix='/api/admin-municipal')
    app.register_blueprint(auditor_bp, url_prefix='/api/auditor')
    app.register_blueprint(gestion_usuarios_bp)
    app.register_blueprint(admin_tools_bp)
    app.register_blueprint(admin_import_bp)
    app.register_blueprint(verificacion_bp)
    app.register_blueprint(config_sistema_bp)
    
    # Public routes (sin autenticación)
    from backend.routes.public import public_bp
    app.register_blueprint(public_bp)
    
    # Init DB route (para inicializar BD en producción sin Pre-Deploy Command)
    from backend.routes.init_db_route import init_db_bp
    app.register_blueprint(init_db_bp)
    
    # Frontend routes
    app.register_blueprint(frontend_bp)


def register_error_handlers(app):
    """Registrar manejadores de errores"""
    from backend.utils.exceptions import BaseAPIException
    
    @app.errorhandler(BaseAPIException)
    def handle_api_exception(error):
        """Manejar excepciones personalizadas de la API"""
        response = error.to_dict()
        return response, error.status_code
    
    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'error': 'Recurso no encontrado'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Error interno: {error}')
        return {'success': False, 'error': 'Error interno del servidor'}, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'success': False, 'error': 'Petición inválida'}, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {'success': False, 'error': 'No autorizado'}, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'success': False, 'error': 'Acceso prohibido'}, 403
