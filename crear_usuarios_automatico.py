#!/usr/bin/env python3
"""
Script para crear usuarios automáticamente basados en DIVIPOLA
Crea testigos para todas las mesas de un puesto específico
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
import secrets
import string

def generar_password_seguro(longitud=12):
    """Generar contraseña segura"""
    caracteres = string.ascii_letters + string.digits + "!@#$%&*"
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def generar_username(rol, ubicacion):
    """Generar username basado en rol y ubicación"""
    prefijos = {
        'testigo_electoral': 'testigo',
        'coordinador_puesto': 'coord.puesto',
        'coordinador_municipal': 'coord.mun',
        'coordinador_departamental': 'coord.dept',
        'admin_municipal': 'admin.mun',
        'admin_departamental': 'admin.dept'
    }
    
    prefijo = prefijos.get(rol, rol)
    
    if ubicacion.tipo == 'mesa':
        return f"{prefijo}.{ubicacion.puesto_codigo}.{ubicacion.mesa_codigo}"
    elif ubicacion.tipo == 'puesto':
        return f"{prefijo}.{ubicacion.puesto_codigo}"
    elif ubicacion.tipo == 'municipio':
        return f"{prefijo}.{ubicacion.municipio_codigo}"
    elif ubicacion.tipo == 'departamento':
        return f"{prefijo}.{ubicacion.departamento_codigo}"
    
    return f"{prefijo}.{ubicacion.id}"

def crear_testigos_puesto(puesto_codigo):
    """Crear testigos para todas las mesas de un puesto"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print(f"CREANDO TESTIGOS PARA PUESTO: {puesto_codigo}")
        print("=" * 80)
        
        # Buscar el puesto
        puesto = Location.query.filter_by(
            tipo='puesto',
            puesto_codigo=puesto_codigo
        ).first()
        
        if not puesto:
            print(f"❌ Puesto {puesto_codigo} no encontrado")
            return
        
        print(f"\n✅ Puesto encontrado: {puesto.nombre_completo}")
        
        # Obtener todas las mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            puesto_codigo=puesto.puesto_codigo,
            zona_codigo=puesto.zona_codigo,
            municipio_codigo=puesto.municipio_codigo,
            departamento_codigo=puesto.departamento_codigo
        ).all()
        
        print(f"📊 Total mesas en el puesto: {len(mesas)}")
        
        if not mesas:
            print("❌ No se encontraron mesas para este puesto")
            return
        
        testigos_creados = []
        testigos_existentes = []
        
        for mesa in mesas:
            # Verificar si ya existe un testigo para esta mesa
            testigo_existente = User.query.filter_by(
                rol='testigo_electoral',
                ubicacion_id=mesa.id
            ).first()
            
            if testigo_existente:
                testigos_existentes.append({
                    'username': testigo_existente.nombre,
                    'mesa': mesa.mesa_codigo
                })
                continue
            
            # Crear nuevo testigo
            username = generar_username('testigo_electoral', mesa)
            password = generar_password_seguro()
            
            testigo = User(
                nombre=username,
                rol='testigo_electoral',
                ubicacion_id=mesa.id,
                activo=True
            )
            testigo.set_password(password)
            
            db.session.add(testigo)
            
            testigos_creados.append({
                'username': username,
                'password': password,
                'mesa': mesa.mesa_codigo,
                'votantes': mesa.total_votantes_registrados
            })
        
        db.session.commit()
        
        print("\n" + "=" * 80)
        print("RESUMEN")
        print("=" * 80)
        print(f"✅ Testigos creados: {len(testigos_creados)}")
        print(f"⚠️  Testigos ya existentes: {len(testigos_existentes)}")
        
        if testigos_creados:
            print("\n📋 CREDENCIALES DE TESTIGOS CREADOS:")
            print("-" * 80)
            for t in testigos_creados:
                print(f"\nMesa: {t['mesa']}")
                print(f"  Username: {t['username']}")
                print(f"  Password: {t['password']}")
                print(f"  Votantes: {t['votantes']}")
        
        if testigos_existentes:
            print("\n⚠️  TESTIGOS YA EXISTENTES:")
            print("-" * 80)
            for t in testigos_existentes:
                print(f"  Mesa {t['mesa']}: {t['username']}")
        
        # Guardar credenciales en archivo
        if testigos_creados:
            filename = f"credenciales_testigos_{puesto_codigo}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"CREDENCIALES TESTIGOS - PUESTO {puesto_codigo}\n")
                f.write(f"Puesto: {puesto.nombre_completo}\n")
                f.write("=" * 80 + "\n\n")
                
                for t in testigos_creados:
                    f.write(f"Mesa: {t['mesa']}\n")
                    f.write(f"Username: {t['username']}\n")
                    f.write(f"Password: {t['password']}\n")
                    f.write(f"Votantes Registrados: {t['votantes']}\n")
                    f.write("-" * 80 + "\n\n")
            
            print(f"\n💾 Credenciales guardadas en: {filename}")

def listar_puestos():
    """Listar todos los puestos disponibles"""
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("PUESTOS DISPONIBLES")
        print("=" * 80)
        
        puestos = Location.query.filter_by(tipo='puesto').all()
        
        print(f"\nTotal puestos: {len(puestos)}\n")
        
        for puesto in puestos:
            # Contar mesas
            mesas = Location.query.filter_by(
                tipo='mesa',
                puesto_codigo=puesto.puesto_codigo,
                zona_codigo=puesto.zona_codigo,
                municipio_codigo=puesto.municipio_codigo,
                departamento_codigo=puesto.departamento_codigo
            ).count()
            
            # Contar testigos existentes
            testigos = 0
            for mesa in Location.query.filter_by(
                tipo='mesa',
                puesto_codigo=puesto.puesto_codigo,
                zona_codigo=puesto.zona_codigo,
                municipio_codigo=puesto.municipio_codigo,
                departamento_codigo=puesto.departamento_codigo
            ).all():
                if User.query.filter_by(rol='testigo_electoral', ubicacion_id=mesa.id).first():
                    testigos += 1
            
            print(f"Código: {puesto.puesto_codigo}")
            print(f"  Nombre: {puesto.puesto_nombre}")
            print(f"  Municipio: {puesto.municipio_nombre}")
            print(f"  Mesas: {mesas}")
            print(f"  Testigos: {testigos}/{mesas}")
            print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python crear_usuarios_automatico.py listar")
        print("  python crear_usuarios_automatico.py crear <codigo_puesto>")
        print("\nEjemplo:")
        print("  python crear_usuarios_automatico.py listar")
        print("  python crear_usuarios_automatico.py crear 001")
        sys.exit(1)
    
    comando = sys.argv[1]
    
    if comando == 'listar':
        listar_puestos()
    elif comando == 'crear' and len(sys.argv) >= 3:
        puesto_codigo = sys.argv[2]
        crear_testigos_puesto(puesto_codigo)
    else:
        print("Comando no válido")
        sys.exit(1)
