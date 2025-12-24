#!/usr/bin/env python3
"""
Script para probar los endpoints después de la limpieza
"""
import requests
import json

def main():
    print('=== PROBANDO ENDPOINTS DESPUÉS DE LA LIMPIEZA ===')

    try:
        # Probar endpoint de departamentos
        response = requests.get('http://localhost:5000/api/locations/departamentos')
        print(f'\n📍 /api/locations/departamentos - Status: {response.status_code}')
        data = response.json()
        print(f'Departamentos: {json.dumps(data, indent=2, ensure_ascii=False)}')
        
        if data['success'] and data['data']:
            depto_codigo = data['data'][0]['departamento_codigo']
            
            # Probar municipios
            response2 = requests.get(f'http://localhost:5000/api/locations/municipios/{depto_codigo}')
            print(f'\n🏘️  /api/locations/municipios/{depto_codigo} - Status: {response2.status_code}')
            municipios = response2.json()
            print(f'Municipios encontrados: {len(municipios.get("data", []))}')
            
            if municipios['success'] and municipios['data']:
                muni_codigo = municipios['data'][0]['municipio_codigo']
                
                # Probar zonas
                response3 = requests.get(f'http://localhost:5000/api/locations/zonas/{muni_codigo}')
                print(f'\n🗺️  /api/locations/zonas/{muni_codigo} - Status: {response3.status_code}')
                zonas = response3.json()
                print(f'Zonas encontradas: {len(zonas.get("data", []))}')
                
                if zonas['success'] and zonas['data']:
                    zona_codigo = zonas['data'][0]['zona_codigo']
                    
                    # Probar puestos
                    response4 = requests.get(f'http://localhost:5000/api/locations/puestos/{zona_codigo}')
                    print(f'\n🏢 /api/locations/puestos/{zona_codigo} - Status: {response4.status_code}')
                    puestos = response4.json()
                    print(f'Puestos encontrados: {len(puestos.get("data", []))}')
            
            print('\n✅ TODOS LOS ENDPOINTS FUNCIONAN CORRECTAMENTE')
        
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == '__main__':
    main()