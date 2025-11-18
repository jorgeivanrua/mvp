#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar que los formularios E-14 tengan acceso a candidatos
"""
from backend.app import create_app
from backend.models.configuracion_electoral import TipoEleccion, Partido, Candidato
from backend.database import db

app = create_app('development')

with app.app_context():
    print("="*80)
    print("VERIFICACIÓN DE CANDIDATOS PARA FORMULARIOS E-14")
    print("="*80)
    
    # Verificar tipos de elección
    print("\n1. TIPOS DE ELECCIÓN")
    print("-"*80)
    tipos = TipoEleccion.query.filter_by(activo=True).all()
    print(f"Total de tipos de elección activos: {len(tipos)}")
    for tipo in tipos:
        print(f"  - {tipo.nombre} ({tipo.codigo})")
        print(f"    Es uninominal: {tipo.es_uninominal}")
        print(f"    Permite lista cerrada: {tipo.permite_lista_cerrada}")
        print(f"    Permite lista abierta: {tipo.permite_lista_abierta}")
    
    # Verificar partidos
    print("\n2. PARTIDOS POLÍTICOS")
    print("-"*80)
    partidos = Partido.query.filter_by(activo=True).all()
    print(f"Total de partidos activos: {len(partidos)}")
    for partido in partidos:
        print(f"  - {partido.nombre} ({partido.nombre_corto})")
        print(f"    Código: {partido.codigo}")
        print(f"    Color: {partido.color}")
    
    # Verificar candidatos
    print("\n3. CANDIDATOS")
    print("-"*80)
    candidatos = Candidato.query.all()
    print(f"Total de candidatos: {len(candidatos)}")
    
    if candidatos:
        print("\nCandidatos por tipo de elección:")
        for tipo in tipos:
            candidatos_tipo = Candidato.query.filter_by(tipo_eleccion_id=tipo.id).all()
            print(f"\n  {tipo.nombre}:")
            print(f"    Total: {len(candidatos_tipo)}")
            
            if candidatos_tipo:
                for i, candidato in enumerate(candidatos_tipo[:5], 1):
                    partido = Partido.query.get(candidato.partido_id)
                    print(f"      {i}. {candidato.nombre} - {partido.nombre if partido else 'Sin partido'}")
                if len(candidatos_tipo) > 5:
                    print(f"      ... y {len(candidatos_tipo) - 5} más")
            else:
                print(f"      ⚠️ No hay candidatos para este tipo de elección")
    else:
        print("\n⚠️ NO HAY CANDIDATOS EN LA BASE DE DATOS")
        print("\nPara que los formularios E-14 funcionen correctamente, necesitas:")
        print("1. Cargar candidatos en la base de datos")
        print("2. Asociar candidatos a tipos de elección")
        print("3. Asociar candidatos a partidos políticos")
    
    # Verificar modelo de Candidato
    print("\n4. ESTRUCTURA DEL MODELO CANDIDATO")
    print("-"*80)
    print("Campos del modelo Candidato:")
    if candidatos:
        candidato = candidatos[0]
        print(f"  - id: {candidato.id}")
        print(f"  - nombre: {candidato.nombre}")
        print(f"  - tipo_eleccion_id: {candidato.tipo_eleccion_id}")
        print(f"  - partido_id: {candidato.partido_id}")
        print(f"  - numero: {getattr(candidato, 'numero', 'N/A')}")
        print(f"  - activo: {getattr(candidato, 'activo', 'N/A')}")
    else:
        print("  No hay candidatos para mostrar estructura")
    
    print("\n" + "="*80)
    print("RESUMEN")
    print("="*80)
    print(f"✓ Tipos de elección: {len(tipos)}")
    print(f"✓ Partidos políticos: {len(partidos)}")
    print(f"{'✓' if candidatos else '✗'} Candidatos: {len(candidatos)}")
    
    if not candidatos:
        print("\n⚠️ ACCIÓN REQUERIDA:")
        print("Necesitas cargar candidatos para que los formularios E-14 funcionen")
        print("Usa el endpoint de Super Admin para cargar candidatos")
