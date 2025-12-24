#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para cargar coordenadas desde DIVIPOLA
Lee el archivo DIVIPOLA y actualiza las coordenadas de puestos y mesas
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
import csv
import io

# Configurar encoding
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, '/d:/Software/mvp')

from backend.app import create_app
from backend.models.location import Location
from backend.database import db

def main():
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("CARGANDO COORDENADAS DESDE DIVIPOLA")
        print("=" * 80)
        print()
        
        # Leer DIVIPOLA
        divipola_path = 'd:\\Software\\mvp\\data\\divipola.csv'
        
        coordenadas_por_puesto = {}
        coordenadas_por_mesa = {}
        
        print("Leyendo DIVIPOLA...")
        try:
            with open(divipola_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    dd = row['dd'].strip().zfill(2)  # Asegurar 2 dígitos
                    mm = row['mm'].strip().zfill(2)  # Asegurar 2 dígitos
                    zz = row['zz'].strip().zfill(2)  # Asegurar 2 dígitos
                    pp = row['pp'].strip().zfill(2)  # Asegurar 2 dígitos
                    mesa = row['mesa'].strip().zfill(2)  # Asegurar 2 dígitos
                    
                    # Solo procesar Quindío (26)
                    if dd != '26':
                        continue
                    
                    # Código de puesto: dd+mm+zz+pp (8 dígitos)
                    puesto_codigo = f"{dd}{mm}{zz}{pp}"
                    # Código de mesa: dd+mm+zz+pp+mesa (10 dígitos)
                    mesa_codigo = f"{dd}{mm}{zz}{pp}{mesa}"
                    
                    try:
                        latitud = float(row['LATITUD'])
                        longitud = float(row['LONGITUD'])
                        
                        if puesto_codigo not in coordenadas_por_puesto:
                            coordenadas_por_puesto[puesto_codigo] = (latitud, longitud)
                        
                        coordenadas_por_mesa[mesa_codigo] = (latitud, longitud)
                    except (ValueError, KeyError):
                        pass
        
        except Exception as e:
            print(f"❌ Error leyendo DIVIPOLA: {str(e)}")
            return False
        
        print(f"✅ DIVIPOLA leído - {len(coordenadas_por_puesto)} puestos, {len(coordenadas_por_mesa)} mesas")
        print()
        
        # Actualizar puestos
        print("Actualizando puestos con coordenadas...")
        puestos_actualizados = 0
        puestos_sin_coordenadas = 0
        
        for puesto in Location.query.filter(
            Location.tipo == 'puesto',
            Location.departamento_codigo == '26',
            Location.activo == True
        ).all():
            # El puesto_codigo en BD es de 8 dígitos: ddmmzzpp
            if puesto.puesto_codigo in coordenadas_por_puesto:
                lat, lon = coordenadas_por_puesto[puesto.puesto_codigo]
                puesto.latitud = lat
                puesto.longitud = lon
                puestos_actualizados += 1
            else:
                puestos_sin_coordenadas += 1
        
        db.session.commit()
        
        print(f"✅ Puestos actualizados: {puestos_actualizados}")
        print(f"⚠️  Puestos sin coordenadas en DIVIPOLA: {puestos_sin_coordenadas}")
        print()
        
        # Actualizar mesas
        print("Actualizando mesas con coordenadas...")
        mesas_actualizadas = 0
        
        for mesa in Location.query.filter(
            Location.tipo == 'mesa',
            Location.departamento_codigo == '26',
            Location.activo == True
        ).all():
            # El mesa_codigo en BD es de 10 dígitos: ddmmzzppmesa
            if mesa.mesa_codigo in coordenadas_por_mesa:
                lat, lon = coordenadas_por_mesa[mesa.mesa_codigo]
                mesa.latitud = lat
                mesa.longitud = lon
                mesas_actualizadas += 1
        
        db.session.commit()
        
        print(f"✅ Mesas actualizadas: {mesas_actualizadas}")
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
        
        mesas_con_coords = Location.query.filter(
            Location.tipo == 'mesa',
            Location.departamento_codigo == '26',
            Location.latitud.isnot(None),
            Location.longitud.isnot(None),
            Location.activo == True
        ).count()
        
        total_mesas = Location.query.filter(
            Location.tipo == 'mesa',
            Location.departamento_codigo == '26',
            Location.activo == True
        ).count()
        
        print("=" * 80)
        print("✅ VERIFICACIÓN FINAL")
        print("=" * 80)
        print(f"Puestos con coordenadas: {puestos_con_coords}/{total_puestos} ({(puestos_con_coords/total_puestos*100):.1f}%)")
        print(f"Mesas con coordenadas: {mesas_con_coords}/{total_mesas} ({(mesas_con_coords/total_mesas*100):.1f}%)")
        print()
        
        return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
