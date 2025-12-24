#!/usr/bin/env python3
"""
Script para corregir las ubicaciones inválidas de los coordinadores
Reasigna coordinadores con ubicacion_id inválidos a ubicaciones válidas existentes
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
    print("\n🔧 CORRECCIÓN DE UBICACIONES DE COORDINADORES")
    print("="*80)
    
    # Obtener todos los coordinadores con ubicaciones inválidas
    coordinadores = User.query.filter_by(
        rol='coordinador_puesto',
        activo=True
    ).filter(User.ubicacion_id.isnot(None)).all()
    
    print(f"Total coordinadores a corregir: {len(coordinadores)}")
    
    # Obtener todas las ubicaciones válidas tipo 'puesto'
    ubicaciones_validas = Location.query.filter_by(tipo='puesto').order_by(Location.id).all()
    print(f"Total ubicaciones válidas disponibles: {len(ubicaciones_validas)}")
    
    if len(coordinadores) > len(ubicaciones_validas):
        print(f"⚠️ ADVERTENCIA: Hay más coordinadores ({len(coordinadores)}) que ubicaciones válidas ({len(ubicaciones_validas)})")
        print("Algunos coordinadores compartirán ubicaciones.")
    
    # Verificar que las ubicaciones actuales son realmente inválidas
    coordinadores_invalidos = []
    for coord in coordinadores:
        ubicacion_actual = Location.query.get(coord.ubicacion_id)
        if ubicacion_actual is None:
            coordinadores_invalidos.append(coord)
    
    print(f"Coordinadores con ubicaciones realmente inválidas: {len(coordinadores_invalidos)}")
    
    if len(coordinadores_invalidos) == 0:
        print("✅ No hay coordinadores con ubicaciones inválidas. Sistema ya corregido.")
        exit(0)
    
    print(f"\n📋 PLAN DE REASIGNACIÓN:")
    print("-"*50)
    
    # Crear mapeo de coordinadores a ubicaciones válidas
    reasignaciones = []
    for i, coord in enumerate(coordinadores_invalidos):
        # Usar módulo para reutilizar ubicaciones si hay más coordinadores que ubicaciones
        ubicacion_index = i % len(ubicaciones_validas)
        nueva_ubicacion = ubicaciones_validas[ubicacion_index]
        
        zona_numero = nueva_ubicacion.zona_codigo[-2:] if len(nueva_ubicacion.zona_codigo) >= 2 else nueva_ubicacion.zona_codigo
        
        reasignaciones.append({
            'coordinador': coord,
            'ubicacion_actual': coord.ubicacion_id,
            'nueva_ubicacion': nueva_ubicacion,
            'zona_numero': zona_numero
        })
        
        if i < 10:  # Mostrar solo los primeros 10 para no saturar la salida
            print(f"{i+1:3d}. {coord.nombre} (ID: {coord.id})")
            print(f"     Ubicación actual: {coord.ubicacion_id} (INVÁLIDA)")
            print(f"     Nueva ubicación: {nueva_ubicacion.id} - {nueva_ubicacion.departamento_nombre} - {nueva_ubicacion.municipio_nombre} - Zona {zona_numero}")
            print(f"     Puesto: {nueva_ubicacion.puesto_nombre}")
            print()
    
    if len(reasignaciones) > 10:
        print(f"... y {len(reasignaciones) - 10} reasignaciones más")
    
    # Confirmar antes de proceder
    print(f"\n⚠️ CONFIRMACIÓN AUTOMÁTICA")
    print(f"Se van a reasignar {len(reasignaciones)} coordinadores a ubicaciones válidas.")
    print(f"Procediendo automáticamente...")
    
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
            
            if (i + 1) % 10 == 0 or i == len(reasignaciones) - 1:
                print(f"Procesados: {i + 1}/{len(reasignaciones)}")
            
            exitosos += 1
        
        # Confirmar cambios en la base de datos
        db.session.commit()
        print(f"\n✅ REASIGNACIÓN COMPLETADA EXITOSAMENTE")
        print(f"Coordinadores reasignados: {exitosos}")
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
        rol='coordinador_puesto',
        activo=True
    ).filter(User.ubicacion_id.isnot(None)).all()
    
    coords_validos = 0
    coords_invalidos = 0
    
    for coord in coordinadores_verificacion:
        ubicacion = Location.query.get(coord.ubicacion_id)
        if ubicacion is None:
            coords_invalidos += 1
        else:
            coords_validos += 1
    
    print(f"Coordinadores con ubicación válida: {coords_validos}")
    print(f"Coordinadores con ubicación inválida: {coords_invalidos}")
    
    if coords_invalidos == 0:
        print(f"\n🎉 ¡CORRECCIÓN EXITOSA!")
        print(f"Todos los coordinadores ahora tienen ubicaciones válidas.")
        print(f"El sistema de login debería funcionar correctamente.")
    else:
        print(f"\n⚠️ Aún quedan {coords_invalidos} coordinadores con ubicaciones inválidas.")
        print(f"Puede ser necesario ejecutar el script nuevamente.")
    
    print("\n" + "="*80)