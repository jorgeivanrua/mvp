#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import sys
sys.path.insert(0, 'd:\\Software\\mvp')

from backend.app import create_app
from backend.models.location import Location

app = create_app()

with app.app_context():
    p = Location.query.filter_by(tipo='puesto', departamento_codigo='26').first()
    print(f'Puesto: {p.puesto_nombre}')
    print(f'Depto: "{p.departamento_codigo}"')
    print(f'Muni: "{p.municipio_codigo}"')
    print(f'Zona: "{p.zona_codigo}"')
    print(f'Puesto: "{p.puesto_codigo}"')
    print()
    print(f'Código completo generado: "{p.departamento_codigo}{p.municipio_codigo}{p.zona_codigo}{p.puesto_codigo}"')
    print()
    
    # Verificar con DIVIPOLA
    import csv
    with open('d:\\Software\\mvp\\data\\divipola.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if row['dd'] == '26':
                if i < 5:  # Mostrar primeras 5 de Quindío
                    codigo_divipola = f"{row['dd']}{row['mm']}{row['zz']}{row['pp']}"
                    print(f'DIVIPOLA código: {codigo_divipola}, Puesto: {row["puesto"]}')
                if i > 10:
                    break
