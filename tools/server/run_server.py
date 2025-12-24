#!/usr/bin/env python
"""
Versión simplificada para ejecutar como foreground
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import os
import sys

os.environ['FLASK_ENV'] = 'production'

print("[START] Iniciando servidor...", flush=True)

try:
    from backend.app import create_app
    print("[OK1] App imported", flush=True)
    
    app = create_app('production')
    print("[OK2] App created", flush=True)
    print(">>> Servidor en http://127.0.0.1:5000", flush=True)
    print("")
    sys.stdout.flush()
    
    # Flask run
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False
    )
    print("[END] Servidor detenido")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
