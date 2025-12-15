#!/usr/bin/env python3
"""
Script para probar el endpoint del coordinador de puesto directamente
"""

import requests
import json

def test_endpoint():
    print("🔍 PROBANDO ENDPOINT DEL COORDINADOR DE PUESTO")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # 1. Probar login
    print("1. 🔐 Probando login...")
    login_data = {
        "rol": "coordinador_puesto",
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "zona_codigo": "01",
        "puesto_codigo": "01",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            login_result = response.json()
            if login_result.get('success'):
                token = login_result['data']['access_token']
                user = login_result['data']['user']
                print(f"   ✅ Login exitoso")
                print(f"   Usuario: {user['nombre']}")
                print(f"   Rol: {user['rol']}")
                print(f"   Token: {token[:50]}...")
            else:
                print(f"   ❌ Login falló: {login_result.get('error')}")
                return
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return
    
    # 2. Probar endpoint de formularios
    print("\n2. 📋 Probando endpoint de formularios...")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f"{base_url}/api/coordinador-puesto/formularios", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            formularios_result = response.json()
            if formularios_result.get('success'):
                formularios = formularios_result['data']['formularios']
                stats = formularios_result['data']['estadisticas']
                print(f"   ✅ Formularios obtenidos exitosamente")
                print(f"   Total formularios: {len(formularios)}")
                print(f"   Estadísticas: {stats}")
                
                if formularios:
                    form = formularios[0]
                    print(f"   Primer formulario:")
                    print(f"     ID: {form['id']}")
                    print(f"     Mesa: {form['mesa_codigo']}")
                    print(f"     Estado: {form['estado']}")
                    print(f"     Total votos: {form['total_votos']}")
            else:
                print(f"   ❌ Error en respuesta: {formularios_result.get('error')}")
                return
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return
    
    # 3. Probar endpoint específico del formulario
    print("\n3. 📄 Probando endpoint específico del formulario...")
    
    try:
        response = requests.get(f"{base_url}/api/coordinador-puesto/formularios/1", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            formulario_result = response.json()
            if formulario_result.get('success'):
                formulario = formulario_result['data']
                print(f"   ✅ Formulario específico obtenido exitosamente")
                print(f"   ID: {formulario['id']}")
                print(f"   Mesa: {formulario['mesa']['codigo']} - {formulario['mesa']['nombre']}")
                print(f"   Testigo: {formulario['testigo']['nombre'] if formulario['testigo'] else 'N/A'}")
                print(f"   Total votos: {formulario['total_votos']}")
                print(f"   Imagen URL: {formulario['imagen_url']}")
                print(f"   Votos por partido: {len(formulario.get('votos_partidos', []))}")
                print(f"   Votos por candidatos: {len(formulario.get('votos_candidatos', []))}")
                
                # Mostrar detalles de votos
                if formulario.get('votos_partidos'):
                    print(f"   Partidos:")
                    for vp in formulario['votos_partidos']:
                        print(f"     - {vp['partido_nombre']}: {vp['votos']} votos")
                
                if formulario.get('votos_candidatos'):
                    print(f"   Candidatos:")
                    for vc in formulario['votos_candidatos']:
                        print(f"     - {vc['candidato_nombre']}: {vc['votos']} votos")
                        
            else:
                print(f"   ❌ Error en respuesta: {formulario_result.get('error')}")
                return
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return
    
    # 4. Probar imagen
    print("\n4. 🖼️ Probando acceso a imagen...")
    
    try:
        response = requests.get(f"{base_url}/static/images/sample-e14.svg")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Imagen accesible")
            print(f"   Content-Type: {response.headers.get('Content-Type')}")
            print(f"   Tamaño: {len(response.content)} bytes")
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 PRUEBAS COMPLETADAS")
    print("\n✅ Si todas las pruebas pasaron, el backend funciona correctamente.")
    print("   El problema debe estar en el frontend o en la autenticación del navegador.")

if __name__ == "__main__":
    test_endpoint()