#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app()
with app.app_context():
    print("\n🎯 PUESTOS CON COORDINADORES DISPONIBLES")
    print("="*80)
    print("Estos son los puestos que SÍ tienen coordinadores asignados:")
    print("="*80)
    
    # Buscar coordinadores de puesto en la zona 260101
    coordinadores = User.query.filter_by(
        rol='coordinador_puesto',
        activo=True
    ).all()
    
    puestos_disponibles = []
    
    for coord in coordinadores:
        if coord.ubicacion_id:
            ubicacion = Location.query.get(coord.ubicacion_id)
            if ubicacion and ubicacion.zona_codigo == '260101':
                puestos_disponibles.append({
                    'coordinador': coord.nombre,
                    'puesto_nombre': ubicacion.puesto_nombre,
                    'puesto_codigo': ubicacion.puesto_codigo,
                    'ubicacion_id': ubicacion.id
                })
    
    if puestos_disponibles:
        print(f"\n✅ ENCONTRADOS {len(puestos_disponibles)} PUESTOS CON COORDINADORES EN ZONA 260101:")
        print("-" * 80)
        for i, puesto in enumerate(puestos_disponibles, 1):
            print(f"{i}. PUESTO: {puesto['puesto_nombre']}")
            print(f"   Código: {puesto['puesto_codigo']}")
            print(f"   Coordinador: {puesto['coordinador']}")
            print(f"   ID Ubicación: {puesto['ubicacion_id']}")
            print()
        
        print("="*80)
        print("📋 INSTRUCCIONES PARA EL LOGIN:")
        print("="*80)
        print("1. En el navegador, selecciona uno de los puestos listados arriba")
        print("2. Usa estas credenciales:")
        print("   - Rol: Coordinador de Puesto")
        print("   - Departamento: QUINDIO")
        print("   - Municipio: ARMENIA")
        print("   - Zona: 260101")
        print("   - Puesto: [Selecciona uno de los listados arriba]")
        print("   - Contraseña: test123")
        print("="*80)
    else:
        print("❌ No se encontraron coordinadores en la zona 260101")
        
        # Buscar en otras zonas
        print("\n🔍 BUSCANDO EN OTRAS ZONAS DE ARMENIA...")
        otros_coordinadores = []
        
        for coord in coordinadores:
            if coord.ubicacion_id:
                ubicacion = Location.query.get(coord.ubicacion_id)
                if ubicacion and ubicacion.municipio_codigo == '2601':
                    otros_coordinadores.append({
                        'coordinador': coord.nombre,
                        'puesto_nombre': ubicacion.puesto_nombre,
                        'zona_codigo': ubicacion.zona_codigo,
                        'puesto_codigo': ubicacion.puesto_codigo
                    })
        
        if otros_coordinadores:
            print(f"\n✅ ENCONTRADOS {len(otros_coordinadores)} COORDINADORES EN ARMENIA:")
            for coord in otros_coordinadores[:5]:  # Mostrar solo los primeros 5
                zona_numero = coord['zona_codigo'][-2:] if len(coord['zona_codigo']) >= 2 else coord['zona_codigo']
                print(f"   - Zona: {zona_numero} | Puesto: {coord['puesto_nombre']}")
    
    print("\n" + "="*80)