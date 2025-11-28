#!/usr/bin/env python3
"""
Script para verificar y cargar todos los datos necesarios en la BD
Ejecutar: python scripts/verificar_y_cargar_datos_completo.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.models.configuracion_electoral import Partido, Candidato

def verificar_divipola():
    """Verificar datos DIVIPOLA"""
    print("\n" + "="*70)
    print("VERIFICANDO DATOS DIVIPOLA")
    print("="*70)
    
    total = Location.query.count()
    departamentos = Location.query.filter_by(tipo='departamento').count()
    municipios = Location.query.filter_by(tipo='municipio').count()
    zonas = Location.query.filter_by(tipo='zona').count()
    puestos = Location.query.filter_by(tipo='puesto').count()
    
    print(f"\n📊 Ubicaciones en BD:")
    print(f"  Total: {total}")
    print(f"  Departamentos: {departamentos}")
    print(f"  Municipios: {municipios}")
    print(f"  Zonas: {zonas}")
    print(f"  Puestos: {puestos}")
    
    if total == 0:
        print("\n❌ NO HAY DATOS DIVIPOLA")
        print("   Ejecutar: python scripts/cargar_divipola_v2.py")
        return False
    else:
        print("\n✅ Datos DIVIPOLA cargados correctamente")
        return True

def verificar_partidos():
    """Verificar partidos políticos"""
    print("\n" + "="*70)
    print("VERIFICANDO PARTIDOS POLÍTICOS")
    print("="*70)
    
    total = Partido.query.count()
    activos = Partido.query.filter_by(activo=True).count()
    con_logo = Partido.query.filter(Partido.logo_url.isnot(None)).count()
    
    print(f"\n📊 Partidos en BD:")
    print(f"  Total: {total}")
    print(f"  Activos: {activos}")
    print(f"  Con logo: {con_logo}")
    
    if total == 0:
        print("\n❌ NO HAY PARTIDOS")
        print("   Ejecutar: python scripts/cargar_partidos_candidatos.py")
        return False
    else:
        print("\n✅ Partidos cargados correctamente")
        
        # Mostrar algunos partidos
        partidos = Partido.query.limit(5).all()
        print("\n   Ejemplos:")
        for p in partidos:
            logo_status = "✓" if p.logo_url else "✗"
            print(f"   [{logo_status}] {p.nombre} ({p.codigo})")
        
        return True

def verificar_candidatos():
    """Verificar candidatos"""
    print("\n" + "="*70)
    print("VERIFICANDO CANDIDATOS")
    print("="*70)
    
    total = Candidato.query.count()
    activos = Candidato.query.filter_by(activo=True).count()
    
    print(f"\n📊 Candidatos en BD:")
    print(f"  Total: {total}")
    print(f"  Activos: {activos}")
    
    if total == 0:
        print("\n❌ NO HAY CANDIDATOS")
        print("   Ejecutar: python scripts/cargar_partidos_candidatos.py")
        return False
    else:
        print("\n✅ Candidatos cargados correctamente")
        
        # Mostrar algunos candidatos
        candidatos = Candidato.query.limit(5).all()
        print("\n   Ejemplos:")
        for c in candidatos:
            partido = Partido.query.get(c.partido_id) if c.partido_id else None
            partido_nombre = partido.nombre_corto if partido else "Independiente"
            print(f"   - {c.nombre_completo} ({partido_nombre})")
        
        return True

def verificar_usuarios():
    """Verificar usuarios del sistema"""
    print("\n" + "="*70)
    print("VERIFICANDO USUARIOS DEL SISTEMA")
    print("="*70)
    
    total = User.query.count()
    activos = User.query.filter_by(activo=True).count()
    
    print(f"\n📊 Usuarios en BD:")
    print(f"  Total: {total}")
    print(f"  Activos: {activos}")
    
    # Por rol
    roles = [
        'super_admin',
        'monitoreo',
        'auditor_electoral',
        'coordinador_departamental',
        'coordinador_municipal',
        'coordinador_puesto',
        'testigo_electoral'
    ]
    
    print("\n   Por rol:")
    for rol in roles:
        count = User.query.filter_by(rol=rol, activo=True).count()
        if count > 0:
            print(f"   - {rol}: {count}")
    
    if total == 0:
        print("\n❌ NO HAY USUARIOS")
        print("   Ejecutar: python scripts/create_sample_users.py")
        return False
    else:
        print("\n✅ Usuarios cargados correctamente")
        return True

def verificar_testigos():
    """Verificar testigos electorales"""
    print("\n" + "="*70)
    print("VERIFICANDO TESTIGOS ELECTORALES")
    print("="*70)
    
    total = User.query.filter_by(rol='testigo_electoral', activo=True).count()
    con_ubicacion = User.query.filter(
        User.rol == 'testigo_electoral',
        User.activo == True,
        User.ubicacion_id.isnot(None)
    ).count()
    
    print(f"\n📊 Testigos en BD:")
    print(f"  Total: {total}")
    print(f"  Con ubicación: {con_ubicacion}")
    
    if total == 0:
        print("\n❌ NO HAY TESTIGOS")
        print("   Ejecutar: python scripts/crear_testigos_iniciales.py")
        return False
    else:
        print("\n✅ Testigos cargados correctamente")
        
        # Mostrar algunos testigos
        testigos = User.query.filter_by(rol='testigo_electoral', activo=True).limit(3).all()
        print("\n   Ejemplos:")
        for t in testigos:
            ubicacion = Location.query.get(t.ubicacion_id) if t.ubicacion_id else None
            ubicacion_nombre = ubicacion.nombre_completo if ubicacion else "Sin ubicación"
            print(f"   - {t.nombre} → {ubicacion_nombre}")
        
        return True

def cargar_datos_faltantes():
    """Intentar cargar datos faltantes"""
    print("\n" + "="*70)
    print("INTENTANDO CARGAR DATOS FALTANTES")
    print("="*70)
    
    # Aquí podrías agregar lógica para cargar datos automáticamente
    # Por ahora solo mostramos los comandos
    
    print("\n📝 Comandos para cargar datos:")
    print("\n1. Cargar DIVIPOLA:")
    print("   python scripts/cargar_divipola_v2.py")
    
    print("\n2. Cargar Partidos y Candidatos:")
    print("   python scripts/cargar_partidos_candidatos.py")
    
    print("\n3. Cargar Logos:")
    print("   python scripts/cargar_logos_bd.py")
    
    print("\n4. Crear Usuarios:")
    print("   python scripts/create_sample_users.py")
    
    print("\n5. Crear Testigos:")
    print("   python scripts/crear_testigos_iniciales.py")

def main():
    print("\n" + "="*70)
    print("VERIFICACIÓN COMPLETA DE DATOS EN BASE DE DATOS")
    print("="*70)
    
    app = create_app()
    
    with app.app_context():
        resultados = {
            'divipola': verificar_divipola(),
            'partidos': verificar_partidos(),
            'candidatos': verificar_candidatos(),
            'usuarios': verificar_usuarios(),
            'testigos': verificar_testigos()
        }
        
        print("\n" + "="*70)
        print("RESUMEN DE VERIFICACIÓN")
        print("="*70)
        
        print("\n📊 Estado de los datos:")
        for nombre, estado in resultados.items():
            icono = "✅" if estado else "❌"
            print(f"  {icono} {nombre.capitalize()}: {'OK' if estado else 'FALTA'}")
        
        todos_ok = all(resultados.values())
        
        if todos_ok:
            print("\n🎉 ¡TODOS LOS DATOS ESTÁN CARGADOS CORRECTAMENTE!")
        else:
            print("\n⚠️  FALTAN DATOS POR CARGAR")
            cargar_datos_faltantes()
        
        print("\n" + "="*70)

if __name__ == '__main__':
    main()
