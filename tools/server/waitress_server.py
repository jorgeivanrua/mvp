#!/usr/bin/env python
"""
Iniciar con Waitress usando socket_timeout explícito
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import os
import sys

os.environ['FLASK_ENV'] = 'production'

print("[1] Cargando app...", flush=True)

from backend.app import create_app
app = create_app('production')

print("[2] App cargada", flush=True)
print(">>> http://127.0.0.1:5000", flush=True)
print("", flush=True)

print("[3] Importando waitress...", flush=True)
from waitress import serve

print("[4] Iniciando serve...", flush=True)
sys.stdout.flush()
sys.stderr.flush()

# Try serve con parámetros correctos
try:
    serve(
        app,
        host='127.0.0.1',
        port=5000,
        threads=4
    )
except KeyboardInterrupt:
    print("\n[CTRL+C] Servidor detenido")
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("[5] serve() returned")
