"""
Verificar ubicación del super admin
"""
from backend.database import db
from backend.models.user import User
from backend.app import create_app

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("VERIFICACIÓN SUPER ADMIN")
    print("="*70)
    
    # Buscar super admin
    super_admin = User.query.filter_by(rol='super_admin').first()
    
    if super_admin:
        print(f"\n✅ Super Admin encontrado:")
        print(f"  - ID: {super_admin.id}")
        print(f"  - Nombre: {super_admin.nombre}")
        print(f"  - Rol: {super_admin.rol}")
        print(f"  - Ubicación ID: {super_admin.ubicacion_id}")
        print(f"  - Activo: {super_admin.activo}")
        print(f"  - Intentos fallidos: {super_admin.intentos_fallidos}")
        print(f"  - Bloqueado hasta: {super_admin.bloqueado_hasta}")
        
        # Verificar contraseña
        if super_admin.check_password('test123'):
            print(f"\n✅ Contraseña 'test123' es correcta")
        else:
            print(f"\n❌ Contraseña 'test123' NO es correcta")
        
        # Si tiene ubicación, corregirla
        if super_admin.ubicacion_id is not None:
            print(f"\n⚠️  Super Admin tiene ubicación asignada (ID: {super_admin.ubicacion_id})")
            print(f"   Corrigiendo...")
            super_admin.ubicacion_id = None
            db.session.commit()
            print(f"✅ Ubicación removida")
    else:
        print(f"\n❌ Super Admin NO encontrado")
    
    print("\n" + "="*70)
