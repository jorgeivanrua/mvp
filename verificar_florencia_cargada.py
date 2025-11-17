"""
Verificar datos de Florencia cargados
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.models.location import Location

def verificar():
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*70)
        print("VERIFICAR FLORENCIA")
        print("="*70)
        
        # Buscar Florencia
        florencia = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo='18'
        ).all()
        
        print(f"\n📍 Municipios del Caquetá: {len(florencia)}")
        for mun in florencia:
            print(f"  - Código: {mun.municipio_codigo} | {mun.nombre_completo}")
        
        # Buscar puestos de Florencia
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='18',
            municipio_codigo='01'
        ).all()
        
        print(f"\n📍 Puestos en Florencia: {len(puestos)}")
        for puesto in puestos[:10]:
            print(f"  - ID: {puesto.id} | {puesto.nombre_completo}")
        
        # Buscar La Salle
        la_salle = Location.query.filter(
            Location.tipo == 'puesto',
            Location.puesto_nombre.like('%LA SALLE%')
        ).all()
        
        print(f"\n📍 Puestos con 'LA SALLE': {len(la_salle)}")
        for puesto in la_salle:
            print(f"  - ID: {puesto.id} | {puesto.nombre_completo}")
            
            # Buscar mesas
            mesas = Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                zona_codigo=puesto.zona_codigo,
                puesto_codigo=puesto.puesto_codigo
            ).all()
            
            print(f"    Mesas: {len(mesas)}")
            for mesa in mesas:
                print(f"      - Mesa {mesa.mesa_codigo}: {mesa.nombre_completo}")

if __name__ == '__main__':
    verificar()
