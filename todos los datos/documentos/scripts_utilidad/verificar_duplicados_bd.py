"""
Verificar si hay datos duplicados en la base de datos
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.models.location import Location
from sqlalchemy import func

def verificar_duplicados():
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*70)
        print("VERIFICAR DUPLICADOS EN BASE DE DATOS")
        print("="*70)
        
        # Verificar departamentos duplicados
        print("\n📍 DEPARTAMENTOS:")
        departamentos = Location.query.filter_by(tipo='departamento').all()
        print(f"Total departamentos: {len(departamentos)}")
        
        for dept in departamentos:
            print(f"  - ID: {dept.id} | Código: {dept.departamento_codigo} | {dept.nombre_completo}")
        
        # Buscar duplicados por código
        duplicados_dept = Location.query.filter_by(tipo='departamento')\
            .with_entities(
                Location.departamento_codigo,
                func.count(Location.id).label('count')
            )\
            .group_by(Location.departamento_codigo)\
            .having(func.count(Location.id) > 1)\
            .all()
        
        if duplicados_dept:
            print("\n⚠️  DEPARTAMENTOS DUPLICADOS:")
            for codigo, count in duplicados_dept:
                print(f"  Código {codigo}: {count} registros")
                depts = Location.query.filter_by(
                    tipo='departamento',
                    departamento_codigo=codigo
                ).all()
                for d in depts:
                    print(f"    - ID: {d.id} | {d.nombre_completo}")
        else:
            print("\n✅ No hay departamentos duplicados")
        
        # Verificar municipios del Caquetá
        print("\n📍 MUNICIPIOS DEL CAQUETÁ:")
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo='18'
        ).all()
        print(f"Total municipios: {len(municipios)}")
        
        for mun in municipios[:5]:
            print(f"  - ID: {mun.id} | Código: {mun.municipio_codigo} | {mun.nombre_completo}")
        
        # Verificar zonas de Florencia
        print("\n📍 ZONAS DE FLORENCIA:")
        zonas = Location.query.filter_by(
            tipo='zona',
            departamento_codigo='18',
            municipio_codigo='01'
        ).all()
        print(f"Total zonas: {len(zonas)}")
        
        for zona in zonas:
            print(f"  - ID: {zona.id} | Código: {zona.zona_codigo} | {zona.nombre_completo}")
        
        # Verificar puestos de Florencia Zona 01
        print("\n📍 PUESTOS DE FLORENCIA ZONA 01:")
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='18',
            municipio_codigo='01',
            zona_codigo='01'
        ).all()
        print(f"Total puestos: {len(puestos)}")
        
        for puesto in puestos[:10]:
            print(f"  - ID: {puesto.id} | Código: {puesto.puesto_codigo} | {puesto.nombre_completo}")

if __name__ == '__main__':
    verificar_duplicados()
