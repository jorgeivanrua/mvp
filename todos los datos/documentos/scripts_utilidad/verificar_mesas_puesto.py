"""
Script para verificar qué mesas existen para el puesto del testigo
"""
from backend.app import create_app
from backend.models.location import Location

app = create_app()

with app.app_context():
    print("\n" + "="*60)
    print("MESAS DEL PUESTO I.E. JUAN BAUTISTA LA SALLE")
    print("="*60)
    
    # Buscar el puesto
    puesto = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='44',
        municipio_codigo='01',
        zona_codigo='01',
        puesto_codigo='01'
    ).first()
    
    if puesto:
        print(f"\n✅ Puesto encontrado:")
        print(f"   ID: {puesto.id}")
        print(f"   Nombre: {puesto.puesto_nombre}")
        print(f"   Nombre completo: {puesto.nombre_completo}")
        
        # Buscar mesas de este puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo='44',
            municipio_codigo='01',
            zona_codigo='01',
            puesto_codigo='01'
        ).all()
        
        print(f"\n📊 Mesas encontradas: {len(mesas)}")
        
        if mesas:
            for mesa in mesas:
                print(f"\n  Mesa {mesa.mesa_codigo}:")
                print(f"    ID: {mesa.id}")
                print(f"    Nombre: {mesa.mesa_nombre}")
                print(f"    Votantes: {mesa.total_votantes_registrados}")
        else:
            print("\n❌ No hay mesas para este puesto")
            print("\nℹ️  El testigo está asignado al puesto, pero no hay mesas registradas.")
            print("   Esto puede causar que el dashboard no funcione correctamente.")
    else:
        print("\n❌ Puesto no encontrado")
    
    print("\n" + "="*60)
