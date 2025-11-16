#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueba completa del sistema con datos de DIVIPOLA"""
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

print("\n" + "="*70)
print("PRUEBA COMPLETA DEL SISTEMA CON DATOS DE DIVIPOLA")
print("="*70 + "\n")

# 1. VERIFICAR ESTRUCTURA DE DATOS
print("1. VERIFICACIÓN DE ESTRUCTURA DE DATOS")
print("-" * 70)

total_puestos = Location.query.filter_by(tipo='puesto').count()
total_mesas = Location.query.filter_by(tipo='mesa').count()
total_usuarios = User.query.count()

print(f"✓ Puestos en sistema: {total_puestos}")
print(f"✓ Mesas en sistema: {total_mesas}")
print(f"✓ Usuarios en sistema: {total_usuarios}")
print()

# 2. VERIFICAR INTEGRIDAD DE TOTALES
print("2. VERIFICACIÓN DE INTEGRIDAD DE TOTALES")
print("-" * 70)

puestos_muestra = Location.query.filter_by(tipo='puesto').limit(10).all()
errores_totales = 0

for puesto in puestos_muestra:
    mesas = Location.query.filter_by(
        tipo='mesa',
        departamento_codigo=puesto.departamento_codigo,
        municipio_codigo=puesto.municipio_codigo,
        zona_codigo=puesto.zona_codigo,
        puesto_codigo=puesto.puesto_codigo
    ).all()
    
    suma_votantes = sum(mesa.total_votantes_registrados or 0 for mesa in mesas)
    
    if puesto.total_votantes_registrados != suma_votantes:
        print(f"✗ ERROR: {puesto.puesto_nombre}")
        print(f"  Puesto: {puesto.total_votantes_registrados}, Suma mesas: {suma_votantes}")
        errores_totales += 1

if errores_totales == 0:
    print("✓ Todos los totales de votantes son correctos")
else:
    print(f"✗ Se encontraron {errores_totales} errores en totales")
print()

# 3. SELECCIONAR PUESTO PARA PRUEBAS
print("3. SELECCIÓN DE PUESTO PARA PRUEBAS")
print("-" * 70)

# Buscar un puesto con múltiples mesas
puesto_prueba = Location.query.filter_by(
    tipo='puesto',
    departamento_codigo='44',
    municipio_codigo='01'
).first()

if puesto_prueba:
    mesas_prueba = Location.query.filter_by(
        tipo='mesa',
        departamento_codigo=puesto_prueba.departamento_codigo,
        municipio_codigo=puesto_prueba.municipio_codigo,
        zona_codigo=puesto_prueba.zona_codigo,
        puesto_codigo=puesto_prueba.puesto_codigo
    ).all()
    
    print(f"✓ Puesto seleccionado: {puesto_prueba.puesto_nombre}")
    print(f"  ID: {puesto_prueba.id}")
    print(f"  Ubicación: {puesto_prueba.nombre_completo}")
    print(f"  Códigos DIVIPOLA:")
    print(f"    - Departamento: {puesto_prueba.departamento_codigo}")
    print(f"    - Municipio: {puesto_prueba.municipio_codigo}")
    print(f"    - Zona: {puesto_prueba.zona_codigo}")
    print(f"    - Puesto: {puesto_prueba.puesto_codigo}")
    print(f"  Total votantes: {puesto_prueba.total_votantes_registrados}")
    print(f"    - Mujeres: {puesto_prueba.mujeres}")
    print(f"    - Hombres: {puesto_prueba.hombres}")
    print(f"  Mesas: {len(mesas_prueba)}")
    print()
    
    print("  Detalle de mesas:")
    for i, mesa in enumerate(mesas_prueba[:5], 1):
        print(f"    {i}. Mesa {mesa.mesa_codigo} (ID: {mesa.id})")
        print(f"       Votantes: {mesa.total_votantes_registrados} (M: {mesa.mujeres}, H: {mesa.hombres})")
    
    if len(mesas_prueba) > 5:
        print(f"    ... y {len(mesas_prueba) - 5} mesas más")
else:
    print("✗ No se encontró puesto para pruebas")
print()

# 4. VERIFICAR JERARQUÍA DE UBICACIONES
print("4. VERIFICACIÓN DE JERARQUÍA DE UBICACIONES")
print("-" * 70)

# Verificar que las mesas tienen parent_id correcto
if puesto_prueba and mesas_prueba:
    mesas_con_parent = [m for m in mesas_prueba if m.parent_id == puesto_prueba.id]
    print(f"✓ Mesas con parent_id correcto: {len(mesas_con_parent)}/{len(mesas_prueba)}")
    
    if len(mesas_con_parent) != len(mesas_prueba):
        print("⚠ Algunas mesas no tienen el parent_id correcto")
print()

# 5. VERIFICAR USUARIOS EXISTENTES
print("5. VERIFICACIÓN DE USUARIOS EXISTENTES")
print("-" * 70)

usuarios = User.query.all()
print(f"Total de usuarios: {len(usuarios)}\n")

roles_count = {}
for user in usuarios:
    roles_count[user.rol] = roles_count.get(user.rol, 0) + 1

for rol, count in sorted(roles_count.items()):
    print(f"  - {rol}: {count}")
print()

# 6. ESTADÍSTICAS GENERALES
print("6. ESTADÍSTICAS GENERALES")
print("-" * 70)

# Departamentos únicos
departamentos = db.session.query(Location.departamento_codigo, Location.departamento_nombre)\
    .filter(Location.tipo == 'puesto')\
    .distinct().all()

print(f"✓ Departamentos: {len(departamentos)}")
for dep_codigo, dep_nombre in departamentos:
    puestos_dep = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo=dep_codigo
    ).count()
    mesas_dep = Location.query.filter_by(
        tipo='mesa',
        departamento_codigo=dep_codigo
    ).count()
    print(f"  - {dep_nombre} ({dep_codigo}): {puestos_dep} puestos, {mesas_dep} mesas")
print()

# Municipios únicos
municipios = db.session.query(Location.municipio_codigo, Location.municipio_nombre)\
    .filter(Location.tipo == 'puesto')\
    .distinct().count()

print(f"✓ Municipios: {municipios}")
print()

# 7. RESUMEN FINAL
print("7. RESUMEN FINAL")
print("-" * 70)

print("Estado del sistema:")
print(f"  ✓ {total_puestos} puestos de votación")
print(f"  ✓ {total_mesas} mesas de votación")
print(f"  ✓ {total_usuarios} usuarios registrados")
print(f"  ✓ {len(departamentos)} departamentos")
print(f"  ✓ {municipios} municipios")
print()

if puesto_prueba:
    print("Datos para crear usuarios de prueba:")
    print(f"  Puesto ID: {puesto_prueba.id}")
    print(f"  Puesto: {puesto_prueba.puesto_nombre}")
    if mesas_prueba:
        print(f"  Mesa ID (primera): {mesas_prueba[0].id}")
        print(f"  Mesa: {mesas_prueba[0].mesa_nombre}")
print()

print("="*70)
print("✓ PRUEBA COMPLETADA EXITOSAMENTE")
print("="*70 + "\n")
