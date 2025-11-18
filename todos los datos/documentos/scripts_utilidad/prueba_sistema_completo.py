#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueba completa del sistema electoral - Todos los roles y funcionalidades"""
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import datetime
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.models.configuracion_electoral import TipoEleccion, Partido, Candidato
from backend.models.formulario_e14 import FormularioE14
from backend.app import create_app
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

print("\n" + "="*80)
print("PRUEBA COMPLETA DEL SISTEMA ELECTORAL")
print("="*80 + "\n")

# ============================================================================
# FASE 1: CONFIGURACIÓN INICIAL (Super Admin)
# ============================================================================
print("FASE 1: CONFIGURACIÓN INICIAL (Super Admin)")
print("-" * 80)

# 1.1 Verificar Super Admin
super_admin = User.query.filter_by(rol='super_admin').first()
if super_admin:
    print(f"✓ Super Admin encontrado: {super_admin.nombre}")
else:
    print("✗ No se encontró Super Admin")
    sys.exit(1)

# 1.2 Habilitar tipos de elección
print("\n1.2 Habilitando tipos de elección...")
tipos_eleccion = [
    {
        'codigo': 'SENADO',
        'nombre': 'Senado',
        'descripcion': 'Elección de Senadores de la República',
        'es_uninominal': False,
        'permite_lista_cerrada': True,
        'permite_lista_abierta': True,
        'permite_coaliciones': True,
        'activo': True,
        'orden': 1
    },
    {
        'codigo': 'CAMARA',
        'nombre': 'Cámara de Representantes',
        'descripcion': 'Elección de Representantes a la Cámara',
        'es_uninominal': False,
        'permite_lista_cerrada': True,
        'permite_lista_abierta': True,
        'permite_coaliciones': True,
        'activo': True,
        'orden': 2
    }
]

for tipo_data in tipos_eleccion:
    tipo = TipoEleccion.query.filter_by(codigo=tipo_data['codigo']).first()
    if not tipo:
        tipo = TipoEleccion(**tipo_data)
        db.session.add(tipo)
        print(f"  ✓ Creado: {tipo_data['nombre']}")
    else:
        print(f"  ✓ Ya existe: {tipo_data['nombre']}")

db.session.commit()

# 1.3 Cargar partidos políticos
print("\n1.3 Cargando partidos políticos...")
partidos_data = [
    {'codigo': 'PL', 'nombre': 'Partido Liberal', 'nombre_corto': 'PL', 'color': '#FF0000'},
    {'codigo': 'PC', 'nombre': 'Partido Conservador', 'nombre_corto': 'PC', 'color': '#0000FF'},
    {'codigo': 'PDA', 'nombre': 'Polo Democrático', 'nombre_corto': 'PDA', 'color': '#FFFF00'},
    {'codigo': 'AV', 'nombre': 'Alianza Verde', 'nombre_corto': 'AV', 'color': '#00FF00'},
    {'codigo': 'CD', 'nombre': 'Centro Democrático', 'nombre_corto': 'CD', 'color': '#FFA500'}
]

partidos_creados = []
for partido_data in partidos_data:
    partido = Partido.query.filter_by(codigo=partido_data['codigo']).first()
    if not partido:
        partido = Partido(**partido_data)
        db.session.add(partido)
        print(f"  ✓ Creado: {partido_data['nombre']} ({partido_data['codigo']})")
    else:
        print(f"  ✓ Ya existe: {partido_data['nombre']}")
    partidos_creados.append(partido)

db.session.commit()

# 1.4 Cargar candidatos
print("\n1.4 Cargando candidatos...")
tipo_senado = TipoEleccion.query.filter_by(codigo='SENADO').first()
tipo_camara = TipoEleccion.query.filter_by(codigo='CAMARA').first()

