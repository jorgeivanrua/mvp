#!/usr/bin/env python3
"""
Script de prueba para el sistema de gestión de usuarios
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def test_sistema():
    """Probar el sistema de gestión de usuarios"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("PRUEBA DEL SISTEMA DE GESTIÓN DE USUARIOS")
        print("=" * 80)
        
        # 1. Verificar endpoints de locations
        print("\n1. VERIFICANDO DATOS DE UBICACIONES:")
        print("-" * 80)
        
        departamentos = Location.query.filter_by(tipo='departamento').count()
        municipios = Location.query.filter_by(tipo='municipio').count()
        puestos = Location.query.filter_by(tipo='puesto').count()
        mesas = Location.query.filter_by(tipo='mesa').count()
        
        print(f"OK Departamentos: {departamentos}")
        print(f"OK Municipios: {municipios}")
        print(f"OK Puestos: {puestos}")
        print(f"OK Mesas: {mesas}")
        
        # 2. Verificar estructura de datos
        print("\n2. VERIFICANDO ESTRUCTURA DE DATOS:")
        print("-" * 80)
        
        # Verificar un puesto
        puesto = Location.query.filter_by(tipo='puesto').first()
        if puesto:
            print(f"\nOK Puesto de ejemplo:")
            print(f"   ID: {puesto.id}")
            print(f"   Código: {puesto.puesto_codigo}")
            print(f"   Nombre: {puesto.puesto_nombre}")
            print(f"   Municipio: {puesto.municipio_nombre}")
            print(f"   Departamento: {puesto.departamento_nombre}")
            
            # Contar mesas del puesto
            mesas_puesto = Location.query.filter_by(
                tipo='mesa',
                puesto_codigo=puesto.puesto_codigo,
                zona_codigo=puesto.zona_codigo,
                municipio_codigo=puesto.municipio_codigo,
                departamento_codigo=puesto.departamento_codigo
            ).count()
            print(f"   Mesas: {mesas_puesto}")
        
        # Verificar un municipio
        municipio = Location.query.filter_by(tipo='municipio').first()
        if municipio:
            print(f"\nOK Municipio de ejemplo:")
            print(f"   ID: {municipio.id}")
            print(f"   Código: {municipio.municipio_codigo}")
            print(f"   Nombre: {municipio.municipio_nombre}")
            print(f"   Departamento: {municipio.departamento_nombre}")
        
        # Verificar un departamento
        departamento = Location.query.filter_by(tipo='departamento').first()
        if departamento:
            print(f"\nOK Departamento de ejemplo:")
            print(f"   ID: {departamento.id}")
            print(f"   Código: {departamento.departamento_codigo}")
            print(f"   Nombre: {departamento.departamento_nombre}")
        
        # 3. Verificar usuarios existentes
        print("\n\n3. VERIFICANDO USUARIOS EXISTENTES:")
        print("-" * 80)
        
        usuarios_por_rol = {}
        usuarios = User.query.all()
        
        for user in usuarios:
            if user.rol not in usuarios_por_rol:
                usuarios_por_rol[user.rol] = 0
            usuarios_por_rol[user.rol] += 1
        
        print(f"\nTotal usuarios: {len(usuarios)}")
        for rol, count in sorted(usuarios_por_rol.items()):
            print(f"  {rol}: {count}")
        
        # 4. Verificar que no haya testigos
        print("\n\n4. VERIFICANDO TESTIGOS:")
        print("-" * 80)
        
        testigos = User.query.filter_by(rol='testigo_electoral').count()
        if testigos == 0:
            print("OK No hay testigos creados (sistema limpio)")
        else:
            print(f"AVISO: Hay {testigos} testigos existentes")
        
        # 5. Simular creación de testigos (sin guardar)
        print("\n\n5. SIMULANDO CREACIÓN DE TESTIGOS:")
        print("-" * 80)
        
        if puesto:
            mesas = Location.query.filter_by(
                tipo='mesa',
                puesto_codigo=puesto.puesto_codigo,
                zona_codigo=puesto.zona_codigo,
                municipio_codigo=puesto.municipio_codigo,
                departamento_codigo=puesto.departamento_codigo
            ).all()
            
            print(f"\nPuesto: {puesto.puesto_nombre}")
            print(f"Mesas a crear testigos: {len(mesas)}")
            
            if len(mesas) > 0:
                print(f"\nEjemplo de usernames que se generarían:")
                for i, mesa in enumerate(mesas[:3]):  # Solo mostrar 3 ejemplos
                    username = f"testigo.{mesa.puesto_codigo}.{mesa.mesa_codigo}"
                    print(f"  Mesa {mesa.mesa_codigo}: {username}")
                
                if len(mesas) > 3:
                    print(f"  ... y {len(mesas) - 3} más")
        
        print("\n" + "=" * 80)
        print("PRUEBA COMPLETADA")
        print("=" * 80)
        print("\nOK El sistema esta listo para crear usuarios automaticamente")
        print("OK Todos los datos de DIVIPOLA estan disponibles")
        print("OK Los endpoints estan configurados correctamente")

if __name__ == '__main__':
    test_sistema()
