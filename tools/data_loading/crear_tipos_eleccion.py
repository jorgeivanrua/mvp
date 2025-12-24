#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Crea los tipos de eleccion faltantes (SENADO y CAMARA) en la BD.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.models.configuracion_electoral import TipoEleccion
from backend.database import db

def main():
    app = create_app()
    
    with app.app_context():
        print('[*] Creating missing election types...')
        
        # Verificar SENADO
        senado = TipoEleccion.query.filter_by(codigo='SENADO').first()
        if not senado:
            senado = TipoEleccion(
                codigo='SENADO',
                nombre='Senado de la Republica',
                descripcion='Senado de la Republica - Circunscripcion Nacional',
                es_uninominal=False,
                permite_lista_cerrada=True,
                permite_lista_abierta=False,
                permite_coaliciones=True,
                activo=True,
                orden=2
            )
            db.session.add(senado)
            print('[OK] Created SENADO')
        else:
            print('[*] SENADO already exists (ID: {})'.format(senado.id))
        
        # Verificar CAMARA
        camara = TipoEleccion.query.filter_by(codigo='CAMARA').first()
        if not camara:
            camara = TipoEleccion(
                codigo='CAMARA',
                nombre='Camara de Representantes',
                descripcion='Camara de Representantes - Por Departamento',
                es_uninominal=False,
                permite_lista_cerrada=True,
                permite_lista_abierta=False,
                permite_coaliciones=True,
                activo=True,
                orden=3
            )
            db.session.add(camara)
            print('[OK] Created CAMARA')
        else:
            print('[*] CAMARA already exists (ID: {})'.format(camara.id))
        
        # Commit
        db.session.commit()
        
        # Verificar resultado
        print('[*] Final election types:')
        tipos = TipoEleccion.query.all()
        for t in tipos:
            print('  - {}: {} (ID: {})'.format(t.codigo, t.nombre, t.id))
        
        print('[OK] Done!')

if __name__ == '__main__':
    main()
