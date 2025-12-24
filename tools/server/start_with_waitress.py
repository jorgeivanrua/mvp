#!/usr/bin/env python
"""
Iniciar servidor con Waitress (más estable en Windows que Flask dev server)
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import os
import sys

# Configurar variables de entorno
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '0'
os.environ['WERKZEUG_DEBUG_PIN'] = 'off'

print("[1] Starting server with Waitress...", flush=True)

from backend.app import create_app

try:
    print("[2] Creating Flask app...", flush=True)
    
    app = create_app('development')
    
    print("[3] Flask app created successfully", flush=True)
    print(">> Servidor corriendo en http://127.0.0.1:8000", flush=True)
    print(">> Base de datos: sqlite:///electoral.db", flush=True)
    print(">> Accede a: http://127.0.0.1:8000", flush=True)
    print("", flush=True)
    
    print("[4] About to import Waitress serve...", flush=True)
    from waitress import serve
    print("[4.5] Waitress imported successfully", flush=True)
    
    print("[5] About to call serve() on port 8000...", flush=True)
    sys.stdout.flush()
    sys.stderr.flush()
    
    # Serve the WSGI app with Waitress
    serve(
        app,
        host='127.0.0.1',
        port=8000,
        threads=10
    )
    
    print("[6] serve() returned??", flush=True)
    
except OSError as ose:
    print(f"[OSError] {ose} - Puerto pudo estar en uso, intentando con 9000...", flush=True)
    try:
        from waitress import serve
        serve(
            app,
            host='127.0.0.1',
            port=9000,
            threads=10
        )
    except Exception as e2:
        print(f"[ERROR2] {e2}", flush=True)
        sys.exit(1)
except Exception as e:
    import traceback
    print(f"[ERROR] {e}", flush=True)
    print(f"[ERROR] Type: {type(e)}", flush=True)
    traceback.print_exc()
    sys.exit(1)


