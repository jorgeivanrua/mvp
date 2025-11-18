"""
Verificar testigos en el puesto 02
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

app = create_app()

with app.app_context():
    print("\n=== VERIFICANDO PUESTO 02 ===\n")
    
    # Buscar el puesto
    puesto = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='18',
        municipio_codigo='01',
        zona_codigo='01',
        puesto_codigo='02'
    ).first()
    
    if puesto:
        print(f"Puesto encontrado:")
        print(f"  ID: {puesto.id}")
        print(f"  Nombre: {puesto.nombre_completo}")
        print(f"  Códigos: Dept={puesto.departamento_codigo}, Mun={puesto.municipio_codigo}, Zona={puesto.zona_codigo}, Puesto={puesto.puesto_codigo}")
        
        # Buscar testigos en este puesto
        testigos = User.query.filter_by(
            rol='testigo_electoral',
            ubicacion_id=puesto.id
        ).all()
        
        print(f"\nTestigos en este puesto: {len(testigos)}")
        for testigo in testigos:
            print(f"  - {testigo.nombre} (ID: {testigo.id})")
        
        # Buscar mesas de este puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo='18',
            municipio_codigo='01',
            zona_codigo='01',
            puesto_codigo='02'
        ).all()
        
        print(f"\nMesas en este puesto: {len(mesas)}")
        for mesa in mesas:
            print(f"  - {mesa.nombre_completo} (ID: {mesa.id})")
            
            # Buscar testigos asignados a esta mesa (incorrectamente)
            testigos_mesa = User.query.filter_by(
                rol='testigo_electoral',
                ubicacion_id=mesa.id
            ).all()
            
            if testigos_mesa:
                print(f"    ⚠️  Testigos asignados a esta mesa (debería ser al puesto):")
                for t in testigos_mesa:
                    print(f"      - {t.nombre} (ID: {t.id})")
    else:
        print("❌ Puesto no encontrado")
        
    print("\n=== TODOS LOS TESTIGOS CON ZONA 01 ===\n")
    
    # Buscar todos los testigos en zona 01
    testigos_zona = User.query.filter_by(rol='testigo_electoral').all()
    
    for testigo in testigos_zona:
        ubicacion = Location.query.get(testigo.ubicacion_id)
        if ubicacion and ubicacion.zona_codigo == '01':
            print(f"Testigo: {testigo.nombre}")
            print(f"  Ubicación: {ubicacion.nombre_completo}")
            print(f"  Tipo: {ubicacion.tipo}")
            print(f"  Códigos: Dept={ubicacion.departamento_codigo}, Mun={ubicacion.municipio_codigo}, Zona={ubicacion.zona_codigo}, Puesto={ubicacion.puesto_codigo}")
            print()
