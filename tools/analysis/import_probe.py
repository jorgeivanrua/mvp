#!/usr/bin/env python
"""
Script para importar módulos del backend de forma secuencial y detectar el primero que falla.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import importlib
import sys
import traceback

modules = [
    'backend.config',
    'backend.utils.logging_config',
    'backend.database',
    'backend.utils.jwt_callbacks',
    'flask_cors',
    'flask_compress',
    'whitenoise',
    'backend.routes.auth',
    'backend.routes.locations',
    'backend.routes.frontend',
    'backend.routes.configuracion',
    'backend.routes.formularios_e14',
    'backend.routes.coordinador_municipal',
    'backend.routes.coordinador_departamental',
    'backend.services',
    'backend.services.websocket_service',
    'backend.app'
]

print('[0] Starting import probe', flush=True)
for idx, mod in enumerate(modules, start=1):
    print(f"[{idx}] Importing {mod}...", flush=True)
    try:
        imported = importlib.import_module(mod)
        print(f"[{idx}] OK: {mod} -> {repr(imported)}", flush=True)
    except Exception as e:
        print(f"[{idx}] FAILED: {mod} -> {type(e).__name__}: {e}", flush=True)
        traceback.print_exc()
        sys.exit(2)

# Extra: try create_app to reproduce earlier behavior
print('[X] All imports OK. Trying create_app("production")...', flush=True)
try:
    from backend.app import create_app
    app = create_app('production')
    print('[X] create_app production OK. app.debug =', app.debug, flush=True)
except Exception as e:
    print(f'[X] create_app FAILED: {type(e).__name__}: {e}', flush=True)
    traceback.print_exc()
    sys.exit(3)

print('[DONE] import probe completed successfully.', flush=True)
sys.exit(0)
