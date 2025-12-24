#!/usr/bin/env python3
"""
Script para cargar coordenadas geográficas de puestos de Quindío
Basado en ubicación de municipios
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
sys.path.insert(0, '/d:/Software/mvp')

from backend.app import create_app
from backend.models.location import Location
from backend.database import db

# Coordenadas aproximadas de municipios del Quindío (CENTRO APROXIMADO)
# Fuente: DANE / Google Maps
COORDENADAS_MUNICIPIOS = {
    '2601': (4.5413, -75.5144),  # FILANDIA
    '2602': (4.5378, -75.7339),  # BUENAVISTA
    '2603': (4.5362, -75.7244),  # CALARCÁ
    '2604': (4.5451, -75.5036),  # CÓRDOBA
    '2605': (4.5376, -75.7255),  # ARMENIA - Capital
    '2606': (4.5480, -75.6033),  # LA TEBAIDA
    '2607': (4.5500, -75.6800),  # MEJÍA
    '2608': (4.5412, -75.5344),  # MONTEBELLO
    '2609': (4.5406, -75.6189),  # PEREIRA (No es Quindío, se excluye)
    '2610': (4.5497, -75.6500),  # QUIMBAYA
    '2611': (4.5447, -75.7328),  # SALENTO
    '2612': (4.5474, -75.6822),  # CIRCASIA
}

def generar_coordenadas_puesto(municipio_codigo, zona_codigo, puesto_codigo):
    """
    Genera coordenadas aproximadas para un puesto basándose en su municipio y zona
    Añade variación para cada zona y puesto dentro del municipio
    """
    if municipio_codigo not in COORDENADAS_MUNICIPIOS:
        return None, None
    
    lat_base, lon_base = COORDENADAS_MUNICIPIOS[municipio_codigo]
    
    # Extraer números de zona y puesto para variación
    try:
        zona_num = int(zona_codigo[-2:]) if len(zona_codigo) >= 2 else 0
        puesto_num = int(puesto_codigo[-2:]) if len(puesto_codigo) >= 2 else 0
    except:
        zona_num = 0
        puesto_num = 0
    
    # Añadir variación pequeña para dispersar los puntos
    # Aproximadamente 0.01 grados = ~1 km
    lat_variacion = (zona_num * 0.0015 + puesto_num * 0.0003) - 0.05
    lon_variacion = (zona_num * 0.0020 + puesto_num * 0.0004) - 0.06
    
    return lat_base + lat_variacion, lon_base + lon_variacion

def main():
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("CARGANDO COORDENADAS PARA PUESTOS DE QUINDÍO")
        print("=" * 80)
        print()
        
        # Obtener todos los puestos de Quindío
        puestos = Location.query.filter(
            Location.tipo == 'puesto',
            Location.departamento_codigo == '26',
            Location.activo == True
        ).all()
        
        print(f"Total puestos encontrados: {len(puestos)}")
        
        if not puestos:
            print("❌ No hay puestos para actualizar")
            return
        
        # Actualizar coordenadas
        actualizados = 0
        sin_coordenadas = 0
        
        for puesto in puestos:
            lat, lon = generar_coordenadas_puesto(
                puesto.municipio_codigo,
                puesto.zona_codigo,
                puesto.puesto_codigo
            )
            
            if lat is not None and lon is not None:
                puesto.latitud = lat
                puesto.longitud = lon
                actualizados += 1
                print(f"✅ {puesto.puesto_nombre} ({puesto.puesto_codigo}) - "
                      f"Lat: {lat:.4f}, Lon: {lon:.4f}")
            else:
                sin_coordenadas += 1
                print(f"⚠️  {puesto.puesto_nombre} - Sin municipio válido")
        
        # Guardar cambios
        try:
            db.session.commit()
            print()
            print(f"✅ ACTUALIZACIÓN COMPLETADA")
            print(f"   - Puestos actualizados: {actualizados}")
            print(f"   - Sin coordenadas: {sin_coordenadas}")
            print()
            
            # Verificar
            puestos_con_coords = Location.query.filter(
                Location.tipo == 'puesto',
                Location.departamento_codigo == '26',
                Location.latitud.isnot(None),
                Location.longitud.isnot(None),
                Location.activo == True
            ).count()
            
            print(f"✅ VERIFICACIÓN:")
            print(f"   - Puestos con coordenadas: {puestos_con_coords}/{len(puestos)}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al guardar: {str(e)}")
            return False
        
        return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
