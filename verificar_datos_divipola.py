#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificar datos de DIVIPOLA cargados en la BD"""
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.app import create_app

app = create_app()
app.app_context().push()

print("\n=== DATOS DE DIVIPOLA EN LA BASE DE DATOS ===\n")

# Departamentos
print("--- DEPARTAMENTOS ---")
departamentos = Location.query.filter_by(tipo='departamento').all()
print(f"Total: {len(departamentos)}")
for dept in departamentos[:5]:
    print(f"  {dept.departamento_codigo} - {dept.departamento_nombre}")

# Municipios
print("\n--- MUNICIPIOS ---")
municipios = Location.query.filter_by(tipo='municipio').all()
print(f"Total: {len(municipios)}")
for mun in municipios[:10]:
    print(f"  {mun.departamento_codigo}-{mun.municipio_codigo} - {mun.municipio_nombre} ({mun.departamento_nombre})")

# Puestos de votación
print("\n--- PUESTOS DE VOTACIÓN ---")
puestos = Location.query.filter_by(tipo='puesto_votacion').all()
print(f"Total: {len(puestos)}")
if puestos:
    for puesto in puestos[:10]:
        print(f"  {puesto.departamento_codigo}-{puesto.municipio_codigo}-{puesto.puesto_codigo} - {puesto.puesto_nombre}")
else:
    print("  ⚠ No hay puestos de votación cargados")

# Mesas
print("\n--- MESAS ---")
mesas = Location.query.filter_by(tipo='mesa').all()
print(f"Total: {len(mesas)}")
if mesas:
    for mesa in mesas[:10]:
        print(f"  Mesa {mesa.mesa_codigo} - {mesa.nombre_completo}")
else:
    print("  ⚠ No hay mesas cargadas")

# Usuarios por ubicación
print("\n--- USUARIOS Y SUS UBICACIONES ---")
usuarios = User.query.all()
print(f"Total usuarios: {len(usuarios)}")

for user in usuarios:
    print(f"\n{user.nombre} ({user.rol})")
    if user.ubicacion_id:
        loc = Location.query.get(user.ubicacion_id)
        if loc:
            print(f"  Ubicación: {loc.nombre_completo}")
            print(f"  Tipo: {loc.tipo}")
            print(f"  Códigos: Dept={loc.departamento_codigo}, Mun={loc.municipio_codigo}, Puesto={loc.puesto_codigo}, Mesa={loc.mesa_codigo}")
    else:
        print(f"  Sin ubicación asignada")

# Buscar ubicaciones específicas para testing
print("\n--- UBICACIONES PARA TESTING ---")

# Buscar un puesto específico si existe
puesto_test = Location.query.filter_by(tipo='puesto_votacion').first()
if puesto_test:
    print(f"\n✓ Puesto de prueba encontrado:")
    print(f"  Nombre: {puesto_test.puesto_nombre}")
    print(f"  Códigos: Dept={puesto_test.departamento_codigo}, Mun={puesto_test.municipio_codigo}, Puesto={puesto_test.puesto_codigo}")
    
    # Buscar mesas de este puesto
    mesas_puesto = Location.query.filter_by(
        tipo='mesa',
        departamento_codigo=puesto_test.departamento_codigo,
        municipio_codigo=puesto_test.municipio_codigo,
        puesto_codigo=puesto_test.puesto_codigo
    ).all()
    print(f"  Mesas en este puesto: {len(mesas_puesto)}")
    for mesa in mesas_puesto[:3]:
        print(f"    - Mesa {mesa.mesa_codigo}")
else:
    print("\n⚠ No hay puestos de votación. Necesitamos crearlos.")
    
    # Sugerir municipio para crear puestos
    mun_test = Location.query.filter_by(tipo='municipio').first()
    if mun_test:
        print(f"\n  Sugerencia: Crear puestos en {mun_test.municipio_nombre}")
        print(f"  Códigos: Dept={mun_test.departamento_codigo}, Mun={mun_test.municipio_codigo}")
