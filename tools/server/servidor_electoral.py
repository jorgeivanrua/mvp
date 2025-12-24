#!/usr/bin/env python
"""
Iniciar servidor Electoral con Waitress
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import os
import sys

os.environ['FLASK_ENV'] = 'production'

print("[SERVIDOR] Cargando aplicacion...", flush=True)

try:
    from backend.app import create_app
    
    print("[SERVIDOR] Creando app en modo production...", flush=True)
    app = create_app('production')
    
    print("[SERVIDOR] App creada exitosamente", flush=True)
    print("", flush=True)
    print("SERVIDOR DISPONIBLE EN:", flush=True)
    print("  http://127.0.0.1:5000", flush=True)
    print("", flush=True)
    
    print("[SERVIDOR] Importando Waitress...", flush=True)
    from waitress import serve
    
    print("[SERVIDOR] Iniciando servidor...", flush=True)
    print("", flush=True)
    
    sys.stdout.flush()
    sys.stderr.flush()
    
    # Iniciar servidor
    serve(
        app,
        host='127.0.0.1',
        port=5000,
        threads=4
    )
    
except KeyboardInterrupt:
    print("\n[SERVIDOR] Detenido por usuario", flush=True)
    sys.exit(0)
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
