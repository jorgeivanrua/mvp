#!/usr/bin/env python
"""
Intento de capturar error de socket a bajo nivel
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import os
import sys
import socket
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

os.environ['FLASK_ENV'] = 'production'

logger.info("=== Socket Debug ===")

# Prueba 1: verificar que podemos crear un socket directamente
try:
    logger.info("[Test1] Intentando crear socket directamente...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.info("[Test1] Socket creado: %s", sock)
    
    logger.info("[Test1] Intentando bind a 127.0.0.1:5000...")
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 5000))
    logger.info("[Test1] Bind exitoso")
    
    sock.listen(1)
    logger.info("[Test1] Listen exitoso")
    
    sock.close()
    logger.info("[Test1] Socket cerrado")
except Exception as e:
    logger.error("[Test1] FAILED: %s", e)
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Prueba 2: cargar app y run
try:
    logger.info("[Test2] Importando create_app...")
    from backend.app import create_app
    
    logger.info("[Test2] Creando app...")
    app = create_app('production')
    
    logger.info("[Test2] App creada. Intentando app.run()...")
    logger.info("[Test2] Por favor observa si Flask se detiene aqui:")
    sys.stdout.flush()
    sys.stderr.flush()
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False
    )
    
    logger.info("[Test2] app.run() retorno??")
    
except Exception as e:
    logger.error("[Test2] EXCEPTION: %s", e)
    import traceback
    traceback.print_exc()
    sys.exit(2)

logger.info("[DONE]")
