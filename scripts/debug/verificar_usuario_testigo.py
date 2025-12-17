"""
Script para verificar y actualizar el usuario testigo_12345678
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.database import db

def verificar_usuario_testigo():
    """Verificar el estado actual del usuario testigo"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("VERIFICACIÓN DEL USUARIO TESTIGO")
        print("=" * 60)
        
        # Buscar usuario
        user = User.query.filter_by(cedula='12345678').first()
        if not user:
            print("❌ Usuario testigo_12345678 no encontrado")
            return
        
        print(f"✅ Usuario encontrado:")
        print(f"   ID: {user.id}")
        print(f"   Nombre: {user.nombre}")
        print(f"   Cédula: {user.cedula}")
        print(f"   Rol: {user.rol}")
        print(f"   Ubicación ID: {user.ubicacion_id}")
        print()
        
        # Verificar ubicación
        if user.ubicacion_id:
            location = Location.query.get(user.ubicacion_id)
            if location:
                print(f"✅ Ubicación actual:")
                print(f"   Nombre completo: {location.nombre_completo}")
                print(f"   Departamento: {location.departamento_nombre}")
                print(f"   Municipio: {location.municipio_nombre}")
                print(f"   Puesto: {location.puesto_nombre}")
                print(f"   Mesa: {location.mesa_nombre}")
                print(f"   Tipo: {location.tipo}")
                print(f"   Código departamento: {location.departamento_codigo}")
                print()
                
                # Verificar si es del Quindío
                if location.departamento_nombre == 'QUINDIO':
                    print("✅ El usuario está correctamente asignado al QUINDÍO")
                else:
                    print(f"❌ El usuario NO está en el Quindío, está en: {location.departamento_nombre}")
                    
                    # Buscar una mesa del Quindío para reasignar
                    print("\n🔄 Buscando mesa del Quindío para reasignar...")
                    mesa_quindio = Location.query.filter_by(
                        departamento_nombre='QUINDIO',
                        tipo='mesa'
                    ).first()
                    
                    if mesa_quindio:
                        print(f"   Mesa encontrada: {mesa_quindio.nombre_completo}")
                        
                        # Actualizar usuario
                        user.ubicacion_id = mesa_quindio.id
                        db.session.commit()
                        
                        print("✅ Usuario actualizado exitosamente")
                        print(f"   Nueva ubicación: {mesa_quindio.nombre_completo}")
                    else:
                        print("❌ No se encontraron mesas del Quindío")
            else:
                print("❌ Ubicación no encontrada en la base de datos")
        else:
            print("❌ Usuario sin ubicación asignada")
        
        print()
        print("=" * 60)

if __name__ == '__main__':
    verificar_usuario_testigo()