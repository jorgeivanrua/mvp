#!/usr/bin/env python
"""
Servidor Flask usando Werkzeug directamente (más control sobre Windows threading)
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import os
import sys
import logging
import threading
import time

os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0'

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

logger.info("=== Flask Server (Werkzeug Direct) ===")

try:
    logger.info("[1] Importing create_app...")
    from backend.app import create_app
    
    logger.info("[2] Creating app (production)...")
    app = create_app('production')
    
    logger.info("[3] App created. debug = %s", app.debug)
    logger.info(">> Servidor corriendo en http://127.0.0.1:5000")
    logger.info(">> Base de datos: sqlite:///electoral.db")
    logger.info("")
    
    logger.info("[4] Starting server via Werkzeug...")
    sys.stdout.flush()
    sys.stderr.flush()
    
    # Importar Werkzeug serving
    from werkzeug.serving import make_server
    
    logger.info("[5] Werkzeug imported, creating server...")
    server = make_server(
        '127.0.0.1',
        5000,
        app,
        threaded=True
    )
    
    logger.info("[6] Server created, starting...")
    sys.stdout.flush()
    sys.stderr.flush()
    
    logger.info("* Running on http://127.0.0.1:5000")
    logger.info("Press CTRL+C to quit")
    sys.stdout.flush()
    sys.stderr.flush()
    
    # Run the server in main thread
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    finally:
        server.shutdown()
    
    logger.info("[7] Server shutdown complete")
    
except Exception as e:
    import traceback
    logger.error("[ERROR] %s: %s", type(e).__name__, e)
    traceback.print_exc()
    sys.exit(1)
