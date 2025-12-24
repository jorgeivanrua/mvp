#!/usr/bin/env python3
"""
Test del endpoint de mesas para verificar por qué no cargan en el frontend
"""

import requests
import json

def test_endpoint_mesas():
    """Probar el endpoint de mesas directamente"""
    print("🔍 PROBANDO ENDPOINT DE MESAS")
    print("=" * 40)
    
    # URL base
    base_url = "http://localhost:5000"
    
    # Obtener zonas para conseguir un puesto
    print("1. 📍 Obteniendo zonas disponibles...")
    try:
        # Primero obtener municipios del departamento 26
        response = requests.get(f"{base_url}/api/locations/municipios/26", timeout=10)
        if response.status_code == 200:
            data = response.json()
            municipios = data.get('data', [])
            if municipios:
                municipio = municipios[0]  # Tomar el primer municipio
                municipio_codigo = municipio['municipio_codigo']
                print(f"   ✅ Municipio encontrado: {municipio_codigo} - {municipio['municipio_nombre']}")
                
                # Obtener zonas del municipio
                zona_response = requests.get(f"{base_url}/api/locations/zonas/{municipio_codigo}", timeout=10)
                if zona_response.status_code == 200:
                    zona_data = zona_response.json()
                    zonas = zona_data.get('data', [])
                    if zonas:
                        zona = zonas[0]  # Tomar la primera zona
                        zona_codigo = zona['zona_codigo']
                        print(f"   ✅ Zona encontrada: {zona_codigo}")
                        
                        # Obtener puestos de la zona
                        puesto_response = requests.get(f"{base_url}/api/locations/puestos/{zona_codigo}", timeout=10)
                        if puesto_response.status_code == 200:
                            puesto_data = puesto_response.json()
                            puestos = puesto_data.get('data', [])
                            if puestos:
                                puesto = puestos[0]  # Tomar el primer puesto
                                puesto_codigo = puesto['puesto_codigo']
                                print(f"   ✅ Puesto encontrado: {puesto_codigo} - {puesto['puesto_nombre']}")
                                
                                # Probar endpoint de mesas
                                print(f"\n2. 🗳️  Probando endpoint de mesas para puesto {puesto_codigo}...")
                                
                                # Probar con query params
                                mesa_url = f"{base_url}/api/locations/mesas?puesto_codigo={puesto_codigo}"
                                print(f"   📡 URL: {mesa_url}")
                                
                                mesa_response = requests.get(mesa_url, timeout=10)
                                print(f"   📊 Status Code: {mesa_response.status_code}")
                                
                                if mesa_response.status_code == 200:
                                    mesa_data = mesa_response.json()
                                    mesas = mesa_data.get('data', [])
                                    
                                    print(f"   ✅ Respuesta exitosa!")
                                    print(f"   📋 Total mesas encontradas: {len(mesas)}")
                                    
                                    if mesas:
                                        print(f"\n   📝 Ejemplos de mesas:")
                                        for i, mesa in enumerate(mesas[:3], 1):
                                            print(f"      {i}. Mesa {mesa['mesa_codigo']} - {mesa['mesa_nombre']}")
                                            print(f"         Votantes: {mesa.get('total_votantes_registrados', 'N/A')}")
                                    else:
                                        print("   ⚠️  No se encontraron mesas para este puesto")
                                        
                                    # Mostrar JSON completo para debug
                                    print(f"\n   🔍 JSON de respuesta (primeras 3 mesas):")
                                    print(json.dumps(mesas[:3], indent=2, ensure_ascii=False))
                                    
                                else:
                                    print(f"   ❌ Error: {mesa_response.status_code}")
                                    print(f"   📄 Respuesta: {mesa_response.text}")
                                    
                            else:
                                print("   ❌ No se encontraron puestos")
                        else:
                            print(f"   ❌ Error obteniendo puestos: {puesto_response.status_code}")
                    else:
                        print("   ❌ No se encontraron zonas")
                else:
                    print(f"   ❌ Error obteniendo zonas: {zona_response.status_code}")
            else:
                print("   ❌ No se encontraron municipios")
        else:
            print(f"   ❌ Error obteniendo municipios: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_endpoints_alternativos():
    """Probar otros endpoints relacionados"""
    print("\n🔍 PROBANDO ENDPOINTS ALTERNATIVOS")
    print("=" * 45)
    
    base_url = "http://localhost:5000"
    
    endpoints = [
        "/api/locations/departamentos",
        "/api/locations/municipios/26",
        "/api/locations/zonas/2601",
        "/api/locations/puestos/260101"
    ]
    
    for endpoint in endpoints:
        print(f"\n📡 Probando: {endpoint}")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('data', [])
                print(f"   ✅ Items encontrados: {len(items)}")
                if items:
                    print(f"   📋 Ejemplo: {items[0].get('departamento_nombre') or items[0].get('municipio_nombre') or items[0].get('zona_codigo') or items[0].get('puesto_nombre', 'N/A')}")
            else:
                print(f"   ❌ Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 TEST DE ENDPOINTS DE UBICACIONES")
    print("=" * 50)
    
    test_endpoint_mesas()
    test_endpoints_alternativos()
    
    print("\n🎯 CONCLUSIONES:")
    print("- Si las mesas aparecen aquí pero no en el frontend,")
    print("  el problema está en el JavaScript del navegador")
    print("- Si no aparecen aquí, el problema está en el backend")
    print("- Revisar la consola del navegador para errores JS")

if __name__ == "__main__":
    main()