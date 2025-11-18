"""
Listar todos los usuarios del sistema con sus credenciales de acceso
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

app = create_app()

with app.app_context():
    print("\n" + "="*100)
    print("  LISTA COMPLETA DE USUARIOS Y CONTRASEÑAS DEL SISTEMA ELECTORAL")
    print("="*100)
    
    # Obtener todos los usuarios ordenados por rol
    usuarios = User.query.order_by(User.rol, User.nombre).all()
    
    print(f"\nTotal de usuarios: {len(usuarios)}")
    print(f"Contraseña universal: test123\n")
    
    # Agrupar por rol
    roles = {}
    for usuario in usuarios:
        if usuario.rol not in roles:
            roles[usuario.rol] = []
        roles[usuario.rol].append(usuario)
    
    # Mostrar por rol
    for rol, usuarios_rol in sorted(roles.items()):
        print("\n" + "-"*100)
        print(f"ROL: {rol.upper().replace('_', ' ')}")
        print("-"*100)
        print(f"Total: {len(usuarios_rol)} usuario(s)\n")
        
        for usuario in usuarios_rol:
            ubicacion = Location.query.get(usuario.ubicacion_id) if usuario.ubicacion_id else None
            
            print(f"Usuario: {usuario.nombre}")
            print(f"   ID: {usuario.id}")
            print(f"   Rol: {usuario.rol}")
            print(f"   Contraseña: test123")
            print(f"   Activo: {'Sí' if usuario.activo else 'No'}")
            
            if ubicacion:
                print(f"   Ubicación: {ubicacion.nombre_completo}")
                print(f"   Tipo ubicación: {ubicacion.tipo}")
                
                # Mostrar códigos para login
                if rol == 'super_admin':
                    print(f"   Login: {{'rol': '{rol}', 'password': 'test123'}}")
                elif rol in ['coordinador_departamental', 'auditor_electoral']:
                    print(f"   Login: {{'rol': '{rol}', 'departamento_codigo': '{ubicacion.departamento_codigo}', 'password': 'test123'}}")
                elif rol == 'coordinador_municipal':
                    print(f"   Login: {{'rol': '{rol}', 'departamento_codigo': '{ubicacion.departamento_codigo}', 'municipio_codigo': '{ubicacion.municipio_codigo}', 'password': 'test123'}}")
                elif rol == 'coordinador_puesto':
                    print(f"   Login: {{'rol': '{rol}', 'departamento_codigo': '{ubicacion.departamento_codigo}', 'municipio_codigo': '{ubicacion.municipio_codigo}', 'zona_codigo': '{ubicacion.zona_codigo}', 'puesto_codigo': '{ubicacion.puesto_codigo}', 'password': 'test123'}}")
                elif rol == 'testigo_electoral':
                    print(f"   Login: {{'rol': '{rol}', 'departamento_codigo': '{ubicacion.departamento_codigo}', 'municipio_codigo': '{ubicacion.municipio_codigo}', 'zona_codigo': '{ubicacion.zona_codigo}', 'puesto_codigo': '{ubicacion.puesto_codigo}', 'password': 'test123'}}")
            else:
                print(f"   Ubicación: Sin ubicación (acceso global)")
                print(f"   Login: {{'rol': '{rol}', 'password': 'test123'}}")
            
            print()
    
    print("\n" + "="*100)
    print("  RESUMEN POR ROL")
    print("="*100 + "\n")
    
    for rol, usuarios_rol in sorted(roles.items()):
        print(f"  {rol.replace('_', ' ').title():.<50} {len(usuarios_rol):>3} usuario(s)")
    
    print("\n" + "="*100)
    print(f"  TOTAL: {len(usuarios)} usuarios")
    print("="*100 + "\n")
