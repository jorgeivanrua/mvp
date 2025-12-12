#!/usr/bin/env python3
"""
Script para verificar que el campo de cédula aparece en la página de login
"""
import requests

def test_cedula_field():
    """Verificar que el campo de cédula está presente"""
    try:
        response = requests.get('http://localhost:5000/login-testigo')
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            html = response.text
            
            # Verificar elementos clave
            checks = [
                ('id="cedula"', 'Campo de cédula'),
                ('NÚMERO DE CÉDULA', 'Label de cédula'),
                ('placeholder="Ingrese su número de cédula', 'Placeholder de cédula'),
                ('cedula-input', 'Clase CSS de cédula'),
                ('<form id="testigoLoginForm">', 'Formulario de testigo')
            ]
            
            for check, description in checks:
                if check in html:
                    print(f'✅ {description} encontrado')
                else:
                    print(f'❌ {description} NO encontrado')
            
            # Mostrar parte del formulario
            print('\n--- Extracto del formulario ---')
            start = html.find('<form')
            if start != -1:
                end = html.find('</form>', start) + 7
                form_html = html[start:end]
                
                # Buscar específicamente el campo de cédula
                cedula_start = form_html.find('id="cedula"')
                if cedula_start != -1:
                    # Mostrar contexto alrededor del campo
                    context_start = max(0, cedula_start - 200)
                    context_end = min(len(form_html), cedula_start + 300)
                    print(form_html[context_start:context_end])
                else:
                    print('Campo de cédula no encontrado en el formulario')
            else:
                print('Formulario no encontrado')
                
        else:
            print(f'❌ Error cargando página: {response.status_code}')
            
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == '__main__':
    test_cedula_field()