candidatos_data = [
    # Senado
    {'codigo': 'SEN-PL-001', 'nombre_completo': 'Juan Pérez', 'partido_id': partidos_creados[0].id, 'tipo_eleccion_id': tipo_senado.id, 'numero_lista': 1},
    {'codigo': 'SEN-PC-001', 'nombre_completo': 'María García', 'partido_id': partidos_creados[1].id, 'tipo_eleccion_id': tipo_senado.id, 'numero_lista': 2},
    {'codigo': 'SEN-PDA-001', 'nombre_completo': 'Carlos López', 'partido_id': partidos_creados[2].id, 'tipo_eleccion_id': tipo_senado.id, 'numero_lista': 3},
    # Cámara
    {'codigo': 'CAM-PL-001', 'nombre_completo': 'Ana Martínez', 'partido_id': partidos_creados[0].id, 'tipo_eleccion_id': tipo_camara.id, 'numero_lista': 1},
    {'codigo': 'CAM-PC-001', 'nombre_completo': 'Pedro Rodríguez', 'partido_id': partidos_creados[1].id, 'tipo_eleccion_id': tipo_camara.id, 'numero_lista': 2},
]

for cand_data in candidatos_data:
    candidato = Candidato.query.filter_by(codigo=cand_data['codigo']).first()
    if not candidato:
        candidato = Candidato(**cand_data)
        db.session.add(candidato)
        tipo = TipoEleccion.query.get(cand_data['tipo_eleccion_id'])
        print(f"  ✓ Creado: {cand_data['nombre_completo']} - {tipo.nombre}")
    else:
        print(f"  ✓ Ya existe: {cand_data['nombre_completo']}")

db.session.commit()

print("\n✓ Configuración inicial completada")

# ============================================================================
# FASE 2: CREACIÓN DE USUARIOS (Admin Departamental/Municipal)
# ============================================================================
print("\n" + "="*80)
print("FASE 2: CREACIÓN DE USUARIOS")
print("-" * 80)

# Obtener ubicaciones de DIVIPOLA
puesto_prueba = Location.query.filter_by(
    tipo='puesto',
    departamento_codigo='44',
    municipio_codigo='01'
).first()

mesas_prueba = Location.query.filter_by(
    tipo='mesa',
    departamento_codigo=puesto_prueba.departamento_codigo,
    municipio_codigo=puesto_prueba.municipio_codigo,
    zona_codigo=puesto_prueba.zona_codigo,
    puesto_codigo=puesto_prueba.puesto_codigo
).limit(3).all()

print(f"\nUsando puesto: {puesto_prueba.puesto_nombre} (ID: {puesto_prueba.id})")
print(f"Mesas disponibles: {len(mesas_prueba)}")

# 2.1 Crear Coordinador de Puesto
coord_puesto = User.query.filter_by(rol='coordinador_puesto', ubicacion_id=puesto_prueba.id).first()
if not coord_puesto:
    coord_puesto = User(
        nombre=f"Coordinador {puesto_prueba.puesto_nombre}",
        password_hash=generate_password_hash('coord123'),
        rol='coordinador_puesto',
        ubicacion_id=puesto_prueba.id,
        activo=True
    )
    db.session.add(coord_puesto)
    print(f"\n✓ Creado Coordinador de Puesto: {coord_puesto.nombre}")
else:
    print(f"\n✓ Ya existe Coordinador de Puesto: {coord_puesto.nombre}")

# 2.2 Crear Testigos Electorales
testigos_creados = []
for i, mesa in enumerate(mesas_prueba, 1):
    testigo = User.query.filter_by(rol='testigo_electoral', ubicacion_id=mesa.id).first()
    if not testigo:
        testigo = User(
            nombre=f"Testigo Mesa {mesa.mesa_codigo}",
            password_hash=generate_password_hash('testigo123'),
            rol='testigo_electoral',
            ubicacion_id=mesa.id,
            activo=True
        )
        db.session.add(testigo)
        print(f"✓ Creado Testigo: {testigo.nombre} (Mesa ID: {mesa.id})")
    else:
        print(f"✓ Ya existe Testigo: {testigo.nombre}")
    testigos_creados.append(testigo)

