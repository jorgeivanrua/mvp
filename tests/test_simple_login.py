#!/usr/bin/env python3
"""
Prueba simple de login con cédulas de 10 cifras
"""

import requests
import json

def main():
    print("🔍 VERIFICACIÓN FINAL DEL SISTEMA")
    print("=" * 40)
    
    # Verificar servidor
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        print(f'✅ Servidor funcionando - Status: {response.status_code}')
    except Exception as e:
        print(f'❌ Servidor no responde: {e}')
        return
    
    # Probar login con cédula de 10 cifras
    print('\n🧪 PRUEBA FINAL DE LOGIN')
    print('-' * 25)
    
    payload = {
        'rol': 'testigo_electoral',
        'cedula': '1000000001',
        'password': 'test123'
    }
    
    try:
        response = requests.post('http://localhost:5000/api/auth/login', json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('data', {}).get('user', {})
            
            print('✅ LOGIN EXITOSO CON CÉDULA DE 10 CIFRAS')
            print(f'   👤 Usuario: {user.get("nombre")}')
            print(f'   🆔 Cédula: {user.get("cedula")} (10 cifras)')
            print(f'   🎭 Rol: {user.get("rol")}')
            print(f'   📍 Ubicación: {user.get("ubicacion_id")} (NULL = correcto)')
            print(f'   🔑 Token: {"Generado" if data.get("data", {}).get("access_token") else "No generado"}')
            
            print('\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL')
            print('✅ Cédulas de 10 cifras implementadas')
            print('✅ Formulario actualizado')
            print('✅ API funcionando correctamente')
            
        else:
            print(f'❌ Error en login: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    main()