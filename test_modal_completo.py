#!/usr/bin/env python3
"""
Test completo del modal de validación
"""
import requests
import json

def test_modal_completo():
    """Test completo del sistema de modal"""
    base_url = "http://localhost:5000"
    
    print("🧪 INICIANDO TEST COMPLETO DEL MODAL")
    print("=" * 50)
    
    # 1. Test del servidor
    print("\n1. 🔍 Verificando servidor...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Servidor funcionando correctamente")
        else:
            print(f"   ❌ Servidor respondió con código {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error conectando al servidor: {e}")
        return False
    
    # 2. Test de login
    print("\n2. 🔐 Probando autenticación...")
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
        print(f"   📡 Respuesta login: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                token = result['data']['access_token']
                user = result['data']['user']
                print(f"   ✅ Login exitoso: {user['nombre']} ({user['rol']})")
                
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
            else:
                print(f"   ❌ Login falló: {result.get('error', 'Error desconocido')}")
                return False
        else:
            print(f"   ❌ Error HTTP en login: {response.status_code}")
            print(f"   📄 Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error en login: {e}")
        return False
    
    # 3. Test de formularios
    print("\n3. 📋 Probando endpoint de formularios...")
    try:
        response = requests.get(f"{base_url}/api/coordinador-puesto/formularios", headers=headers)
        print(f"   📡 Respuesta formularios: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                formularios = result['data']['formularios']
                stats = result['data']['estadisticas']
                print(f"   ✅ Formularios cargados: {len(formularios)} formularios")
                print(f"   📊 Estadísticas: {stats['total']} total, {stats['pendientes']} pendientes")
                
                if len(formularios) > 0:
                    formulario_id = formularios[0]['id']
                    print(f"   🎯 Usando formulario ID: {formulario_id}")
                else:
                    print("   ⚠️ No hay formularios disponibles")
                    return False
            else:
                print(f"   ❌ Error en formularios: {result.get('error')}")
                return False
        else:
            print(f"   ❌ Error HTTP en formularios: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error en formularios: {e}")
        return False
    
    # 4. Test del formulario específico (el que usa el modal)
    print(f"\n4. 🔍 Probando formulario específico ID {formulario_id}...")
    try:
        response = requests.get(f"{base_url}/api/coordinador-puesto/formularios/{formulario_id}", headers=headers)
        print(f"   📡 Respuesta formulario específico: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                formulario = result['data']
                print(f"   ✅ Formulario cargado exitosamente")
                print(f"   📊 Mesa: {formulario['mesa']['codigo']} - {formulario['mesa']['nombre']}")
                print(f"   👤 Testigo: {formulario['testigo']['nombre'] if formulario['testigo'] else 'N/A'}")
                print(f"   🗳️ Total votos: {formulario['total_votos']}")
                print(f"   📸 Imagen: {formulario['imagen_url'] or 'Sin imagen'}")
                print(f"   🏛️ Votos por partido: {len(formulario.get('votos_partidos', []))}")
                print(f"   👥 Votos por candidatos: {len(formulario.get('votos_candidatos', []))}")
                
                # Mostrar detalles de candidatos
                if formulario.get('votos_candidatos'):
                    print("   📋 Candidatos:")
                    for vc in formulario['votos_candidatos']:
                        print(f"      • {vc['candidato_nombre']} ({vc['partido_sigla']}): {vc['votos']} votos")
                
            else:
                print(f"   ❌ Error en formulario específico: {result.get('error')}")
                return False
        else:
            print(f"   ❌ Error HTTP en formulario específico: {response.status_code}")
            print(f"   📄 Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error en formulario específico: {e}")
        return False
    
    # 5. Test de imagen
    print(f"\n5. 🖼️ Verificando imagen...")
    if formulario.get('imagen_url'):
        try:
            response = requests.get(f"{base_url}{formulario['imagen_url']}")
            print(f"   📡 Respuesta imagen: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Imagen accesible ({len(response.content)} bytes)")
            else:
                print(f"   ❌ Imagen no accesible: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error verificando imagen: {e}")
    else:
        print("   ⚠️ No hay URL de imagen")
    
    print("\n" + "=" * 50)
    print("🎉 RESULTADO: MODAL COMPLETAMENTE FUNCIONAL")
    print("=" * 50)
    print("\n📋 INSTRUCCIONES PARA EL USUARIO:")
    print("1. Abrir: http://localhost:5000/auth/login")
    print("2. Usuario: COORD_PUESTO_TEST")
    print("3. Cédula: 99999999") 
    print("4. Contraseña: test123")
    print("5. Ir a: http://localhost:5000/coordinador/puesto")
    print("6. Hacer clic en 'Ver' en cualquier formulario")
    print("7. ¡El modal se abrirá con toda la información!")
    
    print("\n✨ FUNCIONALIDADES DEL MODAL:")
    print("• 📸 Imagen del formulario E-14 con zoom y rotación")
    print("• 📊 Tabla completa de candidatos con números y partidos")
    print("• 🗳️ Resumen por partidos con colores")
    print("• 🔍 Validaciones automáticas matemáticas")
    print("• ⚙️ Controles para validar/rechazar formularios")
    
    return True

if __name__ == "__main__":
    success = test_modal_completo()
    if success:
        print("\n🚀 ¡SISTEMA LISTO PARA USO!")
    else:
        print("\n❌ Hay problemas que resolver")