db.session.commit()

print(f"\n✓ Usuarios creados: {len(testigos_creados)} testigos + 1 coordinador")

# ============================================================================
# FASE 3: FLUJO DE TESTIGO ELECTORAL
# ============================================================================
print("\n" + "="*80)
print("FASE 3: FLUJO DE TESTIGO ELECTORAL")
print("-" * 80)

# 3.1 Testigo reporta formulario E14
testigo1 = testigos_creados[0]
mesa1 = mesas_prueba[0]

print(f"\nTestigo: {testigo1.nombre}")
print(f"Mesa: {mesa1.nombre_completo}")

# Verificar si ya existe formulario
formulario_existente = FormularioE14.query.filter_by(
    mesa_id=mesa1.id,
    testigo_id=testigo1.id,
    tipo_eleccion_id=tipo_senado.id
).first()

if not formulario_existente:
    formulario = FormularioE14(
        mesa_id=mesa1.id,
        testigo_id=testigo1.id,
        tipo_eleccion_id=tipo_senado.id,
        total_votantes_registrados=mesa1.total_votantes_registrados,
        total_votos=250,
        votos_validos=240,
        votos_nulos=5,
        votos_blanco=5,
        tarjetas_no_marcadas=10,
        total_tarjetas=260,
        estado='pendiente',
        observaciones='Formulario de prueba'
    )
    db.session.add(formulario)
    db.session.commit()
    print(f"✓ Formulario E14 creado (ID: {formulario.id})")
    print(f"  - Total votos: {formulario.total_votos}")
    print(f"  - Estado: {formulario.estado}")
else:
    formulario = formulario_existente
    print(f"✓ Formulario E14 ya existe (ID: {formulario.id})")

# ============================================================================
# FASE 4: FLUJO DE COORDINADOR DE PUESTO
# ============================================================================
print("\n" + "="*80)
print("FASE 4: FLUJO DE COORDINADOR DE PUESTO")
print("-" * 80)

print(f"\nCoordinador: {coord_puesto.nombre}")
print(f"Puesto: {puesto_prueba.puesto_nombre}")

# 4.1 Ver formularios pendientes
formularios_pendientes = FormularioE14.query.filter_by(
    mesa_id=mesa1.id,
    estado='pendiente'
).count()

print(f"\n✓ Formularios pendientes en el puesto: {formularios_pendientes}")

# 4.2 Validar formulario
if formulario.estado == 'pendiente':
    formulario.estado = 'validado'
    formulario.validado_por_id = coord_puesto.id
    formulario.validado_at = datetime.utcnow()
    db.session.commit()
    print(f"✓ Formulario validado por coordinador")
else:
    print(f"✓ Formulario ya está en estado: {formulario.estado}")

# ============================================================================
# FASE 5: VERIFICACIÓN DE DASHBOARDS
# ============================================================================
print("\n" + "="*80)
print("FASE 5: VERIFICACIÓN DE DASHBOARDS")
print("-" * 80)

# 5.1 Dashboard Testigo
print("\n5.1 Dashboard Testigo Electoral")
print(f"  Usuario: {testigo1.nombre}")
print(f"  Mesa asignada: {mesa1.nombre_completo}")
formularios_testigo = FormularioE14.query.filter_by(testigo_id=testigo1.id).count()
print(f"  ✓ Formularios reportados: {formularios_testigo}")

# 5.2 Dashboard Coordinador Puesto
print("\n5.2 Dashboard Coordinador de Puesto")
print(f"  Usuario: {coord_puesto.nombre}")
print(f"  Puesto: {puesto_prueba.puesto_nombre}")
mesas_puesto = Location.query.filter_by(
    tipo='mesa',
    departamento_codigo=puesto_prueba.departamento_codigo,
    municipio_codigo=puesto_prueba.municipio_codigo,
    zona_codigo=puesto_prueba.zona_codigo,
    puesto_codigo=puesto_prueba.puesto_codigo
).count()
print(f"  ✓ Mesas en el puesto: {mesas_puesto}")

