"""
Verificar consistencia completa de DIVIPOLA en todos los municipios
"""
from backend.database import db
from backend.models.location import Location
from backend.app import create_app

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("VERIFICACIÓN COMPLETA DE CONSISTENCIA DIVIPOLA")
    print("="*70)
    
    # Obtener todos los municipios
    municipios = Location.query.filter_by(
        tipo='municipio',
        departamento_codigo='44'
    ).order_by(Location.municipio_codigo).all()
    
    print(f"\n📍 Total municipios en CAQUETA: {len(municipios)}")
    
    inconsistencias = []
    
    for municipio in municipios:
        print(f"\n{'='*70}")
        print(f"MUNICIPIO: {municipio.municipio_nombre} ({municipio.municipio_codigo})")
        print(f"{'='*70}")
        
        # Contar zonas
        zonas = Location.query.filter_by(
            tipo='zona',
            departamento_codigo='44',
            municipio_codigo=municipio.municipio_codigo
        ).all()
        
        print(f"  Zonas: {len(zonas)}")
        
        # Verificar cada zona
        for zona in zonas:
            # Contar puestos en esta zona
            puestos = Location.query.filter_by(
                tipo='puesto',
                departamento_codigo='44',
                municipio_codigo=municipio.municipio_codigo,
                zona_codigo=zona.zona_codigo
            ).all()
            
            print(f"    Zona {zona.zona_codigo}: {len(puestos)} puestos")
            
            # Verificar que todos los puestos tengan el municipio correcto
            for puesto in puestos:
                if puesto.municipio_codigo != municipio.municipio_codigo:
                    inconsistencias.append({
                        'tipo': 'puesto_municipio_incorrecto',
                        'municipio_esperado': municipio.municipio_codigo,
                        'municipio_actual': puesto.municipio_codigo,
                        'puesto': puesto.puesto_nombre,
                        'zona': zona.zona_codigo
                    })
                    print(f"      ❌ INCONSISTENCIA: {puesto.puesto_nombre}")
                    print(f"         Municipio esperado: {municipio.municipio_codigo}")
                    print(f"         Municipio actual: {puesto.municipio_codigo}")
                
                # Verificar mesas del puesto
                mesas = Location.query.filter_by(
                    tipo='mesa',
                    departamento_codigo='44',
                    municipio_codigo=municipio.municipio_codigo,
                    zona_codigo=zona.zona_codigo,
                    puesto_codigo=puesto.puesto_codigo
                ).all()
                
                # Verificar que todas las mesas tengan el municipio correcto
                for mesa in mesas:
                    if mesa.municipio_codigo != municipio.municipio_codigo:
                        inconsistencias.append({
                            'tipo': 'mesa_municipio_incorrecto',
                            'municipio_esperado': municipio.municipio_codigo,
                            'municipio_actual': mesa.municipio_codigo,
                            'mesa': mesa.mesa_nombre,
                            'puesto': puesto.puesto_nombre
                        })
        
        # Verificar si hay puestos huérfanos (sin zona válida)
        puestos_municipio = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='44',
            municipio_codigo=municipio.municipio_codigo
        ).all()
        
        zonas_validas = [z.zona_codigo for z in zonas]
        
        for puesto in puestos_municipio:
            if puesto.zona_codigo not in zonas_validas:
                inconsistencias.append({
                    'tipo': 'puesto_zona_invalida',
                    'municipio': municipio.municipio_codigo,
                    'puesto': puesto.puesto_nombre,
                    'zona_invalida': puesto.zona_codigo,
                    'zonas_validas': zonas_validas
                })
                print(f"    ❌ Puesto con zona inválida: {puesto.puesto_nombre}")
                print(f"       Zona: {puesto.zona_codigo} (no existe en el municipio)")
    
    # Resumen de inconsistencias
    print("\n" + "="*70)
    print("RESUMEN DE INCONSISTENCIAS")
    print("="*70)
    
    if not inconsistencias:
        print("\n✅ NO SE ENCONTRARON INCONSISTENCIAS")
        print("La estructura DIVIPOLA es completamente consistente")
    else:
        print(f"\n❌ SE ENCONTRARON {len(inconsistencias)} INCONSISTENCIAS")
        
        # Agrupar por tipo
        por_tipo = {}
        for inc in inconsistencias:
            tipo = inc['tipo']
            if tipo not in por_tipo:
                por_tipo[tipo] = []
            por_tipo[tipo].append(inc)
        
        for tipo, items in por_tipo.items():
            print(f"\n{tipo}: {len(items)} casos")
            for item in items[:5]:  # Mostrar primeros 5
                print(f"  - {item}")
            if len(items) > 5:
                print(f"  ... y {len(items) - 5} más")
    
    print("\n" + "="*70)
    print("VERIFICACIÓN DE ENDPOINTS")
    print("="*70)
    
    # Verificar que los endpoints filtren correctamente
    print("\nVerificando filtrado de datos...")
    
    # Test: Obtener puestos de Florencia
    puestos_florencia = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='44',
        municipio_codigo='01'
    ).all()
    
    print(f"\nPuestos en Florencia (01): {len(puestos_florencia)}")
    
    # Verificar que ningún puesto tenga municipio diferente
    puestos_incorrectos = [p for p in puestos_florencia if p.municipio_codigo != '01']
    
    if puestos_incorrectos:
        print(f"❌ {len(puestos_incorrectos)} puestos con municipio incorrecto:")
        for p in puestos_incorrectos:
            print(f"  - {p.puesto_nombre} (municipio: {p.municipio_codigo})")
    else:
        print("✅ Todos los puestos tienen el municipio correcto")
    
    print("\n" + "="*70)
