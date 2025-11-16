#!/usr/bin/env python3
"""Verificar tipos de ubicaciones en la BD"""
from backend.app import create_app
from backend.models.location import Location

app = create_app('development')

with app.app_context():
    print("\n" + "="*60)
    print("UBICACIONES POR TIPO")
    print("="*60)
    
    tipos = ['departamento', 'municipio', 'zona', 'puesto', 'mesa']
    
    for tipo in tipos:
        count = Location.query.filter_by(tipo=tipo).count()
        print(f"\n{tipo.upper()}: {count} ubicaciones")
        
        if count > 0 and count <= 5:
            ubicaciones = Location.query.filter_by(tipo=tipo).limit(5).all()
            for ub in ubicaciones:
                print(f"  - ID:{ub.id} | {ub.nombre_completo}")
        elif count > 5:
            ubicaciones = Location.query.filter_by(tipo=tipo).limit(3).all()
            for ub in ubicaciones:
                print(f"  - ID:{ub.id} | {ub.nombre_completo}")
            print(f"  ... y {count - 3} más")
    
    print("\n" + "="*60)
    print("VERIFICAR DEPARTAMENTO CAQUETA (44)")
    print("="*60)
    
    depto = Location.query.filter_by(
        tipo='departamento',
        departamento_codigo='44'
    ).first()
    
    if depto:
        print(f"\n✓ Encontrado:")
        print(f"  ID: {depto.id}")
        print(f"  Nombre: {depto.nombre_completo}")
        print(f"  Código: {depto.departamento_codigo}")
        print(f"  Tipo: {depto.tipo}")
    else:
        print("\n✗ NO encontrado")
