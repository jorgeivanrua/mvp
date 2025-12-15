#!/usr/bin/env python3
"""
Agregar votos a partidos existentes para tener más datos en el E-14
"""
from backend.app import create_app
from backend.database import db
from backend.models.formulario_e14 import VotoPartido, VotoCandidato
from backend.models.partido_politico import PartidoPolitico
from backend.models.candidato import Candidato

def agregar_votos_partidos_existentes():
    """Agregar votos a partidos existentes"""
    app = create_app()
    
    with app.app_context():
        print("🎯 AGREGANDO VOTOS A PARTIDOS EXISTENTES")
        print("=" * 50)
        
        formulario_id = 1
        
        # Ver qué partidos existen
        partidos_existentes = PartidoPolitico.query.filter_by(activo=True).all()
        print(f"📋 Partidos disponibles: {len(partidos_existentes)}")
        
        for partido in partidos_existentes:
            print(f"   • {partido.sigla}: {partido.nombre}")
        
        # Agregar votos a partidos que no los tienen
        votos_adicionales = [
            {'sigla': 'CONSERVADOR', 'votos': 45},
            {'sigla': 'CENTRO_DEM', 'votos': 35}, 
            {'sigla': 'CAMBIO_RAD', 'votos': 25},
            {'sigla': 'VERDE', 'votos': 30},
            {'sigla': 'POLO', 'votos': 20},
            {'sigla': 'URIBE', 'votos': 15}
        ]
        
        print(f"\n📊 Agregando votos por partido:")
        
        for voto_data in votos_adicionales:
            # Buscar el partido
            partido = PartidoPolitico.query.filter_by(sigla=voto_data['sigla']).first()
            
            if partido:
                # Verificar si ya tiene votos en este formulario
                voto_existente = VotoPartido.query.filter_by(
                    formulario_id=formulario_id,
                    partido_id=partido.id
                ).first()
                
                if not voto_existente:
                    # Agregar votos
                    voto_partido = VotoPartido(
                        formulario_id=formulario_id,
                        partido_id=partido.id,
                        votos=voto_data['votos']
                    )
                    db.session.add(voto_partido)
                    print(f"   ✅ {voto_data['sigla']}: {voto_data['votos']} votos")
                else:
                    print(f"   ℹ️ {voto_data['sigla']}: Ya tiene votos ({voto_existente.votos})")
            else:
                print(f"   ❌ {voto_data['sigla']}: Partido no encontrado")
        
        # Crear algunos candidatos adicionales para partidos que no los tienen
        candidatos_adicionales = [
            {'nombre': 'Carlos Holguín', 'numero': 4, 'partido_sigla': 'CONSERVADOR', 'votos': 25},
            {'nombre': 'Marta Lucía Ramírez', 'numero': 5, 'partido_sigla': 'CONSERVADOR', 'votos': 20},
            {'nombre': 'Álvaro Uribe', 'numero': 6, 'partido_sigla': 'CENTRO_DEM', 'votos': 20},
            {'nombre': 'María Fernanda Cabal', 'numero': 7, 'partido_sigla': 'CENTRO_DEM', 'votos': 15},
        ]
        
        print(f"\n👥 Agregando candidatos:")
        
        for candidato_data in candidatos_adicionales:
            partido = PartidoPolitico.query.filter_by(sigla=candidato_data['partido_sigla']).first()
            
            if partido:
                # Verificar si el candidato ya existe
                candidato_existente = Candidato.query.filter_by(
                    numero_lista=candidato_data['numero'],
                    partido_id=partido.id
                ).first()
                
                if not candidato_existente:
                    # Crear candidato
                    candidato = Candidato(
                        nombre_completo=candidato_data['nombre'],
                        numero_lista=candidato_data['numero'],
                        partido_id=partido.id,
                        tipo_eleccion_id=1,
                        activo=True
                    )
                    db.session.add(candidato)
                    db.session.flush()
                    
                    # Agregar votos del candidato
                    voto_candidato = VotoCandidato(
                        formulario_id=formulario_id,
                        candidato_id=candidato.id,
                        votos=candidato_data['votos']
                    )
                    db.session.add(voto_candidato)
                    
                    print(f"   ✅ #{candidato_data['numero']} {candidato_data['nombre']} ({candidato_data['partido_sigla']}): {candidato_data['votos']} votos")
                else:
                    print(f"   ℹ️ #{candidato_data['numero']} {candidato_data['nombre']}: Ya existe")
        
        # Actualizar totales del formulario
        from backend.models.formulario_e14 import FormularioE14
        formulario = FormularioE14.query.get(formulario_id)
        
        if formulario:
            # Calcular nuevos totales
            total_votos_partidos = db.session.query(db.func.sum(VotoPartido.votos)).filter_by(formulario_id=formulario_id).scalar() or 0
            total_votos_candidatos = db.session.query(db.func.sum(VotoCandidato.votos)).filter_by(formulario_id=formulario_id).scalar() or 0
            
            # Actualizar formulario (mantener votos nulos y blancos existentes)
            formulario.votos_validos = total_votos_candidatos
            formulario.total_votos = total_votos_candidatos + (formulario.votos_nulos or 0) + (formulario.votos_blanco or 0)
            
            print(f"\n📊 TOTALES ACTUALIZADOS:")
            print(f"   Total votos partidos: {total_votos_partidos}")
            print(f"   Total votos candidatos: {total_votos_candidatos}")
            print(f"   Votos nulos: {formulario.votos_nulos or 0}")
            print(f"   Votos blancos: {formulario.votos_blanco or 0}")
            print(f"   Total formulario: {formulario.total_votos}")
        
        # Guardar cambios
        db.session.commit()
        
        print("\n" + "=" * 50)
        print("🎉 ¡VOTOS AGREGADOS EXITOSAMENTE!")
        print("=" * 50)
        
        # Mostrar resumen final
        votos_finales = VotoPartido.query.filter_by(formulario_id=formulario_id).all()
        print(f"\n📊 RESUMEN FINAL ({len(votos_finales)} partidos):")
        
        total_general = 0
        for voto in votos_finales:
            partido = PartidoPolitico.query.get(voto.partido_id)
            print(f"   • {partido.sigla}: {voto.votos} votos")
            total_general += voto.votos
        
        print(f"\n🗳️ TOTAL GENERAL: {total_general} votos")
        print("\n🚀 ¡Refresca el modal para ver todos los partidos!")

if __name__ == "__main__":
    agregar_votos_partidos_existentes()