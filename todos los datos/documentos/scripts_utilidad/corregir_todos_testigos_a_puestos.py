"""
Corregir TODOS los testigos para que estén asignados a puestos en lugar de mesas
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

app = create_app()

with app.app_context():
    print("\n=== CORRIGIENDO TODOS LOS TESTIGOS ===\n")
    
    # Obtener todos los testigos
    testigos = User.query.filter_by(rol='testigo_electoral').all()
    
    corregidos = 0
    ya_correctos = 0
    
    for testigo in testigos:
        if testigo.ubicacion_id:
            ubicacion = Location.query.get(testigo.ubicacion_id)
            
            if ubicacion and ubicacion.tipo == 'mesa':
                # Buscar el puesto correspondiente
                puesto = Location.query.filter_by(
                    tipo='puesto',
                    departamento_codigo=ubicacion.departamento_codigo,
                    municipio_codigo=ubicacion.municipio_codigo,
                    zona_codigo=ubicacion.zona_codigo,
                    puesto_codigo=ubicacion.puesto_codigo
                ).first()
                
                if puesto:
                    print(f"Corrigiendo: {testigo.nombre}")
                    print(f"  De: {ubicacion.nombre_completo} (mesa)")
                    print(f"  A:  {puesto.nombre_completo} (puesto)")
                    
                    testigo.ubicacion_id = puesto.id
                    corregidos += 1
                else:
                    print(f"⚠️  No se encontró puesto para: {testigo.nombre}")
            elif ubicacion and ubicacion.tipo == 'puesto':
                ya_correctos += 1
    
    db.session.commit()
    
    print(f"\n✅ Testigos corregidos: {corregidos}")
    print(f"✅ Testigos ya correctos: {ya_correctos}")
    print(f"📊 Total testigos: {len(testigos)}")
