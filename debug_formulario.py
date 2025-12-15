#!/usr/bin/env python3
"""
Script para verificar el estado del formulario y datos relacionados
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

def debug_formulario():
    app = create_app()
    
    with app.app_context():
        try:
            print("🔍 DIAGNÓSTICO COMPLETO DEL FORMULARIO")
            print("=" * 50)
            
            # 1. Verificar usuario coordinador
            coordinador = User.query.filter_by(nombre='COORD_PUESTO_TEST').first()
            if coordinador:
                print(f"✅ Usuario coordinador encontrado:")
                print(f"   ID: {coordinador.id}")
                print(f"   Nombre: {coordinador.nombre}")
                print(f"   Rol: {coordinador.rol}")
                print(f"   Ubicación ID: {coordinador.ubicacion_id}")
                print(f"   Activo: {coordinador.activo}")
            else:
                print("❌ Usuario coordinador NO encontrado")
                return
            
            # 2. Verificar puesto
            puesto = Location.query.get(coordinador.ubicacion_id)
            if puesto:
                print(f"\n✅ Puesto encontrado:")
                print(f"   ID: {puesto.id}")
                print(f"   Nombre: {puesto.nombre_completo}")
                print(f"   Código: {puesto.puesto_codigo}")
                print(f"   Tipo: {puesto.tipo}")
            else:
                print("❌ Puesto NO encontrado")
                return
            
            # 3. Verificar mesas del puesto
            mesas = Location.query.filter_by(
                tipo='mesa',
                departamento_codigo=puesto.departamento_codigo,
                municipio_codigo=puesto.municipio_codigo,
                puesto_codigo=puesto.puesto_codigo
            ).all()
            
            print(f"\n📍 Mesas en el puesto: {len(mesas)}")
            for mesa in mesas:
                print(f"   Mesa ID: {mesa.id}, Código: {mesa.mesa_codigo}, Nombre: {mesa.mesa_nombre}")
            
            # 4. Verificar formularios
            formularios = FormularioE14.query.all()
            print(f"\n📋 Total formularios en BD: {len(formularios)}")
            
            for form in formularios:
                print(f"\n📋 Formulario ID: {form.id}")
                print(f"   Mesa ID: {form.mesa_id}")
                print(f"   Testigo ID: {form.testigo_id}")
                print(f"   Estado: {form.estado}")
                print(f"   Total votos: {form.total_votos}")
                print(f"   Imagen URL: {form.imagen_url}")
                
                # Verificar si la mesa pertenece al puesto del coordinador
                mesa_form = Location.query.get(form.mesa_id)
                if mesa_form:
                    pertenece = (mesa_form.departamento_codigo == puesto.departamento_codigo and
                               mesa_form.municipio_codigo == puesto.municipio_codigo and
                               mesa_form.puesto_codigo == puesto.puesto_codigo)
                    print(f"   Mesa: {mesa_form.nombre_completo}")
                    print(f"   Pertenece al puesto del coordinador: {'✅ SÍ' if pertenece else '❌ NO'}")
                
                # Verificar votos por partido
                votos_partidos = VotoPartido.query.filter_by(formulario_id=form.id).all()
                print(f"   Votos por partido: {len(votos_partidos)}")
                for vp in votos_partidos:
                    partido = PartidoPolitico.query.get(vp.partido_id)
                    print(f"     - {partido.nombre if partido else 'Desconocido'}: {vp.votos} votos")
                
                # Verificar votos por candidatos
                votos_candidatos = VotoCandidato.query.filter_by(formulario_id=form.id).all()
                print(f"   Votos por candidatos: {len(votos_candidatos)}")
                for vc in votos_candidatos:
                    candidato = Candidato.query.get(vc.candidato_id)
                    print(f"     - {candidato.nombre_completo if candidato else 'Desconocido'}: {vc.votos} votos")
            
            # 5. Verificar partidos y candidatos disponibles
            partidos = PartidoPolitico.query.all()
            print(f"\n🏛️ Total partidos en BD: {len(partidos)}")
            for partido in partidos[:5]:  # Solo primeros 5
                print(f"   - {partido.nombre} ({partido.sigla})")
            
            candidatos = Candidato.query.all()
            print(f"\n👥 Total candidatos en BD: {len(candidatos)}")
            for candidato in candidatos[:5]:  # Solo primeros 5
                print(f"   - {candidato.nombre_completo} (Número: {candidato.numero_lista})")
            
            print("\n" + "=" * 50)
            print("🎯 DIAGNÓSTICO COMPLETADO")
            
        except Exception as e:
            print(f"❌ Error en diagnóstico: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_formulario()