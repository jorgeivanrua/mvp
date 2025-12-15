#!/usr/bin/env python3
"""
Script para actualizar el formulario con datos completos y coherentes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.models.formulario_e14 import FormularioE14, VotoPartido, VotoCandidato
from backend.database import db

def actualizar_formulario():
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 ACTUALIZANDO FORMULARIO CON DATOS COHERENTES")
            print("=" * 50)
            
            # Obtener el formulario
            formulario = FormularioE14.query.get(1)
            if not formulario:
                print("❌ Formulario no encontrado")
                return
            
            print(f"📋 Formulario encontrado: ID {formulario.id}")
            
            # Actualizar datos básicos del formulario para que sean coherentes
            formulario.total_votantes_registrados = 300
            formulario.total_votos = 250
            formulario.votos_validos = 240
            formulario.votos_nulos = 8
            formulario.votos_blanco = 2
            formulario.tarjetas_no_marcadas = 50
            formulario.total_tarjetas = 300
            formulario.imagen_url = '/static/images/sample-e14.svg'
            formulario.observaciones = 'Formulario de prueba para testing del modal - Datos coherentes'
            
            # Limpiar votos existentes
            VotoPartido.query.filter_by(formulario_id=formulario.id).delete()
            VotoCandidato.query.filter_by(formulario_id=formulario.id).delete()
            
            # Crear votos por partido coherentes
            voto_partido1 = VotoPartido(
                formulario_id=formulario.id,
                partido_id=1,  # Liberal
                votos=150
            )
            voto_partido2 = VotoPartido(
                formulario_id=formulario.id,
                partido_id=9,  # MIRA
                votos=90
            )
            
            db.session.add(voto_partido1)
            db.session.add(voto_partido2)
            
            # Crear votos por candidatos coherentes (total = 240 = votos_validos)
            voto_candidato1 = VotoCandidato(
                formulario_id=formulario.id,
                candidato_id=1,  # Gustavo Bolívar
                votos=80
            )
            voto_candidato2 = VotoCandidato(
                formulario_id=formulario.id,
                candidato_id=2,  # María José Pizarro
                votos=70
            )
            voto_candidato3 = VotoCandidato(
                formulario_id=formulario.id,
                candidato_id=3,  # Iván Cepeda
                votos=90
            )
            
            db.session.add(voto_candidato1)
            db.session.add(voto_candidato2)
            db.session.add(voto_candidato3)
            
            db.session.commit()
            
            print("✅ Formulario actualizado exitosamente:")
            print(f"   Total votantes registrados: {formulario.total_votantes_registrados}")
            print(f"   Total votos: {formulario.total_votos}")
            print(f"   Votos válidos: {formulario.votos_validos}")
            print(f"   Votos nulos: {formulario.votos_nulos}")
            print(f"   Votos blanco: {formulario.votos_blanco}")
            print(f"   Tarjetas no marcadas: {formulario.tarjetas_no_marcadas}")
            print(f"   Imagen URL: {formulario.imagen_url}")
            
            print("\n📊 Votos por partido:")
            print(f"   Liberal: 150 votos")
            print(f"   MIRA: 90 votos")
            print(f"   Total: 240 votos (coincide con votos_validos)")
            
            print("\n👥 Votos por candidatos:")
            print(f"   Gustavo Bolívar: 80 votos")
            print(f"   María José Pizarro: 70 votos")
            print(f"   Iván Cepeda: 90 votos")
            print(f"   Total: 240 votos (coincide con votos_validos)")
            
            print("\n🔍 Verificación matemática:")
            total_calculado = formulario.votos_validos + formulario.votos_nulos + formulario.votos_blanco
            print(f"   Votos válidos + nulos + blanco = {formulario.votos_validos} + {formulario.votos_nulos} + {formulario.votos_blanco} = {total_calculado}")
            print(f"   Total votos reportado = {formulario.total_votos}")
            print(f"   ✅ Coincide: {total_calculado == formulario.total_votos}")
            
            total_tarjetas_calc = formulario.total_votos + formulario.tarjetas_no_marcadas
            print(f"   Total votos + no marcadas = {formulario.total_votos} + {formulario.tarjetas_no_marcadas} = {total_tarjetas_calc}")
            print(f"   Total tarjetas = {formulario.total_tarjetas}")
            print(f"   ✅ Coincide: {total_tarjetas_calc == formulario.total_tarjetas}")
            
            participacion = (formulario.total_votos / formulario.total_votantes_registrados) * 100
            print(f"   Participación = {participacion:.1f}%")
            
            print("\n🎯 FORMULARIO LISTO PARA PRUEBAS")
            
        except Exception as e:
            print(f"❌ Error actualizando formulario: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    actualizar_formulario()