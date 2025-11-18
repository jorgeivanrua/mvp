"""
Resetear contraseñas de todos los usuarios a test123
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.database import db
from backend.models.user import User

def resetear_contraseñas():
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*70)
        print("RESETEAR CONTRASEÑAS DE TODOS LOS USUARIOS")
        print("="*70)
        
        # Obtener todos los usuarios
        usuarios = User.query.all()
        
        print(f"\n📊 Total usuarios encontrados: {len(usuarios)}")
        
        if not usuarios:
            print("\n⚠️  No hay usuarios en el sistema")
            return
        
        print("\n🔄 Reseteando contraseñas...")
        
        usuarios_por_rol = {}
        
        for usuario in usuarios:
            # Resetear contraseña
            usuario.set_password('test123')
            
            # Agrupar por rol
            if usuario.rol not in usuarios_por_rol:
                usuarios_por_rol[usuario.rol] = []
            usuarios_por_rol[usuario.rol].append(usuario)
        
        db.session.commit()
        
        print("\n✅ Contraseñas reseteadas exitosamente")
        
        print("\n" + "="*70)
        print("RESUMEN DE USUARIOS POR ROL")
        print("="*70)
        
        for rol, users in sorted(usuarios_por_rol.items()):
            print(f"\n📋 {rol.upper().replace('_', ' ')} ({len(users)} usuarios):")
            for user in users:
                ubicacion_info = ""
                if user.ubicacion_id:
                    ubicacion_info = f" | Ubicación ID: {user.ubicacion_id}"
                print(f"  - ID: {user.id:3d} | {user.nombre:40s} | Contraseña: test123{ubicacion_info}")
        
        print("\n" + "="*70)
        print("✅ TODAS LAS CONTRASEÑAS ACTUALIZADAS A: test123")
        print("="*70)
        
        # Resumen por rol
        print("\n📊 RESUMEN:")
        for rol, users in sorted(usuarios_por_rol.items()):
            print(f"  {rol:30s}: {len(users):3d} usuarios")
        print(f"  {'TOTAL':30s}: {len(usuarios):3d} usuarios")
        
        print("\n" + "="*70)

if __name__ == '__main__':
    resetear_contraseñas()
