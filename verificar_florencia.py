from backend.app import create_app
from backend.models.location import Location

app = create_app()

with app.app_context():
    florencia = Location.query.filter_by(
        tipo='municipio',
        municipio_nombre='FLORENCIA'
    ).first()
    
    if florencia:
        print(f"✅ Florencia encontrada:")
        print(f"   Código: {florencia.municipio_codigo}")
        print(f"   Nombre completo: {florencia.nombre_completo}")
    else:
        print("❌ Florencia NO encontrada")
        
        # Listar todos los municipios
        municipios = Location.query.filter_by(tipo='municipio').all()
        print(f"\nMunicipios disponibles ({len(municipios)}):")
        for m in municipios[:5]:
            print(f"  - {m.municipio_codigo}: {m.municipio_nombre}")
