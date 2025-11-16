#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cargar candidatos de prueba en la base de datos
"""
from backend.app import create_app
from backend.models.configuracion_electoral import Candidato, Partido, TipoEleccion
from backend.database import db

app = create_app('development')

# Candidatos de prueba por tipo de elección
candidatos_prueba = [
    # PRESIDENCIA (uninominal - 1 candidato por partido)
    {"codigo": "PRES_LIB_001", "nombre_completo": "Juan Pérez García", "partido": "Partido Liberal Colombiano", "tipo": "Presidencia de la República", "numero_lista": 1, "es_cabeza_lista": True},
    {"codigo": "PRES_CON_001", "nombre_completo": "María López Rodríguez", "partido": "Partido Conservador Colombiano", "tipo": "Presidencia de la República", "numero_lista": 1, "es_cabeza_lista": True},
    {"codigo": "PRES_VER_001", "nombre_completo": "Carlos Martínez Silva", "partido": "Partido Alianza Verde", "tipo": "Presidencia de la República", "numero_lista": 1, "es_cabeza_lista": True},
    
    # GOBERNACIÓN (uninominal - 1 candidato por partido)
    {"codigo": "GOB_LIB_001", "nombre_completo": "Ana Gómez Torres", "partido": "Partido Liberal Colombiano", "tipo": "Gobernación Departamental", "numero_lista": 1, "es_cabeza_lista": True},
    {"codigo": "GOB_CON_001", "nombre_completo": "Pedro Ramírez Castro", "partido": "Partido Conservador Colombiano", "tipo": "Gobernación Departamental", "numero_lista": 1, "es_cabeza_lista": True},
    
    # ALCALDÍA (uninominal - 1 candidato por partido)
    {"codigo": "ALC_LIB_001", "nombre_completo": "Laura Sánchez Díaz", "partido": "Partido Liberal Colombiano", "tipo": "Alcaldía Municipal", "numero_lista": 1, "es_cabeza_lista": True},
    {"codigo": "ALC_CON_001", "nombre_completo": "Jorge Hernández Ruiz", "partido": "Partido Conservador Colombiano", "tipo": "Alcaldía Municipal", "numero_lista": 1, "es_cabeza_lista": True},
    {"codigo": "ALC_VER_001", "nombre_completo": "Diana Morales Vega", "partido": "Partido Alianza Verde", "tipo": "Alcaldía Municipal", "numero_lista": 1, "es_cabeza_lista": True},
    
    # SENADO (lista cerrada - múltiples candidatos por partido)
    {"codigo": "SEN_LIB_001", "nombre_completo": "Roberto Castro Méndez", "partido": "Partido Liberal Colombiano", "tipo": "Senado de la República", "numero_lista": 1, "es_cabeza_lista": True},
    {"codigo": "SEN_LIB_002", "nombre_completo": "Patricia Vargas Luna", "partido": "Partido Liberal Colombiano", "tipo": "Senado de la República", "numero_lista": 2, "es_cabeza_lista": False},
    {"codigo": "SEN_LIB_003", "nombre_completo": "Miguel Ángel Rojas", "partido": "Partido Liberal Colombiano", "tipo": "Senado de la República", "numero_lista": 3, "es_cabeza_lista": False},
    
    {"codigo": "SEN_CON_001", "nombre_completo": "Sandra Milena Ortiz", "partido": "Partido Conservador Colombiano", "tipo": "Senado de la República", "numero_lista": 1, "es_cabeza_lista": True},
    {"codigo": "SEN_CON_002", "nombre_completo": "Andrés Felipe Muñoz", "partido": "Partido Conservador Colombiano", "tipo": "Senado de la República", "numero_lista": 2, "es_cabeza_lista": False},
    
    # CÁMARA (lista cerrada - múltiples candidatos por partido)
    {"codigo": "CAM_LIB_001", "nombre_completo": "Gloria Patricia Díaz", "partido": "Partido Liberal Colombiano", "tipo": "Cámara de Representantes", "numero_lista": 1, "es_cabeza_lista": True},
    {"codigo": "CAM_LIB_002", "nombre_completo": "Fernando Gaitán Soto", "partido": "Partido Liberal Colombiano", "tipo": "Cámara de Representantes", "numero_lista": 2, "es_cabeza_lista": False},
    
    {"codigo": "CAM_CON_001", "nombre_completo": "Claudia Marcela Pérez", "partido": "Partido Conservador Colombiano", "tipo": "Cámara de Representantes", "numero_lista": 1, "es_cabeza_lista": True},
    {"codigo": "CAM_CON_002", "nombre_completo": "Luis Eduardo Torres", "partido": "Partido Conservador Colombiano", "tipo": "Cámara de Representantes", "numero_lista": 2, "es_cabeza_lista": False},
]

with app.app_context():
    print("="*80)
    print("CARGANDO CANDIDATOS DE PRUEBA")
    print("="*80)
    
    candidatos_creados = 0
    errores = []
    
    for candidato_data in candidatos_prueba:
        try:
            # Buscar partido
            partido = Partido.query.filter_by(nombre=candidato_data['partido']).first()
            if not partido:
                errores.append(f"Partido '{candidato_data['partido']}' no encontrado para {candidato_data['nombre_completo']}")
                continue
            
            # Buscar tipo de elección
            tipo_eleccion = TipoEleccion.query.filter_by(nombre=candidato_data['tipo']).first()
            if not tipo_eleccion:
                errores.append(f"Tipo de elección '{candidato_data['tipo']}' no encontrado para {candidato_data['nombre_completo']}")
                continue
            
            # Verificar si ya existe
            existing = Candidato.query.filter_by(codigo=candidato_data['codigo']).first()
            if existing:
                print(f"  ⚠ Ya existe: {candidato_data['nombre_completo']}")
                continue
            
            # Crear candidato
            candidato = Candidato(
                codigo=candidato_data['codigo'],
                nombre_completo=candidato_data['nombre_completo'],
                partido_id=partido.id,
                tipo_eleccion_id=tipo_eleccion.id,
                numero_lista=candidato_data.get('numero_lista'),
                es_independiente=candidato_data.get('es_independiente', False),
                es_cabeza_lista=candidato_data.get('es_cabeza_lista', False),
                activo=True
            )
            
            db.session.add(candidato)
            candidatos_creados += 1
            print(f"  ✓ Creado: {candidato_data['nombre_completo']} ({candidato_data['tipo']})")
            
        except Exception as e:
            errores.append(f"Error con {candidato_data['nombre_completo']}: {str(e)}")
    
    # Commit
    if candidatos_creados > 0:
        try:
            db.session.commit()
            print(f"\n{'='*80}")
            print(f"✓ {candidatos_creados} candidatos creados exitosamente")
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error al guardar: {str(e)}")
    else:
        print(f"\n⚠ No se crearon nuevos candidatos")
    
    if errores:
        print(f"\n⚠ Errores ({len(errores)}):")
        for error in errores:
            print(f"  - {error}")
    
    # Verificar total
    total_candidatos = Candidato.query.count()
    print(f"\nTotal de candidatos en BD: {total_candidatos}")
    
    # Mostrar resumen por tipo de elección
    print(f"\n{'='*80}")
    print("RESUMEN POR TIPO DE ELECCIÓN")
    print(f"{'='*80}")
    
    tipos = TipoEleccion.query.filter_by(activo=True).all()
    for tipo in tipos:
        count = Candidato.query.filter_by(tipo_eleccion_id=tipo.id).count()
        if count > 0:
            print(f"  {tipo.nombre}: {count} candidatos")
