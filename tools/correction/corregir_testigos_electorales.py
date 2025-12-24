#!/usr/bin/env python3
"""
Script para corregir las ubicaciones inválidas de los testigos electorales
Asigna ubicaciones válidas de tipo 'puesto' a cada testigo electoral
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.database import db

app = create_app()
with app.app_context():
    print("\n🔧 CORRECCIÓN DE UBICACIONES DE TESTIGOS ELECTORALES")
    print("="*80)
    
    # Obtener todos los testigos electorales con ubicaciones inválidas
    testigos_electorales = User.query.filter_by(
        rol='testigo_electoral',
        activo=True
    ).all()
    
    print(f"Total testigos electorales: {len(testigos_electorales)}")
    
    # Obtener todas las ubicaciones válidas tipo 'puesto'
    ubicaciones_puestos = Location.query.filter_by(tipo='puesto').order_by(Location.id).all()
    print(f"Total ubicaciones de puestos disponibles: {len(ubicaciones_puestos)}")
    
    # Verificar que las ubicaciones actuales son realmente inválidas
    testigos_invalidos = []
    for testigo in testigos_electorales:
        ubicacion_actual = Location.query.get(testigo.ubicacion_id) if testigo.ubicacion_id else None
        if ubicacion_actual is None:
            testigos_invalidos.append(testigo)
    
    print(f"Testigos electorales con ubicaciones inválidas: {len(testigos_invalidos)}")
    
    if len(testigos_invalidos) == 0:
        print("✅ No hay testigos electorales con ubicaciones inválidas.")
        exit(0)
    
    print(f"\n📋 PLAN DE REASIGNACIÓN:")
    print("-"*50)
    
    # Crear mapeo de testigos a ubicaciones de puestos válidas
    reasignaciones = []
    for i, testigo in enumerate(testigos_invalidos):
        # Usar módulo para reutilizar ubicaciones si hay más testigos que ubicaciones
        ubicacion_index = i % len(ubicaciones_puestos)
        nueva_ubicacion = ubicaciones_puestos[ubicacion_index]
        
        zona_numero = nueva_ubicacion.zona_codigo[-2:] if len(nueva_ubicacion.zona_codigo) >= 2 else nueva_ubicacion.zona_codigo
        
        reasignaciones.append({
            'testigo': testigo,
            'ubicacion_actual': testigo.ubicacion_id,
            'nueva_ubicacion': nueva_ubicacion,
            'zona_numero': zona_numero
        })
        
        if i < 10:  # Mostrar solo los primeros 10 para no saturar la salida
            print(f"{i+1:3d}. {testigo.nombre} (Cédula: {testigo.cedula})")
            print(f"     Ubicación actual: {testigo.ubicacion_id} (INVÁLIDA)")
            print(f"     Nueva ubicación: {nueva_ubicacion.id} - {nueva_ubicacion.municipio_nombre} - Zona {zona_numero.zfill(2)}")
            print(f"     Puesto: {nueva_ubicacion.puesto_nombre}")
            print()
    
    if len(reasignaciones) > 10:
        print(f"... y {len(reasignaciones) - 10} reasignaciones más")
    
    print(f"\n🔄 EJECUTANDO REASIGNACIONES...")
    print("-"*50)
    
    # Ejecutar las reasignaciones
    exitosos = 0
    errores = 0
    
    try:
        for i, reasignacion in enumerate(reasignaciones):
            testigo = reasignacion['testigo']
            nueva_ubicacion = reasignacion['nueva_ubicacion']
            
            # Actualizar la ubicación del testigo
            testigo.ubicacion_id = nueva_ubicacion.id
            
            if (i + 1) % 50 == 0 or i == len(reasignaciones) - 1:
                print(f"Procesados: {i + 1}/{len(reasignaciones)}")
            
            exitosos += 1
        
        # Confirmar cambios en la base de datos
        db.session.commit()
        print(f"\n✅ REASIGNACIÓN COMPLETADA EXITOSAMENTE")
        print(f"Testigos electorales reasignados: {exitosos}")
        print(f"Errores: {errores}")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ ERROR DURANTE LA REASIGNACIÓN: {str(e)}")
        print("Todos los cambios han sido revertidos.")
        exit(1)
    
    print(f"\n🎉 ¡CORRECCIÓN EXITOSA!")
    print(f"Todos los testigos electorales ahora tienen ubicaciones válidas.")
    
    print("\n" + "="*80)