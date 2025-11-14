"""
Script para resetear todas las contraseñas a test123
"""
from backend.app import create_app
from backend.database import db
from backend.models.user import User

def reset_all_passwords():
    """Resetear todas las contraseñas a test123"""
    app = create_app()
    
    with app.app_context():
        print("\n🔄 Reseteando contraseñas de todos los usuarios...")
        
        # Obtener todos los usuarios
        users = User.query.all()
        
        if not users:
            print("❌ No se encontraron usuarios en la base de datos")
            return
        
        print(f"📊 Encontrados {len(users)} usuarios\n")
        
        # Resetear contraseña de cada usuario
        for user in users:
            user.set_password('test123')
            print(f"✅ {user.nombre} ({user.rol}) - Contraseña reseteada")
        
        # Guardar cambios
        db.session.commit()
        
        print("\n" + "="*60)
        print("  ✅ TODAS LAS CONTRASEÑAS RESETEADAS")
        print("="*60)
        print("\n🔑 Contraseña universal: test123")
        print("\n📋 Usuarios actualizados:")
        for user in users:
            ubicacion = f"Ubicación ID: {user.ubicacion_id}" if user.ubicacion_id else "Sin ubicación"
            print(f"   • {user.nombre} - {user.rol} - {ubicacion}")
        print()

if __name__ == '__main__':
    reset_all_passwords()
