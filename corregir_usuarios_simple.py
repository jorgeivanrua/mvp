import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

app = create_app()

with app.app_context():
    print("Corrigiendo usuarios...")
    
    # Obtener ubicaciones
    dept = Location.query.filter_by(tipo='departamento', departamento_codigo='18').first()
    mun = Location.query.filter_by(tipo='municipio', departamento_codigo='18', municipio_codigo='01').first()
    puestos = Location.query.filter_by(tipo='puesto', departamento_codigo='18', municipio_codigo='01').all()
    mesas = Location.query.filter_by(tipo='mesa', departamento_codigo='18', municipio_codigo='01').all()
    
    print(f"Ubicaciones: Dept={dept.id if dept else None}, Mun={mun.id if mun else None}, Puestos={len(puestos)}, Mesas={len(mesas)}")
    
    corregidos = 0
    
    # Super admin - sin ubicación
    for u in User.query.filter_by(rol='super_admin').all():
        if u.ubicacion_id:
            u.ubicacion_id = None
            corregidos += 1
    
    # Coordinador departamental
    for u in User.query.filter_by(rol='coordinador_departamental').all():
        if dept and u.ubicacion_id != dept.id:
            u.ubicacion_id = dept.id
            corregidos += 1
            print(f"  Coord Dept: {u.nombre} -> {dept.nombre_completo}")
    
    # Coordinador municipal
    for u in User.query.filter_by(rol='coordinador_municipal').all():
        if mun and u.ubicacion_id != mun.id:
            u.ubicacion_id = mun.id
            corregidos += 1
            print(f"  Coord Mun: {u.nombre} -> {mun.nombre_completo}")
    
    # Coordinadores de puesto
    puesto_idx = 0
    for u in User.query.filter_by(rol='coordinador_puesto').all():
        if puesto_idx < len(puestos):
            if u.ubicacion_id != puestos[puesto_idx].id:
                u.ubicacion_id = puestos[puesto_idx].id
                corregidos += 1
                print(f"  Coord Puesto: {u.nombre} -> {puestos[puesto_idx].nombre_completo}")
            puesto_idx += 1
    
    # Testigos
    mesa_idx = 0
    for u in User.query.filter_by(rol='testigo_electoral').all():
        if mesa_idx < len(mesas):
            if u.ubicacion_id != mesas[mesa_idx].id:
                u.ubicacion_id = mesas[mesa_idx].id
                corregidos += 1
            mesa_idx += 1
    
    # Auditor
    for u in User.query.filter_by(rol='auditor_electoral').all():
        if dept and u.ubicacion_id != dept.id:
            u.ubicacion_id = dept.id
            corregidos += 1
            print(f"  Auditor: {u.nombre} -> {dept.nombre_completo}")
    
    db.session.commit()
    
    print(f"\n✅ Corregidos: {corregidos} usuarios")
    print("\nVerificación:")
    for rol in ['super_admin', 'coordinador_departamental', 'coordinador_municipal', 'coordinador_puesto', 'testigo_electoral', 'auditor_electoral']:
        count = User.query.filter_by(rol=rol).count()
        print(f"  {rol}: {count} usuarios")
