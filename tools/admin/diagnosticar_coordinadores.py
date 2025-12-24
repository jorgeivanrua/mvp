#!/usr/bin/env python3
"""
Script para diagnosticar el problema con los coordinadores
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app()
with app.app_context():
    print("\n🔍 DIAGNÓSTICO COMPLETO DE COORDINADORES")
    print("="*80)
    
    # Buscar todos los coordinadores
    coordinadores = User.query.filter_by(
        rol='coordinador_puesto',
        activo=True
    ).all()
    
    print(f"Total coordinadores activos: {len(coordinadores)}")
    
    # Analizar coordinadores con ubicación
    coords_con_ubicacion = []
    coords_sin_ubicacion = []
    coords_ubicacion_invalida = []
    
    for coord in coordinadores:
        if coord.ubicacion_id is None:
            coords_sin_ubicacion.append(coord)
        else:
            ubicacion = Location.query.get(coord.ubicacion_id)
            if ubicacion is None:
                coords_ubicacion_invalida.append(coord)
            else:
                coords_con_ubicacion.append((coord, ubicacion))
    
    print(f"\n📊 RESUMEN:")
    print(f"- Con ubicación válida: {len(coords_con_ubicacion)}")
    print(f"- Sin ubicación (ubicacion_id = NULL): {len(coords_sin_ubicacion)}")
    print(f"- Con ubicacion_id inválido: {len(coords_ubicacion_invalida)}")
    
    # Mostrar algunos ejemplos de coordinadores sin ubicación
    if coords_sin_ubicacion:
        print(f"\n❌ COORDINADORES SIN UBICACIÓN (primeros 10):")
        for i, coord in enumerate(coords_sin_ubicacion[:10], 1):
            print(f"   {i}. ID: {coord.id} | Nombre: {coord.nombre} | Cédula: {coord.cedula}")
    
    # Mostrar algunos ejemplos de coordinadores con ubicación inválida
    if coords_ubicacion_invalida:
        print(f"\n⚠️ COORDINADORES CON UBICACIÓN INVÁLIDA:")
        for coord in coords_ubicacion_invalida:
            print(f"   - ID: {coord.id} | Nombre: {coord.nombre} | ubicacion_id: {coord.ubicacion_id} (NO EXISTE)")
    
    # Analizar coordinadores con ubicación válida
    if coords_con_ubicacion:
        print(f"\n✅ COORDINADORES CON UBICACIÓN VÁLIDA (primeros 10):")
        for i, (coord, ubicacion) in enumerate(coords_con_ubicacion[:10], 1):
            zona_numero = ubicacion.zona_codigo[-2:] if len(ubicacion.zona_codigo) >= 2 else ubicacion.zona_codigo
            print(f"   {i}. {coord.nombre}")
            print(f"      Ubicación: {ubicacion.departamento_nombre} - {ubicacion.municipio_nombre} - Zona {zona_numero}")
            print(f"      Puesto: {ubicacion.puesto_nombre}")
            print(f"      Códigos: Dept={ubicacion.departamento_codigo}, Mun={ubicacion.municipio_codigo}, Zona={ubicacion.zona_codigo}")
            print()
    
    # Verificar si hay ubicaciones de tipo 'puesto' disponibles
    print(f"\n🏢 VERIFICANDO UBICACIONES DISPONIBLES:")
    total_ubicaciones = Location.query.filter_by(tipo='puesto').count()
    print(f"Total ubicaciones tipo 'puesto': {total_ubicaciones}")
    
    # Mostrar algunas ubicaciones de ejemplo
    ubicaciones_ejemplo = Location.query.filter_by(tipo='puesto').limit(5).all()
    print(f"\nEjemplos de ubicaciones disponibles:")
    for ub in ubicaciones_ejemplo:
        zona_numero = ub.zona_codigo[-2:] if len(ub.zona_codigo) >= 2 else ub.zona_codigo
        print(f"   - ID: {ub.id} | {ub.departamento_nombre} - {ub.municipio_nombre} - Zona {zona_numero}")
        print(f"     Puesto: {ub.puesto_nombre}")
    
    print("\n" + "="*80)