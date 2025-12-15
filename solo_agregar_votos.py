#!/usr/bin/env python3
"""
Solo agregar votos por partido sin crear candidatos
"""
from backend.app import create_app
from backend.database import db
from backend.models.formulario_e14 import VotoPartido, FormularioE14
from backend.models.partido_politico import PartidoPolitico

def solo_agregar_votos():
    """Solo agregar votos por partido"""
    app = create_app()
    
    with app.app_context():
        print("🎯 AGREGANDO SOLO VOTOS POR PARTIDO")
        print("=" * 50)
        
        formulario_id = 1
        
        # Agregar votos a más partidos
        votos_adicionales = [
            {'sigla': 'CAMBIO_RADICAL', 'votos': 25},
            {'sigla': 'U', 'votos': 18},
            {'sigla': 'PACTO_HISTORICO', 'votos': 22},
            {'sigla': 'COMUNES', 'votos': 12}
        ]
        
        print(f"📊 Agregando votos por partido:")
        
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
        
        # Actualizar totales del formulario
        formulario = FormularioE14.query.get(formulario_id)
        
        if formulario:
            # Calcular nuevos totales
            total_votos_partidos = db.session.query(db.func.sum(VotoPartido.votos)).filter_by(formulario_id=formulario_id).scalar() or 0
            
            # Actualizar formulario (mantener votos nulos y blancos existentes)
            formulario.votos_validos = total_votos_partidos
            formulario.total_votos = total_votos_partidos + (formulario.votos_nulos or 0) + (formulario.votos_blanco or 0)
            
            print(f"\n📊 TOTALES ACTUALIZADOS:")
            print(f"   Total votos partidos: {total_votos_partidos}")
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
    solo_agregar_votos()