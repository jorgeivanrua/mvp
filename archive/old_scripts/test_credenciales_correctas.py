#!/usr/bin/env python
"""
Prueba de login con credenciales correctas según documentación
"""
import http.client
import json

def test_login(usuario, password, rol):
    try:
        conn = http.client.HTTPConnection('127.0.0.1', 5000, timeout=5)
        credentials = json.dumps({"usuario": usuario, "password": password, "rol": rol})
        headers = {"Content-Type": "application/json"}
        conn.request('POST', '/api/auth/login', body=credentials, headers=headers)
        response = conn.getresponse()
        body = json.loads(response.read().decode('utf-8'))
        
        print(f"\n[{response.status}] {usuario}/{password} ({rol})")
        if response.status == 200:
            print(f"  SUCCESS - Usuario: {body['data']['user']['nombre']}")
            return True
        else:
            print(f"  FAILED - {body.get('error', 'Error desconocido')}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

print("=" * 60)
print("PRUEBAS DE LOGIN - SERVIDOR ELECTORAL QUINDIO")
print("=" * 60)

# Admin
test_login("admin", "admin123", "super_admin")

# Coordinador Municipal
test_login("ARMENIA", "test123", "coordinador_municipal")

# Coordinador de Puesto
test_login("ARMENIA_P01", "test123", "coordinador_puesto")

# Testigo (por nombre testigo_cedula)
test_login("testigo_2601010101001", "test123", "testigo_electoral")

print("\n" + "=" * 60)
print("SERVIDOR ELECTORAL DISPONIBLE EN: http://127.0.0.1:5000")
print("=" * 60)
