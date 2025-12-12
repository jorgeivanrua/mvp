#!/usr/bin/env python3
"""
Script para probar el login con cédula directamente
"""
import requests
import json

def test_login_cedula():
    """Probar login con cédula"""
    
    # Datos de prueba
    cedula = "12345678"
    
    try:
        print(f'🔐 Probando login con cédula: {cedula}')
        
        # Probar endpoint de testigos registrados
        response = requests.post('http://localhost:5000/api/testigos-registrados/login-cedula-simple', 
                               json={'cedula': cedula})
        
        print(f'Status: {response.status_code}')
        print(f'Response: {response.text}')
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print('✅ Login exitoso!')
                print(f"Usuario: {data.get('user', {}).get('nombre', 'N/A')}")
                return True
            else:
                print(f'❌ Login falló: {data.get("error", "Error desconocido")}')
        else:
            print(f'❌ Error HTTP: {response.status_code}')
            
    except Exception as e:
        print(f'❌ Error: {e}')
    
    return False

if __name__ == '__main__':
    print('🚀 Probando login de testigo con cédula...')
    
    # Primero verificar que el servidor esté corriendo
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print('✅ Servidor está corriendo')
            test_login_cedula()
        else:
            print('❌ Servidor no responde correctamente')
    except:
        print('❌ No se puede conectar al servidor')
        print('💡 Asegúrese de que el servidor esté corriendo con: python run.py')