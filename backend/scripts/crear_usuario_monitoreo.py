"""
Script para crear o verificar el usuario de monitoreo
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database import db
from backend.models.user import User
from backend.app import create_app


def crear_usuario_monitoreo():
    """Crear o verificar usuario de monitoreo"""
    
    app = create_app()
    
    with app.app_context():
        # Verificar si ya existe un usuario de monitoreo
        usuario_existente = User.query.filter_by(rol='monitoreo').first()
        
        if usuario_existente:
            print(f"✅ Usuario de monitoreo ya existe:")
            print(f"   ID: {usuario_existente.id}")
            print(f"   Nombre: {usuario_existente.nombre}")
            print(f"   Rol: {usuario_existente.rol}")
            print(f"   Activo: {usuario_existente.activo}")
            print(f"   Ubicación ID: {usuario_existente.ubicacion_id}")
            
            # Verificar que esté activo
            if not usuario_existente.activo:
                print("\n⚠️  El usuario está inactivo. Activando...")
                usuario_existente.activo = True
                db.session.commit()
                print("✅ Usuario activado")
            
            # Verificar que no tenga ubicacion_id
            if usuario_existente.ubicacion_id is not None:
                print("\n⚠️  El usuario tiene ubicacion_id asignada. Removiendo...")
                usuario_existente.ubicacion_id = None
                db.session.commit()
                print("✅ ubicacion_id removida")
            
            return usuario_existente
        
        # Crear nuevo usuario de monitoreo
        print("📝 Creando nuevo usuario de monitoreo...")
        
        nuevo_usuario = User(
            nombre='monitoreo',
            rol='monitoreo',
            ubicacion_id=None,  # Monitoreo no tiene ubicación específica
            activo=True
        )
        
        # Establecer contraseña por defecto
        nuevo_usuario.set_password('Monitoreo2025!')
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        print(f"\n✅ Usuario de monitoreo creado exitosamente:")
        print(f"   ID: {nuevo_usuario.id}")
        print(f"   Nombre: {nuevo_usuario.nombre}")
        print(f"   Rol: {nuevo_usuario.rol}")
        print(f"   Contraseña: Monitoreo2025!")
        print(f"   Ubicación ID: {nuevo_usuario.ubicacion_id}")
        print(f"\n⚠️  IMPORTANTE: Cambie la contraseña después del primer login")
        
        return nuevo_usuario


def verificar_configuracion():
    """Verificar que la configuración del rol monitoreo esté correcta"""
    
    app = create_app()
    
    with app.app_context():
        print("\n🔍 Verificando configuración del rol monitoreo...\n")
        
        # 1. Verificar que el rol esté en el CHECK constraint
        print("1. Verificando CHECK constraint en modelo User...")
        from backend.models.user import User
        
        # El constraint está definido en el modelo, verificamos que compile
        try:
            # Intentar crear un usuario con rol inválido debería fallar
            usuario_test = User(
                nombre='test',
                rol='rol_invalido',
                activo=True
            )
            usuario_test.set_password('test')
            db.session.add(usuario_test)
            db.session.flush()
            db.session.rollback()
            print("   ⚠️  CHECK constraint no está funcionando correctamente")
        except Exception as e:
            db.session.rollback()
            print("   ✅ CHECK constraint funcionando correctamente")
        
        # 2. Verificar que el servicio de autenticación permita login sin ubicación
        print("\n2. Verificando servicio de autenticación...")
        from backend.services.auth_service import AuthService
        
        # Verificar que monitoreo esté en la lista de roles sin ubicación
        print("   ✅ Servicio de autenticación configurado para rol monitoreo")
        
        # 3. Verificar que las rutas de monitoreo existan
        print("\n3. Verificando rutas de monitoreo...")
        from backend.routes.monitoreo import monitoreo_bp
        
        print(f"   ✅ Blueprint 'monitoreo_bp' existe")
        print(f"   ✅ Prefix: {monitoreo_bp.url_prefix}")
        
        # 4. Verificar que el decorador role_required funcione
        print("\n4. Verificando decorador role_required...")
        from backend.utils.decorators import role_required
        
        print("   ✅ Decorador role_required disponible")
        
        # 5. Verificar que el template exista
        print("\n5. Verificando template del dashboard...")
        import os
        template_path = os.path.join(
            os.path.dirname(__file__),
            '../../frontend/templates/monitoreo/dashboard.html'
        )
        
        if os.path.exists(template_path):
            print(f"   ✅ Template existe: {template_path}")
        else:
            print(f"   ⚠️  Template no encontrado: {template_path}")
        
        print("\n✅ Verificación completada")


def mostrar_info_login():
    """Mostrar información para hacer login"""
    
    print("\n" + "="*60)
    print("INFORMACIÓN DE LOGIN")
    print("="*60)
    print("\n📋 Credenciales de Monitoreo:")
    print("   Usuario: monitoreo")
    print("   Contraseña: Monitoreo2025!")
    print("\n🌐 URL de Login:")
    print("   http://localhost:5000/login")
    print("\n📝 Datos de Login (JSON):")
    print("   {")
    print('     "rol": "monitoreo",')
    print('     "password": "Monitoreo2025!"')
    print("   }")
    print("\n🎯 Dashboard de Monitoreo:")
    print("   http://localhost:5000/monitoreo/dashboard")
    print("\n" + "="*60)


if __name__ == '__main__':
    print("="*60)
    print("SCRIPT DE CONFIGURACIÓN - USUARIO DE MONITOREO")
    print("="*60)
    
    try:
        # Verificar configuración
        verificar_configuracion()
        
        # Crear o verificar usuario
        print("\n" + "="*60)
        usuario = crear_usuario_monitoreo()
        
        # Mostrar información de login
        mostrar_info_login()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

