#!/usr/bin/env python3
"""
Script para encontrar ubicaciones válidas con coordinadores asignados
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app()
with app.app_context():
    print("\n🎯 UBICACIONES VÁLIDAS PARA LOGIN")
    print("="*80)
    
    # Buscar todos los coordinadores de puesto activos con ubicación
    coordinadores = User.query.filter_by(
        rol='coordinador_puesto',
        activo=True
    ).filter(User.ubicacion_id.isnot(None)).all()
    
    print(f"Total coordinadores de puesto con ubicación: {len(coordinadores)}")
    
    # Agrupar por zona para mostrar opciones
    zonas_disponibles = {}
    
    for coord in coordinadores:
        ubicacion = Location.query.get(coord.ubicacion_id)
        if ubicacion:
            # Extraer solo los últimos 2 dígitos del código de zona
            zona_numero = ubicacion.zona_codigo[-2:] if len(ubicacion.zona_codigo) >= 2 else ubicacion.zona_codigo
            zona_key = f"{ubicacion.departamento_nombre} - {ubicacion.municipio_nombre} - Zona {zona_numero}"
            
            if zona_key not in zonas_disponibles:
                zonas_disponibles[zona_key] = []
            
            zonas_disponibles[zona_key].append({
                'coordinador': coord.nombre,
                'puesto_nombre': ubicacion.puesto_nombre,
                'puesto_codigo': ubicacion.puesto_codigo,
                'departamento_codigo': ubicacion.departamento_codigo,
                'municipio_codigo': ubicacion.municipio_codigo,
                'zona_codigo': ubicacion.zona_codigo
            })
    
    print(f"\n✅ ZONAS DISPONIBLES: {len(zonas_disponibles)}")
    print("="*80)
    
    # Mostrar las primeras 5 zonas con más coordinadores
    zonas_ordenadas = sorted(zonas_disponibles.items(), key=lambda x: len(x[1]), reverse=True)
    
    for i, (zona, coordinadores_zona) in enumerate(zonas_ordenadas[:5], 1):
        print(f"\n{i}. {zona}")
        print(f"   Coordinadores disponibles: {len(coordinadores_zona)}")
        
        # Mostrar los primeros 3 puestos de esta zona
        for j, puesto in enumerate(coordinadores_zona[:3], 1):
            print(f"   {j}. PUESTO: {puesto['puesto_nombre']}")
            print(f"      Coordinador: {puesto['coordinador']}")
            print(f"      Códigos: Dept={puesto['departamento_codigo']}, Mun={puesto['municipio_codigo']}, Zona={puesto['zona_codigo']}, Puesto={puesto['puesto_codigo']}")
        
        if len(coordinadores_zona) > 3:
            print(f"   ... y {len(coordinadores_zona) - 3} puestos más")
    
    print("\n" + "="*80)
    print("📋 INSTRUCCIONES PARA HACER LOGIN:")
    print("="*80)
    print("1. Selecciona ROL: 'Coordinador de Puesto'")
    print("2. Selecciona una de las ubicaciones mostradas arriba:")
    print("   - Departamento: QUINDIO")
    print("   - Municipio: (según la zona elegida)")
    print("   - Zona: (según la zona elegida)")
    print("   - Puesto: (uno de los listados)")
    print("3. Contraseña: test123")
    print("="*80)
    
    # Buscar específicamente en Armenia (municipio 2601)
    print(f"\n🔍 COORDINADORES ESPECÍFICOS EN ARMENIA:")
    print("-"*50)
    
    armenia_coords = []
    for coord in coordinadores:
        ubicacion = Location.query.get(coord.ubicacion_id)
        if ubicacion and ubicacion.municipio_codigo == '2601':
            armenia_coords.append({
                'coordinador': coord.nombre,
                'puesto_nombre': ubicacion.puesto_nombre,
                'zona_codigo': ubicacion.zona_codigo,
                'puesto_codigo': ubicacion.puesto_codigo
            })
    
    if armenia_coords:
        print(f"Encontrados {len(armenia_coords)} coordinadores en Armenia:")
        for coord in armenia_coords[:10]:  # Mostrar los primeros 10
            zona_numero = coord['zona_codigo'][-2:] if len(coord['zona_codigo']) >= 2 else coord['zona_codigo']
            print(f"• Zona {zona_numero} - {coord['puesto_nombre']} (Coord: {coord['coordinador']})")
    else:
        print("❌ No se encontraron coordinadores en Armenia")
    
    print("\n" + "="*80)