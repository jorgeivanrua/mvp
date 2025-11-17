"""
Cargar datos DIVIPOLA del Caquetá a la base de datos
"""
import sys
sys.path.insert(0, '.')

import csv
from backend.app import create_app
from backend.database import db
from backend.models.location import Location

def cargar_divipola_caqueta():
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*70)
        print("CARGAR DIVIPOLA - CAQUETÁ")
        print("="*70)
        
        # Verificar si ya existen datos
        caqueta_existente = Location.query.filter_by(
            departamento_codigo='18',
            tipo='departamento'
        ).first()
        
        if caqueta_existente:
            print("\n⚠️  Ya existen datos del Caquetá en la base de datos")
            print(f"   Departamento: {caqueta_existente.nombre_completo}")
            
            # Contar registros
            total_municipios = Location.query.filter_by(
                departamento_codigo='18',
                tipo='municipio'
            ).count()
            
            total_zonas = Location.query.filter_by(
                departamento_codigo='18',
                tipo='zona'
            ).count()
            
            total_puestos = Location.query.filter_by(
                departamento_codigo='18',
                tipo='puesto'
            ).count()
            
            total_mesas = Location.query.filter_by(
                departamento_codigo='18',
                tipo='mesa'
            ).count()
            
            print(f"\n📊 Estadísticas actuales:")
            print(f"   Municipios: {total_municipios}")
            print(f"   Zonas: {total_zonas}")
            print(f"   Puestos: {total_puestos}")
            print(f"   Mesas: {total_mesas}")
            
            return
        
        print("\n📂 Leyendo archivo DIVIPOLA...")
        
        # Leer CSV
        registros_caqueta = []
        with open('todos los datos/divipola.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['departamento'] == 'CAQUETA':
                    registros_caqueta.append(row)
        
        print(f"✅ Encontrados {len(registros_caqueta)} registros del Caquetá")
        
        # Crear departamento
        print("\n📍 Creando departamento...")
        departamento = Location(
            departamento_codigo='18',
            departamento_nombre='CAQUETA',
            nombre_completo='CAQUETA',
            tipo='departamento',
            activo=True
        )
        db.session.add(departamento)
        db.session.flush()
        print(f"✅ Departamento creado: {departamento.nombre_completo}")
        
        # Agrupar por municipio
        municipios = {}
        for reg in registros_caqueta:
            mun_codigo = reg['mm']
            if mun_codigo not in municipios:
                municipios[mun_codigo] = reg['municipio']
        
        print(f"\n📍 Creando {len(municipios)} municipios...")
        municipios_obj = {}
        for mun_codigo, mun_nombre in municipios.items():
            municipio = Location(
                departamento_codigo='18',
                municipio_codigo=mun_codigo,
                departamento_nombre='CAQUETA',
                municipio_nombre=mun_nombre,
                nombre_completo=f'CAQUETA - {mun_nombre}',
                tipo='municipio',
                activo=True,
                parent_id=departamento.id
            )
            db.session.add(municipio)
            db.session.flush()
            municipios_obj[mun_codigo] = municipio
            print(f"  ✅ {municipio.nombre_completo}")
        
        # Agrupar por zona
        zonas = {}
        for reg in registros_caqueta:
            zona_key = f"{reg['mm']}_{reg['zz']}"
            if zona_key not in zonas:
                zonas[zona_key] = {
                    'municipio_codigo': reg['mm'],
                    'zona_codigo': reg['zz'],
                    'municipio_nombre': reg['municipio']
                }
        
        print(f"\n📍 Creando {len(zonas)} zonas...")
        zonas_obj = {}
        for zona_key, zona_data in zonas.items():
            municipio = municipios_obj[zona_data['municipio_codigo']]
            zona = Location(
                departamento_codigo='18',
                municipio_codigo=zona_data['municipio_codigo'],
                zona_codigo=zona_data['zona_codigo'],
                departamento_nombre='CAQUETA',
                municipio_nombre=zona_data['municipio_nombre'],
                nombre_completo=f"CAQUETA - {zona_data['municipio_nombre']} - Zona {zona_data['zona_codigo']}",
                tipo='zona',
                activo=True,
                parent_id=municipio.id
            )
            db.session.add(zona)
            db.session.flush()
            zonas_obj[zona_key] = zona
        
        print(f"✅ Zonas creadas")
        
        # Agrupar por puesto
        puestos = {}
        for reg in registros_caqueta:
            puesto_key = f"{reg['mm']}_{reg['zz']}_{reg['pp']}"
            if puesto_key not in puestos:
                puestos[puesto_key] = {
                    'municipio_codigo': reg['mm'],
                    'zona_codigo': reg['zz'],
                    'puesto_codigo': reg['pp'],
                    'puesto_nombre': reg['puesto'],
                    'municipio_nombre': reg['municipio'],
                    'comuna': reg.get('comuna', ''),
                    'direccion': reg.get('direccion', ''),
                    'latitud': reg.get('LATITUD', ''),
                    'longitud': reg.get('LONGITUD', '')
                }
        
        print(f"\n📍 Creando {len(puestos)} puestos...")
        puestos_obj = {}
        for puesto_key, puesto_data in puestos.items():
            zona_key = f"{puesto_data['municipio_codigo']}_{puesto_data['zona_codigo']}"
            zona = zonas_obj[zona_key]
            
            puesto = Location(
                departamento_codigo='18',
                municipio_codigo=puesto_data['municipio_codigo'],
                zona_codigo=puesto_data['zona_codigo'],
                puesto_codigo=puesto_data['puesto_codigo'],
                departamento_nombre='CAQUETA',
                municipio_nombre=puesto_data['municipio_nombre'],
                puesto_nombre=puesto_data['puesto_nombre'],
                nombre_completo=puesto_data['puesto_nombre'],
                tipo='puesto',
                comuna=puesto_data['comuna'],
                direccion=puesto_data['direccion'],
                latitud=float(puesto_data['latitud']) if puesto_data['latitud'] else None,
                longitud=float(puesto_data['longitud']) if puesto_data['longitud'] else None,
                activo=True,
                parent_id=zona.id
            )
            db.session.add(puesto)
            db.session.flush()
            puestos_obj[puesto_key] = puesto
            print(f"  ✅ {puesto.nombre_completo}")
        
        # Crear mesas
        print(f"\n📍 Creando mesas...")
        mesas_creadas = 0
        for reg in registros_caqueta:
            puesto_key = f"{reg['mm']}_{reg['zz']}_{reg['pp']}"
            puesto = puestos_obj[puesto_key]
            
            mesa = Location(
                departamento_codigo='18',
                municipio_codigo=reg['mm'],
                zona_codigo=reg['zz'],
                puesto_codigo=reg['pp'],
                mesa_codigo=reg['mesa'],
                departamento_nombre='CAQUETA',
                municipio_nombre=reg['municipio'],
                puesto_nombre=reg['puesto'],
                mesa_nombre=reg['mesa_nombre'],
                nombre_completo=reg['mesa_nombre'],
                tipo='mesa',
                total_votantes_registrados=int(reg['total_mesa']) if reg['total_mesa'] else 0,
                mujeres=int(reg['mujeres_mesa']) if reg['mujeres_mesa'] else 0,
                hombres=int(reg['hombres_mesa']) if reg['hombres_mesa'] else 0,
                comuna=reg.get('comuna', ''),
                direccion=reg.get('direccion', ''),
                latitud=float(reg['LATITUD']) if reg['LATITUD'] else None,
                longitud=float(reg['LONGITUD']) if reg['LONGITUD'] else None,
                activo=True,
                parent_id=puesto.id
            )
            db.session.add(mesa)
            mesas_creadas += 1
            
            if mesas_creadas % 100 == 0:
                print(f"  Procesadas {mesas_creadas} mesas...")
        
        db.session.commit()
        
        print(f"\n✅ Total mesas creadas: {mesas_creadas}")
        
        print("\n" + "="*70)
        print("✅ DIVIPOLA CAQUETÁ CARGADO EXITOSAMENTE")
        print("="*70)
        
        print(f"\n📊 Resumen:")
        print(f"   Departamento: 1")
        print(f"   Municipios: {len(municipios)}")
        print(f"   Zonas: {len(zonas)}")
        print(f"   Puestos: {len(puestos)}")
        print(f"   Mesas: {mesas_creadas}")
        
        print("\n" + "="*70)

if __name__ == '__main__':
    cargar_divipola_caqueta()
