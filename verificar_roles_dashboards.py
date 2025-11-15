"""
Script para verificar que todos los roles tengan usuarios y dashboards configurados
"""
from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

def verificar_roles_dashboards():
    """Verificar roles y dashboards"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*80)
        print("VERIFICACIÓN DE ROLES Y DASHBOARDS")
        print("="*80)
        
        # Roles esperados
        roles_esperados = [
            'super_admin',
            'admin_departamental',
            'admin_municipal',
            'coordinador_departamental',
            'coordinador_municipal',
            'coordinador_puesto',
            'testigo_electoral',
            'auditor_electoral'
        ]
        
        # Dashboards configurados
        dashboards = {
            'super_admin': '/admin/dashboard',
            'admin_departamental': '/admin/dashboard',
            'admin_municipal': '/admin/dashboard',
            'coordinador_departamental': '/coordinador/departamental',
            'coordinador_municipal': '/coordinador/municipal',
            'coordinador_puesto': '/coordinador/puesto',
            'testigo_electoral': '/testigo/dashboard',
            'auditor_electoral': '/auditor/dashboard'
        }
        
        print("\n📊 VERIFICACIÓN POR ROL:\n")
        print(f"{'ROL':<35} {'USUARIOS':<10} {'DASHBOARD':<30} {'ESTADO'}")
        print("-" * 80)
        
        for rol in roles_esperados:
            # Contar usuarios con este rol
            usuarios = User.query.filter_by(rol=rol, activo=True).all()
            count = len(usuarios)
            dashboard = dashboards.get(rol, 'No configurado')
            
            # Estado
            if count > 0:
                estado = "✅"
                # Mostrar ubicaciones
                ubicaciones = []
                for user in usuarios:
                    if user.ubicacion_id:
                        loc = Location.query.get(user.ubicacion_id)
                        if loc:
                            ubicaciones.append(f"{user.nombre} ({loc.nombre_completo})")
                    else:
                        ubicaciones.append(f"{user.nombre} (Sin ubicación)")
            else:
                estado = "❌ Sin usuarios"
                ubicaciones = []
            
            print(f"{rol:<35} {count:<10} {dashboard:<30} {estado}")
            
            # Mostrar detalles de usuarios
            if ubicaciones:
                for ub in ubicaciones:
                    print(f"  └─ {ub}")
        
        print("\n" + "="*80)
        print("RESUMEN")
        print("="*80)
        
        total_usuarios = User.query.filter_by(activo=True).count()
        roles_con_usuarios = len([r for r in roles_esperados if User.query.filter_by(rol=r, activo=True).count() > 0])
        
        print(f"\n✅ Total de usuarios activos: {total_usuarios}")
        print(f"✅ Roles con usuarios: {roles_con_usuarios}/{len(roles_esperados)}")
        
        # Verificar roles sin usuarios
        roles_sin_usuarios = [r for r in roles_esperados if User.query.filter_by(rol=r, activo=True).count() == 0]
        if roles_sin_usuarios:
            print(f"\n⚠️  Roles sin usuarios:")
            for rol in roles_sin_usuarios:
                print(f"   • {rol}")
        
        print("\n" + "="*80)
        print("RUTAS DE DASHBOARD CONFIGURADAS")
        print("="*80)
        print("\nRutas en login.js:")
        for rol, url in dashboards.items():
            print(f"  • {rol:<35} → {url}")
        
        print("\n" + "="*80)
        print("RECOMENDACIONES")
        print("="*80)
        
        if roles_sin_usuarios:
            print("\n⚠️  Para crear usuarios faltantes:")
            print("   1. Ejecutar: python load_basic_data.py (usuarios de testing)")
            print("   2. Ejecutar: python backend/scripts/crear_usuarios_florencia.py (usuarios de producción)")
        else:
            print("\n✅ Todos los roles tienen usuarios configurados")
        
        print("\n💡 Para probar el login:")
        print("   1. Ir a: http://localhost:5000/auth/login")
        print("   2. Seleccionar rol")
        print("   3. Seleccionar ubicación (según rol)")
        print("   4. Contraseña: test123")
        print()

if __name__ == '__main__':
    verificar_roles_dashboards()
