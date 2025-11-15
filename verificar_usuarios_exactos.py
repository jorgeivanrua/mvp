"""
Script para ver exactamente qué usuarios existen y sus ubicaciones
"""
from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app()

with app.app_context():
    print("\n" + "="*60)
    print("USUARIOS EN LA BASE DE DATOS")
    print("="*60)
    
    users = User.query.all()
    
    for user in users:
        print(f"\n{'='*60}")
        print(f"ID: {user.id}")
        print(f"Nombre: {user.nombre}")
        print(f"Rol: {user.rol}")
        
        if user.ubicacion_id:
            loc = Location.query.get(user.ubicacion_id)
            if loc:
                print(f"Ubicación ID: {user.ubicacion_id}")
                print(f"Ubicación: {loc.nombre_completo}")
                print(f"Tipo: {loc.tipo}")
                print(f"Departamento: {loc.departamento_nombre} ({loc.departamento_codigo})")
                if loc.municipio_nombre:
                    print(f"Municipio: {loc.municipio_nombre} ({loc.municipio_codigo})")
                if loc.zona_codigo:
                    print(f"Zona: {loc.zona_codigo}")
                if loc.puesto_nombre:
                    print(f"Puesto: {loc.puesto_nombre} ({loc.puesto_codigo})")
        else:
            print("Ubicación: Sin ubicación")
        
        print(f"Activo: {user.activo}")
        
        # Verificar contraseña
        if user.check_password('test123'):
            print("✅ Contraseña test123: CORRECTA")
        else:
            print("❌ Contraseña test123: INCORRECTA")
    
    print(f"\n{'='*60}")
    print(f"Total usuarios: {len(users)}")
    print("="*60)
