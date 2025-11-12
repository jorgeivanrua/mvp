"""
Script para cargar datos DIVIPOLA desde CSV
"""
import os
import sys
import csv

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.location import Location


def load_divipola_from_csv(csv_path):
    """
    Cargar datos DIVIPOLA desde archivo CSV
    
    Args:
        csv_path: Ruta al archivo CSV
    """
    app = create_app('development')
    
    with app.app_context():
        print(f">> Cargando datos desde: {csv_path}")
        print(">> SOLO CARGANDO DEPARTAMENTO DE CAQUETA (codigo 44)")
        
        # Limpiar tabla de ubicaciones
        print(">> Limpiando tabla de ubicaciones...")
        try:
            Location.query.delete()
            db.session.commit()
        except Exception as e:
            print(f">> Advertencia al limpiar: {e}")
            db.session.rollback()
            print("   Continuando con la carga...")
        
        # Leer CSV
        locations_added = 0
        departamentos = {}
        municipios = {}
        zonas = {}
        puestos = {}
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                dd = row['dd']  # Departamento
                
                # SOLO CARGAR CAQUETÁ (código 44)
                if dd != '44':
                    continue
                
                mm = row['mm']  # Municipio
                zz = row['zz']  # Zona
                pp = row['pp']  # Puesto
                mesa = row['mesa']
                
                departamento_nombre = row['departamento']
                municipio_nombre = row['municipio']
                puesto_nombre = row['puesto']
                mesa_nombre = row['mesa_nombre']
                
                # Crear departamento si no existe
                if dd not in departamentos:
                    dept = Location(
                        departamento_codigo=dd,
                        departamento_nombre=departamento_nombre,
                        nombre_completo=departamento_nombre,
                        tipo='departamento'
                    )
                    db.session.add(dept)
                    db.session.flush()
                    departamentos[dd] = dept.id
                    locations_added += 1
                    print(f"  + Departamento: {departamento_nombre}")
                
                # Crear municipio si no existe
                muni_key = f"{dd}-{mm}"
                if muni_key not in municipios:
                    muni = Location(
                        departamento_codigo=dd,
                        municipio_codigo=mm,
                        departamento_nombre=departamento_nombre,
                        municipio_nombre=municipio_nombre,
                        nombre_completo=f"{departamento_nombre} - {municipio_nombre}",
                        tipo='municipio',
                        parent_id=departamentos[dd]
                    )
                    db.session.add(muni)
                    db.session.flush()
                    municipios[muni_key] = muni.id
                    locations_added += 1
                
                # Crear zona si no existe
                zona_key = f"{dd}-{mm}-{zz}"
                if zona_key not in zonas:
                    zona = Location(
                        departamento_codigo=dd,
                        municipio_codigo=mm,
                        zona_codigo=zz,
                        departamento_nombre=departamento_nombre,
                        municipio_nombre=municipio_nombre,
                        nombre_completo=f"{departamento_nombre} - {municipio_nombre} - Zona {zz}",
                        tipo='zona',
                        parent_id=municipios[muni_key]
                    )
                    db.session.add(zona)
                    db.session.flush()
                    zonas[zona_key] = zona.id
                    locations_added += 1
                
                # Crear puesto si no existe
                puesto_key = f"{dd}-{mm}-{zz}-{pp}"
                if puesto_key not in puestos:
                    puesto = Location(
                        departamento_codigo=dd,
                        municipio_codigo=mm,
                        zona_codigo=zz,
                        puesto_codigo=pp,
                        departamento_nombre=departamento_nombre,
                        municipio_nombre=municipio_nombre,
                        puesto_nombre=puesto_nombre,
                        nombre_completo=f"{departamento_nombre} - {municipio_nombre} - Zona {zz} - {puesto_nombre}",
                        tipo='puesto',
                        direccion=row.get('direccion'),
                        comuna=row.get('comuna'),
                        latitud=float(row['LATITUD']) if row.get('LATITUD') else None,
                        longitud=float(row['LONGITUD']) if row.get('LONGITUD') else None,
                        parent_id=zonas[zona_key]
                    )
                    db.session.add(puesto)
                    db.session.flush()
                    puestos[puesto_key] = puesto.id
                    locations_added += 1
                
                # Crear mesa
                mesa_location = Location(
                    departamento_codigo=dd,
                    municipio_codigo=mm,
                    zona_codigo=zz,
                    puesto_codigo=pp,
                    mesa_codigo=mesa,
                    departamento_nombre=departamento_nombre,
                    municipio_nombre=municipio_nombre,
                    puesto_nombre=puesto_nombre,
                    mesa_nombre=mesa_nombre,
                    nombre_completo=f"{departamento_nombre} - {municipio_nombre} - Zona {zz} - {puesto_nombre} - Mesa {mesa}",
                    tipo='mesa',
                    total_votantes_registrados=int(row.get('total_mesa', 0)),
                    mujeres=int(row.get('mujeres_mesa', 0)),
                    hombres=int(row.get('hombres_mesa', 0)),
                    direccion=row.get('direccion'),
                    comuna=row.get('comuna'),
                    latitud=float(row['LATITUD']) if row.get('LATITUD') else None,
                    longitud=float(row['LONGITUD']) if row.get('LONGITUD') else None,
                    parent_id=puestos[puesto_key]
                )
                db.session.add(mesa_location)
                locations_added += 1
                
                # Commit cada 100 registros
                if locations_added % 100 == 0:
                    db.session.commit()
                    print(f"  >> {locations_added} ubicaciones procesadas...")
        
        # Commit final
        db.session.commit()
        
        print(f"\n>> Carga completada!")
        print(f">> Total de ubicaciones creadas: {locations_added}")
        print(f"   - Departamentos: {len(departamentos)}")
        print(f"   - Municipios: {len(municipios)}")
        print(f"   - Zonas: {len(zonas)}")
        print(f"   - Puestos: {len(puestos)}")
        print(f"   - Mesas: {locations_added - len(departamentos) - len(municipios) - len(zonas) - len(puestos)}")


if __name__ == '__main__':
    csv_path = 'todos los datos/divipola.csv'
    
    if not os.path.exists(csv_path):
        print(f"ERROR: No se encontro el archivo {csv_path}")
        sys.exit(1)
    
    load_divipola_from_csv(csv_path)
