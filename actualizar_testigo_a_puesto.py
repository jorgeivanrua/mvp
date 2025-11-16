#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Actualizar testigo para que esté asignado al puesto en lugar de la mesa"""
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.app import create_app

app = create_app()
app.app_context().push()

print("\n=== ACTUALIZANDO TESTIGOS A NIVEL DE PUESTO ===\n")

# Obtener puesto 001
puesto = Location.query.filter_by(
    tipo='puesto',
    departamento_codigo='44',
    municipio_codigo='01',
    puesto_codigo='001'
).first()

if not puesto:
    print("✗ No se encontró el puesto 001")
    exit(1)

print(f"✓ Puesto encontrado: {puesto.nombre_completo}")
print(f"  ID: {puesto.id}")

# Buscar todos los testigos
testigos = User.query.filter_by(rol='testigo_electoral').all()

print(f"\n--- Testigos encontrados: {len(testigos)} ---")
testigos_actualizados = 0
for testigo in testigos:
    ubicacion = Location.query.get(testigo.ubicacion_id) if testigo.ubicacion_id else None
    print(f"  {testigo.nombre}")
    if ubicacion:
        print(f"    Ubicación actual: {ubicacion.nombre_completo} (tipo: {ubicacion.tipo})")
        # Si está en una mesa, moverlo al puesto
        if ubicacion.tipo == 'mesa' and ubicacion.puesto_codigo == '001':
            print(f"    Actualizando a puesto...")
            testigo.ubicacion_id = puesto.id
            testigos_actualizados += 1
            print(f"    ✓ Actualizado")
        elif ubicacion.tipo == 'puesto':
            print(f"    ✓ Ya está en el puesto")
    else:
        print(f"    Sin ubicación asignada")

# Verificar si ya existe un testigo en el puesto
testigo_puesto = User.query.filter_by(
    rol='testigo_electoral',
    ubicacion_id=puesto.id
).first()

if not testigo_puesto and testigos_actualizados == 0:
    print("\n--- Creando nuevo testigo en el puesto ---")
    testigo = User(
        nombre="Testigo Electoral Colegio Nacional",
        rol="testigo_electoral",
        ubicacion_id=puesto.id,
        activo=True
    )
    testigo.set_password("test123")
    db.session.add(testigo)
    print(f"✓ Creado: {testigo.nombre}")

db.session.commit()

print("\n=== VERIFICACIÓN ===")
testigos_puesto = User.query.filter_by(
    rol='testigo_electoral',
    ubicacion_id=puesto.id
).all()

print(f"✓ Testigos en el puesto: {len(testigos_puesto)}")
for testigo in testigos_puesto:
    print(f"  - {testigo.nombre}")

# Obtener mesas del puesto
mesas = Location.query.filter_by(
    tipo='mesa',
    departamento_codigo='44',
    municipio_codigo='01',
    puesto_codigo='001'
).all()

print(f"\n✓ Mesas disponibles en el puesto: {len(mesas)}")
for mesa in mesas:
    print(f"  - Mesa {mesa.mesa_codigo}")

print("\n--- Datos para Login ---")
print(f"Testigo Electoral:")
print(f"  rol: testigo_electoral")
print(f"  departamento_codigo: 44")
print(f"  municipio_codigo: 01")
print(f"  puesto_codigo: 001")
print(f"  password: test123")
print(f"\nNOTA: La mesa se selecciona en el dashboard después del login")

print("\n✓ PROCESO COMPLETADO\n")
