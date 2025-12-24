#!/usr/bin/env python3
"""
Script para corregir las ubicaciones inválidas de los coordinadores municipales
Asigna ubicaciones válidas de tipo 'municipio' a cada coordinador municipal
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
    print("\n🔧 CORRECCIÓN DE UBICACIONES DE COORDINADORES MUNICIPALES")
    print("="*80)
    
    # Obtener todos los coordinadores municipales con ubicaciones inválidas
    coordinadores_municipales = User.query.filter_by(
        rol='coordinador_municipal',
        activo=True
    ).all()
    
    print(f"Total coordinadores municipales: {len(coordinadores_municipales)}")
    
    # Obtener todas las ubicaciones válidas tipo 'municipio'
    ubicaciones_municipios = Location.query.filter_by(tipo='municipio').order_by(Location.id).all()
    print(f"Total ubicaciones municipales disponibles: {len(ubicaciones_municipios)}")
    
    # Verificar que las ubicaciones actuales son realmente inválidas
    coordinadores_invalidos = []
    for coord in coordinadores_municipales:
        ubicacion_actual = Location.query.get(coord.ubicacion_id) if coord.ubicacion_id else None
        if ubicacion_actual is None:
            coordinadores_invalidos.append(coord)
    
    print(f"Coordinadores municipales con ubicaciones inválidas: {len(coordinadores_invalidos)}")
    
    if len(coordinadores_invalidos) == 0:
        print("✅ No hay coordinadores municipales con ubicaciones inválidas.")
        exit(0)
    
    print(f"\n📋 PLAN DE REASIGNACIÓN:")
    print("-"*50)
    
    # Crear mapeo de coordinadores a ubicaciones municipales válidas
    reasignaciones = []
    for i, coord in enumerate(coordinadores_invalidos):
        if i < len(ubicaciones_municipios):
            nueva_ubicacion = ubicaciones_municipios[i]
            
            reasignaciones.append({
                'coordinador': coord,
                'ubicacion_actual': coord.ubicacion_id,
                'nueva_ubicacion': nueva_ubicacion
            })
            
            print(f"{i+1:2d}. {coord.nombre}")
            print(f"     Ubicación actual: {coord.ubicacion_id} (INVÁLIDA)")
            print(f"     Nueva ubicación: {nueva_ubicacion.id} - {nueva_ubicacion.municipio_nombre}")
            print(f"     Departamento: {nueva_ubicacion.departamento_nombre}")
            print()
    
    if len(coordinadores_invalidos) > len(ubicaciones_municipios):
        print(f"⚠️ ADVERTENCIA: Hay más coordinadores ({len(coordinadores_invalidos)}) que ubicaciones municipales ({len(ubicaciones_municipios)})")
    
    print(f"\n🔄 EJECUTANDO REASIGNACIONES...")
    print("-"*50)
    
    # Ejecutar las reasignaciones
    exitosos = 0
    errores = 0
    
    try:
        for i, reasignacion in enumerate(reasignaciones):
            coord = reasignacion['coordinador']
            nueva_ubicacion = reasignacion['nueva_ubicacion']
            
            # Actualizar la ubicación del coordinador
            coord.ubicacion_id = nueva_ubicacion.id
            
            print(f"✅ {coord.nombre} → {nueva_ubicacion.municipio_nombre}")
            exitosos += 1
        
        # Confirmar cambios en la base de datos
        db.session.commit()
        print(f"\n✅ REASIGNACIÓN COMPLETADA EXITOSAMENTE")
        print(f"Coordinadores municipales reasignados: {exitosos}")
        print(f"Errores: {errores}")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ ERROR DURANTE LA REASIGNACIÓN: {str(e)}")
        print("Todos los cambios han sido revertidos.")
        exit(1)
    
    print(f"\n🔍 VERIFICACIÓN POST-CORRECCIÓN")
    print("-"*50)
    
    # Verificar que la corrección fue exitosa
    coordinadores_verificacion = User.query.filter_by(
        rol='coordinador_municipal',
        activo=True
    ).all()
    
    coords_validos = 0
    coords_invalidos = 0
    
    for coord in coordinadores_verificacion:
        ubicacion = Location.query.get(coord.ubicacion_id)
        if ubicacion is None:
            coords_invalidos += 1
        else:
            coords_validos += 1
    
    print(f"Coordinadores municipales con ubicación válida: {coords_validos}")
    print(f"Coordinadores municipales con ubicación inválida: {coords_invalidos}")
    
    if coords_invalidos == 0:
        print(f"\n🎉 ¡CORRECCIÓN EXITOSA!")
        print(f"Todos los coordinadores municipales ahora tienen ubicaciones válidas.")
    else:
        print(f"\n⚠️ Aún quedan {coords_invalidos} coordinadores municipales con ubicaciones inválidas.")
    
    print("\n" + "="*80)