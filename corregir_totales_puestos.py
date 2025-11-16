#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corregir totales de votantes en puestos basándose en la suma de sus mesas"""
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from backend.database import db
from backend.models.location import Location
from backend.app import create_app

app = create_app()
app.app_context().push()

print("\n=== CORRIGIENDO TOTALES DE VOTANTES EN PUESTOS ===\n")

# Obtener todos los puestos
puestos = Location.query.filter_by(tipo='puesto').all()
print(f"Total de puestos a revisar: {len(puestos)}\n")

puestos_corregidos = 0
errores = []

for puesto in puestos:
    # Obtener todas las mesas de este puesto
    mesas = Location.query.filter_by(
        tipo='mesa',
        departamento_codigo=puesto.departamento_codigo,
        municipio_codigo=puesto.municipio_codigo,
        zona_codigo=puesto.zona_codigo,
        puesto_codigo=puesto.puesto_codigo
    ).all()
    
    if not mesas:
        errores.append(f"Puesto sin mesas: {puesto.nombre_completo}")
        continue
    
    # Calcular totales sumando las mesas
    total_votantes = sum(mesa.total_votantes_registrados or 0 for mesa in mesas)
    total_mujeres = sum(mesa.mujeres or 0 for mesa in mesas)
    total_hombres = sum(mesa.hombres or 0 for mesa in mesas)
    
    # Verificar si necesita corrección
    necesita_correccion = (
        puesto.total_votantes_registrados != total_votantes or
        puesto.mujeres != total_mujeres or
        puesto.hombres != total_hombres
    )
    
    if necesita_correccion:
        print(f"Corrigiendo: {puesto.puesto_nombre}")
        print(f"  Ubicación: {puesto.nombre_completo}")
        print(f"  Mesas: {len(mesas)}")
        print(f"  Antes:")
        print(f"    Total: {puesto.total_votantes_registrados}, Mujeres: {puesto.mujeres}, Hombres: {puesto.hombres}")
        print(f"  Después:")
        print(f"    Total: {total_votantes}, Mujeres: {total_mujeres}, Hombres: {total_hombres}")
        print()
        
        # Actualizar el puesto
        puesto.total_votantes_registrados = total_votantes
        puesto.mujeres = total_mujeres
        puesto.hombres = total_hombres
        puestos_corregidos += 1

# Guardar cambios
if puestos_corregidos > 0:
    db.session.commit()
    print(f"\n✓ Se corrigieron {puestos_corregidos} puestos")
else:
    print("\n✓ Todos los puestos tienen los totales correctos")

if errores:
    print(f"\n⚠ Advertencias ({len(errores)}):")
    for error in errores[:5]:
        print(f"  - {error}")
    if len(errores) > 5:
        print(f"  ... y {len(errores) - 5} más")

print("\n=== VERIFICACIÓN FINAL ===\n")

# Verificar algunos puestos al azar
import random
puestos_muestra = random.sample(puestos, min(5, len(puestos)))

for puesto in puestos_muestra:
    mesas = Location.query.filter_by(
        tipo='mesa',
        departamento_codigo=puesto.departamento_codigo,
        municipio_codigo=puesto.municipio_codigo,
        zona_codigo=puesto.zona_codigo,
        puesto_codigo=puesto.puesto_codigo
    ).all()
    
    suma_votantes = sum(mesa.total_votantes_registrados or 0 for mesa in mesas)
    
    print(f"Puesto: {puesto.puesto_nombre}")
    print(f"  Total en puesto: {puesto.total_votantes_registrados}")
    print(f"  Suma de mesas: {suma_votantes}")
    print(f"  Mesas: {len(mesas)}")
    print(f"  ✓ {'Correcto' if puesto.total_votantes_registrados == suma_votantes else '✗ ERROR'}")
    print()

print("✓ CORRECCIÓN COMPLETADA\n")
