"""
Script para actualizar contraseñas en Render a texto plano
Ejecutar desde la consola de Render con: python actualizar_passwords_render.py
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User


def actualizar_passwords():
    """Actualizar todas las contraseñas a texto plano"""
    config_name = os.getenv('FLASK_ENV', 'production')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n>> Actualizando contraseñas a texto plano...")
        
        # Obtener todos los usuarios
        users = User.query.all()
        
        if not users:
            print("❌ No se encontraron usuarios en la base de datos")
            return
        
        print(f">> Encontrados {len(users)} usuarios")
        
        # Actualizar contraseñas
        updated_count = 0
        for user in users:
            try:
                # Determinar la contraseña según el rol
                if user.rol == 'super_admin':
                    new_password = 'admin123'
                else:
                    new_password = 'test123'
                
                # Actualizar contraseña (ahora se guarda en texto plano)
                user.set_password(new_password)
                db.session.commit()
                
                print(f"✅ Actualizado: {user.nombre} ({user.rol}) - Password: {new_password}")
                updated_count += 1
                
            except Exception as e:
                print(f"❌ Error actualizando {user.nombre}: {e}")
                db.session.rollback()
        
        print(f"\n>> Total de contraseñas actualizadas: {updated_count}")
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("CREDENCIALES ACTUALIZADAS")
        print("="*60)
        print("\n🔑 Super Admin:")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        print("\n🔑 Todos los demás usuarios:")
        print("   Contraseña: test123")
        print("\n" + "="*60)
        
        print("\n✅ Contraseñas actualizadas exitosamente!")


if __name__ == '__main__':
    actualizar_passwords()
