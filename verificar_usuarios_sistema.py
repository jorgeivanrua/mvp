"""
Verificar usuarios del sistema por rol
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("USUARIOS POR ROL")
    print("="*70)
    
    roles = [
        'super_admin',
        'coordinador_departamental',
        'coordinador_municipal',
        'coordinador_puesto',
        'testigo_electoral',
        'auditor_electoral'
    ]
    
    for rol in roles:
        usuarios = User.query.filter_by(rol=rol).all()
        print(f"\n📋 {rol.upper().replace('_', ' ')} ({len(usuarios)} usuarios):")
        
        for user in usuarios[:3]:  # Mostrar solo los primeros 3
            ubicacion_info = "Sin ubicación"
            if user.ubicacion_id:
                ubicacion = Location.query.get(user.ubicacion_id)
                if ubicacion:
                    ubicacion_info = f"{ubicacion.tipo}: {ubicacion.nombre_completo}"
            
            print(f"  - {user.nombre}")
            print(f"    ID: {user.id} | Ubicación: {ubicacion_info}")
