#!/usr/bin/env python3
"""
Script para verificar que el campo de cédula aparece cuando se selecciona testigo_electoral
"""
import requests
import webbrowser
import time

def test_cedula_toggle():
    """Probar que el campo de cédula se muestra/oculta correctamente"""
    
    try:
        print('🔍 Probando página de login principal...')
        response = requests.get('http://localhost:5000/login')
        
        if response.status_code == 200:
            html = response.text
            
            # Verificar elementos clave
            checks = [
                ('id="cedulaSection"', 'Sección de cédula'),
                ('style="display: none;"', 'Campo oculto por defecto'),
                ('id="cedula"', 'Campo de input de cédula'),
                ('NÚMERO DE CÉDULA', 'Label de cédula'),
                ('testigo_electoral', 'Opción de testigo en select'),
                ('handleRoleChange', 'Función JavaScript de cambio de rol')
            ]
            
            all_found = True
            for check, description in checks:
                if check in html:
                    print(f'✅ {description}')
                else:
                    print(f'❌ {description} NO encontrado')
                    all_found = False
            
            if all_found:
                print(f'\n🎉 ¡Perfecto! Todos los elementos encontrados')
                print(f'🌐 Abriendo página de login...')
                
                # Abrir en navegador con parámetros para evitar caché
                cache_buster = f'?v={int(time.time())}&nocache=1'
                webbrowser.open(f'http://localhost:5000/login{cache_buster}')
                
                print('\n📝 Instrucciones para probar:')
                print('   1. Seleccione "👤 Testigo Electoral" en el dropdown de Rol')
                print('   2. Debería aparecer un campo naranja para "NÚMERO DE CÉDULA"')
                print('   3. Ingrese una cédula (ej: 12345678)')
                print('   4. Complete la ubicación (departamento, municipio, zona, puesto)')
                print('   5. Use contraseña "test123"')
                print('   6. Haga clic en "Iniciar Sesión"')
                
                return True
            else:
                print(f'❌ Faltan elementos en la página')
        else:
            print(f'❌ Error {response.status_code} cargando página')
                
    except Exception as e:
        print(f'❌ Error conectando: {e}')
    
    return False

if __name__ == '__main__':
    print('🚀 Verificando funcionalidad de campo de cédula dinámico...')
    
    if test_cedula_toggle():
        print('\n✅ Sistema configurado correctamente')
        print('🔄 Si no ve los cambios, presione Ctrl+F5 para forzar recarga')
    else:
        print('\n❌ No se pudo verificar el sistema')