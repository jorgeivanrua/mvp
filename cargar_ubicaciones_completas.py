#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cargar ubicaciones completas: puestos y mesas"""
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.app import create_app

app = create_app()
app.app_context().push()

print("\n=== CARGANDO UBICACIONES COMPLETAS ===\n")

# Obtener municipio de Florencia
florencia = Location.query.filter_by(
    tipo='municipio',
    departamento_codigo='44',
    municipio_codigo='01'
).first()

if not florencia:
    print("✗ No se encontró el municipio de Florencia")
    exit(1)

print(f"✓ Municipio encontrado: {florencia.nombre_completo}")

# Crear puestos de votación
puestos_data = [
    {
        "codigo": "001",
        "nombre": "Colegio Nacional",
        "direccion": "Calle 10 # 15-20",
        "votantes": 1500
    },
    {
        "codigo": "002",
        "nombre": "Escuela La Esperanza",
        "direccion": "Carrera 8 # 12-45",
        "votantes": 1200
    },
    {
        "codigo": "003",
        "nombre": "Instituto Técnico",
        "direccion": "Avenida Circunvalar # 5-30",
        "votantes": 1800
    }
]

print("\n--- Creando Puestos de Votación ---")
puestos_creados = []

for puesto_data in puestos_data:
    # Verificar si ya existe
    puesto_existente = Location.query.filter_by(
        tipo='puesto_votacion',
        departamento_codigo='44',
        municipio_codigo='01',
        puesto_codigo=puesto_data['codigo']
    ).first()
    
    if puesto_existente:
        print(f"  - {puesto_data['nombre']}: Ya existe")
        puestos_creados.append(puesto_existente)
        continue
    
    # Crear puesto
    puesto = Location(
        tipo='puesto_votacion',
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
    puestos_creados.append(puesto)
    print(f"✓ {puesto_data['nombre']}: Creado")

db.session.commit()
print(f"\n✓ Total puestos: {len(puestos_creados)}")
