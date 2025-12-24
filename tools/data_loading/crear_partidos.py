#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Crea los partidos politicos en la BD si no existen.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.models.partido_politico import PartidoPolitico
from backend.database import db

def main():
    app = create_app()
    
    with app.app_context():
        print('[*] Creating political parties...')
        
        partidos_data = [
            ('Partido Liberal Colombiano', 'PLC', '#FF0000'),
            ('Partido Conservador Colombiano', 'PCC', '#0033FF'),
            ('Centro Democratico', 'CD', '#7030A0'),
            ('Pacto Historico', 'PH', '#FF00FF'),
            ('Alianza Verde', 'AV', '#00B050'),
            ('Cambio Radical', 'CR', '#00FFFF'),
            ('Polo Democratico', 'PD', '#FF6600'),
            ('MIRA', 'MIRA', '#FFFF00'),
            ('Partido de la U', 'U', '#003300'),
            ('Comunes', 'COM', '#FF99FF'),
        ]
        
        for nombre, sigla, color in partidos_data:
            existing = PartidoPolitico.query.filter_by(sigla=sigla).first()
            if not existing:
                partido = PartidoPolitico(
                    nombre=nombre,
                    sigla=sigla,
                    color=color,
                    activo=True
                )
                db.session.add(partido)
                print('[OK] Created: {} ({})'.format(nombre, sigla))
            else:
                print('[*] {} already exists (ID: {})'.format(nombre, existing.id))
        
        db.session.commit()
        
        print()
        print('[*] Parties in database:')
        partidos = PartidoPolitico.query.all()
        for p in partidos:
            print('  - {}: {} ({})'.format(p.sigla, p.nombre, p.id))
        
        print('[OK] Done!')

if __name__ == '__main__':
    main()
