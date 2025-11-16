#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crear puestos y mesas usando datos de DIVIPOLA"""
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

print("\n=== CREANDO PUESTOS Y MESAS DE VOTACIÓN ===\n")

# Obtener municipio de Florencia
florencia = Location.query.filter_by(
    tipo='municipio',
    departamento_codigo='44',
    municipio_codigo='01'
).first()

if not florencia:
    print("✗ No se encontró el municipio de Florencia")
    exit(1)

print(f"✓ Municipio: {florencia.nombre_completo}")
print(f"  ID: {florencia.id}")

# Crear 3 puestos de votación en Florencia
puestos_data = [
    {
        "codigo": "001",
        "nombre": "Colegio Nacional",
        "direccion": "Calle 10 # 15-20",
        "votantes": 1500,
        "mesas": 5
    },
    {
        "codigo": "002",
        "nombre": "Escuela La Esperanza",
        "direccion": "Carrera 8 # 12-45",
        "votantes": 1200,
        "mesas": 4
    },
    {
        "codigo": "003",
        "nombre": "Instituto Técnico",
        "direccion": "Avenida Circunvalar # 5-30",
        "votantes": 1800,
        "mesas": 6
    }
]

print("\n--- Creando Puestos de Votación ---")
total_puestos = 0
total_mesas = 0

for puesto_data in puestos_data:
    # Verificar si ya existe
    puesto_existente = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='44',
        municipio_codigo='01',
        puesto_codigo=puesto_data['codigo']
    ).first()
    
    if puesto_existente:
        print(f"  {puesto_data['nombre']}: Ya existe (ID: {puesto_existente.id})")
        puesto = puesto_existente
    else:
        # Crear puesto
        puesto = Location(
            tipo='puesto',
            departamento_codigo='44',
            departamento_nombre='CAQUETA',
            municipio_codigo='01',
            municipio_nombre='FLORENCIA',
            puesto_codigo=puesto_data['codigo'],
            puesto_nombre=puesto_data['nombre'],
            nombre_completo=f"CAQUETA - FLORENCIA - {puesto_data['nombre']}",
            direccion=puesto_data['direccion'],
            total_votantes_registrados=puesto_data['votantes'],
            activo=True,
            parent_id=florencia.id
        )
        
        db.session.add(puesto)
        db.session.flush()  # Para obtener el ID
        print(f"✓ {puesto_data['nombre']}: Creado (ID: {puesto.id})")
        total_puestos += 1
    
    # Crear mesas para este puesto
    print(f"  Creando {puesto_data['mesas']} mesas...")
    for i in range(1, puesto_data['mesas'] + 1):
        mesa_codigo = f"{i:03d}"
        
        # Verificar si ya existe
        mesa_existente = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo='44',
            municipio_codigo='01',
            puesto_codigo=puesto_data['codigo'],
            mesa_codigo=mesa_codigo
        ).first()
        
        if mesa_existente:
            print(f"    Mesa {mesa_codigo}: Ya existe")
            continue
        
        # Crear mesa
        mesa = Location(
            tipo='mesa',
            departamento_codigo='44',
            departamento_nombre='CAQUETA',
            municipio_codigo='01',
            municipio_nombre='FLORENCIA',
            puesto_codigo=puesto_data['codigo'],
            puesto_nombre=puesto_data['nombre'],
            mesa_codigo=mesa_codigo,
            mesa_nombre=f"Mesa {i}",
            nombre_completo=f"CAQUETA - FLORENCIA - {puesto_data['nombre']} - Mesa {i}",
            total_votantes_registrados=300,  # ~300 votantes por mesa
            activo=True,
            parent_id=puesto.id
        )
        
        db.session.add(mesa)
        total_mesas += 1
    
    print(f"  ✓ {puesto_data['mesas']} mesas creadas")

db.session.commit()

print(f"\n=== RESUMEN ===")
print(f"✓ Puestos creados: {total_puestos}")
print(f"✓ Mesas creadas: {total_mesas}")

# Verificar
print(f"\n--- Verificación ---")
puestos = Location.query.filter_by(tipo='puesto').count()
mesas = Location.query.filter_by(tipo='mesa').count()
print(f"Total puestos en BD: {puestos}")
print(f"Total mesas en BD: {mesas}")

# Mostrar un puesto con sus mesas
puesto_ejemplo = Location.query.filter_by(
    tipo='puesto',
    puesto_codigo='001'
).first()

if puesto_ejemplo:
    print(f"\n--- Ejemplo: {puesto_ejemplo.puesto_nombre} ---")
    print(f"Códigos para login:")
    print(f"  departamento_codigo: {puesto_ejemplo.departamento_codigo}")
    print(f"  municipio_codigo: {puesto_ejemplo.municipio_codigo}")
    print(f"  puesto_codigo: {puesto_ejemplo.puesto_codigo}")
    
    mesas_ejemplo = Location.query.filter_by(
        tipo='mesa',
        puesto_codigo='001'
    ).all()
    print(f"\nMesas ({len(mesas_ejemplo)}):")
    for mesa in mesas_ejemplo:
        print(f"  - Mesa {mesa.mesa_codigo}")

print("\n✓ PROCESO COMPLETADO\n")
