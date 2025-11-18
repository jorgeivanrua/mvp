#!/usr/bin/env python3
"""Verificar ubicaciones en el sistema"""
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.app import create_app

app = create_app()
app.app_context().push()

print("\n=== DEPARTAMENTOS ===")
departamentos = Location.query.filter_by(tipo='departamento').all()
for dept in departamentos[:3]:
    print(f"- {dept.departamento_nombre} (código: {dept.departamento_codigo})")

print("\n=== MUNICIPIOS ===")
municipios = Location.query.filter_by(tipo='municipio').all()
for mun in municipios[:3]:
    print(f"- {mun.municipio_nombre} (código: {mun.municipio_codigo}, dept: {mun.departamento_codigo})")

print("\n=== PUESTOS ===")
puestos = Location.query.filter_by(tipo='puesto_votacion').all()
for puesto in puestos[:3]:
    print(f"- {puesto.puesto_nombre} (código: {puesto.puesto_codigo}, mun: {puesto.municipio_codigo})")

print("\n=== USUARIOS ===")
usuarios = User.query.all()
for user in usuarios[:5]:
    print(f"- {user.nombre} ({user.rol})")
    if user.ubicacion_id:
        loc = Location.query.get(user.ubicacion_id)
        if loc:
            print(f"  Ubicación: {loc.nombre_completo}")
