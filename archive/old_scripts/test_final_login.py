#!/usr/bin/env python
"""
Prueba final de login con cédula de testigo
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
        body = response.read().decode('utf-8')
        
        result = json.loads(body) if body else {}
        
        print(f"\nLogin: {usuario}")
        print(f"  Password: {password}")
        print(f"  Rol: {rol}")
        print(f"  Status HTTP: {response.status}")
        
        if response.status == 200 and 'data' in result:
            token = result['data']['access_token'][:50]
            user_info = result['data']['user']
            print(f"  SUCCESS!")
            print(f"  Usuario: {user_info['nombre']}")
            print(f"  Token: {token}...")
        else:
            print(f"  FAILED: {result.get('error', 'Unknown error')}")
        
    except Exception as e:
        print(f"ERROR: {e}")

print("=" * 60)
print("PRUEBA DE LOGIN - SERVIDOR ELECTORAL")
print("=" * 60)

# Prueba 1: Admin
test_login("admin", "admin123", "super_admin")

# Prueba 2: Usuario testigo por cédula
test_login("testigo_2601010101001", "test123", "testigo_electoral")

# Prueba 3: Usuario por cédula solamente
test_login("2601010101001", "test123", "testigo_electoral")

print("\n" + "=" * 60)
print("PRUEBAS COMPLETADAS")
print("=" * 60)
