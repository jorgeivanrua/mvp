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
        
        # 1. Obtener tipos de eleccion
        print("1. Verificando tipos de eleccion...")
        tipo_senado = TipoEleccion.query.filter_by(codigo='SENADO').first()
        tipo_camara = TipoEleccion.query.filter_by(codigo='CAMARA').first()
        citrep_tipo = TipoEleccion.query.filter_by(codigo='CITREP').first()
        
        if not tipo_senado:
            print("   [ERROR] SENADO not found!")
            return
        if not tipo_camara:
            print("   [ERROR] CAMARA not found!")
            return
        if not citrep_tipo:
            print("   [ERROR] CITREP not found!")
            return
            
        print(f"   [OK] SENADO (ID: {tipo_senado.id})")
        print(f"   [OK] CAMARA (ID: {tipo_camara.id})")
        print(f"   [OK] CITREP (ID: {citrep_tipo.id})")
        print()
        
        # 2. Limpiar candidatos existentes
        print("2. Limpiando candidatos existentes...")
        Candidato.query.delete()
        db.session.commit()
        print("   [OK] Candidatos eliminados")
        print()
        
        # 3. Obtener partidos por sigla
        partidos_dict = {}
        partidos = PartidoPolitico.query.all()
        for p in partidos:
            partidos_dict[p.sigla] = p
        
        print(f"3. Partidos cargados: {len(partidos_dict)}")
        print("-" * 80)
        
        # SENADO - Listas mas largas
        candidatos_senado = [
            # PACTO HISTORICO (5)
            ('Gustavo Bolivar', 'PH', 1),
            ('Maria Jose Pizarro', 'PH', 2),
            ('Ivan Cepeda', 'PH', 3),
            ('Alexander Lopez', 'PH', 4),
            ('Isabel Zuleta', 'PH', 5),
            # CENTRO DEMOCRATICO (5)
            ('Paloma Valencia', 'CD', 1),
            ('Miguel Uribe Turbay', 'CD', 2),
            ('Maria Fernanda Cabal', 'CD', 3),
            ('Paola Holguin', 'CD', 4),
            ('Honorio Henriquez', 'CD', 5),
            # ALIANZA VERDE (4)
            ('Angelica Lozano', 'AV', 1),
            ('Ariel Avila', 'AV', 2),
            ('Antonio Sanguino', 'AV', 3),
            ('Humberto de la Calle', 'AV', 4),
            # CONSERVADOR (4)
            ('Efrain Cepeda', 'PCC', 1),
            ('David Barguil', 'PCC', 2),
            ('Nora Garcia', 'PCC', 3),
            ('Ciro Ramirez', 'PCC', 4),
            # LIBERAL (5)
            ('Juan Fernando Cristo', 'PLC', 1),
            ('Alejandro Gaviria', 'PLC', 2),
            ('Horacio Jose Serpa', 'PLC', 3),
            ('Viviane Morales', 'PLC', 4),
            ('Luis Fernando Velasco', 'PLC', 5),
            # CAMBIO RADICAL (4)
            ('German Varon', 'CR', 1),
            ('Carlos Fernando Motoa', 'CR', 2),
            ('Rodrigo Lara', 'CR', 3),
            ('David Luna', 'CR', 4),
            # POLO (3)
            ('Alexander Lopez Maya', 'PD', 1),
            ('Aida Avella', 'PD', 2),
            ('Jorge Enrique Robledo', 'PD', 3),
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
            ('Pablo Catatumbo', 'COM', 1),
            ('Victoria Sandino', 'COM', 2),
        ]
        
        print("\n[*] SENADO:")
        count_senado = 0
        for nombre, sigla, numero in candidatos_senado:
            if sigla in partidos_dict:
                candidato = Candidato(
                    nombre_completo=nombre,
                    partido_id=partidos_dict[sigla].id,
                    tipo_eleccion_id=tipo_senado.id,
                    cargo='Senador',
                    numero_lista=numero,
                    activo=True
                )
                db.session.add(candidato)
                count_senado += 1
                print(f"  [OK] {nombre} ({sigla}) #{numero}")
        print(f"  Total: {count_senado}")
        
        # CAMARA CAQUETA - Maximo 3 por partido
        candidatos_camara = [
            # LIBERAL (3)
            ('Hernan Banguero', 'PLC', 1),
            ('Deisy Gomez', 'PLC', 2),
            ('Roberto Sanchez', 'PLC', 3),
            # CONSERVADOR (3)
            ('Carlos Ramirez', 'PCC', 1),
            ('Martha Villalba', 'PCC', 2),
            ('Jairo Cristancho', 'PCC', 3),
            # PACTO HISTORICO (3)
            ('Ana Maria Torres', 'PH', 1),
            ('Luis Eduardo Diaz', 'PH', 2),
            ('Maria Fernanda Rojas', 'PH', 3),
            # CENTRO DEMOCRATICO (3)
            ('Jorge Enrique Rojas', 'CD', 1),
            ('Claudia Patricia Jimenez', 'CD', 2),
            ('Hector Fabio Useche', 'CD', 3),
            # ALIANZA VERDE (3)
            ('Sandra Milena Gutierrez', 'AV', 1),
            ('Andres Felipe Arias', 'AV', 2),
            ('Diana Carolina Bernal', 'AV', 3),
            # CAMBIO RADICAL (3)
            ('Pedro Nel Jimenez', 'CR', 1),
            ('Luz Mery Trujillo', 'CR', 2),
            ('Oscar Dario Perez', 'CR', 3),
            # PARTIDO DE LA U (3)
            ('Gloria Stella Diaz', 'U', 1),
            ('William Villamizar', 'U', 2),
            ('Yolanda Becerra', 'U', 3),
            # POLO (2)
            ('Jaime Caycedo', 'PD', 1),
            ('Clara Lopez', 'PD', 2),
            # MIRA (2)
            ('Alexandra Moreno', 'MIRA', 1),
            ('Edgar Espindola', 'MIRA', 2),
            # COMUNES (2)
            ('Julian Gallo', 'COM', 1),
            ('Sandra Ramirez', 'COM', 2),
        ]
        
        print("\n[*] CAMARA (Caqueta):")
        count_camara = 0
        for nombre, sigla, numero in candidatos_camara:
            if sigla in partidos_dict:
                candidato = Candidato(
                    nombre_completo=nombre,
                    partido_id=partidos_dict[sigla].id,
                    tipo_eleccion_id=tipo_camara.id,
                    cargo='Representante',
                    numero_lista=numero,
                    activo=True
                )
                db.session.add(candidato)
                count_camara += 1
                print(f"  [OK] {nombre} ({sigla}) #{numero}")
        print(f"  Total: {count_camara}")
        
        # CITREP - Mismos candidatos de Camara, pero departamento transversal
        print("\n[*] CITREP:")
        count_citrep = 0
        for nombre, sigla, numero in candidatos_camara:
            if sigla in partidos_dict:
                candidato = Candidato(
                    nombre_completo=nombre,
                    partido_id=partidos_dict[sigla].id,
                    tipo_eleccion_id=citrep_tipo.id,
                    cargo='Representante CITREP',
                    numero_lista=numero,
                    activo=True
                )
                db.session.add(candidato)
                count_citrep += 1
                print(f"  [OK] {nombre} ({sigla}) #{numero}")
        print(f"  Total: {count_citrep}")
        
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
