"""
Verificar mesas disponibles en Florencia para crear testigos
"""
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.app import create_app

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("MESAS DISPONIBLES EN FLORENCIA")
    print("="*70)
    
    # Buscar puestos en Florencia
    puestos = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='44',
        municipio_codigo='01'
    ).all()
    
    print(f"\n📍 Puestos encontrados en Florencia: {len(puestos)}")
    
    total_mesas = 0
    puestos_info = []
    
    for puesto in puestos:
        # Contar mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo='44',
            municipio_codigo='01',
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo
        ).all()
        
        # Buscar primera mesa
        primera_mesa = mesas[0] if mesas else None
        
        # Verificar si ya tiene testigo
        testigo_existente = None
        if primera_mesa:
            testigo_existente = User.query.filter_by(
                rol='testigo_electoral',
                ubicacion_id=primera_mesa.id
            ).first()
        
        puestos_info.append({
            'puesto': puesto,
            'total_mesas': len(mesas),
            'primera_mesa': primera_mesa,
            'tiene_testigo': testigo_existente is not None,
            'testigo': testigo_existente
        })
        
        total_mesas += len(mesas)
    
    print(f"📊 Total de mesas en Florencia: {total_mesas}")
    
    print("\n" + "-"*70)
    print("DETALLE POR PUESTO")
    print("-"*70)
    
    for info in puestos_info:
        puesto = info['puesto']
        print(f"\n🏢 {puesto.puesto_nombre}")
        print(f"   Código: {puesto.puesto_codigo}")
        print(f"   Zona: {puesto.zona_codigo}")
        print(f"   Total mesas: {info['total_mesas']}")
        
        if info['primera_mesa']:
            print(f"   Primera mesa: {info['primera_mesa'].mesa_nombre}")
            print(f"   Mesa ID: {info['primera_mesa'].id}")
            
            if info['tiene_testigo']:
                print(f"   ✅ Ya tiene testigo: {info['testigo'].nombre}")
            else:
                print(f"   ❌ Sin testigo asignado")
        else:
            print(f"   ⚠️  Sin mesas configuradas")
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    
    puestos_con_testigo = sum(1 for info in puestos_info if info['tiene_testigo'])
    puestos_sin_testigo = sum(1 for info in puestos_info if not info['tiene_testigo'] and info['primera_mesa'])
    puestos_sin_mesas = sum(1 for info in puestos_info if not info['primera_mesa'])
    
    print(f"\n✅ Puestos con testigo: {puestos_con_testigo}")
    print(f"❌ Puestos sin testigo: {puestos_sin_testigo}")
    print(f"⚠️  Puestos sin mesas: {puestos_sin_mesas}")
    print(f"\n📝 Testigos a crear: {puestos_sin_testigo}")
    
    print("\n" + "="*70)
