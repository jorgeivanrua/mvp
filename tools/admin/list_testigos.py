#!/usr/bin/env python
"""
Listar usuarios testigos para probar
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models import User

app = create_app('production')

with app.app_context():
    testigos = User.query.filter_by(rol='testigo_electoral').limit(10).all()
    print("USUARIOS TESTIGOS (primeros 10):")
    print("-" * 50)
    for t in testigos:
        print(f"  Nombre: {t.nombre}")
        print(f"  Usuario: {t.nombre}")
        print(f"  Cedula: {t.cedula}")
        print(f"  Activo: {t.activo}")
        print()
