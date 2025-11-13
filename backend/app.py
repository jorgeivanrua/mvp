"""
Aplicación principal Flask
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

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
    
    return app


def register_blueprints(app):
    """Registrar blueprints de rutas"""
    from backend.routes.auth import auth_bp
    from backend.routes.locations import locations_bp
    from backend.routes.frontend import frontend_bp
    from backend.routes.configuracion import configuracion_bp
    from backend.routes.formularios_e14 import formularios_bp
    from backend.routes.coordinador_municipal import coordinador_municipal_bp
    
    # API routes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(locations_bp, url_prefix='/api/locations')
    app.register_blueprint(configuracion_bp, url_prefix='/api/configuracion')
    app.register_blueprint(formularios_bp)
    app.register_blueprint(coordinador_municipal_bp)
    
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
