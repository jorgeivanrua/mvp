"""
Crear testigos para la primera mesa de cada puesto en Florencia
"""
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.app import create_app

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("CREAR TESTIGOS PARA FLORENCIA")
    print("="*70)
    
    # Buscar puestos en Florencia
    puestos = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='44',
        municipio_codigo='01'
    ).all()
    
    print(f"\n📍 Puestos encontrados: {len(puestos)}")
    
    testigos_creados = []
    testigos_existentes = []
    
    for puesto in puestos:
        # Buscar primera mesa del puesto
        primera_mesa = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo='44',
            municipio_codigo='01',
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo
        ).first()
        
        if not primera_mesa:
            print(f"\n⚠️  {puesto.puesto_nombre}: Sin mesas")
            continue
        
        # Verificar si ya tiene testigo
        testigo_existente = User.query.filter_by(
            rol='testigo_electoral',
            ubicacion_id=primera_mesa.id
        ).first()
        
        if testigo_existente:
            testigos_existentes.append(testigo_existente.nombre)
            print(f"\n✅ {puesto.puesto_nombre}: Ya tiene testigo ({testigo_existente.nombre})")
            continue
        
        # Crear testigo
        nombre_testigo = f"Testigo {puesto.puesto_nombre[:30]}"
        
        testigo = User(
            nombre=nombre_testigo,
            rol='testigo_electoral',
            ubicacion_id=primera_mesa.id,
            activo=True
        )
        testigo.set_password('test123')
        
        db.session.add(testigo)
        testigos_creados.append({
            'nombre': nombre_testigo,
            'puesto': puesto.puesto_nombre,
            'mesa': primera_mesa.mesa_nombre,
            'zona': puesto.zona_codigo
        })
        
        print(f"\n✅ Creado: {nombre_testigo}")
        print(f"   Puesto: {puesto.puesto_nombre}")
        print(f"   Mesa: {primera_mesa.mesa_nombre}")
        print(f"   Zona: {puesto.zona_codigo}")
    
    # Guardar cambios
    db.session.commit()
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    
    print(f"\n✅ Testigos creados: {len(testigos_creados)}")
    print(f"ℹ️  Testigos existentes: {len(testigos_existentes)}")
    print(f"📊 Total testigos en Florencia: {len(testigos_creados) + len(testigos_existentes)}")
    
    if testigos_creados:
        print("\n" + "-"*70)
        print("TESTIGOS CREADOS")
        print("-"*70)
        for testigo in testigos_creados[:10]:  # Mostrar primeros 10
            print(f"\n👤 {testigo['nombre']}")
            print(f"   Puesto: {testigo['puesto']}")
            print(f"   Mesa: {testigo['mesa']}")
            print(f"   Zona: {testigo['zona']}")
        
        if len(testigos_creados) > 10:
            print(f"\n... y {len(testigos_creados) - 10} testigos más")
    
    print("\n" + "="*70)
    print("CREDENCIALES")
    print("="*70)
    print("\nTodos los testigos usan:")
    print("  Password: test123")
    print("\nPara hacer login:")
    print("  1. Rol: testigo_electoral")
    print("  2. Departamento: 44 (CAQUETA)")
    print("  3. Municipio: 01 (FLORENCIA)")
    print("  4. Zona: Seleccionar según el puesto")
    print("  5. Puesto: Seleccionar el puesto correspondiente")
    print("  6. Password: test123")
    print("="*70)
