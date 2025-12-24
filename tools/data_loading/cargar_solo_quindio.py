#!/usr/bin/env python3
"""
Script para cargar SOLO las ubicaciones de Quindío (código 26)
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
import os
import csv

sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.database import db
from backend.models.location import Location

def cargar_quindio():
    app = create_app()
    
    with app.app_context():
        print("[*] CARGANDO UBICACIONES DE QUINDÍO")
        print("=" * 60)
        
        csv_path = 'data/divipola.csv'
        if not os.path.exists(csv_path):
            print(f"[ERROR] No encontrado: {csv_path}")
            return False
        
        print(f"[*] Leyendo: {csv_path}")
        
        locations_added = 0
        departamentos = {}
        municipios = {}
        zonas = {}
        puestos = {}
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                dd = row['dd'].strip().zfill(2)
                
                # SOLO Quindío (código 26)
                if dd != '26':
                    continue
                
                mm = row['mm'].strip().zfill(2)
                zz = row['zz'].strip().zfill(2)
                pp = row['pp'].strip().zfill(2)
                mesa = row['mesa'].strip().zfill(2)
                
                departamento_nombre = row['departamento'].strip()
                municipio_nombre = row['municipio'].strip()
                puesto_nombre = row['puesto'].strip()
                mesa_nombre = row['mesa_nombre'].strip()
                
                depto_codigo = dd
                muni_codigo = f"{dd}{mm}"
                zona_codigo = f"{dd}{mm}{zz}"
                puesto_codigo = f"{dd}{mm}{zz}{pp}"
                mesa_codigo = f"{dd}{mm}{zz}{pp}{mesa}"
                
                # Departamento
                if dd not in departamentos:
                    dept = Location(
                        departamento_codigo=depto_codigo,
                        departamento_nombre=departamento_nombre,
                        nombre_completo=departamento_nombre,
                        tipo='departamento',
                        activo=True
                    )
                    db.session.add(dept)
                    db.session.flush()
                    departamentos[dd] = dept.id
                    locations_added += 1
                
                # Municipio
                if muni_codigo not in municipios:
                    muni = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        departamento_nombre=departamento_nombre,
                        municipio_nombre=municipio_nombre,
                        nombre_completo=f"{departamento_nombre} - {municipio_nombre}",
                        tipo='municipio',
                        parent_id=departamentos[dd],
                        activo=True
                    )
                    db.session.add(muni)
                    db.session.flush()
                    municipios[muni_codigo] = muni.id
                    locations_added += 1
                
                # Zona
                if zona_codigo not in zonas:
                    zona = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        zona_codigo=zona_codigo,
                        departamento_nombre=departamento_nombre,
                        municipio_nombre=municipio_nombre,
                        nombre_completo=f"{departamento_nombre} - {municipio_nombre} - Zona {zz}",
                        tipo='zona',
                        parent_id=municipios[muni_codigo],
                        activo=True
                    )
                    db.session.add(zona)
                    db.session.flush()
                    zonas[zona_codigo] = zona.id
                    locations_added += 1
                
                # Puesto
                if puesto_codigo not in puestos:
                    puesto = Location(
                        departamento_codigo=depto_codigo,
                        municipio_codigo=muni_codigo,
                        zona_codigo=zona_codigo,
                        puesto_codigo=puesto_codigo,
                        departamento_nombre=departamento_nombre,
                        municipio_nombre=municipio_nombre,
                        puesto_nombre=puesto_nombre,
                        nombre_completo=f"{departamento_nombre} - {municipio_nombre} - Zona {zz} - {puesto_nombre}",
                        tipo='puesto',
                        activo=True
                    )
                    db.session.add(puesto)
                    db.session.flush()
                    puestos[puesto_codigo] = puesto.id
                    locations_added += 1
                
                # Mesa
                mesa_loc = Location(
                    departamento_codigo=depto_codigo,
                    municipio_codigo=muni_codigo,
                    zona_codigo=zona_codigo,
                    puesto_codigo=puesto_codigo,
                    mesa_codigo=mesa_codigo,
                    departamento_nombre=departamento_nombre,
                    municipio_nombre=municipio_nombre,
                    puesto_nombre=puesto_nombre,
                    mesa_nombre=mesa_nombre,
                    nombre_completo=f"{departamento_nombre} - {municipio_nombre} - Zona {zz} - {puesto_nombre} - {mesa_nombre}",
                    tipo='mesa',
                    parent_id=puestos[puesto_codigo],
                    activo=True
                )
                db.session.add(mesa_loc)
                locations_added += 1
                
                if locations_added % 500 == 0:
                    db.session.commit()
                    print(f"  [{locations_added}] ubicaciones procesadas...")
        
        # Commit final
        db.session.commit()
        
        # Contar por tipo
        print()
        print("[*] RESUMEN DE CARGA")
        print("=" * 60)
        
        for tipo in ['departamento', 'municipio', 'zona', 'puesto', 'mesa']:
            count = Location.query.filter_by(tipo=tipo, activo=True).count()
            print(f"  {tipo.upper()}: {count}")
        
        total = Location.query.filter(Location.activo == True).count()
        print()
        print(f"[OK] TOTAL UBICACIONES QUINDÍO: {total}")
        print("[OK] Carga completada exitosamente")
        
        return True

if __name__ == '__main__':
    cargar_quindio()
