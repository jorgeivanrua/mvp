#!/usr/bin/env python3
"""
Script para corregir puestos sin municipio válido
Asigna el municipio basándose en el código de zona
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
sys.path.insert(0, '/d:/Software/mvp')

from backend.app import create_app
from backend.models.location import Location
from backend.database import db

# Mapeo de código de zona a municipio_codigo
# Extraer primeros 4 dígitos del zona_codigo = municipio_codigo
def extraer_municipio_de_zona(zona_codigo):
    """Extrae municipio_codigo de zona_codigo"""
    if not zona_codigo or len(zona_codigo) < 4:
        return None
    return zona_codigo[:4]

COORDENADAS_MUNICIPIOS = {
    '2601': (4.5413, -75.5144),  # FILANDIA
    '2602': (4.5378, -75.7339),  # BUENAVISTA
    '2603': (4.5362, -75.7244),  # CALARCÁ
    '2604': (4.5451, -75.5036),  # CÓRDOBA
    '2605': (4.5376, -75.7255),  # ARMENIA - Capital
    '2606': (4.5480, -75.6033),  # LA TEBAIDA
    '2607': (4.5500, -75.6800),  # MEJÍA
    '2608': (4.5412, -75.5344),  # MONTEBELLO
    '2610': (4.5497, -75.6500),  # QUIMBAYA
    '2611': (4.5447, -75.7328),  # SALENTO
    '2612': (4.5474, -75.6822),  # CIRCASIA
}

MUNICIPIOS_NOMBRES = {
    '2601': 'FILANDIA',
    '2602': 'BUENAVISTA',
    '2603': 'CALARCÁ',
    '2604': 'CÓRDOBA',
    '2605': 'ARMENIA',
    '2606': 'LA TEBAIDA',
    '2607': 'MEJÍA',
    '2608': 'MONTEBELLO',
    '2610': 'QUIMBAYA',
    '2611': 'SALENTO',
    '2612': 'CIRCASIA',
}

def main():
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("CORRIGIENDO PUESTOS SIN MUNICIPIO VÁLIDO")
        print("=" * 80)
        print()
        
        # Encontrar puestos sin municipio o con municipio vacío
        puestos = Location.query.filter(
            Location.tipo == 'puesto',
            Location.departamento_codigo == '26',
            Location.activo == True
        ).all()
        
        print(f"Total puestos: {len(puestos)}")
        
        corregidos = 0
        sin_corregir = 0
        
        for puesto in puestos:
            # Si no tiene municipio, intentar extraerlo de la zona
            if not puesto.municipio_codigo or puesto.municipio_codigo.strip() == '':
                municipio_nuevo = extraer_municipio_de_zona(puesto.zona_codigo)
                
                if municipio_nuevo and municipio_nuevo in MUNICIPIOS_NOMBRES:
                    # Asignar municipio
                    puesto.municipio_codigo = municipio_nuevo
                    puesto.municipio_nombre = MUNICIPIOS_NOMBRES[municipio_nuevo]
                    
                    # Asignar coordenadas si no las tiene
                    if not puesto.latitud or not puesto.longitud:
                        lat, lon = COORDENADAS_MUNICIPIOS.get(municipio_nuevo, (None, None))
                        if lat and lon:
                            # Añadir variación
                            puesto_num = int(puesto.puesto_codigo[-2:]) if len(puesto.puesto_codigo) >= 2 else 0
                            zona_num = int(puesto.zona_codigo[-2:]) if len(puesto.zona_codigo) >= 2 else 0
                            puesto.latitud = lat + (zona_num * 0.0015 + puesto_num * 0.0003) - 0.05
                            puesto.longitud = lon + (zona_num * 0.0020 + puesto_num * 0.0004) - 0.06
                    
                    corregidos += 1
                    print(f"✅ {puesto.puesto_nombre} - Municipio: {municipio_nuevo}, Lat: {puesto.latitud:.4f}, Lon: {puesto.longitud:.4f}")
                else:
                    sin_corregir += 1
                    print(f"❌ {puesto.puesto_nombre} - No se pudo extraer municipio de zona {puesto.zona_codigo}")
            elif not puesto.latitud or not puesto.longitud:
                # Tiene municipio pero no coordenadas
                lat, lon = COORDENADAS_MUNICIPIOS.get(puesto.municipio_codigo, (None, None))
                if lat and lon:
                    puesto_num = int(puesto.puesto_codigo[-2:]) if len(puesto.puesto_codigo) >= 2 else 0
                    zona_num = int(puesto.zona_codigo[-2:]) if len(puesto.zona_codigo) >= 2 else 0
                    puesto.latitud = lat + (zona_num * 0.0015 + puesto_num * 0.0003) - 0.05
                    puesto.longitud = lon + (zona_num * 0.0020 + puesto_num * 0.0004) - 0.06
                    corregidos += 1
                    print(f"✅ Coordenadas añadidas: {puesto.puesto_nombre}")
        
        # Guardar cambios
        try:
            db.session.commit()
            print()
            print(f"✅ ACTUALIZACIÓN COMPLETADA")
            print(f"   - Puestos corregidos: {corregidos}")
            print(f"   - Sin corregir: {sin_corregir}")
            print()
            
            # Verificación final
            puestos_con_coords = Location.query.filter(
                Location.tipo == 'puesto',
                Location.departamento_codigo == '26',
                Location.latitud.isnot(None),
                Location.longitud.isnot(None),
                Location.activo == True
            ).count()
            
            total_puestos = Location.query.filter(
                Location.tipo == 'puesto',
                Location.departamento_codigo == '26',
                Location.activo == True
            ).count()
            
            print(f"✅ VERIFICACIÓN FINAL:")
            print(f"   - Puestos con coordenadas: {puestos_con_coords}/{total_puestos}")
            print(f"   - Porcentaje: {(puestos_con_coords/total_puestos*100):.1f}%")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al guardar: {str(e)}")
            return False
        
        return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
