#!/usr/bin/env python3
"""
Script para crear formulario de prueba para el coordinador de puesto
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location
from backend.models.formulario_e14 import FormularioE14, VotoPartido, VotoCandidato
from backend.models.partido_politico import PartidoPolitico
from backend.models.candidato import Candidato
from backend.database import db
from datetime import datetime

def crear_formulario_prueba():
    app = create_app()
    
    with app.app_context():
        try:
            # Buscar el coordinador que acabamos de crear
            coordinador = User.query.filter_by(nombre='COORD_PUESTO_TEST').first()
            if not coordinador:
                print("❌ No se encontró el coordinador COORD_PUESTO_TEST")
                return
            
            print(f"✅ Coordinador encontrado: {coordinador.nombre} (Puesto ID: {coordinador.ubicacion_id})")
            
            # Buscar una mesa en el mismo puesto
            puesto = Location.query.get(coordinador.ubicacion_id)
            mesa = Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                puesto_codigo=puesto.puesto_codigo
            ).first()
            
            if not mesa:
                print("❌ No se encontró ninguna mesa en el puesto")
                return
            
            print(f"📍 Mesa encontrada: {mesa.nombre_completo} (ID: {mesa.id})")
            
            # Buscar un testigo para asignar
            testigo = User.query.filter_by(rol='testigo_electoral').first()
            if not testigo:
                print("❌ No se encontró ningún testigo")
                return
            
            print(f"👤 Testigo encontrado: {testigo.nombre} (ID: {testigo.id})")
            
            # Verificar si ya existe un formulario para esta mesa
            formulario_existente = FormularioE14.query.filter_by(mesa_id=mesa.id).first()
            if formulario_existente:
                print(f"✅ Ya existe formulario para esta mesa: ID {formulario_existente.id}")
                print(f"   Estado: {formulario_existente.estado}")
                print(f"   Imagen URL: {formulario_existente.imagen_url}")
                return formulario_existente
            
            # Crear el formulario
            formulario = FormularioE14(
                mesa_id=mesa.id,
                testigo_id=testigo.id,
                tipo_eleccion_id=1,  # Asumiendo que existe
                total_votantes_registrados=300,
                total_votos=250,
                votos_validos=240,
                votos_nulos=8,
                votos_blanco=2,
                tarjetas_no_marcadas=50,
                total_tarjetas=300,
                estado='pendiente',
                imagen_url='/static/images/sample-e14.svg',
                observaciones='Formulario de prueba para testing del modal'
            )
            
            db.session.add(formulario)
            db.session.flush()  # Para obtener el ID
            
            print(f"📋 Formulario creado: ID {formulario.id}")
            
            # Buscar partidos existentes
            partidos = PartidoPolitico.query.limit(2).all()
            if len(partidos) >= 2:
                # Crear votos por partido
                voto_partido1 = VotoPartido(
                    formulario_id=formulario.id,
                    partido_id=partidos[0].id,
                    votos=150
                )
                voto_partido2 = VotoPartido(
                    formulario_id=formulario.id,
                    partido_id=partidos[1].id,
                    votos=90
                )
                
                db.session.add(voto_partido1)
                db.session.add(voto_partido2)
                
                print(f"🗳️ Votos por partido creados: {partidos[0].nombre} (150), {partidos[1].nombre} (90)")
            
            # Buscar candidatos existentes
            candidatos = Candidato.query.limit(3).all()
            if len(candidatos) >= 3:
                # Crear votos por candidatos
                votos_candidatos = [80, 70, 90]  # Total: 240 (coincide con votos_validos)
                
                for i, candidato in enumerate(candidatos[:3]):
                    voto_candidato = VotoCandidato(
                        formulario_id=formulario.id,
                        candidato_id=candidato.id,
                        votos=votos_candidatos[i]
                    )
                    db.session.add(voto_candidato)
                
                print(f"👥 Votos por candidatos creados: 3 candidatos con {sum(votos_candidatos)} votos totales")
            
            db.session.commit()
            
            print("✅ Formulario de prueba creado exitosamente:")
            print(f"   ID: {formulario.id}")
            print(f"   Mesa: {mesa.nombre_completo}")
            print(f"   Testigo: {testigo.nombre}")
            print(f"   Estado: {formulario.estado}")
            print(f"   Total votos: {formulario.total_votos}")
            print(f"   Imagen: {formulario.imagen_url}")
            
            return formulario
            
        except Exception as e:
            print(f"❌ Error creando formulario: {e}")
            db.session.rollback()
            return None

if __name__ == "__main__":
    crear_formulario_prueba()