#!/usr/bin/env python3
"""
Script para verificar que el formulario E-14 carga correctamente
la mesa del testigo y los votantes registrados
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def verificar_formulario_e14():
    """Verificar configuración del formulario E-14"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("VERIFICACIÓN DEL FORMULARIO E-14")
        print("=" * 80)
        
        # 1. Verificar testigos y sus mesas
        print("\n1. TESTIGOS Y SUS MESAS ASIGNADAS:")
        print("-" * 80)
        
        testigos = User.query.filter_by(rol='testigo').all()
        print(f"Total testigos: {len(testigos)}")
        
        for testigo in testigos:
            mesa = Location.query.get(testigo.ubicacion_id)
            if mesa:
                print(f"\n  Testigo: {testigo.username}")
                print(f"  Mesa ID: {mesa.id}")
                print(f"  Mesa Código: {mesa.mesa_codigo}")
                print(f"  Puesto: {mesa.puesto_nombre}")
                print(f"  Votantes Registrados: {mesa.total_votantes_registrados}")
                print(f"  Municipio: {mesa.municipio_nombre}")
            else:
                print(f"\n  ⚠️  Testigo {testigo.username} NO tiene mesa asignada")
        
        # 2. Verificar que todas las mesas tengan votantes registrados
        print("\n\n2. VERIFICACIÓN DE VOTANTES REGISTRADOS:")
        print("-" * 80)
        
        mesas_sin_votantes = Location.query.filter(
            Location.tipo == 'mesa',
            (Location.total_votantes_registrados == None) | 
            (Location.total_votantes_registrados == 0)
        ).all()
        
        if mesas_sin_votantes:
            print(f"⚠️  {len(mesas_sin_votantes)} mesas SIN votantes registrados:")
            for mesa in mesas_sin_votantes[:5]:  # Mostrar solo las primeras 5
                print(f"  - Mesa {mesa.mesa_codigo}: {mesa.total_votantes_registrados}")
        else:
            print("✅ Todas las mesas tienen votantes registrados")
        
        # 3. Estadísticas generales
        print("\n\n3. ESTADÍSTICAS GENERALES:")
        print("-" * 80)
        
        total_mesas = Location.query.filter_by(tipo='mesa').count()
        mesas_con_votantes = Location.query.filter(
            Location.tipo == 'mesa',
            Location.total_votantes_registrados > 0
        ).count()
        
        print(f"Total mesas: {total_mesas}")
        print(f"Mesas con votantes: {mesas_con_votantes}")
        print(f"Porcentaje: {(mesas_con_votantes/total_mesas*100):.1f}%")
        
        # Promedio de votantes por mesa
        from sqlalchemy import func
        avg_votantes = db.session.query(
            func.avg(Location.total_votantes_registrados)
        ).filter(
            Location.tipo == 'mesa',
            Location.total_votantes_registrados > 0
        ).scalar()
        
        print(f"Promedio votantes por mesa: {avg_votantes:.1f}")
        
        # 4. Verificar archivos JavaScript
        print("\n\n4. VERIFICACIÓN DE ARCHIVOS JAVASCRIPT:")
        print("-" * 80)
        
        js_file = 'frontend/static/js/testigo-dashboard-new.js'
        if os.path.exists(js_file):
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Verificar funciones clave
            funciones = [
                'showCreateForm',
                'cambiarMesaFormulario',
                'mesaFormulario',
                'votantesRegistrados'
            ]
            
            for funcion in funciones:
                if funcion in content:
                    print(f"  ✅ '{funcion}' encontrado")
                else:
                    print(f"  ❌ '{funcion}' NO encontrado")
        else:
            print(f"  ❌ Archivo {js_file} no existe")
        
        # 5. Verificar template HTML
        print("\n\n5. VERIFICACIÓN DE TEMPLATE HTML:")
        print("-" * 80)
        
        html_file = 'frontend/templates/testigo/dashboard.html'
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar elementos clave
            elementos = [
                'id="mesaFormulario"',
                'id="votantesRegistrados"',
                'onchange="cambiarMesaFormulario()"',
                'readonly'
            ]
            
            for elemento in elementos:
                if elemento in content:
                    print(f"  ✅ '{elemento}' encontrado")
                else:
                    print(f"  ❌ '{elemento}' NO encontrado")
        else:
            print(f"  ❌ Archivo {html_file} no existe")
        
        print("\n" + "=" * 80)
        print("VERIFICACIÓN COMPLETADA")
        print("=" * 80)

if __name__ == '__main__':
    verificar_formulario_e14()
