"""
Verificar estructura DIVIPOLA de Florencia y detectar inconsistencias
"""
from backend.database import db
from backend.models.location import Location
from backend.app import create_app

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("VERIFICACIÓN DIVIPOLA - FLORENCIA (44-01)")
    print("="*70)
    
    # Verificar zonas en Florencia
    zonas = Location.query.filter_by(
        tipo='zona',
        departamento_codigo='44',
        municipio_codigo='01'
    ).order_by(Location.zona_codigo).all()
    
    print(f"\n📍 ZONAS EN FLORENCIA: {len(zonas)}")
    for zona in zonas:
        print(f"  - Zona {zona.zona_codigo}: {zona.nombre_completo}")
    
    # Verificar puestos por zona
    print("\n" + "="*70)
    print("PUESTOS POR ZONA")
    print("="*70)
    
    for zona in zonas:
        puestos = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='44',
            municipio_codigo='01',
            zona_codigo=zona.zona_codigo
        ).order_by(Location.puesto_codigo).all()
        
        print(f"\n📌 ZONA {zona.zona_codigo} - {len(puestos)} puestos:")
        for puesto in puestos:
            print(f"  {puesto.puesto_codigo}: {puesto.puesto_nombre}")
    
    # Buscar puestos que podrían ser de otros municipios
    print("\n" + "="*70)
    print("ANÁLISIS DE NOMBRES SOSPECHOSOS")
    print("="*70)
    
    # Nombres que sugieren otros municipios
    municipios_caqueta = [
        'ALBANIA', 'BELEN', 'CARTAGENA', 'CURILLO', 'DONCELLO', 
        'PAUJIL', 'MONTAÑITA', 'MILAN', 'MORELIA', 'PUERTO RICO',
        'SAN JOSE', 'SAN VICENTE', 'SOLANO', 'SOLITA', 'VALPARAISO'
    ]
    
    todos_puestos = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='44',
        municipio_codigo='01'
    ).all()
    
    sospechosos = []
    for puesto in todos_puestos:
        nombre_upper = puesto.puesto_nombre.upper()
        for municipio in municipios_caqueta:
            if municipio in nombre_upper and municipio != 'FLORENCIA':
                sospechosos.append({
                    'puesto': puesto,
                    'municipio_sospechoso': municipio
                })
                break
    
    if sospechosos:
        print(f"\n⚠️  PUESTOS SOSPECHOSOS: {len(sospechosos)}")
        for item in sospechosos:
            puesto = item['puesto']
            print(f"\n  ❌ {puesto.puesto_nombre}")
            print(f"     Código: {puesto.puesto_codigo}")
            print(f"     Zona: {puesto.zona_codigo}")
            print(f"     Posible municipio: {item['municipio_sospechoso']}")
    else:
        print("\n✅ No se encontraron nombres sospechosos")
    
    # Verificar corregimientos de Florencia
    print("\n" + "="*70)
    print("CORREGIMIENTOS RURALES DE FLORENCIA")
    print("="*70)
    
    # Los corregimientos oficiales de Florencia según DIVIPOLA
    corregimientos_florencia = [
        'ORTEGUAZA', 'EL DANUBIO', 'EL CARAÑO', 'SANTO DOMINGO',
        'SAN MARTIN', 'VENECIA', 'SAN PEDRO'
    ]
    
    print("\nCorregimientos oficiales de Florencia:")
    for corr in corregimientos_florencia:
        print(f"  - {corr}")
    
    # Verificar puestos en zona rural (99)
    puestos_rurales = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='44',
        municipio_codigo='01',
        zona_codigo='99'
    ).all()
    
    print(f"\n📍 Puestos en Zona Rural (99): {len(puestos_rurales)}")
    
    validos = []
    invalidos = []
    
    for puesto in puestos_rurales:
        nombre_upper = puesto.puesto_nombre.upper()
        es_valido = False
        
        for corr in corregimientos_florencia:
            if corr in nombre_upper:
                es_valido = True
                validos.append(puesto)
                break
        
        if not es_valido:
            invalidos.append(puesto)
    
    print(f"\n✅ Puestos válidos (en corregimientos de Florencia): {len(validos)}")
    for puesto in validos[:10]:
        print(f"  - {puesto.puesto_nombre}")
    if len(validos) > 10:
        print(f"  ... y {len(validos) - 10} más")
    
    if invalidos:
        print(f"\n❌ Puestos inválidos (NO en corregimientos de Florencia): {len(invalidos)}")
        for puesto in invalidos:
            print(f"  - {puesto.puesto_nombre} (Código: {puesto.puesto_codigo})")
    
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print(f"\nTotal zonas: {len(zonas)}")
    print(f"Total puestos: {len(todos_puestos)}")
    print(f"Puestos válidos en zona rural: {len(validos)}")
    print(f"Puestos inválidos: {len(invalidos)}")
    print(f"Puestos sospechosos: {len(sospechosos)}")
    
    if invalidos or sospechosos:
        print(f"\n⚠️  SE DETECTARON {len(invalidos) + len(sospechosos)} UBICACIONES INCORRECTAS")
        print("Estos puestos deben ser eliminados o reasignados al municipio correcto")
    else:
        print("\n✅ Todas las ubicaciones son correctas")
    
    print("="*70)
