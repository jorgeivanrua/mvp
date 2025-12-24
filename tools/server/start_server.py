#!/usr/bin/env python
"""
Script simple para iniciar el servidor Flask
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import os
import sys
import logging

# Logging to see what happens
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Configurar FLASK_ENV
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '0'
os.environ['WERKZEUG_DEBUG_PIN'] = 'off'

print("[0] Imports OK")
sys.stdout.flush()

from backend.app import create_app

print("[0.5] create_app imported")
sys.stdout.flush()

if __name__ == '__main__':
    print("[1] Main block started")
    sys.stdout.flush()
    
    try:
        print("[2] About to create_app...")
        sys.stdout.flush()
        
        app = create_app('development')
        
        print("[3] App created successfully")
        sys.stdout.flush()
        
        print("[4] About to run app...")
        sys.stdout.flush()
        
        # Try running
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
        
        print("[5] app.run() returned")
        sys.stdout.flush()
        
    except KeyboardInterrupt:
        print("[KeyboardInterrupt] Server stopped")
        sys.exit(0)
    except Exception as e:
        import traceback
        print(f"[ERROR] {e}")
        print(f"[ERROR] Type: {type(e)}")
        traceback.print_exc()
        sys.stdout.flush()
        sys.exit(1)
