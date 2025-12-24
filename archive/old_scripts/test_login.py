#!/usr/bin/env python
"""
Prueba de login al servidor
"""
import http.client
import json
import sys

print("Intentando conectar y hacer login...", flush=True)

try:
    conn = http.client.HTTPConnection('127.0.0.1', 5000, timeout=5)
    
    # Intentar acceder a /api/auth/login (sin auth)
    conn.request('GET', '/api/auth/login')
    response = conn.getresponse()
    status = response.status
    body = response.read()
    
    print(f"GET /api/auth/login -> Status: {status}", flush=True)
    print(f"Body: {body[:300]}", flush=True)
    
    # Intentar POST a /api/auth/login con credenciales
    conn = http.client.HTTPConnection('127.0.0.1', 5000, timeout=5)
    credentials = json.dumps({"usuario": "admin", "password": "admin123"})
    headers = {"Content-Type": "application/json"}
    
    conn.request('POST', '/api/auth/login', body=credentials, headers=headers)
    response = conn.getresponse()
    status = response.status
    body = response.read(500)
    
    print(f"\nPOST /api/auth/login (admin/admin123) -> Status: {status}", flush=True)
    print(f"Body: {body}", flush=True)
    
    conn.close()
    print("\nSUCCESS! Servidor funciona", flush=True)
    sys.exit(0)
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
