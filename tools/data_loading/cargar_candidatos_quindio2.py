#!/usr/bin/env python3
"""
Script para cargar candidatos de Camara, Senado y CITREP
Basados en los candidatos del Caqueta
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.database import db
from backend.models.configuracion_electoral import TipoEleccion
from backend.models.partido_politico import PartidoPolitico
from backend.models.candidato import Candidato

def cargar_candidatos():
    """Cargar candidatos para Senado, Camara y CITREP"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("CARGANDO CANDIDATOS: SENADO, CAMARA Y CITREP")
        print("=" * 80)
        print()
        
        # 1. Agregar CITREP si no existe
        print("1. Verificando tipo de eleccion CITREP...")
        citrep_tipo = TipoEleccion.query.filter_by(codigo='CITREP').first()
        if not citrep_tipo:
            max_orden = db.session.query(db.func.max(TipoEleccion.orden)).scalar() or 0
            citrep_tipo = TipoEleccion(
                codigo='CITREP',
                nombre='Circunscripciones Transitorias Especiales de Paz',
                descripcion='Eleccion de representantes de las Circunscripciones Transitorias Especiales de Paz',
                es_uninominal=False,
                permite_lista_cerrada=True,
                permite_lista_abierta=True,
                permite_coaliciones=True,
                orden=max_orden + 1,
                activo=True
            )
            db.session.add(citrep_tipo)
            db.session.commit()
            print("   [OK] CITREP creado")
        else:
            print(f"   [OK] CITREP ya existe (ID: {citrep_tipo.id})")
        print()
        
        # 2. Limpiar candidatos existentes
        print("2. Limpiando candidatos existentes...")
        Candidato.query.delete()
        db.session.commit()
        print("   [OK] Candidatos eliminados")
        print()
        
        # 3. Obtener tipos y partidos
        tipo_senado = TipoEleccion.query.filter_by(codigo='SENADO').first()
        tipo_camara = TipoEleccion.query.filter_by(codigo='CAMARA').first()
        
        partidos = {p.codigo: p for p in PartidoPolitico.query.all()}
        
        print("3. Creando candidatos por listas...")
        print("-" * 80)
        
        # SENADO - Listas mas largas
        candidatos_senado = [
            # PACTO HISTORICO (5)
            ('Gustavo Bolivar', 'PACTO', 1),
            ('Maria Jose Pizarro', 'PACTO', 2),
            ('Ivan Cepeda', 'PACTO', 3),
            ('Alexander Lopez', 'PACTO', 4),
            ('Isabel Zuleta', 'PACTO', 5),
            # CENTRO DEMOCRATICO (5)
            ('Paloma Valencia', 'CENTRO_DEM', 1),
            ('Miguel Uribe Turbay', 'CENTRO_DEM', 2),
            ('Maria Fernanda Cabal', 'CENTRO_DEM', 3),
            ('Paola Holguin', 'CENTRO_DEM', 4),
            ('Honorio Henriquez', 'CENTRO_DEM', 5),
            # ALIANZA VERDE (4)
            ('Angelica Lozano', 'VERDE', 1),
            ('Ariel Avila', 'VERDE', 2),
            ('Antonio Sanguino', 'VERDE', 3),
            ('Humberto de la Calle', 'VERDE', 4),
            # CONSERVADOR (4)
            ('Efrain Cepeda', 'CONSERVADOR', 1),
            ('David Barguil', 'CONSERVADOR', 2),
            ('Nora Garcia', 'CONSERVADOR', 3),
            ('Ciro Ramirez', 'CONSERVADOR', 4),
            # LIBERAL (5)
            ('Juan Fernando Cristo', 'LIBERAL', 1),
            ('Alejandro Gaviria', 'LIBERAL', 2),
            ('Horacio Jose Serpa', 'LIBERAL', 3),
            ('Viviane Morales', 'LIBERAL', 4),
            ('Luis Fernando Velasco', 'LIBERAL', 5),
            # CAMBIO RADICAL (4)
            ('German Varon', 'CAMBIO_RAD', 1),
            ('Carlos Fernando Motoa', 'CAMBIO_RAD', 2),
            ('Rodrigo Lara', 'CAMBIO_RAD', 3),
            ('David Luna', 'CAMBIO_RAD', 4),
            # POLO (3)
            ('Alexander Lopez Maya', 'POLO', 1),
            ('Aida Avella', 'POLO', 2),
            ('Jorge Enrique Robledo', 'POLO', 3),
            # MIRA (3)
            ('Carlos Alberto Baena', 'MIRA', 1),
            ('John Milton Rodriguez', 'MIRA', 2),
            ('Ana Paola Agudelo', 'MIRA', 3),
            # PARTIDO DE LA U (4)
            ('Roy Barreras', 'U', 1),
            ('Armando Benedetti', 'U', 2),
            ('Juan Mario Laserna', 'U', 3),
            ('Maritza Martinez', 'U', 4),
            # COMUNES (2)
            ('Pablo Catatumbo', 'COMUNES', 1),
            ('Victoria Sandino', 'COMUNES', 2),
        ]
        
        print("\n[*] SENADO:")
        for nombre, partido_cod, numero in candidatos_senado:
            if partido_cod in partidos:
                candidato = Candidato(
                    nombre_completo=nombre,
                    partido_id=partidos[partido_cod].id,
                    tipo_eleccion_id=tipo_senado.id,
                    cargo='Senador',
                    numero_lista=numero,
                    activo=True
                )
                db.session.add(candidato)
                print(f"  [OK] {nombre} ({partidos[partido_cod].sigla}) #{numero}")
        
        # CAMARA CAQUETA - Maximo 3 por partido
        candidatos_camara = [
            # LIBERAL (3)
            ('Hernan Banguero', 'LIBERAL', 1),
            ('Deisy Gomez', 'LIBERAL', 2),
            ('Roberto Sanchez', 'LIBERAL', 3),
            # CONSERVADOR (3)
            ('Carlos Ramirez', 'CONSERVADOR', 1),
            ('Martha Villalba', 'CONSERVADOR', 2),
            ('Jairo Cristancho', 'CONSERVADOR', 3),
            # PACTO HISTORICO (3)
            ('Ana Maria Torres', 'PACTO', 1),
            ('Luis Eduardo Diaz', 'PACTO', 2),
            ('Maria Fernanda Rojas', 'PACTO', 3),
            # CENTRO DEMOCRATICO (3)
            ('Jorge Enrique Rojas', 'CENTRO_DEM', 1),
            ('Claudia Patricia Jimenez', 'CENTRO_DEM', 2),
            ('Hector Fabio Useche', 'CENTRO_DEM', 3),
            # ALIANZA VERDE (3)
            ('Sandra Milena Gutierrez', 'VERDE', 1),
            ('Andres Felipe Arias', 'VERDE', 2),
            ('Diana Carolina Bernal', 'VERDE', 3),
            # CAMBIO RADICAL (3)
            ('Pedro Nel Jimenez', 'CAMBIO_RAD', 1),
            ('Luz Mery Trujillo', 'CAMBIO_RAD', 2),
            ('Oscar Dario Perez', 'CAMBIO_RAD', 3),
            # PARTIDO DE LA U (3)
            ('Gloria Stella Diaz', 'U', 1),
            ('William Villamizar', 'U', 2),
            ('Yolanda Becerra', 'U', 3),
            # POLO (2)
            ('Jaime Caycedo', 'POLO', 1),
            ('Clara Lopez', 'POLO', 2),
            # MIRA (2)
            ('Alexandra Moreno', 'MIRA', 1),
            ('Edgar Espindola', 'MIRA', 2),
            # COMUNES (2)
            ('Julian Gallo', 'COMUNES', 1),
            ('Sandra Ramirez', 'COMUNES', 2),
        ]
        
        print("\n[*] CAMARA (Caqueta):")
        for nombre, partido_cod, numero in candidatos_camara:
            if partido_cod in partidos:
                candidato = Candidato(
                    nombre_completo=nombre,
                    partido_id=partidos[partido_cod].id,
                    tipo_eleccion_id=tipo_camara.id,
                    cargo='Representante',
                    numero_lista=numero,
                    activo=True
                )
                db.session.add(candidato)
                print(f"  [OK] {nombre} ({partidos[partido_cod].sigla}) #{numero}")
        
        # CITREP - Mismos candidatos de Camara, pero departamento transversal
        print("\n[*] CITREP:")
        for nombre, partido_cod, numero in candidatos_camara:
            if partido_cod in partidos:
                candidato = Candidato(
                    nombre_completo=nombre,
                    partido_id=partidos[partido_cod].id,
                    tipo_eleccion_id=citrep_tipo.id,
                    cargo='Representante CITREP',
                    numero_lista=numero,
                    activo=True
                )
                db.session.add(candidato)
                print(f"  [OK] {nombre} ({partidos[partido_cod].sigla}) #{numero}")
        
        db.session.commit()
        
        # Resumen
        print()
        print("=" * 80)
        print("RESUMEN")
        print("=" * 80)
        total_senado = Candidato.query.filter_by(tipo_eleccion_id=tipo_senado.id).count()
        total_camara = Candidato.query.filter_by(tipo_eleccion_id=tipo_camara.id).count()
        total_citrep = Candidato.query.filter_by(tipo_eleccion_id=citrep_tipo.id).count()
        
        print(f"[OK] Candidatos Senado: {total_senado}")
        print(f"[OK] Candidatos Camara (Caqueta): {total_camara}")
        print(f"[OK] Candidatos CITREP: {total_citrep}")
        print(f"[OK] TOTAL: {total_senado + total_camara + total_citrep}")
        print()
        print("=" * 80)
        print("[OK] CANDIDATOS CARGADOS EXITOSAMENTE")
        print("=" * 80)


if __name__ == '__main__':
    cargar_candidatos()
