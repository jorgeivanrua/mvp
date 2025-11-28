"""
Script para crear usuarios FIJOS del sistema (no de prueba)
Estos son los usuarios reales que se usarán en producción
"""
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location


def create_fixed_users():
    """Crear usuarios fijos del sistema"""
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("CREANDO USUARIOS FIJOS DEL SISTEMA")
        print("=" * 80)
        print()
        
        # Obtener ubicaciones necesarias
        caqueta = Location.query.filter_by(
            tipo='departamento',
            departamento_codigo='44'
        ).first()
        
        florencia = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo='44',
            municipio_codigo='4401'
        ).first()
        
        # Obtener todos los puestos de Florencia
        puestos_florencia = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='44',
            municipio_codigo='4401'
        ).order_by(Location.puesto_codigo).all()
        
        if not caqueta or not florencia:
            print("❌ Error: No se encontraron las ubicaciones necesarias")
            print("   Ejecuta primero: python scripts/load_divipola.py")
            return
        
        # Limpiar usuarios existentes
        print("1. LIMPIANDO USUARIOS EXISTENTES")
        print("-" * 80)
        usuarios_anteriores = User.query.count()
        User.query.delete()
        db.session.commit()
        print(f"✅ {usuarios_anteriores} usuarios eliminados")
        print()
        
        # Lista de usuarios FIJOS a crear
        print("2. CREANDO USUARIOS FIJOS")
        print("-" * 80)
        
        usuarios_fijos = [
            # Super Admin (sin ubicación) - Contraseña FIJA admin123
            {
                'nombre': 'admin',
                'nombre_completo': 'Super Administrador',
                'rol': 'super_admin',
                'ubicacion_id': None,
                'password': 'admin123'  # ⚠️ CONTRASEÑA FIJA - NO MODIFICABLE
            },
            
            # Administradores - Contraseña test123 (modificable)
            {
                'nombre': 'admin_caqueta',
                'nombre_completo': 'Admin Departamental Caquetá',
                'rol': 'admin_departamental',
                'ubicacion_id': caqueta.id,
                'password': 'test123'
            },
            {
                'nombre': 'admin_florencia',
                'nombre_completo': 'Admin Municipal Florencia',
                'rol': 'admin_municipal',
                'ubicacion_id': florencia.id,
                'password': 'test123'
            },
            
            # Coordinadores - Contraseña test123 (modificable)
            {
                'nombre': 'coord_dpto_caqueta',
                'nombre_completo': 'Coordinador Departamental Caquetá',
                'rol': 'coordinador_departamental',
                'ubicacion_id': caqueta.id,
                'password': 'test123'
            },
            {
                'nombre': 'coord_mun_florencia',
                'nombre_completo': 'Coordinador Municipal Florencia',
                'rol': 'coordinador_municipal',
                'ubicacion_id': florencia.id,
                'password': 'test123'
            },
            
            # Auditor - Contraseña test123 (modificable)
            {
                'nombre': 'auditor_caqueta',
                'nombre_completo': 'Auditor Electoral Caquetá',
                'rol': 'auditor_electoral',
                'ubicacion_id': caqueta.id,
                'password': 'test123'
            }
        ]
        
        # Agregar coordinadores de puesto (uno por cada puesto) - Contraseña test123
        for i, puesto in enumerate(puestos_florencia[:10], 1):  # Máximo 10 coordinadores
            usuarios_fijos.append({
                'nombre': f'coord_puesto_{puesto.puesto_codigo}',
                'nombre_completo': f'Coordinador {puesto.puesto_nombre}',
                'rol': 'coordinador_puesto',
                'ubicacion_id': puesto.id,
                'password': 'test123'
            })
        
        # Agregar testigos (2-3 por cada puesto) - Contraseña test123
        for i, puesto in enumerate(puestos_florencia[:5], 1):  # Máximo 5 puestos con testigos
            # Testigo 1
            usuarios_fijos.append({
                'nombre': f'testigo_{puesto.puesto_codigo}_1',
                'nombre_completo': f'Testigo 1 - {puesto.puesto_nombre}',
                'rol': 'testigo_electoral',
                'ubicacion_id': puesto.id,
                'password': 'test123'
            })
            # Testigo 2
            usuarios_fijos.append({
                'nombre': f'testigo_{puesto.puesto_codigo}_2',
                'nombre_completo': f'Testigo 2 - {puesto.puesto_nombre}',
                'rol': 'testigo_electoral',
                'ubicacion_id': puesto.id,
                'password': 'test123'
            })
        
        # Crear usuarios
        created_count = 0
        for user_data in usuarios_fijos:
            try:
                user = User(
                    nombre=user_data['nombre'],  # Usar 'nombre' para login, no 'nombre_completo'
                    rol=user_data['rol'],
                    ubicacion_id=user_data['ubicacion_id'],
                    activo=True
                )
                user.set_password(user_data['password'])
                
                db.session.add(user)
                db.session.commit()
                
                ubicacion_info = "Sin ubicación" if user_data['ubicacion_id'] is None else f"Ubicación ID: {user_data['ubicacion_id']}"
                print(f"✅ {user_data['nombre']} ({user_data['nombre_completo']})")
                print(f"   Rol: {user_data['rol']}")
                print(f"   Password: {user_data['password']}")
                print(f"   {ubicacion_info}")
                print()
                created_count += 1
                
            except Exception as e:
                print(f"❌ Error creando {user_data['nombre_completo']}: {e}")
                db.session.rollback()
        
        # Resumen
        print("=" * 80)
        print("RESUMEN")
        print("=" * 80)
        print(f"Total de usuarios creados: {created_count}")
        print()
        
        # Contar por rol
        from sqlalchemy import func
        roles_count = db.session.query(
            User.rol, 
            func.count(User.id)
        ).group_by(User.rol).all()
        
        print("Usuarios por rol:")
        for rol, count in roles_count:
            print(f"  - {rol}: {count}")
        print()
        
        print("=" * 80)
        print("CREDENCIALES DE ACCESO")
        print("=" * 80)
        print()
        print("⚠️  SUPER ADMIN (Contraseña FIJA - NO modificable):")
        print("  Usuario: admin")
        print("  Password: admin123")
        print()
        print("✅ TODOS LOS DEMÁS USUARIOS (Contraseña modificable):")
        print("  Password por defecto: test123")
        print()
        print("  - Administradores: admin_caqueta / admin_florencia")
        print("  - Coordinadores: coord_dpto_caqueta / coord_mun_florencia / coord_puesto_XX")
        print("  - Testigos: testigo_XX_1 / testigo_XX_2")
        print("  - Auditor: auditor_caqueta")
        print()
        print("=" * 80)
        print("NOTAS IMPORTANTES:")
        print("=" * 80)
        print("1. La contraseña del Super Admin (admin123) NO puede ser modificada desde el sistema")
        print("2. Todas las demás contraseñas (test123) pueden ser modificadas por los usuarios")
        print("3. Para cambiar contraseña: Ir a Perfil > Cambiar Contraseña")
        print()
        print("=" * 80)
        print("✅ USUARIOS FIJOS CREADOS EXITOSAMENTE")
        print("=" * 80)


if __name__ == '__main__':
    create_fixed_users()
