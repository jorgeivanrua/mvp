"""
Resetear contraseña del super admin a test123
"""
from backend.database import db
from backend.models.user import User
from backend.app import create_app

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("RESETEAR SUPER ADMIN")
    print("="*70)
    
    # Buscar super admin
    super_admin = User.query.filter_by(rol='super_admin').first()
    
    if super_admin:
        print(f"\n✅ Super Admin encontrado: {super_admin.nombre}")
        print(f"   ID: {super_admin.id}")
        print(f"   Intentos fallidos: {super_admin.intentos_fallidos}")
        
        # Resetear contraseña
        super_admin.set_password('test123')
        super_admin.intentos_fallidos = 0
        super_admin.bloqueado_hasta = None
        
        db.session.commit()
        
        print(f"\n✅ Contraseña reseteada a: test123")
        print(f"✅ Intentos fallidos reseteados a: 0")
        
        # Verificar
        if super_admin.check_password('test123'):
            print(f"\n✅ VERIFICACIÓN: Contraseña 'test123' funciona correctamente")
        else:
            print(f"\n❌ ERROR: Contraseña 'test123' NO funciona")
    else:
        print(f"\n❌ Super Admin NO encontrado")
    
    print("\n" + "="*70)
