#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app()
with app.app_context():
    print('🔍 ANÁLISIS COMPLETO DE COORDINADORES')
    print('='*60)
    
    # Contar todos los coordinadores
    total_coords = User.query.filter_by(rol='coordinador_puesto', activo=True).count()
    print(f'Total coordinadores activos: {total_coords}')
    
    # Buscar coordinadores con ubicación
    coords_con_ubicacion = User.query.filter_by(rol='coordinador_puesto', activo=True).filter(User.ubicacion_id.isnot(None)).all()
    print(f'Coordinadores con ubicación asignada: {len(coords_con_ubicacion)}')
    
    if coords_con_ubicacion:
        print('\n📍 COORDINADORES POR ZONA:')
        zonas = {}
        for coord in coords_con_ubicacion:
            ubicacion = Location.query.get(coord.ubicacion_id)
            if ubicacion:
                # Extraer solo los últimos 2 dígitos del código de zona
                zona_numero = ubicacion.zona_codigo[-2:] if len(ubicacion.zona_codigo) >= 2 else ubicacion.zona_codigo
                if zona_numero not in zonas:
                    zonas[zona_numero] = []
                zonas[zona_numero].append({
                    'nombre': coord.nombre,
                    'puesto': ubicacion.puesto_nombre,
                    'municipio': ubicacion.municipio_nombre
                })
        
        for zona, coords in zonas.items():
            print(f'\nZona {zona}:')
            for coord in coords[:3]:  # Mostrar solo los primeros 3
                print(f'  - {coord["nombre"]} en {coord["puesto"]} ({coord["municipio"]})')
    
    print('\n' + '='*60)