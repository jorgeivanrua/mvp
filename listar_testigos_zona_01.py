"""
Listar todos los testigos de la zona 01
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

app = create_app()

with app.app_context():
    print("\n" + "="*80)
    print("TESTIGOS ELECTORALES - ZONA 01")
    print("="*80 + "\n")
    
    # Obtener todos los testigos
    testigos = User.query.filter_by(rol='testigo_electoral').all()
    
    testigos_zona_01 = []
    
    for testigo in testigos:
        if testigo.ubicacion_id:
            ubicacion = Location.query.get(testigo.ubicacion_id)
            if ubicacion and ubicacion.zona_codigo == '01':
                testigos_zona_01.append((testigo, ubicacion))
    
    print(f"Total testigos en zona 01: {len(testigos_zona_01)}\n")
    
    for testigo, ubicacion in testigos_zona_01:
        print(f"Usuario: {testigo.nombre}")
        print(f"  ID: {testigo.id}")
        print(f"  Ubicación: {ubicacion.nombre_completo}")
        print(f"  Tipo ubicación: {ubicacion.tipo}")
        print(f"  Contraseña: test123")
        print(f"  Login JSON:")
        print(f"  {{")
        print(f"    'rol': 'testigo_electoral',")
        print(f"    'departamento_codigo': '{ubicacion.departamento_codigo}',")
        print(f"    'municipio_codigo': '{ubicacion.municipio_codigo}',")
        print(f"    'zona_codigo': '{ubicacion.zona_codigo}',")
        print(f"    'puesto_codigo': '{ubicacion.puesto_codigo}',")
        print(f"    'password': 'test123'")
        print(f"  }}")
        print()
