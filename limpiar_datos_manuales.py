#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eliminar datos manuales y usar solo DIVIPOLA"""
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.models.formulario_e14 import FormularioE14
from backend.models.incidentes_delitos import IncidenteElectoral, DelitoElectoral
from backend.app import create_app

app = create_app()
app.app_context().push()

print("\n=== LIMPIANDO DATOS MANUALES ===\n")

# 1. Eliminar formularios de las mesas manuales
print("1. Eliminando formularios de mesas manuales...")
formularios = FormularioE14.query.filter(
    FormularioE14.mesa_id.in_([403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417])
).all()
print(f"   Formularios a eliminar: {len(formularios)}")
for form in formularios:
    db.session.delete(form)

# 2. Eliminar incidentes de las mesas manuales
print("2. Eliminando incidentes de mesas manuales...")
incidentes = IncidenteElectoral.query.filter(
    IncidenteElectoral.mesa_id.in_([403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417])
).all()
print(f"   Incidentes a eliminar: {len(incidentes)}")
for inc in incidentes:
    db.session.delete(inc)

# 3. Eliminar delitos de las mesas manuales
print("3. Eliminando delitos de mesas manuales...")
delitos = DelitoElectoral.query.filter(
    DelitoElectoral.mesa_id.in_([403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417])
).all()
print(f"   Delitos a eliminar: {len(delitos)}")
for delito in delitos:
    db.session.delete(delito)

# 4. Primero eliminar seguimiento de reportes de usuarios manuales
print("4. Eliminando seguimiento de reportes de usuarios manuales...")
from backend.models.incidentes_delitos import SeguimientoReporte, NotificacionReporte
seguimientos = SeguimientoReporte.query.filter(
    SeguimientoReporte.usuario_id.in_([9, 10])  # IDs de usuarios manuales
).all()
print(f"   Seguimientos de reportes a eliminar: {len(seguimientos)}")
for seg in seguimientos:
    db.session.delete(seg)
db.session.flush()

# 5. Eliminar notificaciones de reportes de usuarios manuales
print("5. Eliminando notificaciones de reportes de usuarios manuales...")
notif_reportes = NotificacionReporte.query.filter(
    NotificacionReporte.usuario_id.in_([9, 10])  # IDs de usuarios manuales
).all()
print(f"   Notificaciones de reportes a eliminar: {len(notif_reportes)}")
for notif in notif_reportes:
    db.session.delete(notif)
db.session.flush()

# 6. Eliminar usuarios asignados a puestos manuales
print("6. Eliminando usuarios de puestos manuales...")
usuarios = User.query.filter(
    User.ubicacion_id.in_([402, 408, 413])  # IDs de puestos manuales
).all()
print(f"   Usuarios a eliminar: {len(usuarios)}")
for user in usuarios:
    print(f"   - {user.nombre} ({user.rol})")
    db.session.delete(user)
db.session.flush()

# 7. Eliminar mesas manuales
print("7. Eliminando mesas manuales...")
mesas_manuales = Location.query.filter(
    Location.tipo == 'mesa',
    Location.puesto_codigo.in_(['001', '002', '003']),
    Location.puesto_nombre.in_(['Colegio Nacional', 'Escuela La Esperanza', 'Instituto Técnico'])
).all()
print(f"   Mesas a eliminar: {len(mesas_manuales)}")
for mesa in mesas_manuales:
    db.session.delete(mesa)

# 8. Eliminar puestos manuales
print("8. Eliminando puestos manuales...")
puestos_manuales = Location.query.filter(
    Location.tipo == 'puesto',
    Location.puesto_nombre.in_(['Colegio Nacional', 'Escuela La Esperanza', 'Instituto Técnico'])
).all()
print(f"   Puestos a eliminar: {len(puestos_manuales)}")
for puesto in puestos_manuales:
    print(f"   - {puesto.puesto_nombre}")
    db.session.delete(puesto)

db.session.commit()

print("\n=== VERIFICACIÓN ===")
puestos_total = Location.query.filter_by(tipo='puesto').count()
mesas_total = Location.query.filter_by(tipo='mesa').count()
usuarios_total = User.query.count()

print(f"✓ Puestos restantes: {puestos_total}")
print(f"✓ Mesas restantes: {mesas_total}")
print(f"✓ Usuarios restantes: {usuarios_total}")

# Mostrar un puesto de DIVIPOLA para usar en pruebas
print("\n=== PUESTO DE DIVIPOLA PARA PRUEBAS ===")
puesto_divipola = Location.query.filter_by(tipo='puesto').first()
if puesto_divipola:
    print(f"\n✓ Puesto encontrado:")
    print(f"  Nombre: {puesto_divipola.puesto_nombre}")
    print(f"  Ubicación: {puesto_divipola.nombre_completo}")
    print(f"  ID: {puesto_divipola.id}")
    print(f"  Códigos:")
    print(f"    departamento_codigo: {puesto_divipola.departamento_codigo}")
    print(f"    municipio_codigo: {puesto_divipola.municipio_codigo}")
    print(f"    zona_codigo: {puesto_divipola.zona_codigo}")
    print(f"    puesto_codigo: {puesto_divipola.puesto_codigo}")
    
    # Buscar mesas de este puesto
    mesas = Location.query.filter_by(
        tipo='mesa',
        departamento_codigo=puesto_divipola.departamento_codigo,
        municipio_codigo=puesto_divipola.municipio_codigo,
        zona_codigo=puesto_divipola.zona_codigo,
        puesto_codigo=puesto_divipola.puesto_codigo
    ).all()
    
    print(f"\n  Mesas en este puesto: {len(mesas)}")
    for mesa in mesas[:5]:
        print(f"    - Mesa {mesa.mesa_codigo} (ID: {mesa.id})")
else:
    print("✗ No se encontraron puestos de DIVIPOLA")

print("\n✓ LIMPIEZA COMPLETADA\n")
