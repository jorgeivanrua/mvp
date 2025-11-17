"""
Revisar y corregir ubicaciones de todos los usuarios
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def revisar_y_corregir():
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*70)
        print("REVISIÓN Y CORRECCIÓN DE USUARIOS")
        print("="*70)
        
        # Obtener todos los usuarios
        usuarios = User.query.all()
        print(f"\n📊 Total usuarios: {len(usuarios)}")
        
        # Obtener ubicaciones disponibles del Caquetá
        departamento = Location.query.filter_by(tipo='departamento', departamento_codigo='18').first()
        municipio_florencia = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo='18',
            municipio_codigo='01'
        ).first()
        
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='18',
            municipio_codigo='01'
        ).all()
        
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo='18',
            municipio_codigo='01'
        ).all()
        
        print(f"\n📍 Ubicaciones disponibles en Caquetá:")
        print(f"  Departamento: {departamento.nombre_completo if departamento else 'No encontrado'}")
        print(f"  Municipio Florencia: {municipio_florencia.nombre_completo if municipio_florencia else 'No encontrado'}")
        print(f"  Puestos: {len(puestos)}")
        print(f"  Mesas: {len(mesas)}")
        
        # Revisar y corregir usuarios por rol
        usuarios_corregidos = 0
        usuarios_sin_cambios = 0
        
        print("\n" + "="*70)
        print("CORRECCIÓN DE USUARIOS")
        print("="*70)
        
        for usuario in usuarios:
            ubicacion_actual = None
            if usuario.ubicacion_id:
                ubicacion_actual = Location.query.get(usuario.ubicacion_id)
            
            # Determinar si necesita corrección
            necesita_correccion = False
            nueva_ubicacion_id = None
            
            if usuario.rol == 'super_admin':
                # Super admin no necesita ubicación
                if usuario.ubicacion_id:
                    print(f"\n⚠️  {usuario.nombre} (Super Admin)")
                    print(f"    Tiene ubicación pero no la necesita")
                    usuario.ubicacion_id = None
                    necesita_correccion = True
                    
            elif usuario.rol == 'coordinador_departamental':
                # Debe tener ubicación de departamento
                if not ubicacion_actual or ubicacion_actual.tipo != 'departamento':
                    print(f"\n⚠️  {usuario.nombre} (Coordinador Departamental)")
                    if departamento:
                        print(f"    Asignando: {departamento.nombre_completo}")
                        usuario.ubicacion_id = departamento.id
                        necesita_correccion = True
                    else:
                        print(f"    ❌ No hay departamento disponible")
                        
            elif usuario.rol == 'coordinador_municipal':
                # Debe tener ubicación de municipio
                if not ubicacion_actual or ubicacion_actual.tipo != 'municipio':
                    print(f"\n⚠️  {usuario.nombre} (Coordinador Municipal)")
                    if municipio_florencia:
                        print(f"    Asignando: {municipio_florencia.nombre_completo}")
                        usuario.ubicacion_id = municipio_florencia.id
                        necesita_correccion = True
                    else:
                        print(f"    ❌ No hay municipio disponible")
                        
            elif usuario.rol == 'coordinador_puesto':
                # Debe tener ubicación de puesto
                if not ubicacion_actual or ubicacion_actual.tipo != 'puesto':
                    print(f"\n⚠️  {usuario.nombre} (Coordinador Puesto)")
                    if puestos:
                        # Asignar al primer puesto disponible sin coordinador
                        puesto_asignado = None
                        for puesto in puestos:
                            coord_existente = User.query.filter_by(
                                rol='coordinador_puesto',
                                ubicacion_id=puesto.id
                            ).filter(User.id != usuario.id).first()
                            
                            if not coord_existente:
                                puesto_asignado = puesto
                                break
                        
                        if puesto_asignado:
                            print(f"    Asignando: {puesto_asignado.nombre_completo}")
                            usuario.ubicacion_id = puesto_asignado.id
                            necesita_correccion = True
                        else:
                            print(f"    ⚠️  Todos los puestos tienen coordinador")
                    else:
                        print(f"    ❌ No hay puestos disponibles")
                        
            elif usuario.rol == 'testigo_electoral':
                # Debe tener ubicación de mesa
                if not ubicacion_actual or ubicacion_actual.tipo != 'mesa':
                    print(f"\n⚠️  {usuario.nombre} (Testigo)")
                    if mesas:
                        # Asignar a la primera mesa disponible sin testigo
                        mesa_asignada = None
                        for mesa in mesas:
                            testigo_existente = User.query.filter_by(
                                rol='testigo_electoral',
                                ubicacion_id=mesa.id
                            ).filter(User.id != usuario.id).first()
                            
                            if not testigo_existente:
                                mesa_asignada = mesa
                                break
                        
                        if mesa_asignada:
                            print(f"    Asignando: {mesa_asignada.nombre_completo}")
                            usuario.ubicacion_id = mesa_asignada.id
                            necesita_correccion = True
                        else:
                            print(f"    ⚠️  Todas las mesas tienen testigo")
                    else:
                        print(f"    ❌ No hay mesas disponibles")
                        
            elif usuario.rol == 'auditor_electoral':
                # Puede tener ubicación de departamento o ninguna
                if usuario.ubicacion_id and not ubicacion_actual:
                    print(f"\n⚠️  {usuario.nombre} (Auditor)")
                    if departamento:
                        print(f"    Asignando: {departamento.nombre_completo}")
                        usuario.ubicacion_id = departamento.id
                        necesita_correccion = True
            
            if necesita_correccion:
                usuarios_corregidos += 1
            else:
                usuarios_sin_cambios += 1
        
        # Guardar cambios
        db.session.commit()
        
        print("\n" + "="*70)
        print("RESUMEN")
        print("="*70)
        print(f"  Usuarios corregidos: {usuarios_corregidos}")
        print(f"  Usuarios sin cambios: {usuarios_sin_cambios}")
        print(f"  Total: {len(usuarios)}")
        
        # Verificar estado final
        print("\n" + "="*70)
        print("VERIFICACIÓN FINAL")
        print("="*70)
        
        for rol in ['super_admin', 'coordinador_departamental', 'coordinador_municipal', 
                    'coordinador_puesto', 'testigo_electoral', 'auditor_electoral']:
            usuarios_rol = User.query.filter_by(rol=rol).all()
            con_ubicacion_valida = 0
            sin_ubicacion = 0
            ubicacion_invalida = 0
            
            for u in usuarios_rol:
                if u.ubicacion_id:
                    ubicacion = Location.query.get(u.ubicacion_id)
                    if ubicacion:
                        con_ubicacion_valida += 1
                    else:
                        ubicacion_invalida += 1
                else:
                    sin_ubicacion += 1
            
            print(f"\n{rol.upper().replace('_', ' ')}:")
            print(f"  Total: {len(usuarios_rol)}")
            print(f"  Con ubicación válida: {con_ubicacion_valida}")
            print(f"  Sin ubicación: {sin_ubicacion}")
            if ubicacion_invalida > 0:
                print(f"  ⚠️  Con ubicación inválida: {ubicacion_invalida}")
        
        print("\n" + "="*70)
        print("✅ CORRECCIÓN COMPLETADA")
        print("="*70)

if __name__ == '__main__':
    revisar_y_corregir()
