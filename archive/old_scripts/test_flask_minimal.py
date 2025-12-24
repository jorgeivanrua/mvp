#!/usr/bin/env python
"""
Prueba minimalista de Flask
"""
import sys
print("[A] Starting Flask test...", flush=True)

from flask import Flask
print("[B] Flask imported", flush=True)

app = Flask(__name__)
print("[C] Flask app created", flush=True)

@app.route('/')
def hello():
    return "Hello World", 200

print("[D] Route registered", flush=True)

print("[E] About to run app...", flush=True)
sys.stdout.flush()
sys.stderr.flush()

try:
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )
    print("[F] app.run() returned")
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
