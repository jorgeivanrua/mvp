"""
Verificar puesto La Salle y sus mesas
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.models.location import Location
from backend.models.user import User

def verificar_puesto():
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*70)
        print("VERIFICAR PUESTO LA SALLE")
        print("="*70)
        
        # Buscar el puesto
        puestos = Location.query.filter(
            Location.tipo == 'puesto',
            Location.nombre_completo.like('%LA SALLE%')
        ).all()
        
        if not puestos:
            print("\n❌ No se encontró puesto con 'LA SALLE' en el nombre")
            print("\nBuscando todos los puestos en Florencia...")
            
            puestos_florencia = Location.query.filter_by(
                tipo='puesto',
                municipio_codigo='001',
                departamento_codigo='18'
            ).all()
            
            print(f"\n📍 Puestos en Florencia: {len(puestos_florencia)}")
            for p in puestos_florencia:
                print(f"  ID: {p.id:3d} | Código: {p.puesto_codigo} | {p.nombre_completo}")
        else:
            for puesto in puestos:
                print(f"\n✅ Puesto encontrado:")
                print(f"  ID: {puesto.id}")
                print(f"  Nombre: {puesto.nombre_completo}")
                print(f"  Código puesto: {puesto.puesto_codigo}")
                print(f"  Departamento: {puesto.departamento_codigo}")
                print(f"  Municipio: {puesto.municipio_codigo}")
                print(f"  Zona: {puesto.zona_codigo}")
                
                # Buscar mesas
                mesas = Location.query.filter_by(
                    tipo='mesa',
                    departamento_codigo=puesto.departamento_codigo,
                    municipio_codigo=puesto.municipio_codigo,
                    zona_codigo=puesto.zona_codigo,
                    puesto_codigo=puesto.puesto_codigo
                ).all()
                
                print(f"\n📋 Mesas del puesto: {len(mesas)}")
                
                for mesa in mesas:
                    # Verificar testigo
                    testigo = User.query.filter_by(
                        ubicacion_id=mesa.id,
                        rol='testigo_electoral'
                    ).first()
                    
                    estado = f"✅ Testigo: {testigo.username}" if testigo else "❌ Sin testigo"
                    print(f"  Mesa {mesa.mesa_codigo}: ID {mesa.id} - {estado}")

if __name__ == '__main__':
    verificar_puesto()
