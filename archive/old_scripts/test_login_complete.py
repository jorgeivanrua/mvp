#!/usr/bin/env python
"""
Prueba de login completa
"""
import http.client
import json
import sys

def test_login(usuario, password, rol):
    try:
        conn = http.client.HTTPConnection('127.0.0.1', 5000, timeout=5)
        
        credentials = json.dumps({"usuario": usuario, "password": password, "rol": rol})
        headers = {"Content-Type": "application/json"}
        
        conn.request('POST', '/api/auth/login', body=credentials, headers=headers)
        response = conn.getresponse()
        body = response.read().decode('utf-8')
        
        result = json.loads(body) if body else {}
        
        print(f"\nPrueba: {usuario}/{password} (rol: {rol})")
        print(f"Status: {response.status}")
        if 'token' in result:
            print(f"SUCCESS! Token obtenido: {result['token'][:50]}...")
            return True
        else:
            print(f"Response: {result}")
            return False
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

print("=" * 60)
print("PRUEBA DE LOGIN - SERVIDOR ELECTORAL")
print("=" * 60)

# Prueba 1: Admin
test_login("admin", "admin123", "super_admin")

# Prueba 2: Usuario testigo
test_login("ARMENIA_T001", "test123", "testigo_electoral")

print("\n" + "=" * 60)