formularios_puesto = FormularioE14.query.join(Location).filter(
    Location.departamento_codigo == puesto_prueba.departamento_codigo,
    Location.municipio_codigo == puesto_prueba.municipio_codigo,
    Location.zona_codigo == puesto_prueba.zona_codigo,
    Location.puesto_codigo == puesto_prueba.puesto_codigo
).count()
print(f"  ✓ Formularios en el puesto: {formularios_puesto}")

# 5.3 Dashboard Admin Municipal
admin_municipal = User.query.filter_by(rol='admin_municipal').first()
if admin_municipal:
    print("\n5.3 Dashboard Admin Municipal")
    print(f"  Usuario: {admin_municipal.nombre}")
    municipio_loc = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='44',
        municipio_codigo='01'
    ).first()
    if municipio_loc:
        puestos_municipio = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo=municipio_loc.departamento_codigo,
            municipio_codigo=municipio_loc.municipio_codigo
        ).count()
        print(f"  ✓ Puestos en el municipio: {puestos_municipio}")

# 5.4 Dashboard Coordinador Departamental
coord_depto = User.query.filter_by(rol='coordinador_departamental').first()
if coord_depto:
    print("\n5.4 Dashboard Coordinador Departamental")
    print(f"  Usuario: {coord_depto.nombre}")
    puestos_depto = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='44'
    ).count()
    print(f"  ✓ Puestos en el departamento: {puestos_depto}")

# 5.5 Dashboard Auditor Electoral
auditor = User.query.filter_by(rol='auditor_electoral').first()
if auditor:
    print("\n5.5 Dashboard Auditor Electoral")
    print(f"  Usuario: {auditor.nombre}")
    total_formularios = FormularioE14.query.count()
    print(f"  ✓ Total formularios en el sistema: {total_formularios}")

# ============================================================================
# FASE 6: RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("RESUMEN FINAL DEL SISTEMA")
print("="*80)

print("\n📊 CONFIGURACIÓN:")
print(f"  ✓ Tipos de elección: {TipoEleccion.query.filter_by(activo=True).count()}")
print(f"  ✓ Partidos políticos: {Partido.query.count()}")
print(f"  ✓ Candidatos: {Candidato.query.count()}")

print("\n👥 USUARIOS:")
usuarios_por_rol = {}
for user in User.query.all():
    usuarios_por_rol[user.rol] = usuarios_por_rol.get(user.rol, 0) + 1

for rol, count in sorted(usuarios_por_rol.items()):
    print(f"  ✓ {rol}: {count}")

print("\n📍 UBICACIONES:")
print(f"  ✓ Departamentos: 1 (Caquetá)")
print(f"  ✓ Municipios: {Location.query.filter_by(tipo='puesto').distinct(Location.municipio_codigo).count()}")
print(f"  ✓ Puestos: {Location.query.filter_by(tipo='puesto').count()}")
print(f"  ✓ Mesas: {Location.query.filter_by(tipo='mesa').count()}")

print("\n📝 FORMULARIOS:")
print(f"  ✓ Total formularios E14: {FormularioE14.query.count()}")
print(f"  ✓ Pendientes: {FormularioE14.query.filter_by(estado='pendiente').count()}")
print(f"  ✓ Validados: {FormularioE14.query.filter_by(estado='validado').count()}")

print("\n" + "="*80)
print("✅ PRUEBA COMPLETA DEL SISTEMA FINALIZADA EXITOSAMENTE")
print("="*80)

print("\n📋 CREDENCIALES DE PRUEBA:")
print(f"  Super Admin: super_admin / admin123")
print(f"  Coordinador Puesto: {coord_puesto.nombre} / coord123")
print(f"  Testigo: {testigo1.nombre} / testigo123")
print()
