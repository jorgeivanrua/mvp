#!/usr/bin/env python3
"""
Script para verificar que los datos electorales estén cargados correctamente
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.database import db
from backend.models.configuracion_electoral import TipoEleccion, Partido, Candidato

def verificar_datos():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("VERIFICACIÓN DE DATOS ELECTORALES")
        print("=" * 60)
        
        # Verificar tipos de elección
        print("\n📋 TIPOS DE ELECCIÓN:")
        tipos = TipoEleccion.query.filter_by(activo=True).order_by(TipoEleccion.orden).all()
        if tipos:
            for tipo in tipos:
                print(f"  ✓ {tipo.nombre} (ID: {tipo.id}, Uninominal: {tipo.es_uninominal})")
        else:
            print("  ❌ No hay tipos de elección registrados")
        
        # Verificar partidos
        print("\n🎨 PARTIDOS POLÍTICOS:")
        partidos = Partido.query.filter_by(activo=True).order_by(Partido.orden).all()
        if partidos:
            for partido in partidos:
                print(f"  ✓ {partido.nombre} ({partido.nombre_corto})")
        else:
            print("  ❌ No hay partidos registrados")
        
        # Verificar candidatos por tipo de elección
        print("\n👥 CANDIDATOS POR TIPO DE ELECCIÓN:")
        for tipo in tipos:
            candidatos = Candidato.query.filter_by(
                tipo_eleccion_id=tipo.id,
                activo=True
            ).order_by(Candidato.orden).all()
            
            print(f"\n  {tipo.nombre}:")
            if candidatos:
                # Agrupar por partido
                candidatos_por_partido = {}
                for candidato in candidatos:
                    if candidato.partido_id not in candidatos_por_partido:
                        candidatos_por_partido[candidato.partido_id] = []
                    candidatos_por_partido[candidato.partido_id].append(candidato)
                
                for partido_id, cands in candidatos_por_partido.items():
                    partido = Partido.query.get(partido_id)
                    if partido:
                        print(f"    {partido.nombre_corto}:")
                        for cand in cands:
                            lista_info = f" (#{cand.numero_lista})" if cand.numero_lista else ""
                            print(f"      - {cand.nombre_completo}{lista_info}")
            else:
                print(f"    ❌ No hay candidatos para {tipo.nombre}")
        
        print("\n" + "=" * 60)
        print("RESUMEN:")
        print(f"  Tipos de elección: {len(tipos)}")
        print(f"  Partidos: {len(partidos)}")
        total_candidatos = Candidato.query.filter_by(activo=True).count()
        print(f"  Total candidatos: {total_candidatos}")
        print("=" * 60)

if __name__ == '__main__':
    verificar_datos()
