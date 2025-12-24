#!/usr/bin/env python
"""
Prueba de conexión al servidor
"""
import http.client
import sys

print("Intentando conectar a http://127.0.0.1:5000/...", flush=True)

try:
    conn = http.client.HTTPConnection('127.0.0.1', 5000, timeout=5)
    conn.request('GET', '/')
    response = conn.getresponse()
    status = response.status
    body = response.read(200)
    conn.close()
    
    print(f"Status: {status}", flush=True)
    print(f"Body (primeros 200 bytes): {body[:200]}", flush=True)
    print("SUCCESS!", flush=True)
    sys.exit(0)
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    sys.exit(1)
