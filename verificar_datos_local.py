"""
Script para verificar que los datos de CAQUETA estén en local
"""
from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app()

with app.app_context():
    print("\n" + "="*60)
    print("VERIFICACIÓN DE DATOS LOCALES")
    print("="*60)
    
    # Verificar departamento
    dept = Location.query.filter_by(
        tipo='departamento', 
        departamento_codigo='44'
    ).first()
    
    if dept:
        print(f"\n✅ Departamento: {dept.departamento_nombre}")
    else:
        print("\n❌ Departamento CAQUETA NO encontrado")
    
    # Verificar municipio
    muni = Location.query.filter_by(
        tipo='municipio',
        departamento_codigo='44',
        municipio_codigo='001'
    ).first()
    
    if muni:
        print(f"✅ Municipio: {muni.municipio_nombre}")
    else:
        print("❌ Municipio FLORENCIA NO encontrado")
    
    # Verificar usuarios
    total_users = User.query.count()
    testigos = User.query.filter_by(rol='testigo').count()
    coordinadores_puesto = User.query.filter_by(rol='coordinador_puesto').count()
    coordinadores_dept = User.query.filter_by(rol='coordinador_departamental').count()
    
    print(f"\n📊 Estadísticas de Usuarios:")
    print(f"  - Total: {total_users}")
    print(f"  - Testigos: {testigos}")
    print(f"  - Coordinadores Puesto: {coordinadores_puesto}")
    print(f"  - Coordinadores Departamentales: {coordinadores_dept}")
    
    # Verificar ubicaciones
    total_locs = Location.query.count()
    departamentos = Location.query.filter_by(tipo='departamento').count()
    municipios = Location.query.filter_by(tipo='municipio').count()
    zonas = Location.query.filter_by(tipo='zona').count()
    puestos = Location.query.filter_by(tipo='puesto').count()
    mesas = Location.query.filter_by(tipo='mesa').count()
    
    print(f"\n📍 Estadísticas de Ubicaciones:")
    print(f"  - Total: {total_locs}")
    print(f"  - Departamentos: {departamentos}")
    print(f"  - Municipios: {municipios}")
    print(f"  - Zonas: {zonas}")
    print(f"  - Puestos: {puestos}")
    print(f"  - Mesas: {mesas}")
    
    # Verificar un usuario testigo específico
    testigo = User.query.filter_by(rol='testigo').first()
    if testigo:
        print(f"\n👤 Usuario Testigo de Ejemplo:")
        print(f"  - Nombre: {testigo.nombre}")
        print(f"  - Rol: {testigo.rol}")
        if testigo.ubicacion:
            print(f"  - Ubicación: {testigo.ubicacion.nombre_completo}")
    
    print("\n" + "="*60)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("="*60)
