#!/usr/bin/env python3
"""
Script para verificar que el campo de cédula es visible en la nueva URL
"""
import requests
import webbrowser
import time

def test_and_open():
    """Probar la página y abrirla en el navegador"""
    
    # URLs a probar
    urls = [
        'http://localhost:5000/testigo-login-cedula',
        'http://localhost:5000/login-testigo'
    ]
    
    for url in urls:
        try:
            print(f'\n🔍 Probando: {url}')
            response = requests.get(url)
            
            if response.status_code == 200:
                html = response.text
                
                # Verificar elementos clave
                checks = [
                    ('INGRESE SU NÚMERO DE CÉDULA', 'Label principal'),
                    ('id="cedula"', 'Campo de input'),
                    ('placeholder="Ejemplo: 12345678"', 'Placeholder'),
                    ('background: linear-gradient(135deg, #ff6b35', 'Estilo naranja'),
                    ('font-size: 2rem', 'Texto grande')
                ]
                
                all_found = True
                for check, description in checks:
                    if check in html:
                        print(f'✅ {description}')
                    else:
                        print(f'❌ {description} NO encontrado')
                        all_found = False
                
                if all_found:
                    print(f'\n🎉 ¡Perfecto! Todos los elementos encontrados en {url}')
                    print(f'🌐 Abriendo en navegador...')
                    
                    # Abrir en navegador con parámetros para evitar caché
                    cache_buster = f'?v={int(time.time())}&nocache=1'
                    webbrowser.open(f'{url}{cache_buster}')
                    
                    return True
                else:
                    print(f'❌ Faltan elementos en {url}')
            else:
                print(f'❌ Error {response.status_code} en {url}')
                
        except Exception as e:
            print(f'❌ Error conectando a {url}: {e}')
    
    return False

if __name__ == '__main__':
    print('🚀 Verificando campo de cédula...')
    
    if test_and_open():
        print('\n✅ Campo de cédula verificado y página abierta')
        print('📝 Instrucciones:')
        print('   1. Si no ve el campo naranja, presione Ctrl+F5 para forzar recarga')
        print('   2. O cierre y abra el navegador completamente')
        print('   3. El campo debe aparecer con fondo naranja y texto grande')
    else:
        print('\n❌ No se pudo verificar el campo de cédula')