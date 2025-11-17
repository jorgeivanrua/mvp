"""
Eliminar departamento duplicado con código incorrecto
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.database import db
from backend.models.location import Location

def eliminar_duplicado():
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*70)
        print("ELIMINAR DEPARTAMENTO DUPLICADO")
        print("="*70)
        
        # Buscar el departamento con código 44 (incorrecto)
        dept_incorrecto = Location.query.filter_by(
            tipo='departamento',
            departamento_codigo='44'
        ).first()
        
        if not dept_incorrecto:
            print("\n✅ No hay departamento con código 44")
            return
        
        print(f"\n⚠️  Departamento a eliminar:")
        print(f"  ID: {dept_incorrecto.id}")
        print(f"  Código: {dept_incorrecto.departamento_codigo}")
        print(f"  Nombre: {dept_incorrecto.nombre_completo}")
        
        # Buscar datos relacionados
        municipios = Location.query.filter_by(
            tipo='municipio',
            departamento_codigo='44'
        ).count()
        
        zonas = Location.query.filter_by(
            tipo='zona',
            departamento_codigo='44'
        ).count()
        
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='44'
        ).count()
        
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo='44'
        ).count()
        
        print(f"\n📊 Datos relacionados:")
        print(f"  Municipios: {municipios}")
        print(f"  Zonas: {zonas}")
        print(f"  Puestos: {puestos}")
        print(f"  Mesas: {mesas}")
        
        if municipios > 0 or zonas > 0 or puestos > 0 or mesas > 0:
            print("\n⚠️  Eliminando todos los datos relacionados...")
            
            # Eliminar en orden inverso (de hijos a padres)
            Location.query.filter_by(tipo='mesa', departamento_codigo='44').delete()
            Location.query.filter_by(tipo='puesto', departamento_codigo='44').delete()
            Location.query.filter_by(tipo='zona', departamento_codigo='44').delete()
            Location.query.filter_by(tipo='municipio', departamento_codigo='44').delete()
        
        # Eliminar el departamento
        db.session.delete(dept_incorrecto)
        db.session.commit()
        
        print("\n✅ Departamento duplicado eliminado")
        
        # Verificar que solo quede el correcto
        print("\n📍 Departamentos restantes:")
        departamentos = Location.query.filter_by(tipo='departamento').all()
        for dept in departamentos:
            print(f"  - ID: {dept.id} | Código: {dept.departamento_codigo} | {dept.nombre_completo}")
        
        print("\n" + "="*70)

if __name__ == '__main__':
    eliminar_duplicado()
