#!/usr/bin/env python
"""
Script de inicio del servidor - Usa Waitress (estable en Windows)
Cargas los usuarios desde ubicaciones + cédulas para testigos
Coordinadores desde ubicaciones
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import os
import sys
import logging

# Configuración de entorno
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0'

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("=" * 60)
logger.info("SERVIDOR ELECTORAL - QUINDIO")
logger.info("=" * 60)

try:
    logger.info("[1/4] Cargando aplicación Flask...")
    from backend.app import create_app
    
    logger.info("[2/4] Creando instancia de la aplicación...")
    app = create_app('production')
    
    logger.info("[3/4] Cargando servidor Waitress...")
    from waitress import serve
    
    logger.info("[4/4] Iniciando servidor...")
    logger.info("")
    logger.info("  >>> Accede a la aplicación en: http://127.0.0.1:5000")
    logger.info("")
    logger.info("  CREDENCIALES DE PRUEBA:")
    logger.info("  - Admin: usuario=admin | password=admin123")
    logger.info("  - Coordinadores: usuario={nombre_ubicacion} | password=test123")
    logger.info("    (ejemplo: ARMENIA_M01 para coordinador municipal de Armenia)")
    logger.info("  - Testigos: cedula={cedula} | password=test123")
    logger.info("    (ejemplo: 2601010101001 para testigo en puesto ARMENIA_P01)")
    logger.info("")
    logger.info("  Base de datos: electoral.db")
    logger.info("")
    logger.info("  Presiona CTRL+C para detener el servidor")
    logger.info("")
    logger.info("=" * 60)
    logger.info("")
    
    sys.stdout.flush()
    sys.stderr.flush()
    
    # Iniciar servidor con Waitress
    serve(
        app,
        host='127.0.0.1',
        port=5000,
        threads=4
    )
    
except KeyboardInterrupt:
    logger.info("")
    logger.info("Servidor detenido por usuario (CTRL+C)")
    sys.exit(0)
except Exception as e:
    logger.error(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
