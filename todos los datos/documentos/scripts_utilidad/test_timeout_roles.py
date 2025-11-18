#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test solo los roles con timeout"""
import requests
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:5000"

roles_test = [
    {
        "nombre": "super_admin",
        "data": {
            "rol": "super_admin",
            "password": "test123"
        }
    },
    {
        "nombre": "admin_departamental",
        "data": {
            "rol": "admin_departamental",
            "departamento_codigo": "44",
            "password": "test123"
        }
    },
    {
        "nombre": "admin_municipal",
        "data": {
            "rol": "admin_municipal",
            "departamento_codigo": "44",
            "municipio_codigo": "01",
            "password": "test123"
        }
    }
]

print("Probando roles con timeout...")
print("="*60)

for rol_info in roles_test:
    print(f"\n{rol_info['nombre']}:")
    print(f"  Data: {rol_info['data']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=rol_info['data'],
            timeout=15
        )
        
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"  OK Login exitoso!")
                user = data.get('data', {}).get('user', {})
                print(f"  Usuario: {user.get('nombre')}")
            else:
                print(f"  X Error: {data.get('error')}")
        else:
            print(f"  X Error: {response.text[:200]}")
    except requests.exceptions.Timeout:
        print(f"  X TIMEOUT (15s)")
    except Exception as e:
        print(f"  X Exception: {str(e)[:100]}")

print("\n" + "="*60)
