"""
Verificar códigos de ubicaciones en la base de datos
"""
from backend.database import db
from backend.models.location import Location
from backend.app import create_app

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("CÓDIGOS DE UBICACIONES EN LA BASE DE DATOS")
    print("="*70)
    
    # Departamentos
    departamentos = Location.query.filter_by(tipo='departamento').all()
    print(f"\n📍 DEPARTAMENTOS ({len(departamentos)}):")
    for dept in departamentos:
        print(f"  - {dept.departamento_codigo}: {dept.departamento_nombre}")
    
    # Municipios
    municipios = Location.query.filter_by(tipo='municipio').limit(10).all()
    print(f"\n🏘️  MUNICIPIOS (primeros 10):")
    for mun in municipios:
        print(f"  - {mun.municipio_codigo}: {mun.municipio_nombre} (Dept: {mun.departamento_codigo})")
    
    # Zonas
    zonas = Location.query.filter_by(tipo='zona').limit(10).all()
    print(f"\n📌 ZONAS (primeras 10):")
    for zona in zonas:
        print(f"  - {zona.zona_codigo}: Zona {zona.zona_codigo} (Mun: {zona.municipio_codigo})")
    
    # Puestos
    puestos = Location.query.filter_by(tipo='puesto').limit(10).all()
    print(f"\n🏢 PUESTOS (primeros 10):")
    for puesto in puestos:
        print(f"  - {puesto.puesto_codigo}: {puesto.puesto_nombre} (Zona: {puesto.zona_codigo})")
    
    print("\n" + "="*70)
