#!/usr/bin/env python3
"""
Agregar más partidos y candidatos al formulario de prueba
"""
from backend.app import create_app
from backend.database import db
from backend.models.formulario_e14 import VotoPartido, VotoCandidato
from backend.models.partido_politico import PartidoPolitico
from backend.models.candidato import Candidato

def agregar_mas_partidos():
    """Agregar más partidos y candidatos al formulario"""
    app = create_app()
    
    with app.app_context():
        print("🎯 AGREGANDO MÁS PARTIDOS AL E-14")
        print("=" * 50)
        
        # Crear más partidos
        partidos_nuevos = [
            {
                'nombre': 'Partido Conservador Colombiano',
                'sigla': 'CONSERVADOR',
                'color': '#0066CC',
                'votos': 45
            },
            {
                'nombre': 'Centro Democrático',
                'sigla': 'CENTRO_DEM',
                'color': '#FF6600',
                'votos': 35
            },
            {
                'nombre': 'Cambio Radical',
                'sigla': 'CAMBIO_RAD',
                'color': '#FFCC00',
                'votos': 25
            },
            {
                'nombre': 'Alianza Verde',
                'sigla': 'VERDE',
                'color': '#00CC66',
                'votos': 30
            }
        ]
        
        # Candidatos para los nuevos partidos
        candidatos_nuevos = [
            # Conservador
            {
                'nombre': 'Carlos Holguín',
                'numero': 4,
                'partido_sigla': 'CONSERVADOR',
                'votos': 25
            },
            {
                'nombre': 'Marta Lucía Ramírez',
                'numero': 5,
                'partido_sigla': 'CONSERVADOR', 
                'votos': 20
            },
            # Centro Democrático
            {
                'nombre': 'Álvaro Uribe',
                'numero': 6,
                'partido_sigla': 'CENTRO_DEM',
                'votos': 20
            },
            {
                'nombre': 'María Fernanda Cabal',
                'numero': 7,
                'partido_sigla': 'CENTRO_DEM',
                'votos': 15
            },
            # Cambio Radical
            {
                'nombre': 'Germán Vargas Lleras',
                'numero': 8,
                'partido_sigla': 'CAMBIO_RAD',
                'votos': 15
            },
            {
                'nombre': 'Carlos Fernando Galán',
                'numero': 9,
                'partido_sigla': 'CAMBIO_RAD',
                'votos': 10
            },
            # Verde
            {
                'nombre': 'Claudia López',
                'numero': 10,
                'partido_sigla': 'VERDE',
                'votos': 18
            },
            {
                'nombre': 'Sergio Fajardo',
                'numero': 11,
                'partido_sigla': 'VERDE',
                'votos': 12
            }
        ]
        
        # Crear partidos
        partidos_creados = {}
        for partido_data in partidos_nuevos:
            # Verificar si ya existe
            partido_existente = PartidoPolitico.query.filter_by(sigla=partido_data['sigla']).first()
            
            if not partido_existente:
                partido = PartidoPolitico(
                    nombre=partido_data['nombre'],
                    sigla=partido_data['sigla'],
                    color=partido_data['color'],
                    activo=True
                )
                db.session.add(partido)
                db.session.flush()  # Para obtener el ID
                partidos_creados[partido_data['sigla']] = partido
                print(f"✅ Partido creado: {partido_data['sigla']} - {partido_data['nombre']}")
            else:
                partidos_creados[partido_data['sigla']] = partido_existente
                print(f"ℹ️ Partido ya existe: {partido_data['sigla']}")
        
        # Crear candidatos
        candidatos_creados = {}
        for candidato_data in candidatos_nuevos:
            partido = partidos_creados[candidato_data['partido_sigla']]
            
            # Verificar si ya existe
            candidato_existente = Candidato.query.filter_by(
                numero_lista=candidato_data['numero'],
                partido_id=partido.id
            ).first()
            
            if not candidato_existente:
                candidato = Candidato(
                    nombre_completo=candidato_data['nombre'],
                    numero_lista=candidato_data['numero'],
                    partido_id=partido.id,
                    tipo_eleccion_id=1,  # Asumiendo que existe
                    activo=True
                )
                db.session.add(candidato)
                db.session.flush()
                candidatos_creados[candidato_data['numero']] = candidato
                print(f"✅ Candidato creado: #{candidato_data['numero']} {candidato_data['nombre']} ({candidato_data['partido_sigla']})")
            else:
                candidatos_creados[candidato_data['numero']] = candidato_existente
                print(f"ℹ️ Candidato ya existe: #{candidato_data['numero']} {candidato_data['nombre']}")
        
        # Agregar votos por partido al formulario ID 1
        formulario_id = 1
        
        for partido_data in partidos_nuevos:
            partido = partidos_creados[partido_data['sigla']]
            
            # Verificar si ya existe el voto
            voto_existente = VotoPartido.query.filter_by(
                formulario_id=formulario_id,
                partido_id=partido.id
            ).first()
            
            if not voto_existente:
                voto_partido = VotoPartido(
                    formulario_id=formulario_id,
                    partido_id=partido.id,
                    votos=partido_data['votos']
                )
                db.session.add(voto_partido)
                print(f"✅ Votos partido agregados: {partido_data['sigla']} = {partido_data['votos']} votos")
            else:
                print(f"ℹ️ Votos partido ya existen: {partido_data['sigla']}")
        
        # Agregar votos por candidato
        for candidato_data in candidatos_nuevos:
            candidato = candidatos_creados[candidato_data['numero']]
            
            # Verificar si ya existe el voto
            voto_existente = VotoCandidato.query.filter_by(
                formulario_id=formulario_id,
                candidato_id=candidato.id
            ).first()
            
            if not voto_existente:
                voto_candidato = VotoCandidato(
                    formulario_id=formulario_id,
                    candidato_id=candidato.id,
                    votos=candidato_data['votos']
                )
                db.session.add(voto_candidato)
                print(f"✅ Votos candidato agregados: #{candidato_data['numero']} {candidato_data['nombre']} = {candidato_data['votos']} votos")
            else:
                print(f"ℹ️ Votos candidato ya existen: #{candidato_data['numero']} {candidato_data['nombre']}")
        
        # Actualizar totales del formulario
        from backend.models.formulario_e14 import FormularioE14
        formulario = FormularioE14.query.get(formulario_id)
        
        if formulario:
            # Calcular nuevos totales
            total_votos_partidos = db.session.query(db.func.sum(VotoPartido.votos)).filter_by(formulario_id=formulario_id).scalar() or 0
            total_votos_candidatos = db.session.query(db.func.sum(VotoCandidato.votos)).filter_by(formulario_id=formulario_id).scalar() or 0
            
            # Actualizar formulario
            formulario.votos_validos = total_votos_candidatos
            formulario.total_votos = total_votos_candidatos + (formulario.votos_nulos or 0) + (formulario.votos_blanco or 0)
            
            print(f"✅ Formulario actualizado:")
            print(f"   Total votos partidos: {total_votos_partidos}")
            print(f"   Total votos candidatos: {total_votos_candidatos}")
            print(f"   Total votos formulario: {formulario.total_votos}")
        
        # Guardar cambios
        db.session.commit()
        
        print("\n" + "=" * 50)
        print("🎉 ¡MÁS PARTIDOS AGREGADOS EXITOSAMENTE!")
        print("=" * 50)
        print("\n📊 RESUMEN FINAL:")
        print("• LIBERAL: 240 votos (3 candidatos)")
        print("• MIRA: 90 votos")
        print("• CONSERVADOR: 45 votos (2 candidatos)")
        print("• CENTRO_DEM: 35 votos (2 candidatos)")
        print("• CAMBIO_RAD: 25 votos (2 candidatos)")
        print("• VERDE: 30 votos (2 candidatos)")
        print(f"\n🗳️ TOTAL: {total_votos_candidatos} votos")
        print("\n🚀 Ahora refresca el modal para ver todos los partidos!")

if __name__ == "__main__":
    agregar_mas_partidos()