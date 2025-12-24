#!/usr/bin/env python3
"""
Test para verificar que los votantes registrados se cargan correctamente
"""
import requests
import json

def test_carga_votantes():
    base_url = 'http://localhost:5000'
    
    # Login del testigo
    login_data = {
        'rol': 'testigo_electoral',
        'cedula': '1000000001',
        'password': 'test123'
    }
    
    try:
        print('🔐 Haciendo login...')
        response = requests.post(f'{base_url}/api/auth/login', json=login_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            token = data['data']['access_token']
            print('✅ Login exitoso')
            
            # Obtener mesas del puesto (esto es lo que carga el selector)
            print('📋 Obteniendo mesas del puesto...')
            mesa_response = requests.get(
                f'{base_url}/api/locations/mesas/26010101',
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            
            if mesa_response.status_code == 200:
                mesa_data = mesa_response.json()
                mesas = mesa_data.get('data', [])
                
                print('✅ MESAS DISPONIBLES PARA EL SELECTOR:')
                print('=' * 50)
                
                for i, mesa in enumerate(mesas[:3]):  # Mostrar solo las primeras 3
                    print(f'Mesa {i+1}:')
                    print(f'  ID: {mesa["id"]}')
                    print(f'  Código: {mesa["mesa_codigo"]}')
                    print(f'  Nombre: {mesa["mesa_nombre"]}')
                    print(f'  🗳️ Votantes Registrados: {mesa.get("total_votantes_registrados", "N/A")}')
                    print(f'  👥 Mujeres: {mesa.get("mujeres", "N/A")}')
                    print(f'  👥 Hombres: {mesa.get("hombres", "N/A")}')
                    print()
                
                print(f'📊 Total de mesas en el puesto: {len(mesas)}')
                
                # Verificar que todas las mesas tienen votantes registrados
                mesas_con_votantes = [m for m in mesas if m.get('total_votantes_registrados', 0) > 0]
                print(f'✅ Mesas con votantes registrados: {len(mesas_con_votantes)}/{len(mesas)}')
                
                if len(mesas_con_votantes) == len(mesas):
                    print('🎉 ¡PERFECTO! Todas las mesas tienen datos de votantes registrados')
                    print('   La función cambiarMesaFormulario() debería cargar automáticamente estos datos')
                    return True
                else:
                    print('⚠️ Algunas mesas no tienen datos de votantes registrados')
                    return False
                    
            else:
                print(f'❌ Error obteniendo mesas: {mesa_response.status_code}')
                print(mesa_response.text)
                return False
        else:
            print(f'❌ Error en login: {response.status_code}')
            print(response.text)
            return False
            
    except Exception as e:
        print(f'❌ Error: {e}')
        return False

if __name__ == '__main__':
    test_carga_votantes()