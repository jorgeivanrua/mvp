#!/usr/bin/env python
"""
Script de diagnóstico - ejecutar Flask dev server con diagnóstico completo
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import os
import sys
import logging
import traceback

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Variables de entorno
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '0'
os.environ['WERKZEUG_DEBUG_PIN'] = 'off'

logger.info("=== Starting diagnosis ===")
logger.info(f"Python version: {sys.version}")
logger.info(f"Working directory: {os.getcwd()}")
logger.info(f"Port to use: 5000")

try:
    logger.info("[1] Importing create_app...")
    from backend.app import create_app
    logger.info("[1] SUCCESS - create_app imported")
    
    logger.info("[2] Calling create_app('production')...")  # Usar production para deshabilitar debug
    sys.stdout.flush()
    sys.stderr.flush()
    
    app = create_app('production')
    
    logger.info("[2] SUCCESS - App created")
    logger.info(f"App name: {app.name}")
    logger.info(f"App debug: {app.debug}")
    logger.info(f"App config keys: {list(app.config.keys())[:5]}...")
    
    logger.info("[3] About to start Flask dev server...")
    logger.info(">> Servidor corriendo en http://127.0.0.1:5000")
    logger.info(">> Base de datos: sqlite:///electoral.db")
    logger.info(">> Accede a: http://127.0.0.1:5000")
    
    sys.stdout.flush()
    sys.stderr.flush()
    
    logger.info("[4] Calling app.run()...")
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )
    
    logger.info("[5] app.run() returned - THIS SHOULD NOT HAPPEN")
    
except KeyboardInterrupt:
    logger.info("[KeyboardInterrupt] Server stopped by user")
    sys.exit(0)
except Exception as e:
    logger.error(f"[EXCEPTION] {type(e).__name__}: {e}")
    logger.error("Full traceback:")
    traceback.print_exc()
    sys.exit(1)
finally:
    logger.info("=== Diagnosis complete ===")
