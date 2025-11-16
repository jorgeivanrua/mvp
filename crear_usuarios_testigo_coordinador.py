#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crear usuarios testigo y coordinador de puesto"""
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

print("\n=== CREANDO USUARIOS TESTIGO Y COORDINADOR ===\n")

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

# Obtener mesa 001 del puesto 001
mesa = Location.query.filter_by(
    tipo='mesa',
    departamento_codigo='44',
    municipio_codigo='01',
    puesto_codigo='001',
    mesa_codigo='001'
).first()

if not mesa:
    print("✗ No se encontró la mesa 001")
    exit(1)

print(f"✓ Mesa encontrada: {mesa.nombre_completo}")
print(f"  ID: {mesa.id}")

# Crear coordinador de puesto
print("\n--- Creando Coordinador de Puesto ---")
coord_existente = User.query.filter_by(
    rol='coordinador_puesto',
    ubicacion_id=puesto.id
).first()

if coord_existente:
    print(f"  Ya existe: {coord_existente.nombre}")
else:
    coordinador = User(
        nombre="Coordinador Puesto Colegio Nacional",
        rol="coordinador_puesto",
        ubicacion_id=puesto.id,
        activo=True
    )
    coordinador.set_password("test123")
    db.session.add(coordinador)
    print(f"✓ Creado: {coordinador.nombre}")

# Crear testigo electoral
print("\n--- Creando Testigo Electoral ---")
testigo_existente = User.query.filter_by(
    rol='testigo_electoral',
    ubicacion_id=mesa.id
).first()

if testigo_existente:
    print(f"  Ya existe: {testigo_existente.nombre}")
else:
    testigo = User(
        nombre="Testigo Electoral Mesa 001",
        rol="testigo_electoral",
        ubicacion_id=mesa.id,
        activo=True
    )
    testigo.set_password("test123")
    db.session.add(testigo)
    print(f"✓ Creado: {testigo.nombre}")

db.session.commit()

print("\n=== RESUMEN ===")
testigos = User.query.filter_by(rol='testigo_electoral').count()
coordinadores = User.query.filter_by(rol='coordinador_puesto').count()
print(f"✓ Total testigos: {testigos}")
print(f"✓ Total coordinadores de puesto: {coordinadores}")

print("\n--- Datos para Login ---")
print(f"Coordinador Puesto:")
print(f"  rol: coordinador_puesto")
print(f"  departamento_codigo: 44")
print(f"  municipio_codigo: 01")
print(f"  puesto_codigo: 001")
print(f"  password: test123")

print(f"\nTestigo Electoral:")
print(f"  rol: testigo_electoral")
print(f"  departamento_codigo: 44")
print(f"  municipio_codigo: 01")
print(f"  puesto_codigo: 001")
print(f"  mesa_codigo: 001")
print(f"  password: test123")

print("\n✓ PROCESO COMPLETADO\n")
