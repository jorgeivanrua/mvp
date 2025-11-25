#!/usr/bin/env python3
"""
Script simple para verificar si el usuario de monitoreo ya existe
"""

try:
    from backend.database import db
    from backend.models.user import User
    from backend.app import create_app
    
    app = create_app()
    
    with app.app_context():
        # Buscar usuario de monitoreo
        usuario = User.query.filter_by(rol='monitoreo').first()
        
        if usuario:
            print("✅ USUARIO DE MONITOREO ENCONTRADO")
            print(f"   ID: {usuario.id}")
            print(f"   Nombre: {usuario.nombre}")
            print(f"   Rol: {usuario.rol}")
            print(f"   Activo: {usuario.activo}")
            print(f"   Ubicación ID: {usuario.ubicacion_id}")
            print(f"   Creado: {usuario.created_at if hasattr(usuario, 'created_at') else 'N/A'}")
            
            # Verificar configuración
            issues = []
            if not usuario.activo:
                issues.append("❌ Usuario inactivo")
            if usuario.ubicacion_id is not None:
                issues.append("⚠️  Usuario tiene ubicacion_id (debería ser null)")
            
            if issues:
                print("\n🔧 PROBLEMAS ENCONTRADOS:")
                for issue in issues:
                    print(f"   {issue}")
            else:
                print("\n✅ CONFIGURACIÓN CORRECTA")
            
            # Verificar que puede hacer login
            print("\n📋 CREDENCIALES PARA LOGIN:")
            print(f"   Usuario: {usuario.nombre}")
            print("   Contraseña: [Ver en seed_data.py o usar 'Monitoreo2025!']")
            
        else:
            print("❌ USUARIO DE MONITOREO NO ENCONTRADO")
            print("\n💡 Para crearlo, ejecutar:")
            print("   python verificar_monitoreo.py")
            
        # Verificar otros usuarios para contexto
        total_users = User.query.count()
        print(f"\n📊 TOTAL DE USUARIOS EN EL SISTEMA: {total_users}")
        
        # Mostrar todos los roles disponibles
        roles = db.session.query(User.rol).distinct().all()
        print(f"\n👥 ROLES EXISTENTES:")
        for rol in roles:
            count = User.query.filter_by(rol=rol[0]).count()
            print(f"   - {rol[0]}: {count} usuario(s)")
            
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    print("\n💡 Asegúrate de que:")
    print("   1. El servidor de base de datos esté corriendo")
    print("   2. Las variables de entorno estén configuradas")
    print("   3. Estés ejecutando desde la raíz del proyecto")
